r'''
# `azurerm_spring_cloud_app_cosmosdb_association`

Refer to the Terraform Registry for docs: [`azurerm_spring_cloud_app_cosmosdb_association`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association).
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


class SpringCloudAppCosmosdbAssociation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudAppCosmosdbAssociation.SpringCloudAppCosmosdbAssociation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association azurerm_spring_cloud_app_cosmosdb_association}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_type: builtins.str,
        cosmosdb_access_key: builtins.str,
        cosmosdb_account_id: builtins.str,
        name: builtins.str,
        spring_cloud_app_id: builtins.str,
        cosmosdb_cassandra_keyspace_name: typing.Optional[builtins.str] = None,
        cosmosdb_gremlin_database_name: typing.Optional[builtins.str] = None,
        cosmosdb_gremlin_graph_name: typing.Optional[builtins.str] = None,
        cosmosdb_mongo_database_name: typing.Optional[builtins.str] = None,
        cosmosdb_sql_database_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudAppCosmosdbAssociationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association azurerm_spring_cloud_app_cosmosdb_association} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#api_type SpringCloudAppCosmosdbAssociation#api_type}.
        :param cosmosdb_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_access_key SpringCloudAppCosmosdbAssociation#cosmosdb_access_key}.
        :param cosmosdb_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_account_id SpringCloudAppCosmosdbAssociation#cosmosdb_account_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#name SpringCloudAppCosmosdbAssociation#name}.
        :param spring_cloud_app_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#spring_cloud_app_id SpringCloudAppCosmosdbAssociation#spring_cloud_app_id}.
        :param cosmosdb_cassandra_keyspace_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_cassandra_keyspace_name SpringCloudAppCosmosdbAssociation#cosmosdb_cassandra_keyspace_name}.
        :param cosmosdb_gremlin_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_gremlin_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_gremlin_database_name}.
        :param cosmosdb_gremlin_graph_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_gremlin_graph_name SpringCloudAppCosmosdbAssociation#cosmosdb_gremlin_graph_name}.
        :param cosmosdb_mongo_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_mongo_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_mongo_database_name}.
        :param cosmosdb_sql_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_sql_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_sql_database_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#id SpringCloudAppCosmosdbAssociation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#timeouts SpringCloudAppCosmosdbAssociation#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f46c0f17addce4b3c5695365d9e90f8fd7aa7ff02a7dc648bd0e335905b77543)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SpringCloudAppCosmosdbAssociationConfig(
            api_type=api_type,
            cosmosdb_access_key=cosmosdb_access_key,
            cosmosdb_account_id=cosmosdb_account_id,
            name=name,
            spring_cloud_app_id=spring_cloud_app_id,
            cosmosdb_cassandra_keyspace_name=cosmosdb_cassandra_keyspace_name,
            cosmosdb_gremlin_database_name=cosmosdb_gremlin_database_name,
            cosmosdb_gremlin_graph_name=cosmosdb_gremlin_graph_name,
            cosmosdb_mongo_database_name=cosmosdb_mongo_database_name,
            cosmosdb_sql_database_name=cosmosdb_sql_database_name,
            id=id,
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
        '''Generates CDKTF code for importing a SpringCloudAppCosmosdbAssociation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SpringCloudAppCosmosdbAssociation to import.
        :param import_from_id: The id of the existing SpringCloudAppCosmosdbAssociation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SpringCloudAppCosmosdbAssociation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431face7f29c772a2e879e49c930fb4ecd9d1fe4544faa98ceec10631dba0b43)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#create SpringCloudAppCosmosdbAssociation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#delete SpringCloudAppCosmosdbAssociation#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#read SpringCloudAppCosmosdbAssociation#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#update SpringCloudAppCosmosdbAssociation#update}.
        '''
        value = SpringCloudAppCosmosdbAssociationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCosmosdbCassandraKeyspaceName")
    def reset_cosmosdb_cassandra_keyspace_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCosmosdbCassandraKeyspaceName", []))

    @jsii.member(jsii_name="resetCosmosdbGremlinDatabaseName")
    def reset_cosmosdb_gremlin_database_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCosmosdbGremlinDatabaseName", []))

    @jsii.member(jsii_name="resetCosmosdbGremlinGraphName")
    def reset_cosmosdb_gremlin_graph_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCosmosdbGremlinGraphName", []))

    @jsii.member(jsii_name="resetCosmosdbMongoDatabaseName")
    def reset_cosmosdb_mongo_database_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCosmosdbMongoDatabaseName", []))

    @jsii.member(jsii_name="resetCosmosdbSqlDatabaseName")
    def reset_cosmosdb_sql_database_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCosmosdbSqlDatabaseName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    def timeouts(self) -> "SpringCloudAppCosmosdbAssociationTimeoutsOutputReference":
        return typing.cast("SpringCloudAppCosmosdbAssociationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiTypeInput")
    def api_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="cosmosdbAccessKeyInput")
    def cosmosdb_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cosmosdbAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="cosmosdbAccountIdInput")
    def cosmosdb_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cosmosdbAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cosmosdbCassandraKeyspaceNameInput")
    def cosmosdb_cassandra_keyspace_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cosmosdbCassandraKeyspaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cosmosdbGremlinDatabaseNameInput")
    def cosmosdb_gremlin_database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cosmosdbGremlinDatabaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cosmosdbGremlinGraphNameInput")
    def cosmosdb_gremlin_graph_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cosmosdbGremlinGraphNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cosmosdbMongoDatabaseNameInput")
    def cosmosdb_mongo_database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cosmosdbMongoDatabaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="cosmosdbSqlDatabaseNameInput")
    def cosmosdb_sql_database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cosmosdbSqlDatabaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="springCloudAppIdInput")
    def spring_cloud_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "springCloudAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudAppCosmosdbAssociationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudAppCosmosdbAssociationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiType")
    def api_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiType"))

    @api_type.setter
    def api_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41748a7dd65ad10d7c15cd84670d88ac1474b9f295efd406a53a41b327985aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cosmosdbAccessKey")
    def cosmosdb_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cosmosdbAccessKey"))

    @cosmosdb_access_key.setter
    def cosmosdb_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79db368b5c42db15ae88ee6d2a0ec9f447ab4906747f5ff61d00a8317e3d025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cosmosdbAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cosmosdbAccountId")
    def cosmosdb_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cosmosdbAccountId"))

    @cosmosdb_account_id.setter
    def cosmosdb_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606f86b85284d1d1826da759403d5056e966fcb7435edc2b75301a152f6efa81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cosmosdbAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cosmosdbCassandraKeyspaceName")
    def cosmosdb_cassandra_keyspace_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cosmosdbCassandraKeyspaceName"))

    @cosmosdb_cassandra_keyspace_name.setter
    def cosmosdb_cassandra_keyspace_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d42fc8b84fe88913b040305078721cc194a1cafdc9f76a8bf3c785a215501bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cosmosdbCassandraKeyspaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cosmosdbGremlinDatabaseName")
    def cosmosdb_gremlin_database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cosmosdbGremlinDatabaseName"))

    @cosmosdb_gremlin_database_name.setter
    def cosmosdb_gremlin_database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f14b91abaa23daf32c79c59a337810b57b25dbb312c29ae2925fffd6c57101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cosmosdbGremlinDatabaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cosmosdbGremlinGraphName")
    def cosmosdb_gremlin_graph_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cosmosdbGremlinGraphName"))

    @cosmosdb_gremlin_graph_name.setter
    def cosmosdb_gremlin_graph_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5f998652a068fb822dd839c923f5bf6ddac9839b972fd97c53c1ab2fd1333a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cosmosdbGremlinGraphName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cosmosdbMongoDatabaseName")
    def cosmosdb_mongo_database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cosmosdbMongoDatabaseName"))

    @cosmosdb_mongo_database_name.setter
    def cosmosdb_mongo_database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f144ce1a9ef4057f5acc39e7afe0e545b260709e3c902b89d8a313738702cca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cosmosdbMongoDatabaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cosmosdbSqlDatabaseName")
    def cosmosdb_sql_database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cosmosdbSqlDatabaseName"))

    @cosmosdb_sql_database_name.setter
    def cosmosdb_sql_database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4b1bb58f2a8e2c6b7296131f6a263cf4ceb98c5e0a54289afa9adbb2e23c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cosmosdbSqlDatabaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856015c81ccaccf4fb2733b9952ecea1fdadcd9c665c90bba81fb2772e2395d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c866d054506d756167b0bf68b92cc66bc48757bc0ff071ac1fb0b67862eec86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="springCloudAppId")
    def spring_cloud_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "springCloudAppId"))

    @spring_cloud_app_id.setter
    def spring_cloud_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbaa12b3dff277b1160018e30863f3204cd749aa20d5eaa764c175bf2d4119c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "springCloudAppId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudAppCosmosdbAssociation.SpringCloudAppCosmosdbAssociationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_type": "apiType",
        "cosmosdb_access_key": "cosmosdbAccessKey",
        "cosmosdb_account_id": "cosmosdbAccountId",
        "name": "name",
        "spring_cloud_app_id": "springCloudAppId",
        "cosmosdb_cassandra_keyspace_name": "cosmosdbCassandraKeyspaceName",
        "cosmosdb_gremlin_database_name": "cosmosdbGremlinDatabaseName",
        "cosmosdb_gremlin_graph_name": "cosmosdbGremlinGraphName",
        "cosmosdb_mongo_database_name": "cosmosdbMongoDatabaseName",
        "cosmosdb_sql_database_name": "cosmosdbSqlDatabaseName",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class SpringCloudAppCosmosdbAssociationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_type: builtins.str,
        cosmosdb_access_key: builtins.str,
        cosmosdb_account_id: builtins.str,
        name: builtins.str,
        spring_cloud_app_id: builtins.str,
        cosmosdb_cassandra_keyspace_name: typing.Optional[builtins.str] = None,
        cosmosdb_gremlin_database_name: typing.Optional[builtins.str] = None,
        cosmosdb_gremlin_graph_name: typing.Optional[builtins.str] = None,
        cosmosdb_mongo_database_name: typing.Optional[builtins.str] = None,
        cosmosdb_sql_database_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudAppCosmosdbAssociationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#api_type SpringCloudAppCosmosdbAssociation#api_type}.
        :param cosmosdb_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_access_key SpringCloudAppCosmosdbAssociation#cosmosdb_access_key}.
        :param cosmosdb_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_account_id SpringCloudAppCosmosdbAssociation#cosmosdb_account_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#name SpringCloudAppCosmosdbAssociation#name}.
        :param spring_cloud_app_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#spring_cloud_app_id SpringCloudAppCosmosdbAssociation#spring_cloud_app_id}.
        :param cosmosdb_cassandra_keyspace_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_cassandra_keyspace_name SpringCloudAppCosmosdbAssociation#cosmosdb_cassandra_keyspace_name}.
        :param cosmosdb_gremlin_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_gremlin_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_gremlin_database_name}.
        :param cosmosdb_gremlin_graph_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_gremlin_graph_name SpringCloudAppCosmosdbAssociation#cosmosdb_gremlin_graph_name}.
        :param cosmosdb_mongo_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_mongo_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_mongo_database_name}.
        :param cosmosdb_sql_database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_sql_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_sql_database_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#id SpringCloudAppCosmosdbAssociation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#timeouts SpringCloudAppCosmosdbAssociation#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SpringCloudAppCosmosdbAssociationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0f2009a67bd66a3fa0eb8dec03ec353fc4e16fdc09b9e7407d99b1cad1fb9d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_type", value=api_type, expected_type=type_hints["api_type"])
            check_type(argname="argument cosmosdb_access_key", value=cosmosdb_access_key, expected_type=type_hints["cosmosdb_access_key"])
            check_type(argname="argument cosmosdb_account_id", value=cosmosdb_account_id, expected_type=type_hints["cosmosdb_account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spring_cloud_app_id", value=spring_cloud_app_id, expected_type=type_hints["spring_cloud_app_id"])
            check_type(argname="argument cosmosdb_cassandra_keyspace_name", value=cosmosdb_cassandra_keyspace_name, expected_type=type_hints["cosmosdb_cassandra_keyspace_name"])
            check_type(argname="argument cosmosdb_gremlin_database_name", value=cosmosdb_gremlin_database_name, expected_type=type_hints["cosmosdb_gremlin_database_name"])
            check_type(argname="argument cosmosdb_gremlin_graph_name", value=cosmosdb_gremlin_graph_name, expected_type=type_hints["cosmosdb_gremlin_graph_name"])
            check_type(argname="argument cosmosdb_mongo_database_name", value=cosmosdb_mongo_database_name, expected_type=type_hints["cosmosdb_mongo_database_name"])
            check_type(argname="argument cosmosdb_sql_database_name", value=cosmosdb_sql_database_name, expected_type=type_hints["cosmosdb_sql_database_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_type": api_type,
            "cosmosdb_access_key": cosmosdb_access_key,
            "cosmosdb_account_id": cosmosdb_account_id,
            "name": name,
            "spring_cloud_app_id": spring_cloud_app_id,
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
        if cosmosdb_cassandra_keyspace_name is not None:
            self._values["cosmosdb_cassandra_keyspace_name"] = cosmosdb_cassandra_keyspace_name
        if cosmosdb_gremlin_database_name is not None:
            self._values["cosmosdb_gremlin_database_name"] = cosmosdb_gremlin_database_name
        if cosmosdb_gremlin_graph_name is not None:
            self._values["cosmosdb_gremlin_graph_name"] = cosmosdb_gremlin_graph_name
        if cosmosdb_mongo_database_name is not None:
            self._values["cosmosdb_mongo_database_name"] = cosmosdb_mongo_database_name
        if cosmosdb_sql_database_name is not None:
            self._values["cosmosdb_sql_database_name"] = cosmosdb_sql_database_name
        if id is not None:
            self._values["id"] = id
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
    def api_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#api_type SpringCloudAppCosmosdbAssociation#api_type}.'''
        result = self._values.get("api_type")
        assert result is not None, "Required property 'api_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cosmosdb_access_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_access_key SpringCloudAppCosmosdbAssociation#cosmosdb_access_key}.'''
        result = self._values.get("cosmosdb_access_key")
        assert result is not None, "Required property 'cosmosdb_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cosmosdb_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_account_id SpringCloudAppCosmosdbAssociation#cosmosdb_account_id}.'''
        result = self._values.get("cosmosdb_account_id")
        assert result is not None, "Required property 'cosmosdb_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#name SpringCloudAppCosmosdbAssociation#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spring_cloud_app_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#spring_cloud_app_id SpringCloudAppCosmosdbAssociation#spring_cloud_app_id}.'''
        result = self._values.get("spring_cloud_app_id")
        assert result is not None, "Required property 'spring_cloud_app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cosmosdb_cassandra_keyspace_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_cassandra_keyspace_name SpringCloudAppCosmosdbAssociation#cosmosdb_cassandra_keyspace_name}.'''
        result = self._values.get("cosmosdb_cassandra_keyspace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cosmosdb_gremlin_database_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_gremlin_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_gremlin_database_name}.'''
        result = self._values.get("cosmosdb_gremlin_database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cosmosdb_gremlin_graph_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_gremlin_graph_name SpringCloudAppCosmosdbAssociation#cosmosdb_gremlin_graph_name}.'''
        result = self._values.get("cosmosdb_gremlin_graph_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cosmosdb_mongo_database_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_mongo_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_mongo_database_name}.'''
        result = self._values.get("cosmosdb_mongo_database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cosmosdb_sql_database_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#cosmosdb_sql_database_name SpringCloudAppCosmosdbAssociation#cosmosdb_sql_database_name}.'''
        result = self._values.get("cosmosdb_sql_database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#id SpringCloudAppCosmosdbAssociation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SpringCloudAppCosmosdbAssociationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#timeouts SpringCloudAppCosmosdbAssociation#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SpringCloudAppCosmosdbAssociationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudAppCosmosdbAssociationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudAppCosmosdbAssociation.SpringCloudAppCosmosdbAssociationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SpringCloudAppCosmosdbAssociationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#create SpringCloudAppCosmosdbAssociation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#delete SpringCloudAppCosmosdbAssociation#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#read SpringCloudAppCosmosdbAssociation#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#update SpringCloudAppCosmosdbAssociation#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__559008c9e54687c23f8074a8c755f7052d8bb50e3c36f2be9bac68891c47f277)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#create SpringCloudAppCosmosdbAssociation#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#delete SpringCloudAppCosmosdbAssociation#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#read SpringCloudAppCosmosdbAssociation#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_cosmosdb_association#update SpringCloudAppCosmosdbAssociation#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudAppCosmosdbAssociationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudAppCosmosdbAssociationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudAppCosmosdbAssociation.SpringCloudAppCosmosdbAssociationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de20497209de34f5e59e58658cfbce9d98b15e35c2307eae90c532c8201e1a42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a26c6f3ebd7d0c5d7e892152903d97a423f5f8b27c4cf2724308c035184bb7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3507f89a4f41d243bee77ad06edfa26f5ff3d6b2cdc7b58a0c7e0fe7bc99105b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f53a9a073756ad422bef08dbf8ad2c804785c50adcc237d3e241b15b86e8432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7dacf4db350730774a89eef493a07b31c7bcda4530895695c0cc8df036d200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudAppCosmosdbAssociationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudAppCosmosdbAssociationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudAppCosmosdbAssociationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1fe890b4394320a350f0ce858bc4706b8ac4a76aa58ff0bad519b5e1e516a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SpringCloudAppCosmosdbAssociation",
    "SpringCloudAppCosmosdbAssociationConfig",
    "SpringCloudAppCosmosdbAssociationTimeouts",
    "SpringCloudAppCosmosdbAssociationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f46c0f17addce4b3c5695365d9e90f8fd7aa7ff02a7dc648bd0e335905b77543(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_type: builtins.str,
    cosmosdb_access_key: builtins.str,
    cosmosdb_account_id: builtins.str,
    name: builtins.str,
    spring_cloud_app_id: builtins.str,
    cosmosdb_cassandra_keyspace_name: typing.Optional[builtins.str] = None,
    cosmosdb_gremlin_database_name: typing.Optional[builtins.str] = None,
    cosmosdb_gremlin_graph_name: typing.Optional[builtins.str] = None,
    cosmosdb_mongo_database_name: typing.Optional[builtins.str] = None,
    cosmosdb_sql_database_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudAppCosmosdbAssociationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__431face7f29c772a2e879e49c930fb4ecd9d1fe4544faa98ceec10631dba0b43(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41748a7dd65ad10d7c15cd84670d88ac1474b9f295efd406a53a41b327985aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79db368b5c42db15ae88ee6d2a0ec9f447ab4906747f5ff61d00a8317e3d025(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606f86b85284d1d1826da759403d5056e966fcb7435edc2b75301a152f6efa81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d42fc8b84fe88913b040305078721cc194a1cafdc9f76a8bf3c785a215501bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f14b91abaa23daf32c79c59a337810b57b25dbb312c29ae2925fffd6c57101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5f998652a068fb822dd839c923f5bf6ddac9839b972fd97c53c1ab2fd1333a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f144ce1a9ef4057f5acc39e7afe0e545b260709e3c902b89d8a313738702cca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4b1bb58f2a8e2c6b7296131f6a263cf4ceb98c5e0a54289afa9adbb2e23c48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856015c81ccaccf4fb2733b9952ecea1fdadcd9c665c90bba81fb2772e2395d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c866d054506d756167b0bf68b92cc66bc48757bc0ff071ac1fb0b67862eec86e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbaa12b3dff277b1160018e30863f3204cd749aa20d5eaa764c175bf2d4119c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0f2009a67bd66a3fa0eb8dec03ec353fc4e16fdc09b9e7407d99b1cad1fb9d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_type: builtins.str,
    cosmosdb_access_key: builtins.str,
    cosmosdb_account_id: builtins.str,
    name: builtins.str,
    spring_cloud_app_id: builtins.str,
    cosmosdb_cassandra_keyspace_name: typing.Optional[builtins.str] = None,
    cosmosdb_gremlin_database_name: typing.Optional[builtins.str] = None,
    cosmosdb_gremlin_graph_name: typing.Optional[builtins.str] = None,
    cosmosdb_mongo_database_name: typing.Optional[builtins.str] = None,
    cosmosdb_sql_database_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudAppCosmosdbAssociationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559008c9e54687c23f8074a8c755f7052d8bb50e3c36f2be9bac68891c47f277(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de20497209de34f5e59e58658cfbce9d98b15e35c2307eae90c532c8201e1a42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26c6f3ebd7d0c5d7e892152903d97a423f5f8b27c4cf2724308c035184bb7cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3507f89a4f41d243bee77ad06edfa26f5ff3d6b2cdc7b58a0c7e0fe7bc99105b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f53a9a073756ad422bef08dbf8ad2c804785c50adcc237d3e241b15b86e8432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7dacf4db350730774a89eef493a07b31c7bcda4530895695c0cc8df036d200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1fe890b4394320a350f0ce858bc4706b8ac4a76aa58ff0bad519b5e1e516a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudAppCosmosdbAssociationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
