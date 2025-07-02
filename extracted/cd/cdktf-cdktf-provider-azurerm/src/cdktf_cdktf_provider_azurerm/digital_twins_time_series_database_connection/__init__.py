r'''
# `azurerm_digital_twins_time_series_database_connection`

Refer to the Terraform Registry for docs: [`azurerm_digital_twins_time_series_database_connection`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection).
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


class DigitalTwinsTimeSeriesDatabaseConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.digitalTwinsTimeSeriesDatabaseConnection.DigitalTwinsTimeSeriesDatabaseConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection azurerm_digital_twins_time_series_database_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        digital_twins_id: builtins.str,
        eventhub_name: builtins.str,
        eventhub_namespace_endpoint_uri: builtins.str,
        eventhub_namespace_id: builtins.str,
        kusto_cluster_id: builtins.str,
        kusto_cluster_uri: builtins.str,
        kusto_database_name: builtins.str,
        name: builtins.str,
        eventhub_consumer_group_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kusto_table_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DigitalTwinsTimeSeriesDatabaseConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection azurerm_digital_twins_time_series_database_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param digital_twins_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#digital_twins_id DigitalTwinsTimeSeriesDatabaseConnection#digital_twins_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_name DigitalTwinsTimeSeriesDatabaseConnection#eventhub_name}.
        :param eventhub_namespace_endpoint_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_namespace_endpoint_uri DigitalTwinsTimeSeriesDatabaseConnection#eventhub_namespace_endpoint_uri}.
        :param eventhub_namespace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_namespace_id DigitalTwinsTimeSeriesDatabaseConnection#eventhub_namespace_id}.
        :param kusto_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_cluster_id DigitalTwinsTimeSeriesDatabaseConnection#kusto_cluster_id}.
        :param kusto_cluster_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_cluster_uri DigitalTwinsTimeSeriesDatabaseConnection#kusto_cluster_uri}.
        :param kusto_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_database_name DigitalTwinsTimeSeriesDatabaseConnection#kusto_database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#name DigitalTwinsTimeSeriesDatabaseConnection#name}.
        :param eventhub_consumer_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_consumer_group_name DigitalTwinsTimeSeriesDatabaseConnection#eventhub_consumer_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#id DigitalTwinsTimeSeriesDatabaseConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kusto_table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_table_name DigitalTwinsTimeSeriesDatabaseConnection#kusto_table_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#timeouts DigitalTwinsTimeSeriesDatabaseConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c45557ce117d68b7fdc2837bac2b86c5c8c8e1cd2262ee7b46aec45503daee5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DigitalTwinsTimeSeriesDatabaseConnectionConfig(
            digital_twins_id=digital_twins_id,
            eventhub_name=eventhub_name,
            eventhub_namespace_endpoint_uri=eventhub_namespace_endpoint_uri,
            eventhub_namespace_id=eventhub_namespace_id,
            kusto_cluster_id=kusto_cluster_id,
            kusto_cluster_uri=kusto_cluster_uri,
            kusto_database_name=kusto_database_name,
            name=name,
            eventhub_consumer_group_name=eventhub_consumer_group_name,
            id=id,
            kusto_table_name=kusto_table_name,
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
        '''Generates CDKTF code for importing a DigitalTwinsTimeSeriesDatabaseConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DigitalTwinsTimeSeriesDatabaseConnection to import.
        :param import_from_id: The id of the existing DigitalTwinsTimeSeriesDatabaseConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DigitalTwinsTimeSeriesDatabaseConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5343a4a7d08cd78b8d2fe02a33ebd7d7e3b9cbfdac4669d9260e4703a24d75)
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
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#create DigitalTwinsTimeSeriesDatabaseConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#delete DigitalTwinsTimeSeriesDatabaseConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#read DigitalTwinsTimeSeriesDatabaseConnection#read}.
        '''
        value = DigitalTwinsTimeSeriesDatabaseConnectionTimeouts(
            create=create, delete=delete, read=read
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEventhubConsumerGroupName")
    def reset_eventhub_consumer_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventhubConsumerGroupName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKustoTableName")
    def reset_kusto_table_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKustoTableName", []))

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
    def timeouts(
        self,
    ) -> "DigitalTwinsTimeSeriesDatabaseConnectionTimeoutsOutputReference":
        return typing.cast("DigitalTwinsTimeSeriesDatabaseConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="digitalTwinsIdInput")
    def digital_twins_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "digitalTwinsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubConsumerGroupNameInput")
    def eventhub_consumer_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubConsumerGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubNameInput")
    def eventhub_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubNamespaceEndpointUriInput")
    def eventhub_namespace_endpoint_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubNamespaceEndpointUriInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubNamespaceIdInput")
    def eventhub_namespace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubNamespaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kustoClusterIdInput")
    def kusto_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kustoClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="kustoClusterUriInput")
    def kusto_cluster_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kustoClusterUriInput"))

    @builtins.property
    @jsii.member(jsii_name="kustoDatabaseNameInput")
    def kusto_database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kustoDatabaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kustoTableNameInput")
    def kusto_table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kustoTableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DigitalTwinsTimeSeriesDatabaseConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DigitalTwinsTimeSeriesDatabaseConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="digitalTwinsId")
    def digital_twins_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digitalTwinsId"))

    @digital_twins_id.setter
    def digital_twins_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b241714ebef624399a7df324e5d864a034bc87e6d6e9ddb5d4d7a0201659b704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digitalTwinsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubConsumerGroupName")
    def eventhub_consumer_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubConsumerGroupName"))

    @eventhub_consumer_group_name.setter
    def eventhub_consumer_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40fc93709a6314fd6faed1911a4c3fcc343e07319c4df2f66efef79f2f0b145a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubConsumerGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubName")
    def eventhub_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubName"))

    @eventhub_name.setter
    def eventhub_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424ffd237c92584786ff691d80bfadd7eb3c7e3899f19bcd08892e14bb151a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubNamespaceEndpointUri")
    def eventhub_namespace_endpoint_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubNamespaceEndpointUri"))

    @eventhub_namespace_endpoint_uri.setter
    def eventhub_namespace_endpoint_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f4009cdf7be55335bd1b24f37aadf8564eebc359bf0616529fd1549b3d0772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubNamespaceEndpointUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubNamespaceId")
    def eventhub_namespace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubNamespaceId"))

    @eventhub_namespace_id.setter
    def eventhub_namespace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a371283e351c0d6da5027a316e2a038d2140c2303908e9787b1214545a2b9748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubNamespaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b27f196fd715e7f84f2655522119e303bc43e4352401d466d4089fe5a51027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kustoClusterId")
    def kusto_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kustoClusterId"))

    @kusto_cluster_id.setter
    def kusto_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd611930258b6448cd8f36a08552faa74904feed22c64694d29d9cb7cb2f4a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kustoClusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kustoClusterUri")
    def kusto_cluster_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kustoClusterUri"))

    @kusto_cluster_uri.setter
    def kusto_cluster_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35de8c21e932c3de47fef63c74b52234c17bafa554838a496cbef4967e79c953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kustoClusterUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kustoDatabaseName")
    def kusto_database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kustoDatabaseName"))

    @kusto_database_name.setter
    def kusto_database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1410ff728658a998930091e787552e48c8d16f5d522fb4d29847641f9d151e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kustoDatabaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kustoTableName")
    def kusto_table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kustoTableName"))

    @kusto_table_name.setter
    def kusto_table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755b04b0ee731dae2a3c3073c067f606e16c5a1de6c42584bb04060e2d868c8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kustoTableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712d0a03cc7f2a75a28a4e56c02bee5f24ca8547ab601edb1083f5238b4de209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.digitalTwinsTimeSeriesDatabaseConnection.DigitalTwinsTimeSeriesDatabaseConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "digital_twins_id": "digitalTwinsId",
        "eventhub_name": "eventhubName",
        "eventhub_namespace_endpoint_uri": "eventhubNamespaceEndpointUri",
        "eventhub_namespace_id": "eventhubNamespaceId",
        "kusto_cluster_id": "kustoClusterId",
        "kusto_cluster_uri": "kustoClusterUri",
        "kusto_database_name": "kustoDatabaseName",
        "name": "name",
        "eventhub_consumer_group_name": "eventhubConsumerGroupName",
        "id": "id",
        "kusto_table_name": "kustoTableName",
        "timeouts": "timeouts",
    },
)
class DigitalTwinsTimeSeriesDatabaseConnectionConfig(
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
        digital_twins_id: builtins.str,
        eventhub_name: builtins.str,
        eventhub_namespace_endpoint_uri: builtins.str,
        eventhub_namespace_id: builtins.str,
        kusto_cluster_id: builtins.str,
        kusto_cluster_uri: builtins.str,
        kusto_database_name: builtins.str,
        name: builtins.str,
        eventhub_consumer_group_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kusto_table_name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DigitalTwinsTimeSeriesDatabaseConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param digital_twins_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#digital_twins_id DigitalTwinsTimeSeriesDatabaseConnection#digital_twins_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_name DigitalTwinsTimeSeriesDatabaseConnection#eventhub_name}.
        :param eventhub_namespace_endpoint_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_namespace_endpoint_uri DigitalTwinsTimeSeriesDatabaseConnection#eventhub_namespace_endpoint_uri}.
        :param eventhub_namespace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_namespace_id DigitalTwinsTimeSeriesDatabaseConnection#eventhub_namespace_id}.
        :param kusto_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_cluster_id DigitalTwinsTimeSeriesDatabaseConnection#kusto_cluster_id}.
        :param kusto_cluster_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_cluster_uri DigitalTwinsTimeSeriesDatabaseConnection#kusto_cluster_uri}.
        :param kusto_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_database_name DigitalTwinsTimeSeriesDatabaseConnection#kusto_database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#name DigitalTwinsTimeSeriesDatabaseConnection#name}.
        :param eventhub_consumer_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_consumer_group_name DigitalTwinsTimeSeriesDatabaseConnection#eventhub_consumer_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#id DigitalTwinsTimeSeriesDatabaseConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kusto_table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_table_name DigitalTwinsTimeSeriesDatabaseConnection#kusto_table_name}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#timeouts DigitalTwinsTimeSeriesDatabaseConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DigitalTwinsTimeSeriesDatabaseConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6baab0788127a7808f26c8d89801819ec08995f16671c6820d520f3eb66d151)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument digital_twins_id", value=digital_twins_id, expected_type=type_hints["digital_twins_id"])
            check_type(argname="argument eventhub_name", value=eventhub_name, expected_type=type_hints["eventhub_name"])
            check_type(argname="argument eventhub_namespace_endpoint_uri", value=eventhub_namespace_endpoint_uri, expected_type=type_hints["eventhub_namespace_endpoint_uri"])
            check_type(argname="argument eventhub_namespace_id", value=eventhub_namespace_id, expected_type=type_hints["eventhub_namespace_id"])
            check_type(argname="argument kusto_cluster_id", value=kusto_cluster_id, expected_type=type_hints["kusto_cluster_id"])
            check_type(argname="argument kusto_cluster_uri", value=kusto_cluster_uri, expected_type=type_hints["kusto_cluster_uri"])
            check_type(argname="argument kusto_database_name", value=kusto_database_name, expected_type=type_hints["kusto_database_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument eventhub_consumer_group_name", value=eventhub_consumer_group_name, expected_type=type_hints["eventhub_consumer_group_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kusto_table_name", value=kusto_table_name, expected_type=type_hints["kusto_table_name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "digital_twins_id": digital_twins_id,
            "eventhub_name": eventhub_name,
            "eventhub_namespace_endpoint_uri": eventhub_namespace_endpoint_uri,
            "eventhub_namespace_id": eventhub_namespace_id,
            "kusto_cluster_id": kusto_cluster_id,
            "kusto_cluster_uri": kusto_cluster_uri,
            "kusto_database_name": kusto_database_name,
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
        if eventhub_consumer_group_name is not None:
            self._values["eventhub_consumer_group_name"] = eventhub_consumer_group_name
        if id is not None:
            self._values["id"] = id
        if kusto_table_name is not None:
            self._values["kusto_table_name"] = kusto_table_name
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
    def digital_twins_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#digital_twins_id DigitalTwinsTimeSeriesDatabaseConnection#digital_twins_id}.'''
        result = self._values.get("digital_twins_id")
        assert result is not None, "Required property 'digital_twins_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_name DigitalTwinsTimeSeriesDatabaseConnection#eventhub_name}.'''
        result = self._values.get("eventhub_name")
        assert result is not None, "Required property 'eventhub_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_namespace_endpoint_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_namespace_endpoint_uri DigitalTwinsTimeSeriesDatabaseConnection#eventhub_namespace_endpoint_uri}.'''
        result = self._values.get("eventhub_namespace_endpoint_uri")
        assert result is not None, "Required property 'eventhub_namespace_endpoint_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_namespace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_namespace_id DigitalTwinsTimeSeriesDatabaseConnection#eventhub_namespace_id}.'''
        result = self._values.get("eventhub_namespace_id")
        assert result is not None, "Required property 'eventhub_namespace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kusto_cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_cluster_id DigitalTwinsTimeSeriesDatabaseConnection#kusto_cluster_id}.'''
        result = self._values.get("kusto_cluster_id")
        assert result is not None, "Required property 'kusto_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kusto_cluster_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_cluster_uri DigitalTwinsTimeSeriesDatabaseConnection#kusto_cluster_uri}.'''
        result = self._values.get("kusto_cluster_uri")
        assert result is not None, "Required property 'kusto_cluster_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kusto_database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_database_name DigitalTwinsTimeSeriesDatabaseConnection#kusto_database_name}.'''
        result = self._values.get("kusto_database_name")
        assert result is not None, "Required property 'kusto_database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#name DigitalTwinsTimeSeriesDatabaseConnection#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_consumer_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#eventhub_consumer_group_name DigitalTwinsTimeSeriesDatabaseConnection#eventhub_consumer_group_name}.'''
        result = self._values.get("eventhub_consumer_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#id DigitalTwinsTimeSeriesDatabaseConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kusto_table_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#kusto_table_name DigitalTwinsTimeSeriesDatabaseConnection#kusto_table_name}.'''
        result = self._values.get("kusto_table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["DigitalTwinsTimeSeriesDatabaseConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#timeouts DigitalTwinsTimeSeriesDatabaseConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DigitalTwinsTimeSeriesDatabaseConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DigitalTwinsTimeSeriesDatabaseConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.digitalTwinsTimeSeriesDatabaseConnection.DigitalTwinsTimeSeriesDatabaseConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "read": "read"},
)
class DigitalTwinsTimeSeriesDatabaseConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#create DigitalTwinsTimeSeriesDatabaseConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#delete DigitalTwinsTimeSeriesDatabaseConnection#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#read DigitalTwinsTimeSeriesDatabaseConnection#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2d514e414f6f975453718a1f12a28c5269fb248dd35b94f3b842fdc352f41a)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#create DigitalTwinsTimeSeriesDatabaseConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#delete DigitalTwinsTimeSeriesDatabaseConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/digital_twins_time_series_database_connection#read DigitalTwinsTimeSeriesDatabaseConnection#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DigitalTwinsTimeSeriesDatabaseConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DigitalTwinsTimeSeriesDatabaseConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.digitalTwinsTimeSeriesDatabaseConnection.DigitalTwinsTimeSeriesDatabaseConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8e7d350292b21311df4949bbfa9695df35175f07c22de2ade41c189081e69db)
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
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9e29beac9d60c695be85309aac19b42b1668de7ddae7a015ae40a758a91d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4a40fab874e49dfd0f83cc2c7a31473731329d7c78687ab583223a4e600cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e88a39021f3eb6f7ad765725aaef2afb265f5d913983e06631fc84f3267a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DigitalTwinsTimeSeriesDatabaseConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DigitalTwinsTimeSeriesDatabaseConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DigitalTwinsTimeSeriesDatabaseConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292ea98db463b3ad4b6572f89395b590b5058c1ea8c4fd525cf3c73b1ae31a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DigitalTwinsTimeSeriesDatabaseConnection",
    "DigitalTwinsTimeSeriesDatabaseConnectionConfig",
    "DigitalTwinsTimeSeriesDatabaseConnectionTimeouts",
    "DigitalTwinsTimeSeriesDatabaseConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__8c45557ce117d68b7fdc2837bac2b86c5c8c8e1cd2262ee7b46aec45503daee5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    digital_twins_id: builtins.str,
    eventhub_name: builtins.str,
    eventhub_namespace_endpoint_uri: builtins.str,
    eventhub_namespace_id: builtins.str,
    kusto_cluster_id: builtins.str,
    kusto_cluster_uri: builtins.str,
    kusto_database_name: builtins.str,
    name: builtins.str,
    eventhub_consumer_group_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kusto_table_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DigitalTwinsTimeSeriesDatabaseConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ee5343a4a7d08cd78b8d2fe02a33ebd7d7e3b9cbfdac4669d9260e4703a24d75(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b241714ebef624399a7df324e5d864a034bc87e6d6e9ddb5d4d7a0201659b704(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40fc93709a6314fd6faed1911a4c3fcc343e07319c4df2f66efef79f2f0b145a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424ffd237c92584786ff691d80bfadd7eb3c7e3899f19bcd08892e14bb151a8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f4009cdf7be55335bd1b24f37aadf8564eebc359bf0616529fd1549b3d0772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a371283e351c0d6da5027a316e2a038d2140c2303908e9787b1214545a2b9748(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b27f196fd715e7f84f2655522119e303bc43e4352401d466d4089fe5a51027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd611930258b6448cd8f36a08552faa74904feed22c64694d29d9cb7cb2f4a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35de8c21e932c3de47fef63c74b52234c17bafa554838a496cbef4967e79c953(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1410ff728658a998930091e787552e48c8d16f5d522fb4d29847641f9d151e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755b04b0ee731dae2a3c3073c067f606e16c5a1de6c42584bb04060e2d868c8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712d0a03cc7f2a75a28a4e56c02bee5f24ca8547ab601edb1083f5238b4de209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6baab0788127a7808f26c8d89801819ec08995f16671c6820d520f3eb66d151(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    digital_twins_id: builtins.str,
    eventhub_name: builtins.str,
    eventhub_namespace_endpoint_uri: builtins.str,
    eventhub_namespace_id: builtins.str,
    kusto_cluster_id: builtins.str,
    kusto_cluster_uri: builtins.str,
    kusto_database_name: builtins.str,
    name: builtins.str,
    eventhub_consumer_group_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kusto_table_name: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DigitalTwinsTimeSeriesDatabaseConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2d514e414f6f975453718a1f12a28c5269fb248dd35b94f3b842fdc352f41a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e7d350292b21311df4949bbfa9695df35175f07c22de2ade41c189081e69db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9e29beac9d60c695be85309aac19b42b1668de7ddae7a015ae40a758a91d28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4a40fab874e49dfd0f83cc2c7a31473731329d7c78687ab583223a4e600cbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e88a39021f3eb6f7ad765725aaef2afb265f5d913983e06631fc84f3267a13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292ea98db463b3ad4b6572f89395b590b5058c1ea8c4fd525cf3c73b1ae31a87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DigitalTwinsTimeSeriesDatabaseConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
