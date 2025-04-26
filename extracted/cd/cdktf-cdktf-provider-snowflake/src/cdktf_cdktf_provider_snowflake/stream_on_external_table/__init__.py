r'''
# `snowflake_stream_on_external_table`

Refer to the Terraform Registry for docs: [`snowflake_stream_on_external_table`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table).
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


class StreamOnExternalTable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTable",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table snowflake_stream_on_external_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        external_table: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        at: typing.Optional[typing.Union["StreamOnExternalTableAt", typing.Dict[builtins.str, typing.Any]]] = None,
        before: typing.Optional[typing.Union["StreamOnExternalTableBefore", typing.Dict[builtins.str, typing.Any]]] = None,
        comment: typing.Optional[builtins.str] = None,
        copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        insert_only: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table snowflake_stream_on_external_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#database StreamOnExternalTable#database}
        :param external_table: Specifies an identifier for the external table the stream will monitor. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./external_table>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#external_table StreamOnExternalTable#external_table}
        :param name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#name StreamOnExternalTable#name}
        :param schema: The schema in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#schema StreamOnExternalTable#schema}
        :param at: at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#at StreamOnExternalTable#at}
        :param before: before block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#before StreamOnExternalTable#before}
        :param comment: Specifies a comment for the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#comment StreamOnExternalTable#comment}
        :param copy_grants: Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause. This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#copy_grants StreamOnExternalTable#copy_grants}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#id StreamOnExternalTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insert_only: Specifies whether this is an insert-only stream. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#insert_only StreamOnExternalTable#insert_only}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5acd36c3f8c027933e5a129c20b0c745d05beda023ff20360e279f489bb1200a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StreamOnExternalTableConfig(
            database=database,
            external_table=external_table,
            name=name,
            schema=schema,
            at=at,
            before=before,
            comment=comment,
            copy_grants=copy_grants,
            id=id,
            insert_only=insert_only,
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
        '''Generates CDKTF code for importing a StreamOnExternalTable resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StreamOnExternalTable to import.
        :param import_from_id: The id of the existing StreamOnExternalTable that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StreamOnExternalTable to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71894b958c4ccc3aab8811551a00cf81a17a526a3d6bece7b9f94723c7bda45a)
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
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#offset StreamOnExternalTable#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#statement StreamOnExternalTable#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#stream StreamOnExternalTable#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#timestamp StreamOnExternalTable#timestamp}
        '''
        value = StreamOnExternalTableAt(
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
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#offset StreamOnExternalTable#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#statement StreamOnExternalTable#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#stream StreamOnExternalTable#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#timestamp StreamOnExternalTable#timestamp}
        '''
        value = StreamOnExternalTableBefore(
            offset=offset, statement=statement, stream=stream, timestamp=timestamp
        )

        return typing.cast(None, jsii.invoke(self, "putBefore", [value]))

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

    @jsii.member(jsii_name="resetInsertOnly")
    def reset_insert_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsertOnly", []))

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
    def at(self) -> "StreamOnExternalTableAtOutputReference":
        return typing.cast("StreamOnExternalTableAtOutputReference", jsii.get(self, "at"))

    @builtins.property
    @jsii.member(jsii_name="before")
    def before(self) -> "StreamOnExternalTableBeforeOutputReference":
        return typing.cast("StreamOnExternalTableBeforeOutputReference", jsii.get(self, "before"))

    @builtins.property
    @jsii.member(jsii_name="describeOutput")
    def describe_output(self) -> "StreamOnExternalTableDescribeOutputList":
        return typing.cast("StreamOnExternalTableDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "StreamOnExternalTableShowOutputList":
        return typing.cast("StreamOnExternalTableShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="stale")
    def stale(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "stale"))

    @builtins.property
    @jsii.member(jsii_name="streamType")
    def stream_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamType"))

    @builtins.property
    @jsii.member(jsii_name="atInput")
    def at_input(self) -> typing.Optional["StreamOnExternalTableAt"]:
        return typing.cast(typing.Optional["StreamOnExternalTableAt"], jsii.get(self, "atInput"))

    @builtins.property
    @jsii.member(jsii_name="beforeInput")
    def before_input(self) -> typing.Optional["StreamOnExternalTableBefore"]:
        return typing.cast(typing.Optional["StreamOnExternalTableBefore"], jsii.get(self, "beforeInput"))

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
    @jsii.member(jsii_name="externalTableInput")
    def external_table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalTableInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="insertOnlyInput")
    def insert_only_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "insertOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c29e80e87f85c115eba47f20b7b6806ed023b8b4cfc5d5ccc41cd815da75edf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ef8c3be403daa4eeb1ccfea759f23066404fcad9c7273e8d53f767726d3afb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyGrants", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348f4ffb8c11b400c16c517c1dd50f75516f551375772a441bdccca2ee7bd114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalTable")
    def external_table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalTable"))

    @external_table.setter
    def external_table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea275df77d50d893321386428428203e3e8af3cb7c835bceba27a11de6a6ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c8ea4a5c76f840c138e3fe0e12c2f110bc20e731b2e2f198aa9f9ecbb879ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insertOnly")
    def insert_only(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "insertOnly"))

    @insert_only.setter
    def insert_only(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8992dbaf6a1f9da06b067fbee0b6d79f7d5bd9ed8f0e4c479564ffb3fce335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insertOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f2f00b02f2a9aa353e3a9434d3efea3c7326fdb4c2bfa74fcb0ce52bcd7293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe3135cd02a473a42d3282b720fa8d3b99518801d2209922b9d0f676b4d0749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableAt",
    jsii_struct_bases=[],
    name_mapping={
        "offset": "offset",
        "statement": "statement",
        "stream": "stream",
        "timestamp": "timestamp",
    },
)
class StreamOnExternalTableAt:
    def __init__(
        self,
        *,
        offset: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
        stream: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#offset StreamOnExternalTable#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#statement StreamOnExternalTable#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#stream StreamOnExternalTable#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#timestamp StreamOnExternalTable#timestamp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f412b883f587ceafbb06240d38c35055600e627ce25fba053aca51491766880)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#offset StreamOnExternalTable#offset}
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement(self) -> typing.Optional[builtins.str]:
        '''Specifies the query ID of a statement to use as the reference point for Time Travel.

        This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#statement StreamOnExternalTable#statement}
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream(self) -> typing.Optional[builtins.str]:
        '''Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#stream StreamOnExternalTable#stream}
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''Specifies an exact date and time to use for Time Travel.

        The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#timestamp StreamOnExternalTable#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnExternalTableAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnExternalTableAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70b98578a9a92b0731063241487ecfdbdaac3faca4fc3a158dbd0696674220d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__369bcc1f81c7a72d581f05f1a2697a3ccf02587c96caf17821b157af60822d31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa8ac48c49b4ae2c0c71411f11226b62f3a4813d97eb072db3dc252ffdc3ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stream"))

    @stream.setter
    def stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e591801335cb85f3ee4c00e7520c613dc01ca2c7ee442dbb4b74d2c249634f98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stream", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @timestamp.setter
    def timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73afb65b4c15c0eba0dc0a4eed15252b732c6d143bbd006dbf057deba4c8f997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StreamOnExternalTableAt]:
        return typing.cast(typing.Optional[StreamOnExternalTableAt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StreamOnExternalTableAt]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89454c056b2ab20f1d0d89014d25167eccf48f1e0241c8c86988007ec2f9dfdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableBefore",
    jsii_struct_bases=[],
    name_mapping={
        "offset": "offset",
        "statement": "statement",
        "stream": "stream",
        "timestamp": "timestamp",
    },
)
class StreamOnExternalTableBefore:
    def __init__(
        self,
        *,
        offset: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
        stream: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#offset StreamOnExternalTable#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#statement StreamOnExternalTable#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#stream StreamOnExternalTable#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#timestamp StreamOnExternalTable#timestamp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9b10a512c7ed3151bb0125ad1421a2e7e50da6418272fe76f2eb9c60b927eb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#offset StreamOnExternalTable#offset}
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement(self) -> typing.Optional[builtins.str]:
        '''Specifies the query ID of a statement to use as the reference point for Time Travel.

        This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#statement StreamOnExternalTable#statement}
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream(self) -> typing.Optional[builtins.str]:
        '''Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#stream StreamOnExternalTable#stream}
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''Specifies an exact date and time to use for Time Travel.

        The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#timestamp StreamOnExternalTable#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnExternalTableBefore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnExternalTableBeforeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableBeforeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd1406506d9c2a3f40bc9531a7998eb438273da3c8e43d8e0eb6d971a1d893f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06459f2fe6d4b9e4378f63e697c001b3f1baddca5c949bf3ca9e9ca9111ed4d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd1f5d53846ce976599251bd05a74bf7ddfd031a6982aadcbccad457c79e57b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stream"))

    @stream.setter
    def stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1de75bf1e7de2e2476f184b316b7fa4067c1486de956c2030581973ec3cf599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stream", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @timestamp.setter
    def timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255a67846dad6773b4a03c16ef9240d201eda732c874491ffa57523556e93e80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StreamOnExternalTableBefore]:
        return typing.cast(typing.Optional[StreamOnExternalTableBefore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StreamOnExternalTableBefore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5018468861e2fb36d93bcf877ec5720adc84de879746ae6673685682e3c4dc01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableConfig",
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
        "external_table": "externalTable",
        "name": "name",
        "schema": "schema",
        "at": "at",
        "before": "before",
        "comment": "comment",
        "copy_grants": "copyGrants",
        "id": "id",
        "insert_only": "insertOnly",
    },
)
class StreamOnExternalTableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        external_table: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        at: typing.Optional[typing.Union[StreamOnExternalTableAt, typing.Dict[builtins.str, typing.Any]]] = None,
        before: typing.Optional[typing.Union[StreamOnExternalTableBefore, typing.Dict[builtins.str, typing.Any]]] = None,
        comment: typing.Optional[builtins.str] = None,
        copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        insert_only: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#database StreamOnExternalTable#database}
        :param external_table: Specifies an identifier for the external table the stream will monitor. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./external_table>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#external_table StreamOnExternalTable#external_table}
        :param name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#name StreamOnExternalTable#name}
        :param schema: The schema in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#schema StreamOnExternalTable#schema}
        :param at: at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#at StreamOnExternalTable#at}
        :param before: before block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#before StreamOnExternalTable#before}
        :param comment: Specifies a comment for the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#comment StreamOnExternalTable#comment}
        :param copy_grants: Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause. This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#copy_grants StreamOnExternalTable#copy_grants}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#id StreamOnExternalTable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param insert_only: Specifies whether this is an insert-only stream. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#insert_only StreamOnExternalTable#insert_only}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(at, dict):
            at = StreamOnExternalTableAt(**at)
        if isinstance(before, dict):
            before = StreamOnExternalTableBefore(**before)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6562d65134a50011c3f3c00a065736c78da28114ef856681cbd8639398dea70)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument external_table", value=external_table, expected_type=type_hints["external_table"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument at", value=at, expected_type=type_hints["at"])
            check_type(argname="argument before", value=before, expected_type=type_hints["before"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument copy_grants", value=copy_grants, expected_type=type_hints["copy_grants"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument insert_only", value=insert_only, expected_type=type_hints["insert_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "external_table": external_table,
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
        if insert_only is not None:
            self._values["insert_only"] = insert_only

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#database StreamOnExternalTable#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_table(self) -> builtins.str:
        '''Specifies an identifier for the external table the stream will monitor.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./external_table>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#external_table StreamOnExternalTable#external_table}
        '''
        result = self._values.get("external_table")
        assert result is not None, "Required property 'external_table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the stream;

        must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#name StreamOnExternalTable#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the stream.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#schema StreamOnExternalTable#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def at(self) -> typing.Optional[StreamOnExternalTableAt]:
        '''at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#at StreamOnExternalTable#at}
        '''
        result = self._values.get("at")
        return typing.cast(typing.Optional[StreamOnExternalTableAt], result)

    @builtins.property
    def before(self) -> typing.Optional[StreamOnExternalTableBefore]:
        '''before block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#before StreamOnExternalTable#before}
        '''
        result = self._values.get("before")
        return typing.cast(typing.Optional[StreamOnExternalTableBefore], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#comment StreamOnExternalTable#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_grants(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause.

        This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#copy_grants StreamOnExternalTable#copy_grants}
        '''
        result = self._values.get("copy_grants")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#id StreamOnExternalTable#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insert_only(self) -> typing.Optional[builtins.str]:
        '''Specifies whether this is an insert-only stream.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_external_table#insert_only StreamOnExternalTable#insert_only}
        '''
        result = self._values.get("insert_only")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnExternalTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class StreamOnExternalTableDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnExternalTableDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnExternalTableDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f4e6712f82b339a92cec20625ad7b509a0cf65e6160c168ee38ac515205668)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StreamOnExternalTableDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f017293004329aaf77b87d5033b6ac899854216837680d274e8c5377765cad01)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StreamOnExternalTableDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7261b0ecfc3db4bdf373ee35db394405867acfe4c0f67157d33fc3cbbe6a827c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e5de3a768bc573c803f87dd76d08a5470b19ae7c6adddd25b93a3e09798fc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__463b71b914d5234f7e03cb2b1a041f016159db4246df9a4e5bb8ede47d279565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StreamOnExternalTableDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1db2d6632dc0df8bb7dd9d68fdbe8c6baf6e6f1447a0935783f3e3d93821467)
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
    def internal_value(self) -> typing.Optional[StreamOnExternalTableDescribeOutput]:
        return typing.cast(typing.Optional[StreamOnExternalTableDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StreamOnExternalTableDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba5952ae672b99cebb30b627193cd03cf665963d50867212838610f6575660d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class StreamOnExternalTableShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnExternalTableShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnExternalTableShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c8960da0eaaef8386b710a0cec90c42af43c5a015ffd5a32c7f5839394806c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StreamOnExternalTableShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cadb80892c7c56bc26b333fa39c7aae3cee1d407ff698ddb15abb284ac432b25)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StreamOnExternalTableShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b2dc8946c68045b4715cdafcf6010941ff1c4a87d62bbf7bfecd7e48139103)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97bd3d5cdd78e2bff0f3ecd75307bf1cbe58ab7d2c4287c08331908cb8afbfe5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__164fae3601c882175e02fdac07340f4b1c3e99f1ab02ba2af414d6100a13c9d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StreamOnExternalTableShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnExternalTable.StreamOnExternalTableShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32a32eb50f2be0668c1120403498d6e1279ef3fd9d4934f2effb11c0245f9abf)
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
    def internal_value(self) -> typing.Optional[StreamOnExternalTableShowOutput]:
        return typing.cast(typing.Optional[StreamOnExternalTableShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StreamOnExternalTableShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe166dfdc46a456708220fc4918f20cafe82a88c266a4844592814b4a9df8d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StreamOnExternalTable",
    "StreamOnExternalTableAt",
    "StreamOnExternalTableAtOutputReference",
    "StreamOnExternalTableBefore",
    "StreamOnExternalTableBeforeOutputReference",
    "StreamOnExternalTableConfig",
    "StreamOnExternalTableDescribeOutput",
    "StreamOnExternalTableDescribeOutputList",
    "StreamOnExternalTableDescribeOutputOutputReference",
    "StreamOnExternalTableShowOutput",
    "StreamOnExternalTableShowOutputList",
    "StreamOnExternalTableShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__5acd36c3f8c027933e5a129c20b0c745d05beda023ff20360e279f489bb1200a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    external_table: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    at: typing.Optional[typing.Union[StreamOnExternalTableAt, typing.Dict[builtins.str, typing.Any]]] = None,
    before: typing.Optional[typing.Union[StreamOnExternalTableBefore, typing.Dict[builtins.str, typing.Any]]] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    insert_only: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__71894b958c4ccc3aab8811551a00cf81a17a526a3d6bece7b9f94723c7bda45a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c29e80e87f85c115eba47f20b7b6806ed023b8b4cfc5d5ccc41cd815da75edf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef8c3be403daa4eeb1ccfea759f23066404fcad9c7273e8d53f767726d3afb6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348f4ffb8c11b400c16c517c1dd50f75516f551375772a441bdccca2ee7bd114(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea275df77d50d893321386428428203e3e8af3cb7c835bceba27a11de6a6ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c8ea4a5c76f840c138e3fe0e12c2f110bc20e731b2e2f198aa9f9ecbb879ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8992dbaf6a1f9da06b067fbee0b6d79f7d5bd9ed8f0e4c479564ffb3fce335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f2f00b02f2a9aa353e3a9434d3efea3c7326fdb4c2bfa74fcb0ce52bcd7293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe3135cd02a473a42d3282b720fa8d3b99518801d2209922b9d0f676b4d0749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f412b883f587ceafbb06240d38c35055600e627ce25fba053aca51491766880(
    *,
    offset: typing.Optional[builtins.str] = None,
    statement: typing.Optional[builtins.str] = None,
    stream: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b98578a9a92b0731063241487ecfdbdaac3faca4fc3a158dbd0696674220d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369bcc1f81c7a72d581f05f1a2697a3ccf02587c96caf17821b157af60822d31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa8ac48c49b4ae2c0c71411f11226b62f3a4813d97eb072db3dc252ffdc3ff0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e591801335cb85f3ee4c00e7520c613dc01ca2c7ee442dbb4b74d2c249634f98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73afb65b4c15c0eba0dc0a4eed15252b732c6d143bbd006dbf057deba4c8f997(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89454c056b2ab20f1d0d89014d25167eccf48f1e0241c8c86988007ec2f9dfdc(
    value: typing.Optional[StreamOnExternalTableAt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9b10a512c7ed3151bb0125ad1421a2e7e50da6418272fe76f2eb9c60b927eb(
    *,
    offset: typing.Optional[builtins.str] = None,
    statement: typing.Optional[builtins.str] = None,
    stream: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1406506d9c2a3f40bc9531a7998eb438273da3c8e43d8e0eb6d971a1d893f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06459f2fe6d4b9e4378f63e697c001b3f1baddca5c949bf3ca9e9ca9111ed4d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd1f5d53846ce976599251bd05a74bf7ddfd031a6982aadcbccad457c79e57b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1de75bf1e7de2e2476f184b316b7fa4067c1486de956c2030581973ec3cf599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255a67846dad6773b4a03c16ef9240d201eda732c874491ffa57523556e93e80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5018468861e2fb36d93bcf877ec5720adc84de879746ae6673685682e3c4dc01(
    value: typing.Optional[StreamOnExternalTableBefore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6562d65134a50011c3f3c00a065736c78da28114ef856681cbd8639398dea70(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    external_table: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    at: typing.Optional[typing.Union[StreamOnExternalTableAt, typing.Dict[builtins.str, typing.Any]]] = None,
    before: typing.Optional[typing.Union[StreamOnExternalTableBefore, typing.Dict[builtins.str, typing.Any]]] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    insert_only: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f4e6712f82b339a92cec20625ad7b509a0cf65e6160c168ee38ac515205668(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f017293004329aaf77b87d5033b6ac899854216837680d274e8c5377765cad01(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7261b0ecfc3db4bdf373ee35db394405867acfe4c0f67157d33fc3cbbe6a827c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e5de3a768bc573c803f87dd76d08a5470b19ae7c6adddd25b93a3e09798fc0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463b71b914d5234f7e03cb2b1a041f016159db4246df9a4e5bb8ede47d279565(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1db2d6632dc0df8bb7dd9d68fdbe8c6baf6e6f1447a0935783f3e3d93821467(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba5952ae672b99cebb30b627193cd03cf665963d50867212838610f6575660d(
    value: typing.Optional[StreamOnExternalTableDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8960da0eaaef8386b710a0cec90c42af43c5a015ffd5a32c7f5839394806c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadb80892c7c56bc26b333fa39c7aae3cee1d407ff698ddb15abb284ac432b25(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b2dc8946c68045b4715cdafcf6010941ff1c4a87d62bbf7bfecd7e48139103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bd3d5cdd78e2bff0f3ecd75307bf1cbe58ab7d2c4287c08331908cb8afbfe5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164fae3601c882175e02fdac07340f4b1c3e99f1ab02ba2af414d6100a13c9d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a32eb50f2be0668c1120403498d6e1279ef3fd9d4934f2effb11c0245f9abf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe166dfdc46a456708220fc4918f20cafe82a88c266a4844592814b4a9df8d3(
    value: typing.Optional[StreamOnExternalTableShowOutput],
) -> None:
    """Type checking stubs"""
    pass
