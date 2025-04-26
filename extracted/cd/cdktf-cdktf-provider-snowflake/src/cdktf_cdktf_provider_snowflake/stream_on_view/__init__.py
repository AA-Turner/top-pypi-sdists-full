r'''
# `snowflake_stream_on_view`

Refer to the Terraform Registry for docs: [`snowflake_stream_on_view`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view).
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


class StreamOnView(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnView",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view snowflake_stream_on_view}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        view: builtins.str,
        append_only: typing.Optional[builtins.str] = None,
        at: typing.Optional[typing.Union["StreamOnViewAt", typing.Dict[builtins.str, typing.Any]]] = None,
        before: typing.Optional[typing.Union["StreamOnViewBefore", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view snowflake_stream_on_view} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#database StreamOnView#database}
        :param name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#name StreamOnView#name}
        :param schema: The schema in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#schema StreamOnView#schema}
        :param view: Specifies an identifier for the view the stream will monitor. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./view>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#view StreamOnView#view}
        :param append_only: Specifies whether this is an append-only stream. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#append_only StreamOnView#append_only}
        :param at: at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#at StreamOnView#at}
        :param before: before block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#before StreamOnView#before}
        :param comment: Specifies a comment for the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#comment StreamOnView#comment}
        :param copy_grants: Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause. This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#copy_grants StreamOnView#copy_grants}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#id StreamOnView#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param show_initial_rows: Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#show_initial_rows StreamOnView#show_initial_rows}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4946a8ef5acc3da3de246bf097fa3d866487b03b8cdfca9e9b867d68a790250a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StreamOnViewConfig(
            database=database,
            name=name,
            schema=schema,
            view=view,
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
        '''Generates CDKTF code for importing a StreamOnView resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StreamOnView to import.
        :param import_from_id: The id of the existing StreamOnView that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StreamOnView to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__726864913359db7600b1ae3a6804f3d60b0fb026730b41c7fc5cb938378d5467)
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
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#offset StreamOnView#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#statement StreamOnView#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#stream StreamOnView#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#timestamp StreamOnView#timestamp}
        '''
        value = StreamOnViewAt(
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
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#offset StreamOnView#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#statement StreamOnView#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#stream StreamOnView#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#timestamp StreamOnView#timestamp}
        '''
        value = StreamOnViewBefore(
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
    def at(self) -> "StreamOnViewAtOutputReference":
        return typing.cast("StreamOnViewAtOutputReference", jsii.get(self, "at"))

    @builtins.property
    @jsii.member(jsii_name="before")
    def before(self) -> "StreamOnViewBeforeOutputReference":
        return typing.cast("StreamOnViewBeforeOutputReference", jsii.get(self, "before"))

    @builtins.property
    @jsii.member(jsii_name="describeOutput")
    def describe_output(self) -> "StreamOnViewDescribeOutputList":
        return typing.cast("StreamOnViewDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "StreamOnViewShowOutputList":
        return typing.cast("StreamOnViewShowOutputList", jsii.get(self, "showOutput"))

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
    def at_input(self) -> typing.Optional["StreamOnViewAt"]:
        return typing.cast(typing.Optional["StreamOnViewAt"], jsii.get(self, "atInput"))

    @builtins.property
    @jsii.member(jsii_name="beforeInput")
    def before_input(self) -> typing.Optional["StreamOnViewBefore"]:
        return typing.cast(typing.Optional["StreamOnViewBefore"], jsii.get(self, "beforeInput"))

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
    @jsii.member(jsii_name="viewInput")
    def view_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewInput"))

    @builtins.property
    @jsii.member(jsii_name="appendOnly")
    def append_only(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appendOnly"))

    @append_only.setter
    def append_only(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b640836ad07f9d92e7bd6330685779524227f9cb328d44975a934cd7962595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appendOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a77e1f0135b54698ef7d6a170586b06e41e727a0921ac1b287633d803f4d30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__795029736af16eef84c6f9cd9a7c7af5078c9545a7f153306a42b8bc7ac1c6c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyGrants", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a24e0919a4f53246f6b5b9615d98dee8445e1c732e313243756d0e05a100caa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1344a3f26c578fa6a2aab4f59014bb969a6955bfbe3c59314c938c322d661c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e66183298dd54260ce8527c48c4d12f5eec916dcf4f63c922b7b940800922f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b024dd7c64de0314443b3cae343354c947a87e6de1f139bad2743020202a80fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="showInitialRows")
    def show_initial_rows(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "showInitialRows"))

    @show_initial_rows.setter
    def show_initial_rows(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e8c0b7176065da42f152072ce310d6e5c8cd7707e2dd4b5b4a4602df772132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "showInitialRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="view")
    def view(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "view"))

    @view.setter
    def view(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f97b219d731e1d9d889c57c7d696093607f4ab88341cdf1f22515e5321ef889c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "view", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewAt",
    jsii_struct_bases=[],
    name_mapping={
        "offset": "offset",
        "statement": "statement",
        "stream": "stream",
        "timestamp": "timestamp",
    },
)
class StreamOnViewAt:
    def __init__(
        self,
        *,
        offset: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
        stream: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#offset StreamOnView#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#statement StreamOnView#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#stream StreamOnView#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#timestamp StreamOnView#timestamp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbcb7d0ebd711f6e0a2b3b541172bdfe9656b3d7a783cadac202b0e89c7d931)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#offset StreamOnView#offset}
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement(self) -> typing.Optional[builtins.str]:
        '''Specifies the query ID of a statement to use as the reference point for Time Travel.

        This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#statement StreamOnView#statement}
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream(self) -> typing.Optional[builtins.str]:
        '''Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#stream StreamOnView#stream}
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''Specifies an exact date and time to use for Time Travel.

        The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#timestamp StreamOnView#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnViewAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnViewAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9e0e1168b3b2d0a931e0dd7a8b62df52c7bcdd78eef7dd5d623ebbc80bea391)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bab6b67d264501dcc469d668e8d53de60e26efae914f2fc1125baa4c78fa862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ea969585a9e1df4453f435b6537530169aaf1bfe7a8a8bb8ccb273ed29adfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stream"))

    @stream.setter
    def stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e36b0db817fa4fe7f73a1b2781f578d68f5b567f96f3e476681fed8ea54ae43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stream", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @timestamp.setter
    def timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb47ee37417f7a8674ae6d90469b9fa92e834a205bbd344a66762bad5462190)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StreamOnViewAt]:
        return typing.cast(typing.Optional[StreamOnViewAt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StreamOnViewAt]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae2bd1603431cef42f7a42e1bd24204b041ff6515058a10d284276b98b4e019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewBefore",
    jsii_struct_bases=[],
    name_mapping={
        "offset": "offset",
        "statement": "statement",
        "stream": "stream",
        "timestamp": "timestamp",
    },
)
class StreamOnViewBefore:
    def __init__(
        self,
        *,
        offset: typing.Optional[builtins.str] = None,
        statement: typing.Optional[builtins.str] = None,
        stream: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param offset: Specifies the difference in seconds from the current time to use for Time Travel, in the form -N where N can be an integer or arithmetic expression (e.g. -120 is 120 seconds, -30*60 is 1800 seconds or 30 minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#offset StreamOnView#offset}
        :param statement: Specifies the query ID of a statement to use as the reference point for Time Travel. This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#statement StreamOnView#statement}
        :param stream: Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#stream StreamOnView#stream}
        :param timestamp: Specifies an exact date and time to use for Time Travel. The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#timestamp StreamOnView#timestamp}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a320ee1044eae289e15498a48ddf93877e1a0d2a0a366c87467e5292504b801b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#offset StreamOnView#offset}
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement(self) -> typing.Optional[builtins.str]:
        '''Specifies the query ID of a statement to use as the reference point for Time Travel.

        This parameter supports any statement of one of the following types: DML (e.g. INSERT, UPDATE, DELETE), TCL (BEGIN, COMMIT transaction), SELECT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#statement StreamOnView#statement}
        '''
        result = self._values.get("statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream(self) -> typing.Optional[builtins.str]:
        '''Specifies the identifier (i.e. name) for an existing stream on the queried table or view. The current offset in the stream is used as the AT point in time for returning change data for the source object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#stream StreamOnView#stream}
        '''
        result = self._values.get("stream")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''Specifies an exact date and time to use for Time Travel.

        The value must be explicitly cast to a TIMESTAMP, TIMESTAMP_LTZ, TIMESTAMP_NTZ, or TIMESTAMP_TZ data type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#timestamp StreamOnView#timestamp}
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnViewBefore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnViewBeforeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewBeforeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83005c0067c96f4f87f6a5417aa73af21fb7d0a958d13fb98616d9ff4da5fa8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dae3f2431b580a77ff4eb626fa5d0f2d5a0709c90ce8ce39b88f28d37066d67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statement")
    def statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statement"))

    @statement.setter
    def statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f97cf490a3bf521ac7111e216306d80aacef7517af3c409360be2e0c0a4f9068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stream")
    def stream(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stream"))

    @stream.setter
    def stream(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6a78d1a44d55fb9accc7e1b6c2cc8ba5f9e443870f65ca04ee52c81107a87f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stream", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @timestamp.setter
    def timestamp(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fec2f9024aafaaced5af9ff8cc9552079ffa8c1806d834770c5bd639073706a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestamp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StreamOnViewBefore]:
        return typing.cast(typing.Optional[StreamOnViewBefore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StreamOnViewBefore]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e584244dfe0f7e3dc718c7aeaa38671cdf0c974fb3068358d2038c46bf774e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewConfig",
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
        "view": "view",
        "append_only": "appendOnly",
        "at": "at",
        "before": "before",
        "comment": "comment",
        "copy_grants": "copyGrants",
        "id": "id",
        "show_initial_rows": "showInitialRows",
    },
)
class StreamOnViewConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        view: builtins.str,
        append_only: typing.Optional[builtins.str] = None,
        at: typing.Optional[typing.Union[StreamOnViewAt, typing.Dict[builtins.str, typing.Any]]] = None,
        before: typing.Optional[typing.Union[StreamOnViewBefore, typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param database: The database in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#database StreamOnView#database}
        :param name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#name StreamOnView#name}
        :param schema: The schema in which to create the stream. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#schema StreamOnView#schema}
        :param view: Specifies an identifier for the view the stream will monitor. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./view>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#view StreamOnView#view}
        :param append_only: Specifies whether this is an append-only stream. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#append_only StreamOnView#append_only}
        :param at: at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#at StreamOnView#at}
        :param before: before block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#before StreamOnView#before}
        :param comment: Specifies a comment for the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#comment StreamOnView#comment}
        :param copy_grants: Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause. This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#copy_grants StreamOnView#copy_grants}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#id StreamOnView#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param show_initial_rows: Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#show_initial_rows StreamOnView#show_initial_rows}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(at, dict):
            at = StreamOnViewAt(**at)
        if isinstance(before, dict):
            before = StreamOnViewBefore(**before)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e989709030fba0b638e0b9a9ff32020e6320e4add3e8fb3485cee435eecb6d34)
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
            check_type(argname="argument view", value=view, expected_type=type_hints["view"])
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
            "view": view,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#database StreamOnView#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the stream;

        must be unique for the database and schema in which the stream is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#name StreamOnView#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the stream.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#schema StreamOnView#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def view(self) -> builtins.str:
        '''Specifies an identifier for the view the stream will monitor.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./view>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#view StreamOnView#view}
        '''
        result = self._values.get("view")
        assert result is not None, "Required property 'view' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def append_only(self) -> typing.Optional[builtins.str]:
        '''Specifies whether this is an append-only stream.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#append_only StreamOnView#append_only}
        '''
        result = self._values.get("append_only")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def at(self) -> typing.Optional[StreamOnViewAt]:
        '''at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#at StreamOnView#at}
        '''
        result = self._values.get("at")
        return typing.cast(typing.Optional[StreamOnViewAt], result)

    @builtins.property
    def before(self) -> typing.Optional[StreamOnViewBefore]:
        '''before block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#before StreamOnView#before}
        '''
        result = self._values.get("before")
        return typing.cast(typing.Optional[StreamOnViewBefore], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#comment StreamOnView#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def copy_grants(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Retains the access permissions from the original stream when a stream is recreated using the OR REPLACE clause.

        This is used when the provider detects changes for fields that can not be changed by ALTER. This value will not have any effect during creating a new object with Terraform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#copy_grants StreamOnView#copy_grants}
        '''
        result = self._values.get("copy_grants")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#id StreamOnView#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def show_initial_rows(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/stream_on_view#show_initial_rows StreamOnView#show_initial_rows}
        '''
        result = self._values.get("show_initial_rows")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnViewConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class StreamOnViewDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnViewDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnViewDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adffa25d8003b51a5b932ef3726e7dc1596392a845b778b9de6a2d6805dfb41a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "StreamOnViewDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1f8ff564232757514148d7114648d1883b86ae43ea59871294e34df0599546)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StreamOnViewDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92817e19f30138d0c0c6779ae01a3e72cc0e4410c7e632a4f58eacbe8279decd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce7f6f2072ac5f6805de1f53a9bdf2f4ee32761c5b1abd2d57c7d1f2db6f1b64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f264cdedd8e4598dd999cf72d2d40f460e4cdddfc26f291e044ba2cd38d118f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StreamOnViewDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6acd3a16f86772cea20870b1e0d90185b675e6130bd0111fec156edee27a4da9)
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
    def internal_value(self) -> typing.Optional[StreamOnViewDescribeOutput]:
        return typing.cast(typing.Optional[StreamOnViewDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StreamOnViewDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569e566770d35013e8c67a752772688389280734ca75616b5916d6c46f70b5bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class StreamOnViewShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamOnViewShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StreamOnViewShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8f730d26b6ae5434efb3cf12218cb98271d5fb24f88ea8a817303a47b06e18b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "StreamOnViewShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00146ed5fe8230a4af6b97c1c015143179ad122783da7e4589cc0177c6ce80d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StreamOnViewShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82ef0f94c0b3da291082012bf7ed03cf01fc540c0639c3e5497cdd8ce9bb09db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34786a204ba7a1300ed0f07e5361fda6d38888c49f4da027058f2f9d9c86927d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d733906004e7df3db6791d6235c46492b8c374c146713458914638d13dbb05ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class StreamOnViewShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.streamOnView.StreamOnViewShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__817f6140097567ee07fdf135b61285bb805d9a0de0a502cd43afb7da75336b57)
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
    def internal_value(self) -> typing.Optional[StreamOnViewShowOutput]:
        return typing.cast(typing.Optional[StreamOnViewShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StreamOnViewShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f2a8b91777a49d26b6167945d406d87f7fe73e5e62229b3c2757e998d0905a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StreamOnView",
    "StreamOnViewAt",
    "StreamOnViewAtOutputReference",
    "StreamOnViewBefore",
    "StreamOnViewBeforeOutputReference",
    "StreamOnViewConfig",
    "StreamOnViewDescribeOutput",
    "StreamOnViewDescribeOutputList",
    "StreamOnViewDescribeOutputOutputReference",
    "StreamOnViewShowOutput",
    "StreamOnViewShowOutputList",
    "StreamOnViewShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__4946a8ef5acc3da3de246bf097fa3d866487b03b8cdfca9e9b867d68a790250a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    view: builtins.str,
    append_only: typing.Optional[builtins.str] = None,
    at: typing.Optional[typing.Union[StreamOnViewAt, typing.Dict[builtins.str, typing.Any]]] = None,
    before: typing.Optional[typing.Union[StreamOnViewBefore, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__726864913359db7600b1ae3a6804f3d60b0fb026730b41c7fc5cb938378d5467(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b640836ad07f9d92e7bd6330685779524227f9cb328d44975a934cd7962595(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a77e1f0135b54698ef7d6a170586b06e41e727a0921ac1b287633d803f4d30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795029736af16eef84c6f9cd9a7c7af5078c9545a7f153306a42b8bc7ac1c6c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a24e0919a4f53246f6b5b9615d98dee8445e1c732e313243756d0e05a100caa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1344a3f26c578fa6a2aab4f59014bb969a6955bfbe3c59314c938c322d661c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e66183298dd54260ce8527c48c4d12f5eec916dcf4f63c922b7b940800922f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b024dd7c64de0314443b3cae343354c947a87e6de1f139bad2743020202a80fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e8c0b7176065da42f152072ce310d6e5c8cd7707e2dd4b5b4a4602df772132(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97b219d731e1d9d889c57c7d696093607f4ab88341cdf1f22515e5321ef889c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbcb7d0ebd711f6e0a2b3b541172bdfe9656b3d7a783cadac202b0e89c7d931(
    *,
    offset: typing.Optional[builtins.str] = None,
    statement: typing.Optional[builtins.str] = None,
    stream: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e0e1168b3b2d0a931e0dd7a8b62df52c7bcdd78eef7dd5d623ebbc80bea391(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bab6b67d264501dcc469d668e8d53de60e26efae914f2fc1125baa4c78fa862(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ea969585a9e1df4453f435b6537530169aaf1bfe7a8a8bb8ccb273ed29adfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e36b0db817fa4fe7f73a1b2781f578d68f5b567f96f3e476681fed8ea54ae43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb47ee37417f7a8674ae6d90469b9fa92e834a205bbd344a66762bad5462190(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae2bd1603431cef42f7a42e1bd24204b041ff6515058a10d284276b98b4e019(
    value: typing.Optional[StreamOnViewAt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a320ee1044eae289e15498a48ddf93877e1a0d2a0a366c87467e5292504b801b(
    *,
    offset: typing.Optional[builtins.str] = None,
    statement: typing.Optional[builtins.str] = None,
    stream: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83005c0067c96f4f87f6a5417aa73af21fb7d0a958d13fb98616d9ff4da5fa8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae3f2431b580a77ff4eb626fa5d0f2d5a0709c90ce8ce39b88f28d37066d67f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97cf490a3bf521ac7111e216306d80aacef7517af3c409360be2e0c0a4f9068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6a78d1a44d55fb9accc7e1b6c2cc8ba5f9e443870f65ca04ee52c81107a87f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fec2f9024aafaaced5af9ff8cc9552079ffa8c1806d834770c5bd639073706a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e584244dfe0f7e3dc718c7aeaa38671cdf0c974fb3068358d2038c46bf774e3(
    value: typing.Optional[StreamOnViewBefore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e989709030fba0b638e0b9a9ff32020e6320e4add3e8fb3485cee435eecb6d34(
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
    view: builtins.str,
    append_only: typing.Optional[builtins.str] = None,
    at: typing.Optional[typing.Union[StreamOnViewAt, typing.Dict[builtins.str, typing.Any]]] = None,
    before: typing.Optional[typing.Union[StreamOnViewBefore, typing.Dict[builtins.str, typing.Any]]] = None,
    comment: typing.Optional[builtins.str] = None,
    copy_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    show_initial_rows: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adffa25d8003b51a5b932ef3726e7dc1596392a845b778b9de6a2d6805dfb41a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1f8ff564232757514148d7114648d1883b86ae43ea59871294e34df0599546(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92817e19f30138d0c0c6779ae01a3e72cc0e4410c7e632a4f58eacbe8279decd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7f6f2072ac5f6805de1f53a9bdf2f4ee32761c5b1abd2d57c7d1f2db6f1b64(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f264cdedd8e4598dd999cf72d2d40f460e4cdddfc26f291e044ba2cd38d118f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acd3a16f86772cea20870b1e0d90185b675e6130bd0111fec156edee27a4da9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569e566770d35013e8c67a752772688389280734ca75616b5916d6c46f70b5bc(
    value: typing.Optional[StreamOnViewDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f730d26b6ae5434efb3cf12218cb98271d5fb24f88ea8a817303a47b06e18b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00146ed5fe8230a4af6b97c1c015143179ad122783da7e4589cc0177c6ce80d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ef0f94c0b3da291082012bf7ed03cf01fc540c0639c3e5497cdd8ce9bb09db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34786a204ba7a1300ed0f07e5361fda6d38888c49f4da027058f2f9d9c86927d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d733906004e7df3db6791d6235c46492b8c374c146713458914638d13dbb05ff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__817f6140097567ee07fdf135b61285bb805d9a0de0a502cd43afb7da75336b57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f2a8b91777a49d26b6167945d406d87f7fe73e5e62229b3c2757e998d0905a(
    value: typing.Optional[StreamOnViewShowOutput],
) -> None:
    """Type checking stubs"""
    pass
