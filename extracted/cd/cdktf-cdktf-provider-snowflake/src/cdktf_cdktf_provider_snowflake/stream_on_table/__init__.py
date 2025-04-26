r'''
# `snowflake_stream_on_table`

Refer to the Terraform Registry for docs: [`snowflake_stream_on_table`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table).
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


class StreamOnTable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTable",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table snowflake_stream_on_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        table: builtins.str,
        append_only: typing.Optional[builtins.str] = None,
        at: typing.Optional[typing.Union["StreamOnTableAt", typing.Dict[builtins.str, typing.Any]]] = None,
        before: typing.Optional[typing.Union["StreamOnTableBefore", typing.Dict[builtins.str, typing.Any]]] = None,
        comment: typing.Optional[builtins.str] = None,
        copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        show_initial_rows: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table snowflake_stream_on_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#database StreamOnTable#database}
        :param name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#name StreamOnTable#name}
        :param schema: The schema in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#schema StreamOnTable#schema}
        :param table: Specifies an identifier for the table the stream will monitor. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./table>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#table StreamOnTable#table}
        :param append_only: Specifies whether this is an append-only stream. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#append_only StreamOnTable#append_only}
        :param at: at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#at StreamOnTable#at}
        :param before: before block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#before StreamOnTable#before}
        :param comment: Specifies a comment for the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#comment StreamOnTable#comment}
        :param copy_grants: Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause. This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#copy_grants StreamOnTable#copy_grants}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#id StreamOnTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param show_initial_rows: Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#show_initial_rows StreamOnTable#show_initial_rows}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b887a82b845907e71e48a29a225a8f18c22253c3bfb44d5a6779a17af026830a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StreamOnTableConfig(
            database=database,
            name=name,
            schema=schema,
            table=table,
            append_only=append_only,
            at=at,
            before=before,
            comment=comment,
            copy_grants=copy_grants,
            id=id,
            show_initial_rows=show_initial_rows,
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
        '''Generates CDKTF code for importing a StreamOnTable resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StreamOnTable to import.
        :param import_from_id: The id of the existing StreamOnTable that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StreamOnTable to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199bd8ebc9200009761f4796250b249fb74a8f0e82b3db5c91bc6a3230ecd0c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAt")
    def put_at(
        self,
        *,
        offset: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
        stream: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#offset StreamOnTable#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#statement StreamOnTable#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#stream StreamOnTable#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#timestamp StreamOnTable#timestamp}
        '''
        value = StreamOnTableAt(
            offset=offset, statement=statement, stream=stream, timestamp=timestamp
        )

        return typing.cast(None, jsii.invoke(self, "putAt", [value]))

    @jsii.member(jsii_name="putBefore")
    def put_before(
        self,
        *,
        offset: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
        stream: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#offset StreamOnTable#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#statement StreamOnTable#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#stream StreamOnTable#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#timestamp StreamOnTable#timestamp}
        '''
        value = StreamOnTableBefore(
            offset=offset, statement=statement, stream=stream, timestamp=timestamp
        )

        return typing.cast(None, jsii.invoke(self, "putBefore", [value]))

    @jsii.member(jsii_name="resetAppendOnly")
    def reset_append_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppendOnly", []))

    @jsii.member(jsii_name="resetAt")
    def reset_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAt", []))

    @jsii.member(jsii_name="resetBefore")
    def reset_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBefore", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCopyGrants")
    def reset_copy_grants(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyGrants", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetShowInitialRows")
    def reset_show_initial_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShowInitialRows", []))

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
    @jsii.member(jsii_name="at")
    def at(self) -> "StreamOnTableAtOutputReference":
        return typing.cast("StreamOnTableAtOutputReference", jsii.get(self, "at"))

    @builtins.property
    @jsii.member(jsii_name="before")
    def before(self) -> "StreamOnTableBeforeOutputReference":
        return typing.cast("StreamOnTableBeforeOutputReference", jsii.get(self, "before"))

    @builtins.property
    @jsii.member(jsii_name="describeOutput")
    def describe_output(self) -> "StreamOnTableDescribeOutputList":
        return typing.cast("StreamOnTableDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "StreamOnTableShowOutputList":
        return typing.cast("StreamOnTableShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="stale")
    def stale(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "stale"))

    @builtins.property
    @jsii.member(jsii_name="streamType")
    def stream_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamType"))

    @builtins.property
    @jsii.member(jsii_name="appendOnlyInput")
    def append_only_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appendOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="atInput")
    def at_input(self) -> typing.Optional["StreamOnTableAt"]:
        return typing.cast(typing.Optional["StreamOnTableAt"], jsii.get(self, "atInput"))

    @builtins.property
    @jsii.member(jsii_name="beforeInput")
    def before_input(self) -> typing.Optional["StreamOnTableBefore"]:
        return typing.cast(typing.Optional["StreamOnTableBefore"], jsii.get(self, "beforeInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="copyGrantsInput")
    def copy_grants_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyGrantsInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="showInitialRowsInput")
    def show_initial_rows_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "showInitialRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="appendOnly")
    def append_only(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appendOnly"))

    @append_only.setter
    def append_only(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d5d69ed2157eb2a9c154234a4fc0043b7f4e335becbac55eb3ea9e251b346b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appendOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11dba37d256f55c04f4a7e1aebe5a9c1792b1881ecf3597294eb26957fcf1acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyGrants")
    def copy_grants(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyGrants"))

    @copy_grants.setter
    def copy_grants(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8f4a35dfd50dfbd6d8fd48f1f2f9d1dcd882e4e91f4903988c4ca44cab9f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyGrants", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9ffd62f28b339f51e9e453221a27133d34f7aac7f3f2372ab24e5ae56480a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ddbe36d0f9318d93f045fc8a8960b7168c9f26d992adb0e12f75919cc1a604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324967fc352f61e45b9602c99f2f40715029cd1ff8678cc2ccb67a9554a30f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87d16a219725080cec8c9cbe9405f05fcc3e93098454576b8a658b300d238cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="showInitialRows")
    def show_initial_rows(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "showInitialRows"))

    @show_initial_rows.setter
    def show_initial_rows(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48863f7796b05c7aa33cb8a4febf25de20b5bc90b613420a627459d03167f936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "showInitialRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012b6a431e33eea2f4bc58fafd8702a734ea8b6c51c02c152231b89f3d02f2dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableAt",
    jsii_struct_bases=[],
    name_mapping={
        "offset": "offset",
        "statement": "statement",
        "stream": "stream",
        "timestamp": "timestamp",
    },
)
class StreamOnTableAt:
    def __init__(
        self,
        *,
        offset: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
        stream: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#offset StreamOnTable#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#statement StreamOnTable#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#stream StreamOnTable#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#timestamp StreamOnTable#timestamp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33427d646def90a3aee965894ea4271d2a5fa641fe93a5a804b3ccdd92c4bd07)
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if offset is not None:
            self._values["offset"] = offset
        if statement is not None:
            self._values["statement"] = statement
        if stream is not None:
            self._values["stream"] = stream
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def offset(self) -> typing.Optional[builtins.str]:
        '''Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#offset StreamOnTable#offset}
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement(self) -> typing.Optional[builtins.str]:
        '''Specifies the query ID of a statement to use as the reference point for Time Travel.

        This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#statement StreamOnTable#statement}
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream(self) -> typing.Optional[builtins.str]:
        '''Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#stream StreamOnTable#stream}
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''Specifies an exact date and time to use for Time Travel.

        The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#timestamp StreamOnTable#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnTableAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnTableAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9ac8c690fe8c3eb4a6907864536ecb3205e43c98e77e288d7b80629ba932b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOffset")
    def reset_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOffset", []))

    @jsii.member(jsii_name="resetStatement")
    def reset_statement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatement", []))

    @jsii.member(jsii_name="resetStream")
    def reset_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStream", []))

    @jsii.member(jsii_name="resetTimestamp")
    def reset_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="offsetInput")
    def offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offsetInput"))

    @builtins.property
    @jsii.member(jsii_name="statementInput")
    def statement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementInput"))

    @builtins.property
    @jsii.member(jsii_name="streamInput")
    def stream_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInput")
    def timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampInput"))

    @builtins.property
    @jsii.member(jsii_name="offset")
    def offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offset"))

    @offset.setter
    def offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdcd9b343319bb530f82ab4de4bc69bb0446405e3556cf2b9db6e98158e61c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda2d6d8468e7462a461b4cd057c82bbeadf2e5f83e2c6f21c0a28f3bb8deb5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stream"))

    @stream.setter
    def stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320b9ee59bae0ca8cc01e8324b36e7591ddecc2bd633af69d6db80ab6e271720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stream", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @timestamp.setter
    def timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63bc08fdfa6fb8b51918572a8115004129b306de72d0f5fb415db1125a41b3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StreamOnTableAt]:
        return typing.cast(typing.Optional[StreamOnTableAt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StreamOnTableAt]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530ff7da479cfd1c278adb84d571c57cf8119996ad50a4de6cecbe2e396f9608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableBefore",
    jsii_struct_bases=[],
    name_mapping={
        "offset": "offset",
        "statement": "statement",
        "stream": "stream",
        "timestamp": "timestamp",
    },
)
class StreamOnTableBefore:
    def __init__(
        self,
        *,
        offset: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
        stream: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#offset StreamOnTable#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#statement StreamOnTable#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#stream StreamOnTable#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#timestamp StreamOnTable#timestamp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb669bbaeb0b358ab3ac1deb4d8a86f574a182271d705269fa5bee0b00c6f040)
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if offset is not None:
            self._values["offset"] = offset
        if statement is not None:
            self._values["statement"] = statement
        if stream is not None:
            self._values["stream"] = stream
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def offset(self) -> typing.Optional[builtins.str]:
        '''Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#offset StreamOnTable#offset}
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement(self) -> typing.Optional[builtins.str]:
        '''Specifies the query ID of a statement to use as the reference point for Time Travel.

        This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#statement StreamOnTable#statement}
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream(self) -> typing.Optional[builtins.str]:
        '''Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#stream StreamOnTable#stream}
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''Specifies an exact date and time to use for Time Travel.

        The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#timestamp StreamOnTable#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnTableBefore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnTableBeforeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableBeforeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ce95c8c9c30df1027ae772cce7ff8b43fde6865f6d770ebd88dacfe17ddf9e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOffset")
    def reset_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOffset", []))

    @jsii.member(jsii_name="resetStatement")
    def reset_statement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatement", []))

    @jsii.member(jsii_name="resetStream")
    def reset_stream(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStream", []))

    @jsii.member(jsii_name="resetTimestamp")
    def reset_timestamp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestamp", []))

    @builtins.property
    @jsii.member(jsii_name="offsetInput")
    def offset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "offsetInput"))

    @builtins.property
    @jsii.member(jsii_name="statementInput")
    def statement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementInput"))

    @builtins.property
    @jsii.member(jsii_name="streamInput")
    def stream_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInput")
    def timestamp_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampInput"))

    @builtins.property
    @jsii.member(jsii_name="offset")
    def offset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "offset"))

    @offset.setter
    def offset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45975bbec5d3f68755d8b823233ba9fd7a0f94d952fd9c485adbf7994d067c0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07df85daa799f5bc04b66968099fb8954a4cfa664e73811033ccb39c06279f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stream"))

    @stream.setter
    def stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3cd0d20c91b5bcc3c14a71ef9c7380e33b14f444f7723162923befd3cebaa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stream", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @timestamp.setter
    def timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0077ba22e209e9e78d59b57c308b6694603fd872538066a9cc9a6be4737204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StreamOnTableBefore]:
        return typing.cast(typing.Optional[StreamOnTableBefore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StreamOnTableBefore]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690fec6ce1b9313a72ebf2a021f7daac9a06c1adfb2aff290111889a8ca5f56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database": "database",
        "name": "name",
        "schema": "schema",
        "table": "table",
        "append_only": "appendOnly",
        "at": "at",
        "before": "before",
        "comment": "comment",
        "copy_grants": "copyGrants",
        "id": "id",
        "show_initial_rows": "showInitialRows",
    },
)
class StreamOnTableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        table: builtins.str,
        append_only: typing.Optional[builtins.str] = None,
        at: typing.Optional[typing.Union[StreamOnTableAt, typing.Dict[builtins.str, typing.Any]]] = None,
        before: typing.Optional[typing.Union[StreamOnTableBefore, typing.Dict[builtins.str, typing.Any]]] = None,
        comment: typing.Optional[builtins.str] = None,
        copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        show_initial_rows: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#database StreamOnTable#database}
        :param name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#name StreamOnTable#name}
        :param schema: The schema in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#schema StreamOnTable#schema}
        :param table: Specifies an identifier for the table the stream will monitor. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./table>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#table StreamOnTable#table}
        :param append_only: Specifies whether this is an append-only stream. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#append_only StreamOnTable#append_only}
        :param at: at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#at StreamOnTable#at}
        :param before: before block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#before StreamOnTable#before}
        :param comment: Specifies a comment for the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#comment StreamOnTable#comment}
        :param copy_grants: Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause. This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#copy_grants StreamOnTable#copy_grants}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#id StreamOnTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param show_initial_rows: Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#show_initial_rows StreamOnTable#show_initial_rows}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(at, dict):
            at = StreamOnTableAt(**at)
        if isinstance(before, dict):
            before = StreamOnTableBefore(**before)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78fec34ebc171479c886dc72ffbf82849979f33aca4a5de439a727bda08d272f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument append_only", value=append_only, expected_type=type_hints["append_only"])
            check_type(argname="argument at", value=at, expected_type=type_hints["at"])
            check_type(argname="argument before", value=before, expected_type=type_hints["before"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument copy_grants", value=copy_grants, expected_type=type_hints["copy_grants"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument show_initial_rows", value=show_initial_rows, expected_type=type_hints["show_initial_rows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "name": name,
            "schema": schema,
            "table": table,
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
        if append_only is not None:
            self._values["append_only"] = append_only
        if at is not None:
            self._values["at"] = at
        if before is not None:
            self._values["before"] = before
        if comment is not None:
            self._values["comment"] = comment
        if copy_grants is not None:
            self._values["copy_grants"] = copy_grants
        if id is not None:
            self._values["id"] = id
        if show_initial_rows is not None:
            self._values["show_initial_rows"] = show_initial_rows

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
    def database(self) -> builtins.str:
        '''The database in which to create the stream.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#database StreamOnTable#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the stream;

        must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#name StreamOnTable#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the stream.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#schema StreamOnTable#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table(self) -> builtins.str:
        '''Specifies an identifier for the table the stream will monitor.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./table>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#table StreamOnTable#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def append_only(self) -> typing.Optional[builtins.str]:
        '''Specifies whether this is an append-only stream.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#append_only StreamOnTable#append_only}
        '''
        result = self._values.get("append_only")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def at(self) -> typing.Optional[StreamOnTableAt]:
        '''at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#at StreamOnTable#at}
        '''
        result = self._values.get("at")
        return typing.cast(typing.Optional[StreamOnTableAt], result)

    @builtins.property
    def before(self) -> typing.Optional[StreamOnTableBefore]:
        '''before block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#before StreamOnTable#before}
        '''
        result = self._values.get("before")
        return typing.cast(typing.Optional[StreamOnTableBefore], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#comment StreamOnTable#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_grants(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause.

        This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#copy_grants StreamOnTable#copy_grants}
        '''
        result = self._values.get("copy_grants")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#id StreamOnTable#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def show_initial_rows(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_table#show_initial_rows StreamOnTable#show_initial_rows}
        '''
        result = self._values.get("show_initial_rows")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class StreamOnTableDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnTableDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnTableDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4741c9384e685d36256959dc075ef32fca7e9989e0920db04dc9df8a22c1f7e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "StreamOnTableDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672f86943391fd51567fff4efe5983e0a18936eab82e13c5433a0d087f5bba73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StreamOnTableDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fdd40b87d0205d4583f96a4a06c334493e6c17539d365f93dda69856cf535d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5104d8dfffe251da6b5adc838b270d49725aa9c0cc0744904cf005ff8e03b592)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32bc5b60ed598e8b3073b676f48b689fb3004ed8aeb321f127154bd2a3beef75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StreamOnTableDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e61d3806b9a42add8725053a22dd90bedba373ba4924985496e1f9dfd9de2bd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="baseTables")
    def base_tables(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "baseTables"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="invalidReason")
    def invalid_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invalidReason"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="ownerRoleType")
    def owner_role_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerRoleType"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @builtins.property
    @jsii.member(jsii_name="stale")
    def stale(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "stale"))

    @builtins.property
    @jsii.member(jsii_name="staleAfter")
    def stale_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "staleAfter"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StreamOnTableDescribeOutput]:
        return typing.cast(typing.Optional[StreamOnTableDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StreamOnTableDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609cd02ec708fed41646d870ce82edfd8e29c17edb9c2d4d0f6a272d2cdd5a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class StreamOnTableShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnTableShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnTableShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a350be70f5dcb740bbd5cf2a01ab93b6c86d3128702d2a5868c4ea62292de8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "StreamOnTableShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6d6d193cd47afe3ec9b54d5ca0c101e547ef60d7c24be3f55286ca3be35a1f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StreamOnTableShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ce7bd7da0f56af223b022602d6d962fc9ddf9f18f79e4b011cb60a7ef3bdbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29af97e80d79f49a0372bd7c9412eac49ac3a95b242dccc96ce0919627152c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fa91250cd4d50a1d2b5382e383b8b8afce282b5b69a5be927d419b6a96e30f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StreamOnTableShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnTable.StreamOnTableShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea6ca31dd3079c810761376d5ab4bf4b61401ff5bd43500e3c619d83627cf674)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="baseTables")
    def base_tables(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "baseTables"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="invalidReason")
    def invalid_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invalidReason"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="ownerRoleType")
    def owner_role_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerRoleType"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @builtins.property
    @jsii.member(jsii_name="stale")
    def stale(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "stale"))

    @builtins.property
    @jsii.member(jsii_name="staleAfter")
    def stale_after(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "staleAfter"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StreamOnTableShowOutput]:
        return typing.cast(typing.Optional[StreamOnTableShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StreamOnTableShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb22dc176a174102905d20d74808d7cac22666c1295b3d964688ce6e5b92f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StreamOnTable",
    "StreamOnTableAt",
    "StreamOnTableAtOutputReference",
    "StreamOnTableBefore",
    "StreamOnTableBeforeOutputReference",
    "StreamOnTableConfig",
    "StreamOnTableDescribeOutput",
    "StreamOnTableDescribeOutputList",
    "StreamOnTableDescribeOutputOutputReference",
    "StreamOnTableShowOutput",
    "StreamOnTableShowOutputList",
    "StreamOnTableShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__b887a82b845907e71e48a29a225a8f18c22253c3bfb44d5a6779a17af026830a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    table: builtins.str,
    append_only: typing.Optional[builtins.str] = None,
    at: typing.Optional[typing.Union[StreamOnTableAt, typing.Dict[builtins.str, typing.Any]]] = None,
    before: typing.Optional[typing.Union[StreamOnTableBefore, typing.Dict[builtins.str, typing.Any]]] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    show_initial_rows: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__199bd8ebc9200009761f4796250b249fb74a8f0e82b3db5c91bc6a3230ecd0c2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d5d69ed2157eb2a9c154234a4fc0043b7f4e335becbac55eb3ea9e251b346b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11dba37d256f55c04f4a7e1aebe5a9c1792b1881ecf3597294eb26957fcf1acb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8f4a35dfd50dfbd6d8fd48f1f2f9d1dcd882e4e91f4903988c4ca44cab9f8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9ffd62f28b339f51e9e453221a27133d34f7aac7f3f2372ab24e5ae56480a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ddbe36d0f9318d93f045fc8a8960b7168c9f26d992adb0e12f75919cc1a604(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324967fc352f61e45b9602c99f2f40715029cd1ff8678cc2ccb67a9554a30f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87d16a219725080cec8c9cbe9405f05fcc3e93098454576b8a658b300d238cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48863f7796b05c7aa33cb8a4febf25de20b5bc90b613420a627459d03167f936(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012b6a431e33eea2f4bc58fafd8702a734ea8b6c51c02c152231b89f3d02f2dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33427d646def90a3aee965894ea4271d2a5fa641fe93a5a804b3ccdd92c4bd07(
    *,
    offset: typing.Optional[builtins.str] = None,
    statement: typing.Optional[builtins.str] = None,
    stream: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9ac8c690fe8c3eb4a6907864536ecb3205e43c98e77e288d7b80629ba932b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcd9b343319bb530f82ab4de4bc69bb0446405e3556cf2b9db6e98158e61c24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda2d6d8468e7462a461b4cd057c82bbeadf2e5f83e2c6f21c0a28f3bb8deb5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320b9ee59bae0ca8cc01e8324b36e7591ddecc2bd633af69d6db80ab6e271720(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63bc08fdfa6fb8b51918572a8115004129b306de72d0f5fb415db1125a41b3df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530ff7da479cfd1c278adb84d571c57cf8119996ad50a4de6cecbe2e396f9608(
    value: typing.Optional[StreamOnTableAt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb669bbaeb0b358ab3ac1deb4d8a86f574a182271d705269fa5bee0b00c6f040(
    *,
    offset: typing.Optional[builtins.str] = None,
    statement: typing.Optional[builtins.str] = None,
    stream: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce95c8c9c30df1027ae772cce7ff8b43fde6865f6d770ebd88dacfe17ddf9e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45975bbec5d3f68755d8b823233ba9fd7a0f94d952fd9c485adbf7994d067c0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07df85daa799f5bc04b66968099fb8954a4cfa664e73811033ccb39c06279f12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3cd0d20c91b5bcc3c14a71ef9c7380e33b14f444f7723162923befd3cebaa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0077ba22e209e9e78d59b57c308b6694603fd872538066a9cc9a6be4737204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690fec6ce1b9313a72ebf2a021f7daac9a06c1adfb2aff290111889a8ca5f56f(
    value: typing.Optional[StreamOnTableBefore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fec34ebc171479c886dc72ffbf82849979f33aca4a5de439a727bda08d272f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    table: builtins.str,
    append_only: typing.Optional[builtins.str] = None,
    at: typing.Optional[typing.Union[StreamOnTableAt, typing.Dict[builtins.str, typing.Any]]] = None,
    before: typing.Optional[typing.Union[StreamOnTableBefore, typing.Dict[builtins.str, typing.Any]]] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    show_initial_rows: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4741c9384e685d36256959dc075ef32fca7e9989e0920db04dc9df8a22c1f7e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672f86943391fd51567fff4efe5983e0a18936eab82e13c5433a0d087f5bba73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fdd40b87d0205d4583f96a4a06c334493e6c17539d365f93dda69856cf535d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5104d8dfffe251da6b5adc838b270d49725aa9c0cc0744904cf005ff8e03b592(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32bc5b60ed598e8b3073b676f48b689fb3004ed8aeb321f127154bd2a3beef75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61d3806b9a42add8725053a22dd90bedba373ba4924985496e1f9dfd9de2bd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609cd02ec708fed41646d870ce82edfd8e29c17edb9c2d4d0f6a272d2cdd5a6e(
    value: typing.Optional[StreamOnTableDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a350be70f5dcb740bbd5cf2a01ab93b6c86d3128702d2a5868c4ea62292de8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6d6d193cd47afe3ec9b54d5ca0c101e547ef60d7c24be3f55286ca3be35a1f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ce7bd7da0f56af223b022602d6d962fc9ddf9f18f79e4b011cb60a7ef3bdbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29af97e80d79f49a0372bd7c9412eac49ac3a95b242dccc96ce0919627152c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa91250cd4d50a1d2b5382e383b8b8afce282b5b69a5be927d419b6a96e30f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6ca31dd3079c810761376d5ab4bf4b61401ff5bd43500e3c619d83627cf674(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb22dc176a174102905d20d74808d7cac22666c1295b3d964688ce6e5b92f19(
    value: typing.Optional[StreamOnTableShowOutput],
) -> None:
    """Type checking stubs"""
    pass
