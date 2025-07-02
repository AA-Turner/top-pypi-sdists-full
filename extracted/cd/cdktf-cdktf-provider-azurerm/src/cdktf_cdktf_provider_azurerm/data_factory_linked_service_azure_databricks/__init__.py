r'''
# `azurerm_data_factory_linked_service_azure_databricks`

Refer to the Terraform Registry for docs: [`azurerm_data_factory_linked_service_azure_databricks`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks).
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


class DataFactoryLinkedServiceAzureDatabricks(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricks",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks azurerm_data_factory_linked_service_azure_databricks}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        adb_domain: builtins.str,
        data_factory_id: builtins.str,
        name: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        existing_cluster_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_pool: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureDatabricksInstancePool", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_runtime_name: typing.Optional[builtins.str] = None,
        key_vault_password: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        msi_work_space_resource_id: typing.Optional[builtins.str] = None,
        new_cluster_config: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureDatabricksNewClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureDatabricksTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks azurerm_data_factory_linked_service_azure_databricks} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param adb_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#adb_domain DataFactoryLinkedServiceAzureDatabricks#adb_domain}.
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#data_factory_id DataFactoryLinkedServiceAzureDatabricks#data_factory_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#name DataFactoryLinkedServiceAzureDatabricks#name}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#access_token DataFactoryLinkedServiceAzureDatabricks#access_token}.
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#additional_properties DataFactoryLinkedServiceAzureDatabricks#additional_properties}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#annotations DataFactoryLinkedServiceAzureDatabricks#annotations}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#description DataFactoryLinkedServiceAzureDatabricks#description}.
        :param existing_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#existing_cluster_id DataFactoryLinkedServiceAzureDatabricks#existing_cluster_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#id DataFactoryLinkedServiceAzureDatabricks#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_pool: instance_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#instance_pool DataFactoryLinkedServiceAzureDatabricks#instance_pool}
        :param integration_runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#integration_runtime_name DataFactoryLinkedServiceAzureDatabricks#integration_runtime_name}.
        :param key_vault_password: key_vault_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#key_vault_password DataFactoryLinkedServiceAzureDatabricks#key_vault_password}
        :param msi_work_space_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#msi_work_space_resource_id DataFactoryLinkedServiceAzureDatabricks#msi_work_space_resource_id}.
        :param new_cluster_config: new_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#new_cluster_config DataFactoryLinkedServiceAzureDatabricks#new_cluster_config}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#parameters DataFactoryLinkedServiceAzureDatabricks#parameters}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#timeouts DataFactoryLinkedServiceAzureDatabricks#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babcb0a972a54184755ff381f998d6bef688c2d2a43880fa0cba27baeb5b842e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataFactoryLinkedServiceAzureDatabricksConfig(
            adb_domain=adb_domain,
            data_factory_id=data_factory_id,
            name=name,
            access_token=access_token,
            additional_properties=additional_properties,
            annotations=annotations,
            description=description,
            existing_cluster_id=existing_cluster_id,
            id=id,
            instance_pool=instance_pool,
            integration_runtime_name=integration_runtime_name,
            key_vault_password=key_vault_password,
            msi_work_space_resource_id=msi_work_space_resource_id,
            new_cluster_config=new_cluster_config,
            parameters=parameters,
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
        '''Generates CDKTF code for importing a DataFactoryLinkedServiceAzureDatabricks resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataFactoryLinkedServiceAzureDatabricks to import.
        :param import_from_id: The id of the existing DataFactoryLinkedServiceAzureDatabricks that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataFactoryLinkedServiceAzureDatabricks to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89494bba6a7220094474f86aacecb245b4e043d0c812d73a1637969e5d6538d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInstancePool")
    def put_instance_pool(
        self,
        *,
        cluster_version: builtins.str,
        instance_pool_id: builtins.str,
        max_number_of_workers: typing.Optional[jsii.Number] = None,
        min_number_of_workers: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#cluster_version DataFactoryLinkedServiceAzureDatabricks#cluster_version}.
        :param instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#instance_pool_id DataFactoryLinkedServiceAzureDatabricks#instance_pool_id}.
        :param max_number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#max_number_of_workers DataFactoryLinkedServiceAzureDatabricks#max_number_of_workers}.
        :param min_number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#min_number_of_workers DataFactoryLinkedServiceAzureDatabricks#min_number_of_workers}.
        '''
        value = DataFactoryLinkedServiceAzureDatabricksInstancePool(
            cluster_version=cluster_version,
            instance_pool_id=instance_pool_id,
            max_number_of_workers=max_number_of_workers,
            min_number_of_workers=min_number_of_workers,
        )

        return typing.cast(None, jsii.invoke(self, "putInstancePool", [value]))

    @jsii.member(jsii_name="putKeyVaultPassword")
    def put_key_vault_password(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#linked_service_name DataFactoryLinkedServiceAzureDatabricks#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#secret_name DataFactoryLinkedServiceAzureDatabricks#secret_name}.
        '''
        value = DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword(
            linked_service_name=linked_service_name, secret_name=secret_name
        )

        return typing.cast(None, jsii.invoke(self, "putKeyVaultPassword", [value]))

    @jsii.member(jsii_name="putNewClusterConfig")
    def put_new_cluster_config(
        self,
        *,
        cluster_version: builtins.str,
        node_type: builtins.str,
        custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        driver_node_type: typing.Optional[builtins.str] = None,
        init_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_destination: typing.Optional[builtins.str] = None,
        max_number_of_workers: typing.Optional[jsii.Number] = None,
        min_number_of_workers: typing.Optional[jsii.Number] = None,
        spark_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#cluster_version DataFactoryLinkedServiceAzureDatabricks#cluster_version}.
        :param node_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#node_type DataFactoryLinkedServiceAzureDatabricks#node_type}.
        :param custom_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#custom_tags DataFactoryLinkedServiceAzureDatabricks#custom_tags}.
        :param driver_node_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#driver_node_type DataFactoryLinkedServiceAzureDatabricks#driver_node_type}.
        :param init_scripts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#init_scripts DataFactoryLinkedServiceAzureDatabricks#init_scripts}.
        :param log_destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#log_destination DataFactoryLinkedServiceAzureDatabricks#log_destination}.
        :param max_number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#max_number_of_workers DataFactoryLinkedServiceAzureDatabricks#max_number_of_workers}.
        :param min_number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#min_number_of_workers DataFactoryLinkedServiceAzureDatabricks#min_number_of_workers}.
        :param spark_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#spark_config DataFactoryLinkedServiceAzureDatabricks#spark_config}.
        :param spark_environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#spark_environment_variables DataFactoryLinkedServiceAzureDatabricks#spark_environment_variables}.
        '''
        value = DataFactoryLinkedServiceAzureDatabricksNewClusterConfig(
            cluster_version=cluster_version,
            node_type=node_type,
            custom_tags=custom_tags,
            driver_node_type=driver_node_type,
            init_scripts=init_scripts,
            log_destination=log_destination,
            max_number_of_workers=max_number_of_workers,
            min_number_of_workers=min_number_of_workers,
            spark_config=spark_config,
            spark_environment_variables=spark_environment_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putNewClusterConfig", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#create DataFactoryLinkedServiceAzureDatabricks#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#delete DataFactoryLinkedServiceAzureDatabricks#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#read DataFactoryLinkedServiceAzureDatabricks#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#update DataFactoryLinkedServiceAzureDatabricks#update}.
        '''
        value = DataFactoryLinkedServiceAzureDatabricksTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessToken")
    def reset_access_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessToken", []))

    @jsii.member(jsii_name="resetAdditionalProperties")
    def reset_additional_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalProperties", []))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExistingClusterId")
    def reset_existing_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExistingClusterId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstancePool")
    def reset_instance_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstancePool", []))

    @jsii.member(jsii_name="resetIntegrationRuntimeName")
    def reset_integration_runtime_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationRuntimeName", []))

    @jsii.member(jsii_name="resetKeyVaultPassword")
    def reset_key_vault_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultPassword", []))

    @jsii.member(jsii_name="resetMsiWorkSpaceResourceId")
    def reset_msi_work_space_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMsiWorkSpaceResourceId", []))

    @jsii.member(jsii_name="resetNewClusterConfig")
    def reset_new_cluster_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNewClusterConfig", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

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
    @jsii.member(jsii_name="instancePool")
    def instance_pool(
        self,
    ) -> "DataFactoryLinkedServiceAzureDatabricksInstancePoolOutputReference":
        return typing.cast("DataFactoryLinkedServiceAzureDatabricksInstancePoolOutputReference", jsii.get(self, "instancePool"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPassword")
    def key_vault_password(
        self,
    ) -> "DataFactoryLinkedServiceAzureDatabricksKeyVaultPasswordOutputReference":
        return typing.cast("DataFactoryLinkedServiceAzureDatabricksKeyVaultPasswordOutputReference", jsii.get(self, "keyVaultPassword"))

    @builtins.property
    @jsii.member(jsii_name="newClusterConfig")
    def new_cluster_config(
        self,
    ) -> "DataFactoryLinkedServiceAzureDatabricksNewClusterConfigOutputReference":
        return typing.cast("DataFactoryLinkedServiceAzureDatabricksNewClusterConfigOutputReference", jsii.get(self, "newClusterConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "DataFactoryLinkedServiceAzureDatabricksTimeoutsOutputReference":
        return typing.cast("DataFactoryLinkedServiceAzureDatabricksTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessTokenInput")
    def access_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="adbDomainInput")
    def adb_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adbDomainInput"))

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
    @jsii.member(jsii_name="dataFactoryIdInput")
    def data_factory_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFactoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="existingClusterIdInput")
    def existing_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "existingClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instancePoolInput")
    def instance_pool_input(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureDatabricksInstancePool"]:
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureDatabricksInstancePool"], jsii.get(self, "instancePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationRuntimeNameInput")
    def integration_runtime_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationRuntimeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPasswordInput")
    def key_vault_password_input(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword"]:
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword"], jsii.get(self, "keyVaultPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="msiWorkSpaceResourceIdInput")
    def msi_work_space_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "msiWorkSpaceResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="newClusterConfigInput")
    def new_cluster_config_input(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureDatabricksNewClusterConfig"]:
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureDatabricksNewClusterConfig"], jsii.get(self, "newClusterConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryLinkedServiceAzureDatabricksTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataFactoryLinkedServiceAzureDatabricksTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__562015d27bada1e580225b00608d4b16d09d79955c4810af68c38477eec8d0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="adbDomain")
    def adb_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adbDomain"))

    @adb_domain.setter
    def adb_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7943f2f5beb628390187192cf8be4f7712ee07df2a187a3d707ff2e160c6d7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adbDomain", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__27994058a17531ba8820ffc92b17795526a22af7ce718064ef89d73265bfea56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a06d28b204d10d9a523a109e4ceed700930692bc0af68ce959948081c8fff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFactoryId")
    def data_factory_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFactoryId"))

    @data_factory_id.setter
    def data_factory_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02196925d7fe383f5336e0b31cc8e49d5e258132121110d1f9720c24b2379a7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFactoryId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec65c9889007f988269e04f4ae36f71a0d421422a4f60209d7409c772bddb41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="existingClusterId")
    def existing_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "existingClusterId"))

    @existing_cluster_id.setter
    def existing_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1e677f29e6d2350d7d713a71a8ac764202b1887e597030c6f80347f4f4b963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "existingClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560adf06f234a12a4a8488a5c66aa5f7d508ae837f33897a2ef6b15b4d439585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationRuntimeName")
    def integration_runtime_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationRuntimeName"))

    @integration_runtime_name.setter
    def integration_runtime_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56212f70f34917745e537f3d5251243a3177804f8efbc2ed6d236e4d713aee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationRuntimeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msiWorkSpaceResourceId")
    def msi_work_space_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "msiWorkSpaceResourceId"))

    @msi_work_space_resource_id.setter
    def msi_work_space_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64e05de3dea3c830ba83c580ae73f6117defaf787e24287c30d48a7c2593851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msiWorkSpaceResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8757f47927e3cf653536543e62335b419a763a46fd064dc26ed5fc76b1821c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb47f78969453810aaa9d66bf65bd6cd87bbd61d643895790b8afc8e00e33031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "adb_domain": "adbDomain",
        "data_factory_id": "dataFactoryId",
        "name": "name",
        "access_token": "accessToken",
        "additional_properties": "additionalProperties",
        "annotations": "annotations",
        "description": "description",
        "existing_cluster_id": "existingClusterId",
        "id": "id",
        "instance_pool": "instancePool",
        "integration_runtime_name": "integrationRuntimeName",
        "key_vault_password": "keyVaultPassword",
        "msi_work_space_resource_id": "msiWorkSpaceResourceId",
        "new_cluster_config": "newClusterConfig",
        "parameters": "parameters",
        "timeouts": "timeouts",
    },
)
class DataFactoryLinkedServiceAzureDatabricksConfig(
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
        adb_domain: builtins.str,
        data_factory_id: builtins.str,
        name: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        existing_cluster_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_pool: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureDatabricksInstancePool", typing.Dict[builtins.str, typing.Any]]] = None,
        integration_runtime_name: typing.Optional[builtins.str] = None,
        key_vault_password: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword", typing.Dict[builtins.str, typing.Any]]] = None,
        msi_work_space_resource_id: typing.Optional[builtins.str] = None,
        new_cluster_config: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureDatabricksNewClusterConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DataFactoryLinkedServiceAzureDatabricksTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param adb_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#adb_domain DataFactoryLinkedServiceAzureDatabricks#adb_domain}.
        :param data_factory_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#data_factory_id DataFactoryLinkedServiceAzureDatabricks#data_factory_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#name DataFactoryLinkedServiceAzureDatabricks#name}.
        :param access_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#access_token DataFactoryLinkedServiceAzureDatabricks#access_token}.
        :param additional_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#additional_properties DataFactoryLinkedServiceAzureDatabricks#additional_properties}.
        :param annotations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#annotations DataFactoryLinkedServiceAzureDatabricks#annotations}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#description DataFactoryLinkedServiceAzureDatabricks#description}.
        :param existing_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#existing_cluster_id DataFactoryLinkedServiceAzureDatabricks#existing_cluster_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#id DataFactoryLinkedServiceAzureDatabricks#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_pool: instance_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#instance_pool DataFactoryLinkedServiceAzureDatabricks#instance_pool}
        :param integration_runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#integration_runtime_name DataFactoryLinkedServiceAzureDatabricks#integration_runtime_name}.
        :param key_vault_password: key_vault_password block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#key_vault_password DataFactoryLinkedServiceAzureDatabricks#key_vault_password}
        :param msi_work_space_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#msi_work_space_resource_id DataFactoryLinkedServiceAzureDatabricks#msi_work_space_resource_id}.
        :param new_cluster_config: new_cluster_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#new_cluster_config DataFactoryLinkedServiceAzureDatabricks#new_cluster_config}
        :param parameters: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#parameters DataFactoryLinkedServiceAzureDatabricks#parameters}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#timeouts DataFactoryLinkedServiceAzureDatabricks#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(instance_pool, dict):
            instance_pool = DataFactoryLinkedServiceAzureDatabricksInstancePool(**instance_pool)
        if isinstance(key_vault_password, dict):
            key_vault_password = DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword(**key_vault_password)
        if isinstance(new_cluster_config, dict):
            new_cluster_config = DataFactoryLinkedServiceAzureDatabricksNewClusterConfig(**new_cluster_config)
        if isinstance(timeouts, dict):
            timeouts = DataFactoryLinkedServiceAzureDatabricksTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5691899a46f51f0cee81613868f4acce9558b6100669b31da116f0ee6073e3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument adb_domain", value=adb_domain, expected_type=type_hints["adb_domain"])
            check_type(argname="argument data_factory_id", value=data_factory_id, expected_type=type_hints["data_factory_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument additional_properties", value=additional_properties, expected_type=type_hints["additional_properties"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument existing_cluster_id", value=existing_cluster_id, expected_type=type_hints["existing_cluster_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_pool", value=instance_pool, expected_type=type_hints["instance_pool"])
            check_type(argname="argument integration_runtime_name", value=integration_runtime_name, expected_type=type_hints["integration_runtime_name"])
            check_type(argname="argument key_vault_password", value=key_vault_password, expected_type=type_hints["key_vault_password"])
            check_type(argname="argument msi_work_space_resource_id", value=msi_work_space_resource_id, expected_type=type_hints["msi_work_space_resource_id"])
            check_type(argname="argument new_cluster_config", value=new_cluster_config, expected_type=type_hints["new_cluster_config"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "adb_domain": adb_domain,
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
        if access_token is not None:
            self._values["access_token"] = access_token
        if additional_properties is not None:
            self._values["additional_properties"] = additional_properties
        if annotations is not None:
            self._values["annotations"] = annotations
        if description is not None:
            self._values["description"] = description
        if existing_cluster_id is not None:
            self._values["existing_cluster_id"] = existing_cluster_id
        if id is not None:
            self._values["id"] = id
        if instance_pool is not None:
            self._values["instance_pool"] = instance_pool
        if integration_runtime_name is not None:
            self._values["integration_runtime_name"] = integration_runtime_name
        if key_vault_password is not None:
            self._values["key_vault_password"] = key_vault_password
        if msi_work_space_resource_id is not None:
            self._values["msi_work_space_resource_id"] = msi_work_space_resource_id
        if new_cluster_config is not None:
            self._values["new_cluster_config"] = new_cluster_config
        if parameters is not None:
            self._values["parameters"] = parameters
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
    def adb_domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#adb_domain DataFactoryLinkedServiceAzureDatabricks#adb_domain}.'''
        result = self._values.get("adb_domain")
        assert result is not None, "Required property 'adb_domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_factory_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#data_factory_id DataFactoryLinkedServiceAzureDatabricks#data_factory_id}.'''
        result = self._values.get("data_factory_id")
        assert result is not None, "Required property 'data_factory_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#name DataFactoryLinkedServiceAzureDatabricks#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#access_token DataFactoryLinkedServiceAzureDatabricks#access_token}.'''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#additional_properties DataFactoryLinkedServiceAzureDatabricks#additional_properties}.'''
        result = self._values.get("additional_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def annotations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#annotations DataFactoryLinkedServiceAzureDatabricks#annotations}.'''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#description DataFactoryLinkedServiceAzureDatabricks#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#existing_cluster_id DataFactoryLinkedServiceAzureDatabricks#existing_cluster_id}.'''
        result = self._values.get("existing_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#id DataFactoryLinkedServiceAzureDatabricks#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_pool(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureDatabricksInstancePool"]:
        '''instance_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#instance_pool DataFactoryLinkedServiceAzureDatabricks#instance_pool}
        '''
        result = self._values.get("instance_pool")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureDatabricksInstancePool"], result)

    @builtins.property
    def integration_runtime_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#integration_runtime_name DataFactoryLinkedServiceAzureDatabricks#integration_runtime_name}.'''
        result = self._values.get("integration_runtime_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_password(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword"]:
        '''key_vault_password block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#key_vault_password DataFactoryLinkedServiceAzureDatabricks#key_vault_password}
        '''
        result = self._values.get("key_vault_password")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword"], result)

    @builtins.property
    def msi_work_space_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#msi_work_space_resource_id DataFactoryLinkedServiceAzureDatabricks#msi_work_space_resource_id}.'''
        result = self._values.get("msi_work_space_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def new_cluster_config(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureDatabricksNewClusterConfig"]:
        '''new_cluster_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#new_cluster_config DataFactoryLinkedServiceAzureDatabricks#new_cluster_config}
        '''
        result = self._values.get("new_cluster_config")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureDatabricksNewClusterConfig"], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#parameters DataFactoryLinkedServiceAzureDatabricks#parameters}.'''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DataFactoryLinkedServiceAzureDatabricksTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#timeouts DataFactoryLinkedServiceAzureDatabricks#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataFactoryLinkedServiceAzureDatabricksTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureDatabricksConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksInstancePool",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_version": "clusterVersion",
        "instance_pool_id": "instancePoolId",
        "max_number_of_workers": "maxNumberOfWorkers",
        "min_number_of_workers": "minNumberOfWorkers",
    },
)
class DataFactoryLinkedServiceAzureDatabricksInstancePool:
    def __init__(
        self,
        *,
        cluster_version: builtins.str,
        instance_pool_id: builtins.str,
        max_number_of_workers: typing.Optional[jsii.Number] = None,
        min_number_of_workers: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#cluster_version DataFactoryLinkedServiceAzureDatabricks#cluster_version}.
        :param instance_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#instance_pool_id DataFactoryLinkedServiceAzureDatabricks#instance_pool_id}.
        :param max_number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#max_number_of_workers DataFactoryLinkedServiceAzureDatabricks#max_number_of_workers}.
        :param min_number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#min_number_of_workers DataFactoryLinkedServiceAzureDatabricks#min_number_of_workers}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63e3df91c0d7fc09506b0104ae7b02b5e454e5998d3ff3f8e54a164f5362876)
            check_type(argname="argument cluster_version", value=cluster_version, expected_type=type_hints["cluster_version"])
            check_type(argname="argument instance_pool_id", value=instance_pool_id, expected_type=type_hints["instance_pool_id"])
            check_type(argname="argument max_number_of_workers", value=max_number_of_workers, expected_type=type_hints["max_number_of_workers"])
            check_type(argname="argument min_number_of_workers", value=min_number_of_workers, expected_type=type_hints["min_number_of_workers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_version": cluster_version,
            "instance_pool_id": instance_pool_id,
        }
        if max_number_of_workers is not None:
            self._values["max_number_of_workers"] = max_number_of_workers
        if min_number_of_workers is not None:
            self._values["min_number_of_workers"] = min_number_of_workers

    @builtins.property
    def cluster_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#cluster_version DataFactoryLinkedServiceAzureDatabricks#cluster_version}.'''
        result = self._values.get("cluster_version")
        assert result is not None, "Required property 'cluster_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#instance_pool_id DataFactoryLinkedServiceAzureDatabricks#instance_pool_id}.'''
        result = self._values.get("instance_pool_id")
        assert result is not None, "Required property 'instance_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_number_of_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#max_number_of_workers DataFactoryLinkedServiceAzureDatabricks#max_number_of_workers}.'''
        result = self._values.get("max_number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_number_of_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#min_number_of_workers DataFactoryLinkedServiceAzureDatabricks#min_number_of_workers}.'''
        result = self._values.get("min_number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureDatabricksInstancePool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceAzureDatabricksInstancePoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksInstancePoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48cb5f8b27cc4222fe49b7685a220a194714ea866ccd8228e2135d79676ff32e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxNumberOfWorkers")
    def reset_max_number_of_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNumberOfWorkers", []))

    @jsii.member(jsii_name="resetMinNumberOfWorkers")
    def reset_min_number_of_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNumberOfWorkers", []))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionInput")
    def cluster_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="instancePoolIdInput")
    def instance_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instancePoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNumberOfWorkersInput")
    def max_number_of_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNumberOfWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="minNumberOfWorkersInput")
    def min_number_of_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNumberOfWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterVersion"))

    @cluster_version.setter
    def cluster_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8b7cc1fdd043ba18527c04d541448238ba636969ee33e81ed91fac4a1a024f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instancePoolId")
    def instance_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instancePoolId"))

    @instance_pool_id.setter
    def instance_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fa1ba65565491228bab1286bdd812314144efc448cf3cd278d3300e66c7f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instancePoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxNumberOfWorkers")
    def max_number_of_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNumberOfWorkers"))

    @max_number_of_workers.setter
    def max_number_of_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1c17b1ae2fee4f61a1c170209f0203c609bd06cac49af5f833623c0ffce13c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNumberOfWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNumberOfWorkers")
    def min_number_of_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNumberOfWorkers"))

    @min_number_of_workers.setter
    def min_number_of_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe74564f99d25f69deb38c72f4310f55f49e941accabd92ca1c908bca742ad81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNumberOfWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryLinkedServiceAzureDatabricksInstancePool]:
        return typing.cast(typing.Optional[DataFactoryLinkedServiceAzureDatabricksInstancePool], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryLinkedServiceAzureDatabricksInstancePool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e903b92ae4f3f847e081f781201ada888b388502429a4683b5529e5e8f0703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword",
    jsii_struct_bases=[],
    name_mapping={
        "linked_service_name": "linkedServiceName",
        "secret_name": "secretName",
    },
)
class DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword:
    def __init__(
        self,
        *,
        linked_service_name: builtins.str,
        secret_name: builtins.str,
    ) -> None:
        '''
        :param linked_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#linked_service_name DataFactoryLinkedServiceAzureDatabricks#linked_service_name}.
        :param secret_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#secret_name DataFactoryLinkedServiceAzureDatabricks#secret_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de79dc8254e86ed8ffd4cc9fd3aa4c8ced71677edcb86d5c72e15b5b2d7f1d32)
            check_type(argname="argument linked_service_name", value=linked_service_name, expected_type=type_hints["linked_service_name"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_service_name": linked_service_name,
            "secret_name": secret_name,
        }

    @builtins.property
    def linked_service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#linked_service_name DataFactoryLinkedServiceAzureDatabricks#linked_service_name}.'''
        result = self._values.get("linked_service_name")
        assert result is not None, "Required property 'linked_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#secret_name DataFactoryLinkedServiceAzureDatabricks#secret_name}.'''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceAzureDatabricksKeyVaultPasswordOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksKeyVaultPasswordOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dee7270d8e8164af406976d4958f49f6407e2c8777db39768a58708c62275110)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f59173bb187de237df6d54f62964e6aceee2cbb100d29553d216f8ae4967b615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1db2c4376a5f2795a3c537e571a3dfda65b4ba5fe0e9bcba810bd9c0f4524c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword]:
        return typing.cast(typing.Optional[DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77deed19fb69299002c05f6fa576356cbe5f02e08912862c21b9ed0f59a0036c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksNewClusterConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_version": "clusterVersion",
        "node_type": "nodeType",
        "custom_tags": "customTags",
        "driver_node_type": "driverNodeType",
        "init_scripts": "initScripts",
        "log_destination": "logDestination",
        "max_number_of_workers": "maxNumberOfWorkers",
        "min_number_of_workers": "minNumberOfWorkers",
        "spark_config": "sparkConfig",
        "spark_environment_variables": "sparkEnvironmentVariables",
    },
)
class DataFactoryLinkedServiceAzureDatabricksNewClusterConfig:
    def __init__(
        self,
        *,
        cluster_version: builtins.str,
        node_type: builtins.str,
        custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        driver_node_type: typing.Optional[builtins.str] = None,
        init_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_destination: typing.Optional[builtins.str] = None,
        max_number_of_workers: typing.Optional[jsii.Number] = None,
        min_number_of_workers: typing.Optional[jsii.Number] = None,
        spark_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        spark_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#cluster_version DataFactoryLinkedServiceAzureDatabricks#cluster_version}.
        :param node_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#node_type DataFactoryLinkedServiceAzureDatabricks#node_type}.
        :param custom_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#custom_tags DataFactoryLinkedServiceAzureDatabricks#custom_tags}.
        :param driver_node_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#driver_node_type DataFactoryLinkedServiceAzureDatabricks#driver_node_type}.
        :param init_scripts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#init_scripts DataFactoryLinkedServiceAzureDatabricks#init_scripts}.
        :param log_destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#log_destination DataFactoryLinkedServiceAzureDatabricks#log_destination}.
        :param max_number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#max_number_of_workers DataFactoryLinkedServiceAzureDatabricks#max_number_of_workers}.
        :param min_number_of_workers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#min_number_of_workers DataFactoryLinkedServiceAzureDatabricks#min_number_of_workers}.
        :param spark_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#spark_config DataFactoryLinkedServiceAzureDatabricks#spark_config}.
        :param spark_environment_variables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#spark_environment_variables DataFactoryLinkedServiceAzureDatabricks#spark_environment_variables}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ddee8ef1200ac86a88af58ee014ac3fdf846cdccc3224b17b9d70aa8f285140)
            check_type(argname="argument cluster_version", value=cluster_version, expected_type=type_hints["cluster_version"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument custom_tags", value=custom_tags, expected_type=type_hints["custom_tags"])
            check_type(argname="argument driver_node_type", value=driver_node_type, expected_type=type_hints["driver_node_type"])
            check_type(argname="argument init_scripts", value=init_scripts, expected_type=type_hints["init_scripts"])
            check_type(argname="argument log_destination", value=log_destination, expected_type=type_hints["log_destination"])
            check_type(argname="argument max_number_of_workers", value=max_number_of_workers, expected_type=type_hints["max_number_of_workers"])
            check_type(argname="argument min_number_of_workers", value=min_number_of_workers, expected_type=type_hints["min_number_of_workers"])
            check_type(argname="argument spark_config", value=spark_config, expected_type=type_hints["spark_config"])
            check_type(argname="argument spark_environment_variables", value=spark_environment_variables, expected_type=type_hints["spark_environment_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_version": cluster_version,
            "node_type": node_type,
        }
        if custom_tags is not None:
            self._values["custom_tags"] = custom_tags
        if driver_node_type is not None:
            self._values["driver_node_type"] = driver_node_type
        if init_scripts is not None:
            self._values["init_scripts"] = init_scripts
        if log_destination is not None:
            self._values["log_destination"] = log_destination
        if max_number_of_workers is not None:
            self._values["max_number_of_workers"] = max_number_of_workers
        if min_number_of_workers is not None:
            self._values["min_number_of_workers"] = min_number_of_workers
        if spark_config is not None:
            self._values["spark_config"] = spark_config
        if spark_environment_variables is not None:
            self._values["spark_environment_variables"] = spark_environment_variables

    @builtins.property
    def cluster_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#cluster_version DataFactoryLinkedServiceAzureDatabricks#cluster_version}.'''
        result = self._values.get("cluster_version")
        assert result is not None, "Required property 'cluster_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#node_type DataFactoryLinkedServiceAzureDatabricks#node_type}.'''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#custom_tags DataFactoryLinkedServiceAzureDatabricks#custom_tags}.'''
        result = self._values.get("custom_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def driver_node_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#driver_node_type DataFactoryLinkedServiceAzureDatabricks#driver_node_type}.'''
        result = self._values.get("driver_node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def init_scripts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#init_scripts DataFactoryLinkedServiceAzureDatabricks#init_scripts}.'''
        result = self._values.get("init_scripts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#log_destination DataFactoryLinkedServiceAzureDatabricks#log_destination}.'''
        result = self._values.get("log_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_number_of_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#max_number_of_workers DataFactoryLinkedServiceAzureDatabricks#max_number_of_workers}.'''
        result = self._values.get("max_number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_number_of_workers(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#min_number_of_workers DataFactoryLinkedServiceAzureDatabricks#min_number_of_workers}.'''
        result = self._values.get("min_number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def spark_config(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#spark_config DataFactoryLinkedServiceAzureDatabricks#spark_config}.'''
        result = self._values.get("spark_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def spark_environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#spark_environment_variables DataFactoryLinkedServiceAzureDatabricks#spark_environment_variables}.'''
        result = self._values.get("spark_environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureDatabricksNewClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceAzureDatabricksNewClusterConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksNewClusterConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74c56619b382f9b78845c9bef1d1c3c699f0ddefb6006fc2330393af336d9883)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomTags")
    def reset_custom_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomTags", []))

    @jsii.member(jsii_name="resetDriverNodeType")
    def reset_driver_node_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverNodeType", []))

    @jsii.member(jsii_name="resetInitScripts")
    def reset_init_scripts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitScripts", []))

    @jsii.member(jsii_name="resetLogDestination")
    def reset_log_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDestination", []))

    @jsii.member(jsii_name="resetMaxNumberOfWorkers")
    def reset_max_number_of_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxNumberOfWorkers", []))

    @jsii.member(jsii_name="resetMinNumberOfWorkers")
    def reset_min_number_of_workers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNumberOfWorkers", []))

    @jsii.member(jsii_name="resetSparkConfig")
    def reset_spark_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkConfig", []))

    @jsii.member(jsii_name="resetSparkEnvironmentVariables")
    def reset_spark_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkEnvironmentVariables", []))

    @builtins.property
    @jsii.member(jsii_name="clusterVersionInput")
    def cluster_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="customTagsInput")
    def custom_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverNodeTypeInput")
    def driver_node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverNodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="initScriptsInput")
    def init_scripts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "initScriptsInput"))

    @builtins.property
    @jsii.member(jsii_name="logDestinationInput")
    def log_destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="maxNumberOfWorkersInput")
    def max_number_of_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxNumberOfWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="minNumberOfWorkersInput")
    def min_number_of_workers_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNumberOfWorkersInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkConfigInput")
    def spark_config_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sparkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkEnvironmentVariablesInput")
    def spark_environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sparkEnvironmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterVersion"))

    @cluster_version.setter
    def cluster_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c30914c8cee7e9a86de48a52742fd1dd13a3ec822ea380481093ec80e29f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customTags")
    def custom_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customTags"))

    @custom_tags.setter
    def custom_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524ba6062d66f8ac460b22efc33855fa678b6a8d642581af737aee448aa62c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverNodeType")
    def driver_node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverNodeType"))

    @driver_node_type.setter
    def driver_node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18821e6b566f87537fb2b4a16210c591a00044c8e8f6a7192fd68043e66c1421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverNodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initScripts")
    def init_scripts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "initScripts"))

    @init_scripts.setter
    def init_scripts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0740b541f7ebf190c98a5f549cff0bf64a73e6070bd3754a7bccc3a841c3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initScripts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logDestination")
    def log_destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logDestination"))

    @log_destination.setter
    def log_destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba88902a5cf49e8cc5a52c8ca289836044f068cf5041c6003bf7542d0517c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDestination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxNumberOfWorkers")
    def max_number_of_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNumberOfWorkers"))

    @max_number_of_workers.setter
    def max_number_of_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48368cafe0db63f7a9bd7b07436e9fa370e4db9c3af77928cd498d687c5716d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxNumberOfWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNumberOfWorkers")
    def min_number_of_workers(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNumberOfWorkers"))

    @min_number_of_workers.setter
    def min_number_of_workers(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9257ff8c185f12cd7cf222e222a50373a697d268e2928df0981c90961381fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNumberOfWorkers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f81d264c05b2eac91f4edcfd18c0bd4864ffd0253b3114e3d5e9168585d45a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkConfig")
    def spark_config(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sparkConfig"))

    @spark_config.setter
    def spark_config(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f889c8e0368f1ba24d766f84981afaa8117228dacdc79905bb662e0cb05a664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkEnvironmentVariables")
    def spark_environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sparkEnvironmentVariables"))

    @spark_environment_variables.setter
    def spark_environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05915ba9b09e321cee472e680935abcc253a509887189071888fc3c2fb707ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkEnvironmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataFactoryLinkedServiceAzureDatabricksNewClusterConfig]:
        return typing.cast(typing.Optional[DataFactoryLinkedServiceAzureDatabricksNewClusterConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataFactoryLinkedServiceAzureDatabricksNewClusterConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4feab81d3efdeb584efe18f3e5b49c345bf3c0801e020e81109004b517abf3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DataFactoryLinkedServiceAzureDatabricksTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#create DataFactoryLinkedServiceAzureDatabricks#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#delete DataFactoryLinkedServiceAzureDatabricks#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#read DataFactoryLinkedServiceAzureDatabricks#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#update DataFactoryLinkedServiceAzureDatabricks#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4091c5f998c2bd280760b4a4cf39a2dc5b70c2af59088bcaf036dc7ffec956)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#create DataFactoryLinkedServiceAzureDatabricks#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#delete DataFactoryLinkedServiceAzureDatabricks#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#read DataFactoryLinkedServiceAzureDatabricks#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/data_factory_linked_service_azure_databricks#update DataFactoryLinkedServiceAzureDatabricks#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFactoryLinkedServiceAzureDatabricksTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFactoryLinkedServiceAzureDatabricksTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataFactoryLinkedServiceAzureDatabricks.DataFactoryLinkedServiceAzureDatabricksTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f6dc2545a4f1e963e3ca4c02317549ded008130c560ea203d6161d44131dc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f64d05ba1dcba1b8503ddab7432e0eb2147498f499f98c3e3a4d01742b87d039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a511fa22ff8098ef2e7451653f5371f6f6be7e0e1691bd9b37449d937831ba36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad11e5797e4f65a3a013722149b302efb107fc0617aebc12000f0ba71cc261dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1086da76777a03c396dcbb38cf7a20b4bfc00a3f76ff11062f39de63d99e9444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceAzureDatabricksTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceAzureDatabricksTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceAzureDatabricksTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c284d5bb46c7ca84df9e3b7e5c06c0a74bdd94e5c59529df401300a479550f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataFactoryLinkedServiceAzureDatabricks",
    "DataFactoryLinkedServiceAzureDatabricksConfig",
    "DataFactoryLinkedServiceAzureDatabricksInstancePool",
    "DataFactoryLinkedServiceAzureDatabricksInstancePoolOutputReference",
    "DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword",
    "DataFactoryLinkedServiceAzureDatabricksKeyVaultPasswordOutputReference",
    "DataFactoryLinkedServiceAzureDatabricksNewClusterConfig",
    "DataFactoryLinkedServiceAzureDatabricksNewClusterConfigOutputReference",
    "DataFactoryLinkedServiceAzureDatabricksTimeouts",
    "DataFactoryLinkedServiceAzureDatabricksTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__babcb0a972a54184755ff381f998d6bef688c2d2a43880fa0cba27baeb5b842e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    adb_domain: builtins.str,
    data_factory_id: builtins.str,
    name: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    existing_cluster_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_pool: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureDatabricksInstancePool, typing.Dict[builtins.str, typing.Any]]] = None,
    integration_runtime_name: typing.Optional[builtins.str] = None,
    key_vault_password: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    msi_work_space_resource_id: typing.Optional[builtins.str] = None,
    new_cluster_config: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureDatabricksNewClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureDatabricksTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d89494bba6a7220094474f86aacecb245b4e043d0c812d73a1637969e5d6538d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__562015d27bada1e580225b00608d4b16d09d79955c4810af68c38477eec8d0e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7943f2f5beb628390187192cf8be4f7712ee07df2a187a3d707ff2e160c6d7bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27994058a17531ba8820ffc92b17795526a22af7ce718064ef89d73265bfea56(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a06d28b204d10d9a523a109e4ceed700930692bc0af68ce959948081c8fff4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02196925d7fe383f5336e0b31cc8e49d5e258132121110d1f9720c24b2379a7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec65c9889007f988269e04f4ae36f71a0d421422a4f60209d7409c772bddb41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1e677f29e6d2350d7d713a71a8ac764202b1887e597030c6f80347f4f4b963(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560adf06f234a12a4a8488a5c66aa5f7d508ae837f33897a2ef6b15b4d439585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56212f70f34917745e537f3d5251243a3177804f8efbc2ed6d236e4d713aee9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64e05de3dea3c830ba83c580ae73f6117defaf787e24287c30d48a7c2593851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8757f47927e3cf653536543e62335b419a763a46fd064dc26ed5fc76b1821c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb47f78969453810aaa9d66bf65bd6cd87bbd61d643895790b8afc8e00e33031(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5691899a46f51f0cee81613868f4acce9558b6100669b31da116f0ee6073e3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    adb_domain: builtins.str,
    data_factory_id: builtins.str,
    name: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    additional_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    annotations: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    existing_cluster_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_pool: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureDatabricksInstancePool, typing.Dict[builtins.str, typing.Any]]] = None,
    integration_runtime_name: typing.Optional[builtins.str] = None,
    key_vault_password: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword, typing.Dict[builtins.str, typing.Any]]] = None,
    msi_work_space_resource_id: typing.Optional[builtins.str] = None,
    new_cluster_config: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureDatabricksNewClusterConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DataFactoryLinkedServiceAzureDatabricksTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63e3df91c0d7fc09506b0104ae7b02b5e454e5998d3ff3f8e54a164f5362876(
    *,
    cluster_version: builtins.str,
    instance_pool_id: builtins.str,
    max_number_of_workers: typing.Optional[jsii.Number] = None,
    min_number_of_workers: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48cb5f8b27cc4222fe49b7685a220a194714ea866ccd8228e2135d79676ff32e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8b7cc1fdd043ba18527c04d541448238ba636969ee33e81ed91fac4a1a024f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fa1ba65565491228bab1286bdd812314144efc448cf3cd278d3300e66c7f58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1c17b1ae2fee4f61a1c170209f0203c609bd06cac49af5f833623c0ffce13c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe74564f99d25f69deb38c72f4310f55f49e941accabd92ca1c908bca742ad81(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e903b92ae4f3f847e081f781201ada888b388502429a4683b5529e5e8f0703(
    value: typing.Optional[DataFactoryLinkedServiceAzureDatabricksInstancePool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de79dc8254e86ed8ffd4cc9fd3aa4c8ced71677edcb86d5c72e15b5b2d7f1d32(
    *,
    linked_service_name: builtins.str,
    secret_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee7270d8e8164af406976d4958f49f6407e2c8777db39768a58708c62275110(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59173bb187de237df6d54f62964e6aceee2cbb100d29553d216f8ae4967b615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1db2c4376a5f2795a3c537e571a3dfda65b4ba5fe0e9bcba810bd9c0f4524c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77deed19fb69299002c05f6fa576356cbe5f02e08912862c21b9ed0f59a0036c(
    value: typing.Optional[DataFactoryLinkedServiceAzureDatabricksKeyVaultPassword],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddee8ef1200ac86a88af58ee014ac3fdf846cdccc3224b17b9d70aa8f285140(
    *,
    cluster_version: builtins.str,
    node_type: builtins.str,
    custom_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    driver_node_type: typing.Optional[builtins.str] = None,
    init_scripts: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_destination: typing.Optional[builtins.str] = None,
    max_number_of_workers: typing.Optional[jsii.Number] = None,
    min_number_of_workers: typing.Optional[jsii.Number] = None,
    spark_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    spark_environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c56619b382f9b78845c9bef1d1c3c699f0ddefb6006fc2330393af336d9883(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c30914c8cee7e9a86de48a52742fd1dd13a3ec822ea380481093ec80e29f4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524ba6062d66f8ac460b22efc33855fa678b6a8d642581af737aee448aa62c79(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18821e6b566f87537fb2b4a16210c591a00044c8e8f6a7192fd68043e66c1421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0740b541f7ebf190c98a5f549cff0bf64a73e6070bd3754a7bccc3a841c3f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba88902a5cf49e8cc5a52c8ca289836044f068cf5041c6003bf7542d0517c6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48368cafe0db63f7a9bd7b07436e9fa370e4db9c3af77928cd498d687c5716d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9257ff8c185f12cd7cf222e222a50373a697d268e2928df0981c90961381fe1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f81d264c05b2eac91f4edcfd18c0bd4864ffd0253b3114e3d5e9168585d45a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f889c8e0368f1ba24d766f84981afaa8117228dacdc79905bb662e0cb05a664(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05915ba9b09e321cee472e680935abcc253a509887189071888fc3c2fb707ec9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feab81d3efdeb584efe18f3e5b49c345bf3c0801e020e81109004b517abf3dc(
    value: typing.Optional[DataFactoryLinkedServiceAzureDatabricksNewClusterConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4091c5f998c2bd280760b4a4cf39a2dc5b70c2af59088bcaf036dc7ffec956(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f6dc2545a4f1e963e3ca4c02317549ded008130c560ea203d6161d44131dc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64d05ba1dcba1b8503ddab7432e0eb2147498f499f98c3e3a4d01742b87d039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a511fa22ff8098ef2e7451653f5371f6f6be7e0e1691bd9b37449d937831ba36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad11e5797e4f65a3a013722149b302efb107fc0617aebc12000f0ba71cc261dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1086da76777a03c396dcbb38cf7a20b4bfc00a3f76ff11062f39de63d99e9444(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c284d5bb46c7ca84df9e3b7e5c06c0a74bdd94e5c59529df401300a479550f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataFactoryLinkedServiceAzureDatabricksTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
