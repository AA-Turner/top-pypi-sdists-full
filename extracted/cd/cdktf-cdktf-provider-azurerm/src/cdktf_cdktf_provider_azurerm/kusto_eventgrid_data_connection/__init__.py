r'''
# `azurerm_kusto_eventgrid_data_connection`

Refer to the Terraform Registry for docs: [`azurerm_kusto_eventgrid_data_connection`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection).
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


class KustoEventgridDataConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoEventgridDataConnection.KustoEventgridDataConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection azurerm_kusto_eventgrid_data_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_name: builtins.str,
        database_name: builtins.str,
        eventhub_consumer_group_name: builtins.str,
        eventhub_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_account_id: builtins.str,
        blob_storage_event_type: typing.Optional[builtins.str] = None,
        database_routing_type: typing.Optional[builtins.str] = None,
        data_format: typing.Optional[builtins.str] = None,
        eventgrid_event_subscription_id: typing.Optional[builtins.str] = None,
        eventgrid_resource_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        managed_identity_id: typing.Optional[builtins.str] = None,
        managed_identity_resource_id: typing.Optional[builtins.str] = None,
        mapping_rule_name: typing.Optional[builtins.str] = None,
        skip_first_record: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        table_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KustoEventgridDataConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection azurerm_kusto_eventgrid_data_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#cluster_name KustoEventgridDataConnection#cluster_name}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#database_name KustoEventgridDataConnection#database_name}.
        :param eventhub_consumer_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventhub_consumer_group_name KustoEventgridDataConnection#eventhub_consumer_group_name}.
        :param eventhub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventhub_id KustoEventgridDataConnection#eventhub_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#location KustoEventgridDataConnection#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#name KustoEventgridDataConnection#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#resource_group_name KustoEventgridDataConnection#resource_group_name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#storage_account_id KustoEventgridDataConnection#storage_account_id}.
        :param blob_storage_event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#blob_storage_event_type KustoEventgridDataConnection#blob_storage_event_type}.
        :param database_routing_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#database_routing_type KustoEventgridDataConnection#database_routing_type}.
        :param data_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#data_format KustoEventgridDataConnection#data_format}.
        :param eventgrid_event_subscription_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventgrid_event_subscription_id KustoEventgridDataConnection#eventgrid_event_subscription_id}.
        :param eventgrid_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventgrid_resource_id KustoEventgridDataConnection#eventgrid_resource_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#id KustoEventgridDataConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param managed_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#managed_identity_id KustoEventgridDataConnection#managed_identity_id}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#managed_identity_resource_id KustoEventgridDataConnection#managed_identity_resource_id}.
        :param mapping_rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#mapping_rule_name KustoEventgridDataConnection#mapping_rule_name}.
        :param skip_first_record: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#skip_first_record KustoEventgridDataConnection#skip_first_record}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#table_name KustoEventgridDataConnection#table_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#timeouts KustoEventgridDataConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec6226945dd229cc0f59fff29b3a0e31ed3f2bc58a5f6dbae0441e1197e0ce3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KustoEventgridDataConnectionConfig(
            cluster_name=cluster_name,
            database_name=database_name,
            eventhub_consumer_group_name=eventhub_consumer_group_name,
            eventhub_id=eventhub_id,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            storage_account_id=storage_account_id,
            blob_storage_event_type=blob_storage_event_type,
            database_routing_type=database_routing_type,
            data_format=data_format,
            eventgrid_event_subscription_id=eventgrid_event_subscription_id,
            eventgrid_resource_id=eventgrid_resource_id,
            id=id,
            managed_identity_id=managed_identity_id,
            managed_identity_resource_id=managed_identity_resource_id,
            mapping_rule_name=mapping_rule_name,
            skip_first_record=skip_first_record,
            table_name=table_name,
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
        '''Generates CDKTF code for importing a KustoEventgridDataConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KustoEventgridDataConnection to import.
        :param import_from_id: The id of the existing KustoEventgridDataConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KustoEventgridDataConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206361b8c9390bdd12bba140c4417535b031ef854ddb589615c8351a3d41daf2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#create KustoEventgridDataConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#delete KustoEventgridDataConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#read KustoEventgridDataConnection#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#update KustoEventgridDataConnection#update}.
        '''
        value = KustoEventgridDataConnectionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBlobStorageEventType")
    def reset_blob_storage_event_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlobStorageEventType", []))

    @jsii.member(jsii_name="resetDatabaseRoutingType")
    def reset_database_routing_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseRoutingType", []))

    @jsii.member(jsii_name="resetDataFormat")
    def reset_data_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFormat", []))

    @jsii.member(jsii_name="resetEventgridEventSubscriptionId")
    def reset_eventgrid_event_subscription_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventgridEventSubscriptionId", []))

    @jsii.member(jsii_name="resetEventgridResourceId")
    def reset_eventgrid_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventgridResourceId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetManagedIdentityId")
    def reset_managed_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedIdentityId", []))

    @jsii.member(jsii_name="resetManagedIdentityResourceId")
    def reset_managed_identity_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedIdentityResourceId", []))

    @jsii.member(jsii_name="resetMappingRuleName")
    def reset_mapping_rule_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingRuleName", []))

    @jsii.member(jsii_name="resetSkipFirstRecord")
    def reset_skip_first_record(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipFirstRecord", []))

    @jsii.member(jsii_name="resetTableName")
    def reset_table_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableName", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KustoEventgridDataConnectionTimeoutsOutputReference":
        return typing.cast("KustoEventgridDataConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="blobStorageEventTypeInput")
    def blob_storage_event_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blobStorageEventTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseRoutingTypeInput")
    def database_routing_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseRoutingTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFormatInput")
    def data_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="eventgridEventSubscriptionIdInput")
    def eventgrid_event_subscription_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventgridEventSubscriptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventgridResourceIdInput")
    def eventgrid_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventgridResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubConsumerGroupNameInput")
    def eventhub_consumer_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubConsumerGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubIdInput")
    def eventhub_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedIdentityIdInput")
    def managed_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="managedIdentityResourceIdInput")
    def managed_identity_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedIdentityResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingRuleNameInput")
    def mapping_rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingRuleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skipFirstRecordInput")
    def skip_first_record_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipFirstRecordInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KustoEventgridDataConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KustoEventgridDataConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="blobStorageEventType")
    def blob_storage_event_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "blobStorageEventType"))

    @blob_storage_event_type.setter
    def blob_storage_event_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fb0ab9d77be111cb14357921ff332f5a115e84c7c2915ab0122addf41220c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blobStorageEventType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b71a7f275d4b9f59b0551638ac1a7a0e9d6d3e9fa89dc0a6184bfa653668c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c88328f242686ef4d67dd45b9dd30e11f4878c6d630f6116c5b58ffea39763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseRoutingType")
    def database_routing_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseRoutingType"))

    @database_routing_type.setter
    def database_routing_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80bf199fca6433c2117806464b1bdbcb87402a2eae7387e9f277980f987e70bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseRoutingType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataFormat")
    def data_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFormat"))

    @data_format.setter
    def data_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402d1a57625876a1cbb433afe2ced7802c8f8fa8f9ec8f53c960f986a370b612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventgridEventSubscriptionId")
    def eventgrid_event_subscription_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventgridEventSubscriptionId"))

    @eventgrid_event_subscription_id.setter
    def eventgrid_event_subscription_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c3d989f69198301d58c56e13d8a7dddff91c70e6e6d37bfe7216f0e6e9fbd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventgridEventSubscriptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventgridResourceId")
    def eventgrid_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventgridResourceId"))

    @eventgrid_resource_id.setter
    def eventgrid_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398fb868b6cd42e58c0439964ff6f7a3beb5ccb7469cdba5ee151ca606578e1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventgridResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubConsumerGroupName")
    def eventhub_consumer_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubConsumerGroupName"))

    @eventhub_consumer_group_name.setter
    def eventhub_consumer_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02127df21f56069484eb32bf0fe8857f9c73338405052e14fa8a9251184b60a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubConsumerGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubId")
    def eventhub_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubId"))

    @eventhub_id.setter
    def eventhub_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d54f421ae9432845816cd35e18047ea199815344abf9d545a8c33e468b26062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab590799c759759ca0a574c59578b9e9bcd958bcb8a92f74467ad75962edbd7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3a861396ccc79b88309bfc92e0bc20c81a799f4d55fc631d914f1ed1400e7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedIdentityId")
    def managed_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedIdentityId"))

    @managed_identity_id.setter
    def managed_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ab503db7649c6390fe3902004b57545b8bfd078ded63251515e3fe4bd4b20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedIdentityResourceId")
    def managed_identity_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedIdentityResourceId"))

    @managed_identity_resource_id.setter
    def managed_identity_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf04e56abe6491c89797338ac876cc45c7989886c395d95e7922e6bca2d71a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedIdentityResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mappingRuleName")
    def mapping_rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mappingRuleName"))

    @mapping_rule_name.setter
    def mapping_rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19bf9d7fb5f059f9d068f2e6bdcfb740548f141074043c66995a43cfccedee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappingRuleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b097fc07c7876f97c4bf23af28218479a0129734bb804ac34b67636833a509a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96153776062dee3029cecffb20c2845d5cb9dca8195718008b4d6da25235d543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipFirstRecord")
    def skip_first_record(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipFirstRecord"))

    @skip_first_record.setter
    def skip_first_record(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0299683b6faff5a4f520e8f34d2d16da7d366542a076129ea067c015ae8145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipFirstRecord", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9a492ba9a12f99ed39997498f40aa445b6a7762f8b79aff5146ff747caa566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139ec699ab949f78333d45ca31762a68af3bc9903270a931206416b9ba6ecfe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoEventgridDataConnection.KustoEventgridDataConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_name": "clusterName",
        "database_name": "databaseName",
        "eventhub_consumer_group_name": "eventhubConsumerGroupName",
        "eventhub_id": "eventhubId",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "storage_account_id": "storageAccountId",
        "blob_storage_event_type": "blobStorageEventType",
        "database_routing_type": "databaseRoutingType",
        "data_format": "dataFormat",
        "eventgrid_event_subscription_id": "eventgridEventSubscriptionId",
        "eventgrid_resource_id": "eventgridResourceId",
        "id": "id",
        "managed_identity_id": "managedIdentityId",
        "managed_identity_resource_id": "managedIdentityResourceId",
        "mapping_rule_name": "mappingRuleName",
        "skip_first_record": "skipFirstRecord",
        "table_name": "tableName",
        "timeouts": "timeouts",
    },
)
class KustoEventgridDataConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_name: builtins.str,
        database_name: builtins.str,
        eventhub_consumer_group_name: builtins.str,
        eventhub_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_account_id: builtins.str,
        blob_storage_event_type: typing.Optional[builtins.str] = None,
        database_routing_type: typing.Optional[builtins.str] = None,
        data_format: typing.Optional[builtins.str] = None,
        eventgrid_event_subscription_id: typing.Optional[builtins.str] = None,
        eventgrid_resource_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        managed_identity_id: typing.Optional[builtins.str] = None,
        managed_identity_resource_id: typing.Optional[builtins.str] = None,
        mapping_rule_name: typing.Optional[builtins.str] = None,
        skip_first_record: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        table_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KustoEventgridDataConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#cluster_name KustoEventgridDataConnection#cluster_name}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#database_name KustoEventgridDataConnection#database_name}.
        :param eventhub_consumer_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventhub_consumer_group_name KustoEventgridDataConnection#eventhub_consumer_group_name}.
        :param eventhub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventhub_id KustoEventgridDataConnection#eventhub_id}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#location KustoEventgridDataConnection#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#name KustoEventgridDataConnection#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#resource_group_name KustoEventgridDataConnection#resource_group_name}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#storage_account_id KustoEventgridDataConnection#storage_account_id}.
        :param blob_storage_event_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#blob_storage_event_type KustoEventgridDataConnection#blob_storage_event_type}.
        :param database_routing_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#database_routing_type KustoEventgridDataConnection#database_routing_type}.
        :param data_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#data_format KustoEventgridDataConnection#data_format}.
        :param eventgrid_event_subscription_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventgrid_event_subscription_id KustoEventgridDataConnection#eventgrid_event_subscription_id}.
        :param eventgrid_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventgrid_resource_id KustoEventgridDataConnection#eventgrid_resource_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#id KustoEventgridDataConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param managed_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#managed_identity_id KustoEventgridDataConnection#managed_identity_id}.
        :param managed_identity_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#managed_identity_resource_id KustoEventgridDataConnection#managed_identity_resource_id}.
        :param mapping_rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#mapping_rule_name KustoEventgridDataConnection#mapping_rule_name}.
        :param skip_first_record: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#skip_first_record KustoEventgridDataConnection#skip_first_record}.
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#table_name KustoEventgridDataConnection#table_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#timeouts KustoEventgridDataConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = KustoEventgridDataConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244a90a584d5e652be625b48d9a3cef4a583b8d0d6f2a191647f4c654fd752dd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument eventhub_consumer_group_name", value=eventhub_consumer_group_name, expected_type=type_hints["eventhub_consumer_group_name"])
            check_type(argname="argument eventhub_id", value=eventhub_id, expected_type=type_hints["eventhub_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument blob_storage_event_type", value=blob_storage_event_type, expected_type=type_hints["blob_storage_event_type"])
            check_type(argname="argument database_routing_type", value=database_routing_type, expected_type=type_hints["database_routing_type"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument eventgrid_event_subscription_id", value=eventgrid_event_subscription_id, expected_type=type_hints["eventgrid_event_subscription_id"])
            check_type(argname="argument eventgrid_resource_id", value=eventgrid_resource_id, expected_type=type_hints["eventgrid_resource_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed_identity_id", value=managed_identity_id, expected_type=type_hints["managed_identity_id"])
            check_type(argname="argument managed_identity_resource_id", value=managed_identity_resource_id, expected_type=type_hints["managed_identity_resource_id"])
            check_type(argname="argument mapping_rule_name", value=mapping_rule_name, expected_type=type_hints["mapping_rule_name"])
            check_type(argname="argument skip_first_record", value=skip_first_record, expected_type=type_hints["skip_first_record"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "database_name": database_name,
            "eventhub_consumer_group_name": eventhub_consumer_group_name,
            "eventhub_id": eventhub_id,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "storage_account_id": storage_account_id,
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
        if blob_storage_event_type is not None:
            self._values["blob_storage_event_type"] = blob_storage_event_type
        if database_routing_type is not None:
            self._values["database_routing_type"] = database_routing_type
        if data_format is not None:
            self._values["data_format"] = data_format
        if eventgrid_event_subscription_id is not None:
            self._values["eventgrid_event_subscription_id"] = eventgrid_event_subscription_id
        if eventgrid_resource_id is not None:
            self._values["eventgrid_resource_id"] = eventgrid_resource_id
        if id is not None:
            self._values["id"] = id
        if managed_identity_id is not None:
            self._values["managed_identity_id"] = managed_identity_id
        if managed_identity_resource_id is not None:
            self._values["managed_identity_resource_id"] = managed_identity_resource_id
        if mapping_rule_name is not None:
            self._values["mapping_rule_name"] = mapping_rule_name
        if skip_first_record is not None:
            self._values["skip_first_record"] = skip_first_record
        if table_name is not None:
            self._values["table_name"] = table_name
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
    def cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#cluster_name KustoEventgridDataConnection#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#database_name KustoEventgridDataConnection#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_consumer_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventhub_consumer_group_name KustoEventgridDataConnection#eventhub_consumer_group_name}.'''
        result = self._values.get("eventhub_consumer_group_name")
        assert result is not None, "Required property 'eventhub_consumer_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventhub_id KustoEventgridDataConnection#eventhub_id}.'''
        result = self._values.get("eventhub_id")
        assert result is not None, "Required property 'eventhub_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#location KustoEventgridDataConnection#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#name KustoEventgridDataConnection#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#resource_group_name KustoEventgridDataConnection#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#storage_account_id KustoEventgridDataConnection#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        assert result is not None, "Required property 'storage_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def blob_storage_event_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#blob_storage_event_type KustoEventgridDataConnection#blob_storage_event_type}.'''
        result = self._values.get("blob_storage_event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_routing_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#database_routing_type KustoEventgridDataConnection#database_routing_type}.'''
        result = self._values.get("database_routing_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#data_format KustoEventgridDataConnection#data_format}.'''
        result = self._values.get("data_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventgrid_event_subscription_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventgrid_event_subscription_id KustoEventgridDataConnection#eventgrid_event_subscription_id}.'''
        result = self._values.get("eventgrid_event_subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventgrid_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#eventgrid_resource_id KustoEventgridDataConnection#eventgrid_resource_id}.'''
        result = self._values.get("eventgrid_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#id KustoEventgridDataConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#managed_identity_id KustoEventgridDataConnection#managed_identity_id}.'''
        result = self._values.get("managed_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_identity_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#managed_identity_resource_id KustoEventgridDataConnection#managed_identity_resource_id}.'''
        result = self._values.get("managed_identity_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mapping_rule_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#mapping_rule_name KustoEventgridDataConnection#mapping_rule_name}.'''
        result = self._values.get("mapping_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_first_record(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#skip_first_record KustoEventgridDataConnection#skip_first_record}.'''
        result = self._values.get("skip_first_record")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#table_name KustoEventgridDataConnection#table_name}.'''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KustoEventgridDataConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#timeouts KustoEventgridDataConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KustoEventgridDataConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoEventgridDataConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoEventgridDataConnection.KustoEventgridDataConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KustoEventgridDataConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#create KustoEventgridDataConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#delete KustoEventgridDataConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#read KustoEventgridDataConnection#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#update KustoEventgridDataConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f693c058af2f674fcf5eeb4a6c4adaf106718e0d0ecf002dbe513f0ea45027a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#create KustoEventgridDataConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#delete KustoEventgridDataConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#read KustoEventgridDataConnection#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_eventgrid_data_connection#update KustoEventgridDataConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoEventgridDataConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoEventgridDataConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoEventgridDataConnection.KustoEventgridDataConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37728d652646324d438974563df70be1edfea1ff0047b7e2d9165d2e1faecced)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab62db7ac9b028fb8ac584fdea20f7a1780402cc80a9201667a040a14eb3c892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3351ac61bb4bddaa35e3e5a1b80a64d44c289fd3728cf5f6b4a5e8e7cec9587e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8986adbdd4195e98fb8f651317322ebb940d1bb80b4bef636db93a2d82213b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a56be8ec6817ca630fcad298fe0a1ace9f988777d0a5535fcdd61c8b25b4964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoEventgridDataConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoEventgridDataConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoEventgridDataConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd315cd592508600193ddbfb27b34eb970f7b65fefc1bacce4bdadc2dfae3037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KustoEventgridDataConnection",
    "KustoEventgridDataConnectionConfig",
    "KustoEventgridDataConnectionTimeouts",
    "KustoEventgridDataConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8ec6226945dd229cc0f59fff29b3a0e31ed3f2bc58a5f6dbae0441e1197e0ce3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_name: builtins.str,
    database_name: builtins.str,
    eventhub_consumer_group_name: builtins.str,
    eventhub_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_account_id: builtins.str,
    blob_storage_event_type: typing.Optional[builtins.str] = None,
    database_routing_type: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    eventgrid_event_subscription_id: typing.Optional[builtins.str] = None,
    eventgrid_resource_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    managed_identity_id: typing.Optional[builtins.str] = None,
    managed_identity_resource_id: typing.Optional[builtins.str] = None,
    mapping_rule_name: typing.Optional[builtins.str] = None,
    skip_first_record: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    table_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KustoEventgridDataConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__206361b8c9390bdd12bba140c4417535b031ef854ddb589615c8351a3d41daf2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fb0ab9d77be111cb14357921ff332f5a115e84c7c2915ab0122addf41220c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b71a7f275d4b9f59b0551638ac1a7a0e9d6d3e9fa89dc0a6184bfa653668c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c88328f242686ef4d67dd45b9dd30e11f4878c6d630f6116c5b58ffea39763(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80bf199fca6433c2117806464b1bdbcb87402a2eae7387e9f277980f987e70bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402d1a57625876a1cbb433afe2ced7802c8f8fa8f9ec8f53c960f986a370b612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c3d989f69198301d58c56e13d8a7dddff91c70e6e6d37bfe7216f0e6e9fbd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398fb868b6cd42e58c0439964ff6f7a3beb5ccb7469cdba5ee151ca606578e1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02127df21f56069484eb32bf0fe8857f9c73338405052e14fa8a9251184b60a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d54f421ae9432845816cd35e18047ea199815344abf9d545a8c33e468b26062(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab590799c759759ca0a574c59578b9e9bcd958bcb8a92f74467ad75962edbd7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3a861396ccc79b88309bfc92e0bc20c81a799f4d55fc631d914f1ed1400e7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ab503db7649c6390fe3902004b57545b8bfd078ded63251515e3fe4bd4b20f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf04e56abe6491c89797338ac876cc45c7989886c395d95e7922e6bca2d71a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19bf9d7fb5f059f9d068f2e6bdcfb740548f141074043c66995a43cfccedee7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b097fc07c7876f97c4bf23af28218479a0129734bb804ac34b67636833a509a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96153776062dee3029cecffb20c2845d5cb9dca8195718008b4d6da25235d543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0299683b6faff5a4f520e8f34d2d16da7d366542a076129ea067c015ae8145(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9a492ba9a12f99ed39997498f40aa445b6a7762f8b79aff5146ff747caa566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139ec699ab949f78333d45ca31762a68af3bc9903270a931206416b9ba6ecfe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244a90a584d5e652be625b48d9a3cef4a583b8d0d6f2a191647f4c654fd752dd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_name: builtins.str,
    database_name: builtins.str,
    eventhub_consumer_group_name: builtins.str,
    eventhub_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_account_id: builtins.str,
    blob_storage_event_type: typing.Optional[builtins.str] = None,
    database_routing_type: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    eventgrid_event_subscription_id: typing.Optional[builtins.str] = None,
    eventgrid_resource_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    managed_identity_id: typing.Optional[builtins.str] = None,
    managed_identity_resource_id: typing.Optional[builtins.str] = None,
    mapping_rule_name: typing.Optional[builtins.str] = None,
    skip_first_record: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    table_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KustoEventgridDataConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f693c058af2f674fcf5eeb4a6c4adaf106718e0d0ecf002dbe513f0ea45027a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37728d652646324d438974563df70be1edfea1ff0047b7e2d9165d2e1faecced(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab62db7ac9b028fb8ac584fdea20f7a1780402cc80a9201667a040a14eb3c892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3351ac61bb4bddaa35e3e5a1b80a64d44c289fd3728cf5f6b4a5e8e7cec9587e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8986adbdd4195e98fb8f651317322ebb940d1bb80b4bef636db93a2d82213b6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a56be8ec6817ca630fcad298fe0a1ace9f988777d0a5535fcdd61c8b25b4964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd315cd592508600193ddbfb27b34eb970f7b65fefc1bacce4bdadc2dfae3037(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoEventgridDataConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
