r'''
# `snowflake_table`

Refer to the Terraform Registry for docs: [`snowflake_table`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table).
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


class Table(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.table.Table",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table snowflake_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TableColumn", typing.Dict[builtins.str, typing.Any]]]],
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        change_tracking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cluster_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        primary_key: typing.Optional[typing.Union["TablePrimaryKey", typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TableTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table snowflake_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param column: column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#column Table#column}
        :param database: The database in which to create the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#database Table#database}
        :param name: Specifies the identifier for the table; must be unique for the database and schema in which the table is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        :param schema: The schema in which to create the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#schema Table#schema}
        :param change_tracking: Specifies whether to enable change tracking on the table. Default false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#change_tracking Table#change_tracking}
        :param cluster_by: A list of one or more table columns/expressions to be used as clustering key(s) for the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#cluster_by Table#cluster_by}
        :param comment: Specifies a comment for the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#comment Table#comment}
        :param data_retention_time_in_days: Specifies the retention period for the table so that Time Travel actions (SELECT, CLONE, UNDROP) can be performed on historical data in the table. If you wish to inherit the parent schema setting then pass in the schema attribute to this argument or do not fill this parameter at all; the default value for this field is -1, which is a fallback to use Snowflake default - in this case the schema value Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#data_retention_time_in_days Table#data_retention_time_in_days}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#id Table#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_key: primary_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#primary_key Table#primary_key}
        :param tag: tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#tag Table#tag}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c34a3a7fbf467b6f088ccaec0448dce902e91b6d06e75b1342820d42d64919bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TableConfig(
            column=column,
            database=database,
            name=name,
            schema=schema,
            change_tracking=change_tracking,
            cluster_by=cluster_by,
            comment=comment,
            data_retention_time_in_days=data_retention_time_in_days,
            id=id,
            primary_key=primary_key,
            tag=tag,
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
        '''Generates CDKTF code for importing a Table resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Table to import.
        :param import_from_id: The id of the existing Table that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Table to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d5b041b62800ee19fde346ac50747c2919a7443e6bdfe72b7e6d756f49bd94)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putColumn")
    def put_column(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TableColumn", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b2e37b75797643ef19decac7a128e25092e1bcaa78e2ece60c035498249f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumn", [value]))

    @jsii.member(jsii_name="putPrimaryKey")
    def put_primary_key(
        self,
        *,
        keys: typing.Sequence[builtins.str],
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keys: Columns to use in primary key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#keys Table#keys}
        :param name: Name of constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        '''
        value = TablePrimaryKey(keys=keys, name=name)

        return typing.cast(None, jsii.invoke(self, "putPrimaryKey", [value]))

    @jsii.member(jsii_name="putTag")
    def put_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TableTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e100d52ca3195287c2347dd8c3022dc8f6635227756cd89413407575a96ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTag", [value]))

    @jsii.member(jsii_name="resetChangeTracking")
    def reset_change_tracking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeTracking", []))

    @jsii.member(jsii_name="resetClusterBy")
    def reset_cluster_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterBy", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDataRetentionTimeInDays")
    def reset_data_retention_time_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataRetentionTimeInDays", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPrimaryKey")
    def reset_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKey", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

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
    @jsii.member(jsii_name="column")
    def column(self) -> "TableColumnList":
        return typing.cast("TableColumnList", jsii.get(self, "column"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> "TablePrimaryKeyOutputReference":
        return typing.cast("TablePrimaryKeyOutputReference", jsii.get(self, "primaryKey"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> "TableTagList":
        return typing.cast("TableTagList", jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="changeTrackingInput")
    def change_tracking_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "changeTrackingInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterByInput")
    def cluster_by_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clusterByInput"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TableColumn"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TableColumn"]]], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDaysInput")
    def data_retention_time_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataRetentionTimeInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(self) -> typing.Optional["TablePrimaryKey"]:
        return typing.cast(typing.Optional["TablePrimaryKey"], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TableTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TableTag"]]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="changeTracking")
    def change_tracking(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "changeTracking"))

    @change_tracking.setter
    def change_tracking(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f557e7c84f994d84d4c16246166e8e353309fb4f9662b281325e26093a034d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeTracking", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterBy")
    def cluster_by(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clusterBy"))

    @cluster_by.setter
    def cluster_by(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e40ab087f3526f143c3275eedb9d34927eeb7c729e40d1d081bda3a774b969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85c05d5178c7333068a66082054d259c457cef559571259efe3378824695981b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f947c3a810d5b964279b465a639a464458fbcaf0cdd8020591a8e84a6a389af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDays")
    def data_retention_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataRetentionTimeInDays"))

    @data_retention_time_in_days.setter
    def data_retention_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31ae151252fe01f4073fc2b01c61bc7bdecd86ad64d8b4003fde5ba96e93b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRetentionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd2419094c3776b7d1c01d7ec92d391297332daec25c2c700bdc75548b3ae49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc7c37352818083790b99200d1f788303122d057eb4c8cdc985e4acb4ae020c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdbd6cc8b25e7863301f9288544eff6f1709455b3d9a40f8474eb334893b8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.table.TableColumn",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "collate": "collate",
        "comment": "comment",
        "default": "default",
        "identity": "identity",
        "masking_policy": "maskingPolicy",
        "nullable": "nullable",
    },
)
class TableColumn:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        collate: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        default: typing.Optional[typing.Union["TableColumnDefault", typing.Dict[builtins.str, typing.Any]]] = None,
        identity: typing.Optional[typing.Union["TableColumnIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        masking_policy: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        :param type: Column type, e.g. VARIANT. For a full list of column types, see `Summary of Data Types <https://docs.snowflake.com/en/sql-reference/intro-summary-data-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#type Table#type}
        :param collate: Column collation, e.g. utf8. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#collate Table#collate}
        :param comment: Column comment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#comment Table#comment}
        :param default: default block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#default Table#default}
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#identity Table#identity}
        :param masking_policy: Masking policy to apply on column. It has to be a fully qualified name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#masking_policy Table#masking_policy}
        :param nullable: Whether this column can contain null values. **Note**: Depending on your Snowflake version, the default value will not suffice if this column is used in a primary key constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#nullable Table#nullable}
        '''
        if isinstance(default, dict):
            default = TableColumnDefault(**default)
        if isinstance(identity, dict):
            identity = TableColumnIdentity(**identity)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc19f46e9a052b2d4fb46a8c36fe8e7972b2326f98634a831453ebeccc2985e5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument collate", value=collate, expected_type=type_hints["collate"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument masking_policy", value=masking_policy, expected_type=type_hints["masking_policy"])
            check_type(argname="argument nullable", value=nullable, expected_type=type_hints["nullable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if collate is not None:
            self._values["collate"] = collate
        if comment is not None:
            self._values["comment"] = comment
        if default is not None:
            self._values["default"] = default
        if identity is not None:
            self._values["identity"] = identity
        if masking_policy is not None:
            self._values["masking_policy"] = masking_policy
        if nullable is not None:
            self._values["nullable"] = nullable

    @builtins.property
    def name(self) -> builtins.str:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Column type, e.g. VARIANT. For a full list of column types, see `Summary of Data Types <https://docs.snowflake.com/en/sql-reference/intro-summary-data-types>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#type Table#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collate(self) -> typing.Optional[builtins.str]:
        '''Column collation, e.g. utf8.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#collate Table#collate}
        '''
        result = self._values.get("collate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Column comment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#comment Table#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional["TableColumnDefault"]:
        '''default block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#default Table#default}
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional["TableColumnDefault"], result)

    @builtins.property
    def identity(self) -> typing.Optional["TableColumnIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#identity Table#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["TableColumnIdentity"], result)

    @builtins.property
    def masking_policy(self) -> typing.Optional[builtins.str]:
        '''Masking policy to apply on column. It has to be a fully qualified name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#masking_policy Table#masking_policy}
        '''
        result = self._values.get("masking_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nullable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this column can contain null values.

        **Note**: Depending on your Snowflake version, the default value will not suffice if this column is used in a primary key constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#nullable Table#nullable}
        '''
        result = self._values.get("nullable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableColumn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.table.TableColumnDefault",
    jsii_struct_bases=[],
    name_mapping={
        "constant": "constant",
        "expression": "expression",
        "sequence": "sequence",
    },
)
class TableColumnDefault:
    def __init__(
        self,
        *,
        constant: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        sequence: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param constant: The default constant value for the column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#constant Table#constant}
        :param expression: The default expression value for the column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#expression Table#expression}
        :param sequence: The default sequence to use for the column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#sequence Table#sequence}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f228c533337613ba577647df9836f23d1e17c64cecf1e3b40248703bdfa8362)
            check_type(argname="argument constant", value=constant, expected_type=type_hints["constant"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument sequence", value=sequence, expected_type=type_hints["sequence"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if constant is not None:
            self._values["constant"] = constant
        if expression is not None:
            self._values["expression"] = expression
        if sequence is not None:
            self._values["sequence"] = sequence

    @builtins.property
    def constant(self) -> typing.Optional[builtins.str]:
        '''The default constant value for the column.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#constant Table#constant}
        '''
        result = self._values.get("constant")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''The default expression value for the column.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#expression Table#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sequence(self) -> typing.Optional[builtins.str]:
        '''The default sequence to use for the column.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#sequence Table#sequence}
        '''
        result = self._values.get("sequence")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableColumnDefault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TableColumnDefaultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.table.TableColumnDefaultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3bf3c582b673ed8c3f3e64d281aa4bd9593b385041498bd06b4779b2224e5e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConstant")
    def reset_constant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstant", []))

    @jsii.member(jsii_name="resetExpression")
    def reset_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpression", []))

    @jsii.member(jsii_name="resetSequence")
    def reset_sequence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSequence", []))

    @builtins.property
    @jsii.member(jsii_name="constantInput")
    def constant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constantInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="sequenceInput")
    def sequence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sequenceInput"))

    @builtins.property
    @jsii.member(jsii_name="constant")
    def constant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "constant"))

    @constant.setter
    def constant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3670ef1a6fbdf7d132d1040dde2677503f05afd7e1ba924a739b21c620e8326d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d191e122d9cedd4964245f1444ff873e881c294cac04725f059a8734ebe9ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sequence")
    def sequence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sequence"))

    @sequence.setter
    def sequence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1229953c1ac290efe443d42d016a3491bc2b37796f88ac67e4b6fb4cf484a270)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sequence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TableColumnDefault]:
        return typing.cast(typing.Optional[TableColumnDefault], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TableColumnDefault]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283084e69fbd1d9937b0e3e93e6e629b945faffa49c71234d869a723236836c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.table.TableColumnIdentity",
    jsii_struct_bases=[],
    name_mapping={"start_num": "startNum", "step_num": "stepNum"},
)
class TableColumnIdentity:
    def __init__(
        self,
        *,
        start_num: typing.Optional[jsii.Number] = None,
        step_num: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_num: The number to start incrementing at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#start_num Table#start_num}
        :param step_num: Step size to increment by. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#step_num Table#step_num}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d69646ba613dad1f329becefb3324fd5cb6d5666b29162a84c7a28be76fce2a)
            check_type(argname="argument start_num", value=start_num, expected_type=type_hints["start_num"])
            check_type(argname="argument step_num", value=step_num, expected_type=type_hints["step_num"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if start_num is not None:
            self._values["start_num"] = start_num
        if step_num is not None:
            self._values["step_num"] = step_num

    @builtins.property
    def start_num(self) -> typing.Optional[jsii.Number]:
        '''The number to start incrementing at.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#start_num Table#start_num}
        '''
        result = self._values.get("start_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def step_num(self) -> typing.Optional[jsii.Number]:
        '''Step size to increment by.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#step_num Table#step_num}
        '''
        result = self._values.get("step_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableColumnIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TableColumnIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.table.TableColumnIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10da2c0ae8b81f4fa88feaba62472465986bb8f7e29c204f8711aa7bf7065ec9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStartNum")
    def reset_start_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartNum", []))

    @jsii.member(jsii_name="resetStepNum")
    def reset_step_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStepNum", []))

    @builtins.property
    @jsii.member(jsii_name="startNumInput")
    def start_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startNumInput"))

    @builtins.property
    @jsii.member(jsii_name="stepNumInput")
    def step_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stepNumInput"))

    @builtins.property
    @jsii.member(jsii_name="startNum")
    def start_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startNum"))

    @start_num.setter
    def start_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bcfc93464bb633acb29c2374a1f353c11c94702e8b732b80a59e2dc3f901b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stepNum")
    def step_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stepNum"))

    @step_num.setter
    def step_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05cb28324ed7c3b61ec35b6ca63a88a116bb8bc984bf24c6339b82efff0e43e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stepNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TableColumnIdentity]:
        return typing.cast(typing.Optional[TableColumnIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TableColumnIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15b4e2100691675b57cdde77be87b51b1f346508b8968cce5090f5fc17ab9e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TableColumnList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.table.TableColumnList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__475896fa9b0842d106ebfd21e3eb7a03a08dc086bf966a418e5d21c9ea9153ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TableColumnOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0833c486e2df5f3fb0f7a9ea630dd3dac87a7b5f6480d131ce8fcc1d90fb3a5a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TableColumnOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669dc44ad78306cd9efe55a949917760c51fa123f07e6556c22cfb3882688680)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4749eeea9dcfa86b53f1dbc45f30c99d5baf1c134b1a4219903845a048880ade)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb2520e2646b9597c90afdbe6cbb536ae8c47e02eb2e8b86c108f27704d77da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableColumn]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableColumn]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableColumn]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705fab543eb578ec9f1bd9ede33474c16d8b720345993b8e47e2a75b1340dd1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TableColumnOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.table.TableColumnOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2255bceb5447e57792b892b67d4d1eb11f2b1c92266ffc12dd0650122d874d3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDefault")
    def put_default(
        self,
        *,
        constant: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        sequence: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param constant: The default constant value for the column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#constant Table#constant}
        :param expression: The default expression value for the column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#expression Table#expression}
        :param sequence: The default sequence to use for the column. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#sequence Table#sequence}
        '''
        value = TableColumnDefault(
            constant=constant, expression=expression, sequence=sequence
        )

        return typing.cast(None, jsii.invoke(self, "putDefault", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        start_num: typing.Optional[jsii.Number] = None,
        step_num: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param start_num: The number to start incrementing at. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#start_num Table#start_num}
        :param step_num: Step size to increment by. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#step_num Table#step_num}
        '''
        value = TableColumnIdentity(start_num=start_num, step_num=step_num)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="resetCollate")
    def reset_collate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollate", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetMaskingPolicy")
    def reset_masking_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaskingPolicy", []))

    @jsii.member(jsii_name="resetNullable")
    def reset_nullable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullable", []))

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> TableColumnDefaultOutputReference:
        return typing.cast(TableColumnDefaultOutputReference, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> TableColumnIdentityOutputReference:
        return typing.cast(TableColumnIdentityOutputReference, jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="schemaEvolutionRecord")
    def schema_evolution_record(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaEvolutionRecord"))

    @builtins.property
    @jsii.member(jsii_name="collateInput")
    def collate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collateInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(self) -> typing.Optional[TableColumnDefault]:
        return typing.cast(typing.Optional[TableColumnDefault], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional[TableColumnIdentity]:
        return typing.cast(typing.Optional[TableColumnIdentity], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="maskingPolicyInput")
    def masking_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maskingPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nullableInput")
    def nullable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nullableInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="collate")
    def collate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collate"))

    @collate.setter
    def collate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98cb7456a68739e97e01060c91440db400920e4fda8438f560a1b1b82f5b870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ce58cf2b9ea13ae92cf542c283382a16ed2d12f62c07961ccef723d3517d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maskingPolicy")
    def masking_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maskingPolicy"))

    @masking_policy.setter
    def masking_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5324f1265946d8ab6dc5b94ef6efdfb7852ca5353cd543255b2cace7c9cb9666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maskingPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fba95cf5a3dcdfcb1a7a1bca66b7cca42192da439f6959a40e63724ee3be386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nullable"))

    @nullable.setter
    def nullable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c63746afe108f5e89557dc361fb55c3e95e49b8abfd9af97339a5c5b594fba16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1364327a787e159af7afceeff81ea5502e7ea08317605dfedccf299ca5376fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TableColumn]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TableColumn]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TableColumn]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21088387084d74b3c4dc1a29547e6d2ca16d62c927df6485129e4e8d22b92e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.table.TableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "column": "column",
        "database": "database",
        "name": "name",
        "schema": "schema",
        "change_tracking": "changeTracking",
        "cluster_by": "clusterBy",
        "comment": "comment",
        "data_retention_time_in_days": "dataRetentionTimeInDays",
        "id": "id",
        "primary_key": "primaryKey",
        "tag": "tag",
    },
)
class TableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TableColumn, typing.Dict[builtins.str, typing.Any]]]],
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        change_tracking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cluster_by: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        primary_key: typing.Optional[typing.Union["TablePrimaryKey", typing.Dict[builtins.str, typing.Any]]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TableTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param column: column block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#column Table#column}
        :param database: The database in which to create the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#database Table#database}
        :param name: Specifies the identifier for the table; must be unique for the database and schema in which the table is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        :param schema: The schema in which to create the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#schema Table#schema}
        :param change_tracking: Specifies whether to enable change tracking on the table. Default false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#change_tracking Table#change_tracking}
        :param cluster_by: A list of one or more table columns/expressions to be used as clustering key(s) for the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#cluster_by Table#cluster_by}
        :param comment: Specifies a comment for the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#comment Table#comment}
        :param data_retention_time_in_days: Specifies the retention period for the table so that Time Travel actions (SELECT, CLONE, UNDROP) can be performed on historical data in the table. If you wish to inherit the parent schema setting then pass in the schema attribute to this argument or do not fill this parameter at all; the default value for this field is -1, which is a fallback to use Snowflake default - in this case the schema value Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#data_retention_time_in_days Table#data_retention_time_in_days}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#id Table#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_key: primary_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#primary_key Table#primary_key}
        :param tag: tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#tag Table#tag}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(primary_key, dict):
            primary_key = TablePrimaryKey(**primary_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac05d8eaa3fd00717b2eed92d74c322e02128fde62a8f61fd8e80919c43ca42b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument change_tracking", value=change_tracking, expected_type=type_hints["change_tracking"])
            check_type(argname="argument cluster_by", value=cluster_by, expected_type=type_hints["cluster_by"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument data_retention_time_in_days", value=data_retention_time_in_days, expected_type=type_hints["data_retention_time_in_days"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "database": database,
            "name": name,
            "schema": schema,
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
        if change_tracking is not None:
            self._values["change_tracking"] = change_tracking
        if cluster_by is not None:
            self._values["cluster_by"] = cluster_by
        if comment is not None:
            self._values["comment"] = comment
        if data_retention_time_in_days is not None:
            self._values["data_retention_time_in_days"] = data_retention_time_in_days
        if id is not None:
            self._values["id"] = id
        if primary_key is not None:
            self._values["primary_key"] = primary_key
        if tag is not None:
            self._values["tag"] = tag

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
    def column(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableColumn]]:
        '''column block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#column Table#column}
        '''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableColumn]], result)

    @builtins.property
    def database(self) -> builtins.str:
        '''The database in which to create the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#database Table#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the table;

        must be unique for the database and schema in which the table is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#schema Table#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def change_tracking(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to enable change tracking on the table. Default false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#change_tracking Table#change_tracking}
        '''
        result = self._values.get("change_tracking")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cluster_by(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of one or more table columns/expressions to be used as clustering key(s) for the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#cluster_by Table#cluster_by}
        '''
        result = self._values.get("cluster_by")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#comment Table#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_retention_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the retention period for the table so that Time Travel actions (SELECT, CLONE, UNDROP) can be performed on historical data in the table.

        If you wish to inherit the parent schema setting then pass in the schema attribute to this argument or do not fill this parameter at all; the default value for this field is -1, which is a fallback to use Snowflake default - in this case the schema value

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#data_retention_time_in_days Table#data_retention_time_in_days}
        '''
        result = self._values.get("data_retention_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#id Table#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_key(self) -> typing.Optional["TablePrimaryKey"]:
        '''primary_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#primary_key Table#primary_key}
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional["TablePrimaryKey"], result)

    @builtins.property
    def tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TableTag"]]]:
        '''tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#tag Table#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TableTag"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.table.TablePrimaryKey",
    jsii_struct_bases=[],
    name_mapping={"keys": "keys", "name": "name"},
)
class TablePrimaryKey:
    def __init__(
        self,
        *,
        keys: typing.Sequence[builtins.str],
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param keys: Columns to use in primary key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#keys Table#keys}
        :param name: Name of constraint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b83d277a71158a0b7d1b68db84f581f7a9a3a26606538c9a94becf6a0b597b0)
            check_type(argname="argument keys", value=keys, expected_type=type_hints["keys"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "keys": keys,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def keys(self) -> typing.List[builtins.str]:
        '''Columns to use in primary key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#keys Table#keys}
        '''
        result = self._values.get("keys")
        assert result is not None, "Required property 'keys' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of constraint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TablePrimaryKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TablePrimaryKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.table.TablePrimaryKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0228d3408f16bb0f4ef51d5856dddf881a08105de828d986bf626eaa28b6ef0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="keysInput")
    def keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keysInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="keys")
    def keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keys"))

    @keys.setter
    def keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a410e4f01f474c2cc443cc84932b8a280c8f2c8b3c07c9970a4dc069ce8c64b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c4b283a36728baa0a7fbe6e83e844d4dc3dcf20acc88987b12571a10f07aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TablePrimaryKey]:
        return typing.cast(typing.Optional[TablePrimaryKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TablePrimaryKey]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366ed374e5cd41004e15a7279c365f640aa48284c26cb02bcb101f96a530ad21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.table.TableTag",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "value": "value",
        "database": "database",
        "schema": "schema",
    },
)
class TableTag:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: builtins.str,
        database: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Tag name, e.g. department. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        :param value: Tag value, e.g. marketing_info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#value Table#value}
        :param database: Name of the database that the tag was created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#database Table#database}
        :param schema: Name of the schema that the tag was created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#schema Table#schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25936c5c9190c8854badeb92b6a010e3675185446908c41550a6d447cea808c0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }
        if database is not None:
            self._values["database"] = database
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def name(self) -> builtins.str:
        '''Tag name, e.g. department.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#name Table#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Tag value, e.g. marketing_info.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#value Table#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Name of the database that the tag was created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#database Table#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Name of the schema that the tag was created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/table#schema Table#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TableTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.table.TableTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36fc001c11ba664209f015677c4a91fca51f57e19baef5ccd91207d25943154e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TableTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee914f62dc5efc7e66fb5716d1eba8b2fc7cd4b5b978b10d65f2c11e5e1bd5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TableTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ad8d9cca6e75972209deadc0afb77f17804a7ac37bcee414ad55c8b56ea13e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4247d8cd62a36a7631c69b350fd273be411447fdb7ca8910e6fae88c09a2252d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35632c7b5f729a41f7dc34f57098f09f6e9d2f60eebce5e39fc90512e45bbfe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75abb82e1c533943ab02f8491cc75725d443f2876a67b31ca58717862b32ea63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TableTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.table.TableTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e08a8311705a96a6cd5765d4709cb6b0bd2c176dca0900c50292b3886d38a48b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea6f31a65ff9a9551bfa6f3c7146fa0786269ed0f86cfe21d5aea9b4deee735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a2c95536638ec2ba3de76e83889c8495d6fca26f15629dc38c221b466cad48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aacdf963c87f58a97f775dd89291ab05366d83d459ce7012b90ec5601990cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51454120cc71a02dce435b52966a4bb397f00bd8cdb8040a168e783153dbcfaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TableTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TableTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TableTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6925f0ff58242f27e3b8af233815c2a67713ab9c4b7e5eb5f257a47c51ccbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Table",
    "TableColumn",
    "TableColumnDefault",
    "TableColumnDefaultOutputReference",
    "TableColumnIdentity",
    "TableColumnIdentityOutputReference",
    "TableColumnList",
    "TableColumnOutputReference",
    "TableConfig",
    "TablePrimaryKey",
    "TablePrimaryKeyOutputReference",
    "TableTag",
    "TableTagList",
    "TableTagOutputReference",
]

publication.publish()

def _typecheckingstub__c34a3a7fbf467b6f088ccaec0448dce902e91b6d06e75b1342820d42d64919bd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TableColumn, typing.Dict[builtins.str, typing.Any]]]],
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    change_tracking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cluster_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    primary_key: typing.Optional[typing.Union[TablePrimaryKey, typing.Dict[builtins.str, typing.Any]]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TableTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__54d5b041b62800ee19fde346ac50747c2919a7443e6bdfe72b7e6d756f49bd94(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b2e37b75797643ef19decac7a128e25092e1bcaa78e2ece60c035498249f2d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TableColumn, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e100d52ca3195287c2347dd8c3022dc8f6635227756cd89413407575a96ed0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TableTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f557e7c84f994d84d4c16246166e8e353309fb4f9662b281325e26093a034d41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e40ab087f3526f143c3275eedb9d34927eeb7c729e40d1d081bda3a774b969(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c05d5178c7333068a66082054d259c457cef559571259efe3378824695981b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f947c3a810d5b964279b465a639a464458fbcaf0cdd8020591a8e84a6a389af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31ae151252fe01f4073fc2b01c61bc7bdecd86ad64d8b4003fde5ba96e93b9a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd2419094c3776b7d1c01d7ec92d391297332daec25c2c700bdc75548b3ae49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc7c37352818083790b99200d1f788303122d057eb4c8cdc985e4acb4ae020c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdbd6cc8b25e7863301f9288544eff6f1709455b3d9a40f8474eb334893b8d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc19f46e9a052b2d4fb46a8c36fe8e7972b2326f98634a831453ebeccc2985e5(
    *,
    name: builtins.str,
    type: builtins.str,
    collate: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    default: typing.Optional[typing.Union[TableColumnDefault, typing.Dict[builtins.str, typing.Any]]] = None,
    identity: typing.Optional[typing.Union[TableColumnIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    masking_policy: typing.Optional[builtins.str] = None,
    nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f228c533337613ba577647df9836f23d1e17c64cecf1e3b40248703bdfa8362(
    *,
    constant: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    sequence: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bf3c582b673ed8c3f3e64d281aa4bd9593b385041498bd06b4779b2224e5e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3670ef1a6fbdf7d132d1040dde2677503f05afd7e1ba924a739b21c620e8326d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d191e122d9cedd4964245f1444ff873e881c294cac04725f059a8734ebe9ed5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1229953c1ac290efe443d42d016a3491bc2b37796f88ac67e4b6fb4cf484a270(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283084e69fbd1d9937b0e3e93e6e629b945faffa49c71234d869a723236836c3(
    value: typing.Optional[TableColumnDefault],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d69646ba613dad1f329becefb3324fd5cb6d5666b29162a84c7a28be76fce2a(
    *,
    start_num: typing.Optional[jsii.Number] = None,
    step_num: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10da2c0ae8b81f4fa88feaba62472465986bb8f7e29c204f8711aa7bf7065ec9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bcfc93464bb633acb29c2374a1f353c11c94702e8b732b80a59e2dc3f901b2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05cb28324ed7c3b61ec35b6ca63a88a116bb8bc984bf24c6339b82efff0e43e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15b4e2100691675b57cdde77be87b51b1f346508b8968cce5090f5fc17ab9e8(
    value: typing.Optional[TableColumnIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475896fa9b0842d106ebfd21e3eb7a03a08dc086bf966a418e5d21c9ea9153ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0833c486e2df5f3fb0f7a9ea630dd3dac87a7b5f6480d131ce8fcc1d90fb3a5a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669dc44ad78306cd9efe55a949917760c51fa123f07e6556c22cfb3882688680(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4749eeea9dcfa86b53f1dbc45f30c99d5baf1c134b1a4219903845a048880ade(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2520e2646b9597c90afdbe6cbb536ae8c47e02eb2e8b86c108f27704d77da5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705fab543eb578ec9f1bd9ede33474c16d8b720345993b8e47e2a75b1340dd1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableColumn]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2255bceb5447e57792b892b67d4d1eb11f2b1c92266ffc12dd0650122d874d3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98cb7456a68739e97e01060c91440db400920e4fda8438f560a1b1b82f5b870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ce58cf2b9ea13ae92cf542c283382a16ed2d12f62c07961ccef723d3517d13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5324f1265946d8ab6dc5b94ef6efdfb7852ca5353cd543255b2cace7c9cb9666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fba95cf5a3dcdfcb1a7a1bca66b7cca42192da439f6959a40e63724ee3be386(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c63746afe108f5e89557dc361fb55c3e95e49b8abfd9af97339a5c5b594fba16(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1364327a787e159af7afceeff81ea5502e7ea08317605dfedccf299ca5376fc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21088387084d74b3c4dc1a29547e6d2ca16d62c927df6485129e4e8d22b92e94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TableColumn]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac05d8eaa3fd00717b2eed92d74c322e02128fde62a8f61fd8e80919c43ca42b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    column: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TableColumn, typing.Dict[builtins.str, typing.Any]]]],
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    change_tracking: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cluster_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    primary_key: typing.Optional[typing.Union[TablePrimaryKey, typing.Dict[builtins.str, typing.Any]]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TableTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b83d277a71158a0b7d1b68db84f581f7a9a3a26606538c9a94becf6a0b597b0(
    *,
    keys: typing.Sequence[builtins.str],
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0228d3408f16bb0f4ef51d5856dddf881a08105de828d986bf626eaa28b6ef0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a410e4f01f474c2cc443cc84932b8a280c8f2c8b3c07c9970a4dc069ce8c64b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c4b283a36728baa0a7fbe6e83e844d4dc3dcf20acc88987b12571a10f07aed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366ed374e5cd41004e15a7279c365f640aa48284c26cb02bcb101f96a530ad21(
    value: typing.Optional[TablePrimaryKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25936c5c9190c8854badeb92b6a010e3675185446908c41550a6d447cea808c0(
    *,
    name: builtins.str,
    value: builtins.str,
    database: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fc001c11ba664209f015677c4a91fca51f57e19baef5ccd91207d25943154e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee914f62dc5efc7e66fb5716d1eba8b2fc7cd4b5b978b10d65f2c11e5e1bd5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ad8d9cca6e75972209deadc0afb77f17804a7ac37bcee414ad55c8b56ea13e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4247d8cd62a36a7631c69b350fd273be411447fdb7ca8910e6fae88c09a2252d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35632c7b5f729a41f7dc34f57098f09f6e9d2f60eebce5e39fc90512e45bbfe5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75abb82e1c533943ab02f8491cc75725d443f2876a67b31ca58717862b32ea63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TableTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08a8311705a96a6cd5765d4709cb6b0bd2c176dca0900c50292b3886d38a48b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea6f31a65ff9a9551bfa6f3c7146fa0786269ed0f86cfe21d5aea9b4deee735(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a2c95536638ec2ba3de76e83889c8495d6fca26f15629dc38c221b466cad48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aacdf963c87f58a97f775dd89291ab05366d83d459ce7012b90ec5601990cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51454120cc71a02dce435b52966a4bb397f00bd8cdb8040a168e783153dbcfaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6925f0ff58242f27e3b8af233815c2a67713ab9c4b7e5eb5f257a47c51ccbc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TableTag]],
) -> None:
    """Type checking stubs"""
    pass
