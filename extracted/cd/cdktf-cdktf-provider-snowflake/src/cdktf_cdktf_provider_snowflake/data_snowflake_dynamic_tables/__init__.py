r'''
# `data_snowflake_dynamic_tables`

Refer to the Terraform Registry for docs: [`data_snowflake_dynamic_tables`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables).
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


class DataSnowflakeDynamicTables(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTables",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables snowflake_dynamic_tables}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        in_: typing.Optional[typing.Union["DataSnowflakeDynamicTablesIn", typing.Dict[builtins.str, typing.Any]]] = None,
        like: typing.Optional[typing.Union["DataSnowflakeDynamicTablesLike", typing.Dict[builtins.str, typing.Any]]] = None,
        limit: typing.Optional[typing.Union["DataSnowflakeDynamicTablesLimit", typing.Dict[builtins.str, typing.Any]]] = None,
        starts_with: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables snowflake_dynamic_tables} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#id DataSnowflakeDynamicTables#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_: in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#in DataSnowflakeDynamicTables#in}
        :param like: like block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#like DataSnowflakeDynamicTables#like}
        :param limit: limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#limit DataSnowflakeDynamicTables#limit}
        :param starts_with: Optionally filters the command output based on the characters that appear at the beginning of the object name. The string is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#starts_with DataSnowflakeDynamicTables#starts_with}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2a8353bcaf1605251623e774bf6d02fcad59d53125b6b75ea3abef2d254927)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataSnowflakeDynamicTablesConfig(
            id=id,
            in_=in_,
            like=like,
            limit=limit,
            starts_with=starts_with,
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
        '''Generates CDKTF code for importing a DataSnowflakeDynamicTables resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataSnowflakeDynamicTables to import.
        :param import_from_id: The id of the existing DataSnowflakeDynamicTables that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataSnowflakeDynamicTables to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35ee8e86bb97dfe43e1b659b220e186acbf14eeae9e27e872741ed111d85a48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIn")
    def put_in(
        self,
        *,
        account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        database: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: Returns records for the entire account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#account DataSnowflakeDynamicTables#account}
        :param database: Returns records for the current database in use or for a specified database (db_name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#database DataSnowflakeDynamicTables#database}
        :param schema: Returns records for the current schema in use or a specified schema (schema_name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#schema DataSnowflakeDynamicTables#schema}
        '''
        value = DataSnowflakeDynamicTablesIn(
            account=account, database=database, schema=schema
        )

        return typing.cast(None, jsii.invoke(self, "putIn", [value]))

    @jsii.member(jsii_name="putLike")
    def put_like(self, *, pattern: builtins.str) -> None:
        '''
        :param pattern: Filters the command output by object name. The filter uses case-insensitive pattern matching with support for SQL wildcard characters (% and _). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#pattern DataSnowflakeDynamicTables#pattern}
        '''
        value = DataSnowflakeDynamicTablesLike(pattern=pattern)

        return typing.cast(None, jsii.invoke(self, "putLike", [value]))

    @jsii.member(jsii_name="putLimit")
    def put_limit(
        self,
        *,
        from_: typing.Optional[builtins.str] = None,
        rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param from_: The optional FROM 'name_string' subclause effectively serves as a “cursor” for the results. This enables fetching the specified number of rows following the first row whose object name matches the specified string Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#from DataSnowflakeDynamicTables#from}
        :param rows: Specifies the maximum number of rows to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#rows DataSnowflakeDynamicTables#rows}
        '''
        value = DataSnowflakeDynamicTablesLimit(from_=from_, rows=rows)

        return typing.cast(None, jsii.invoke(self, "putLimit", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIn")
    def reset_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIn", []))

    @jsii.member(jsii_name="resetLike")
    def reset_like(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLike", []))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @jsii.member(jsii_name="resetStartsWith")
    def reset_starts_with(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartsWith", []))

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
    @jsii.member(jsii_name="in")
    def in_(self) -> "DataSnowflakeDynamicTablesInOutputReference":
        return typing.cast("DataSnowflakeDynamicTablesInOutputReference", jsii.get(self, "in"))

    @builtins.property
    @jsii.member(jsii_name="like")
    def like(self) -> "DataSnowflakeDynamicTablesLikeOutputReference":
        return typing.cast("DataSnowflakeDynamicTablesLikeOutputReference", jsii.get(self, "like"))

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> "DataSnowflakeDynamicTablesLimitOutputReference":
        return typing.cast("DataSnowflakeDynamicTablesLimitOutputReference", jsii.get(self, "limit"))

    @builtins.property
    @jsii.member(jsii_name="records")
    def records(self) -> "DataSnowflakeDynamicTablesRecordsList":
        return typing.cast("DataSnowflakeDynamicTablesRecordsList", jsii.get(self, "records"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inInput")
    def in_input(self) -> typing.Optional["DataSnowflakeDynamicTablesIn"]:
        return typing.cast(typing.Optional["DataSnowflakeDynamicTablesIn"], jsii.get(self, "inInput"))

    @builtins.property
    @jsii.member(jsii_name="likeInput")
    def like_input(self) -> typing.Optional["DataSnowflakeDynamicTablesLike"]:
        return typing.cast(typing.Optional["DataSnowflakeDynamicTablesLike"], jsii.get(self, "likeInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional["DataSnowflakeDynamicTablesLimit"]:
        return typing.cast(typing.Optional["DataSnowflakeDynamicTablesLimit"], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="startsWithInput")
    def starts_with_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a84bf1f796cc47fd97e3161ee5d5c5d99e0e3ed5936ab9366861497ef5d0413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startsWith")
    def starts_with(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startsWith"))

    @starts_with.setter
    def starts_with(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__932fa978bb4c82077b97223845b92c9b13f7892674686cb3cc6c80925da1fa8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startsWith", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "in_": "in",
        "like": "like",
        "limit": "limit",
        "starts_with": "startsWith",
    },
)
class DataSnowflakeDynamicTablesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        in_: typing.Optional[typing.Union["DataSnowflakeDynamicTablesIn", typing.Dict[builtins.str, typing.Any]]] = None,
        like: typing.Optional[typing.Union["DataSnowflakeDynamicTablesLike", typing.Dict[builtins.str, typing.Any]]] = None,
        limit: typing.Optional[typing.Union["DataSnowflakeDynamicTablesLimit", typing.Dict[builtins.str, typing.Any]]] = None,
        starts_with: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#id DataSnowflakeDynamicTables#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_: in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#in DataSnowflakeDynamicTables#in}
        :param like: like block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#like DataSnowflakeDynamicTables#like}
        :param limit: limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#limit DataSnowflakeDynamicTables#limit}
        :param starts_with: Optionally filters the command output based on the characters that appear at the beginning of the object name. The string is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#starts_with DataSnowflakeDynamicTables#starts_with}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(in_, dict):
            in_ = DataSnowflakeDynamicTablesIn(**in_)
        if isinstance(like, dict):
            like = DataSnowflakeDynamicTablesLike(**like)
        if isinstance(limit, dict):
            limit = DataSnowflakeDynamicTablesLimit(**limit)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9369d580224784ecb30358ecb7f11113583c30963b8d0bacc1dca4d12289ffbc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument in_", value=in_, expected_type=type_hints["in_"])
            check_type(argname="argument like", value=like, expected_type=type_hints["like"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument starts_with", value=starts_with, expected_type=type_hints["starts_with"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if id is not None:
            self._values["id"] = id
        if in_ is not None:
            self._values["in_"] = in_
        if like is not None:
            self._values["like"] = like
        if limit is not None:
            self._values["limit"] = limit
        if starts_with is not None:
            self._values["starts_with"] = starts_with

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#id DataSnowflakeDynamicTables#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_(self) -> typing.Optional["DataSnowflakeDynamicTablesIn"]:
        '''in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#in DataSnowflakeDynamicTables#in}
        '''
        result = self._values.get("in_")
        return typing.cast(typing.Optional["DataSnowflakeDynamicTablesIn"], result)

    @builtins.property
    def like(self) -> typing.Optional["DataSnowflakeDynamicTablesLike"]:
        '''like block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#like DataSnowflakeDynamicTables#like}
        '''
        result = self._values.get("like")
        return typing.cast(typing.Optional["DataSnowflakeDynamicTablesLike"], result)

    @builtins.property
    def limit(self) -> typing.Optional["DataSnowflakeDynamicTablesLimit"]:
        '''limit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#limit DataSnowflakeDynamicTables#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional["DataSnowflakeDynamicTablesLimit"], result)

    @builtins.property
    def starts_with(self) -> typing.Optional[builtins.str]:
        '''Optionally filters the command output based on the characters that appear at the beginning of the object name.

        The string is case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#starts_with DataSnowflakeDynamicTables#starts_with}
        '''
        result = self._values.get("starts_with")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeDynamicTablesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesIn",
    jsii_struct_bases=[],
    name_mapping={"account": "account", "database": "database", "schema": "schema"},
)
class DataSnowflakeDynamicTablesIn:
    def __init__(
        self,
        *,
        account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        database: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: Returns records for the entire account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#account DataSnowflakeDynamicTables#account}
        :param database: Returns records for the current database in use or for a specified database (db_name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#database DataSnowflakeDynamicTables#database}
        :param schema: Returns records for the current schema in use or a specified schema (schema_name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#schema DataSnowflakeDynamicTables#schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d19a9e0404c82508d8a25a1ea3b60a6473c32ab584e0beb05d5e5fdfc220099)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if database is not None:
            self._values["database"] = database
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def account(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Returns records for the entire account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#account DataSnowflakeDynamicTables#account}
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Returns records for the current database in use or for a specified database (db_name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#database DataSnowflakeDynamicTables#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Returns records for the current schema in use or a specified schema (schema_name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#schema DataSnowflakeDynamicTables#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeDynamicTablesIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeDynamicTablesInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85e3661a6a81cda9d51b049e33c4f30d08b100203220a25903819aeafdc8a454)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccount")
    def reset_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccount", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="accountInput")
    def account_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accountInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "account"))

    @account.setter
    def account(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d21f10820c4e21bc715d70588ccab3c6d49fb1a913d310027da5a3b84498b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "account", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73ce4cce265d07652a7dd28305dce6840889b7e7d5c1a16105308ba55ec36e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbcfe5f9a0b598d67be88137180beed04bfcf643a3b0a77fa7b2eb2712c524fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeDynamicTablesIn]:
        return typing.cast(typing.Optional[DataSnowflakeDynamicTablesIn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeDynamicTablesIn],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b11e688a677cd01d4096a6e996ea982eab6ee2dc0bdca32c88f5925baaac17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesLike",
    jsii_struct_bases=[],
    name_mapping={"pattern": "pattern"},
)
class DataSnowflakeDynamicTablesLike:
    def __init__(self, *, pattern: builtins.str) -> None:
        '''
        :param pattern: Filters the command output by object name. The filter uses case-insensitive pattern matching with support for SQL wildcard characters (% and _). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#pattern DataSnowflakeDynamicTables#pattern}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e944de936825d3218846995284f4d056a69d46347c8f269cf542a09dfb1e36)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pattern": pattern,
        }

    @builtins.property
    def pattern(self) -> builtins.str:
        '''Filters the command output by object name.

        The filter uses case-insensitive pattern matching with support for SQL wildcard characters (% and _).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#pattern DataSnowflakeDynamicTables#pattern}
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeDynamicTablesLike(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeDynamicTablesLikeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesLikeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__533369c30dd8d4d4af8aea9599a22881a834c73cb3c8046eddf013b93e1de3c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c837e3756574da6b9900e2d12b166b6a2eed27e0a3da136da364f7b8a6289e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeDynamicTablesLike]:
        return typing.cast(typing.Optional[DataSnowflakeDynamicTablesLike], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeDynamicTablesLike],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad570d39c652101d660d109eb2fc8e0aaeaeca8a2ae44d7703e9be07d5c50367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesLimit",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "rows": "rows"},
)
class DataSnowflakeDynamicTablesLimit:
    def __init__(
        self,
        *,
        from_: typing.Optional[builtins.str] = None,
        rows: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param from_: The optional FROM 'name_string' subclause effectively serves as a “cursor” for the results. This enables fetching the specified number of rows following the first row whose object name matches the specified string Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#from DataSnowflakeDynamicTables#from}
        :param rows: Specifies the maximum number of rows to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#rows DataSnowflakeDynamicTables#rows}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f5cf660d24e28c0ee893a07e1b16d8716c15d29fcaea783c2b25461623ebbb)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument rows", value=rows, expected_type=type_hints["rows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if from_ is not None:
            self._values["from_"] = from_
        if rows is not None:
            self._values["rows"] = rows

    @builtins.property
    def from_(self) -> typing.Optional[builtins.str]:
        '''The optional FROM 'name_string' subclause effectively serves as a “cursor” for the results.

        This enables fetching the specified number of rows following the first row whose object name matches the specified string

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#from DataSnowflakeDynamicTables#from}
        '''
        result = self._values.get("from_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rows(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of rows to return.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/dynamic_tables#rows DataSnowflakeDynamicTables#rows}
        '''
        result = self._values.get("rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeDynamicTablesLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeDynamicTablesLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0f71393924907e767d848f40966740c188c63a4e539b751e9b42e0971e23786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrom")
    def reset_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrom", []))

    @jsii.member(jsii_name="resetRows")
    def reset_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRows", []))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="rowsInput")
    def rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowsInput"))

    @builtins.property
    @jsii.member(jsii_name="from")
    def from_(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "from"))

    @from_.setter
    def from_(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416b98e4813c49e5a0c06bf9bbfa86376a4c7a32099d0382637f55b96c567cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rows")
    def rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rows"))

    @rows.setter
    def rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc6b446f838cda78847f0230c6071467ee36da2f81ce4f2d8713bae21c9077a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeDynamicTablesLimit]:
        return typing.cast(typing.Optional[DataSnowflakeDynamicTablesLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeDynamicTablesLimit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2dcc779a0c66b5a8d190bf6c62682e4915b35b06b53949ce1ea6f655f17cdb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesRecords",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeDynamicTablesRecords:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeDynamicTablesRecords(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeDynamicTablesRecordsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesRecordsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d761da99ad6422af641cd01c5ff1dba1a1433592061bfd00e173e3e616311e55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeDynamicTablesRecordsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56264aca7bad85db11ea0f958753653c92cf00c3f5ab56d2e4be899c4d62065b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeDynamicTablesRecordsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78043296771c6280f00c27da2dcc13baee055d9f6a8e206c123a3a3f874d84dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b5f000288b3986d070e05ba4fcaa515726677b43652c8a7c7f7082cb0a795b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__243026d41c340ee1d20070be4a5816a60a5ca3e4190a6e40afeb6fa3057691bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeDynamicTablesRecordsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeDynamicTables.DataSnowflakeDynamicTablesRecordsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53a45962092dbde6bb36537525ab403791cb186744fa143eae26517c24044893)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="automaticClustering")
    def automatic_clustering(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "automaticClustering"))

    @builtins.property
    @jsii.member(jsii_name="bytes")
    def bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bytes"))

    @builtins.property
    @jsii.member(jsii_name="clusterBy")
    def cluster_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterBy"))

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
    @jsii.member(jsii_name="dataTimestamp")
    def data_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="isClone")
    def is_clone(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isClone"))

    @builtins.property
    @jsii.member(jsii_name="isReplica")
    def is_replica(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isReplica"))

    @builtins.property
    @jsii.member(jsii_name="lastSuspendedOn")
    def last_suspended_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastSuspendedOn"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="refreshMode")
    def refresh_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshMode"))

    @builtins.property
    @jsii.member(jsii_name="refreshModeReason")
    def refresh_mode_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshModeReason"))

    @builtins.property
    @jsii.member(jsii_name="rows")
    def rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rows"))

    @builtins.property
    @jsii.member(jsii_name="schedulingState")
    def scheduling_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedulingState"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="targetLag")
    def target_lag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetLag"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="warehouse")
    def warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouse"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeDynamicTablesRecords]:
        return typing.cast(typing.Optional[DataSnowflakeDynamicTablesRecords], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeDynamicTablesRecords],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84424c313a89cb3ae10bbfdfde1e3cc5b3655c1babeb5758ecf6aabc9f6480d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataSnowflakeDynamicTables",
    "DataSnowflakeDynamicTablesConfig",
    "DataSnowflakeDynamicTablesIn",
    "DataSnowflakeDynamicTablesInOutputReference",
    "DataSnowflakeDynamicTablesLike",
    "DataSnowflakeDynamicTablesLikeOutputReference",
    "DataSnowflakeDynamicTablesLimit",
    "DataSnowflakeDynamicTablesLimitOutputReference",
    "DataSnowflakeDynamicTablesRecords",
    "DataSnowflakeDynamicTablesRecordsList",
    "DataSnowflakeDynamicTablesRecordsOutputReference",
]

publication.publish()

def _typecheckingstub__cd2a8353bcaf1605251623e774bf6d02fcad59d53125b6b75ea3abef2d254927(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    in_: typing.Optional[typing.Union[DataSnowflakeDynamicTablesIn, typing.Dict[builtins.str, typing.Any]]] = None,
    like: typing.Optional[typing.Union[DataSnowflakeDynamicTablesLike, typing.Dict[builtins.str, typing.Any]]] = None,
    limit: typing.Optional[typing.Union[DataSnowflakeDynamicTablesLimit, typing.Dict[builtins.str, typing.Any]]] = None,
    starts_with: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d35ee8e86bb97dfe43e1b659b220e186acbf14eeae9e27e872741ed111d85a48(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a84bf1f796cc47fd97e3161ee5d5c5d99e0e3ed5936ab9366861497ef5d0413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__932fa978bb4c82077b97223845b92c9b13f7892674686cb3cc6c80925da1fa8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9369d580224784ecb30358ecb7f11113583c30963b8d0bacc1dca4d12289ffbc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    in_: typing.Optional[typing.Union[DataSnowflakeDynamicTablesIn, typing.Dict[builtins.str, typing.Any]]] = None,
    like: typing.Optional[typing.Union[DataSnowflakeDynamicTablesLike, typing.Dict[builtins.str, typing.Any]]] = None,
    limit: typing.Optional[typing.Union[DataSnowflakeDynamicTablesLimit, typing.Dict[builtins.str, typing.Any]]] = None,
    starts_with: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d19a9e0404c82508d8a25a1ea3b60a6473c32ab584e0beb05d5e5fdfc220099(
    *,
    account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    database: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e3661a6a81cda9d51b049e33c4f30d08b100203220a25903819aeafdc8a454(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d21f10820c4e21bc715d70588ccab3c6d49fb1a913d310027da5a3b84498b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73ce4cce265d07652a7dd28305dce6840889b7e7d5c1a16105308ba55ec36e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbcfe5f9a0b598d67be88137180beed04bfcf643a3b0a77fa7b2eb2712c524fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b11e688a677cd01d4096a6e996ea982eab6ee2dc0bdca32c88f5925baaac17(
    value: typing.Optional[DataSnowflakeDynamicTablesIn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e944de936825d3218846995284f4d056a69d46347c8f269cf542a09dfb1e36(
    *,
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533369c30dd8d4d4af8aea9599a22881a834c73cb3c8046eddf013b93e1de3c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c837e3756574da6b9900e2d12b166b6a2eed27e0a3da136da364f7b8a6289e49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad570d39c652101d660d109eb2fc8e0aaeaeca8a2ae44d7703e9be07d5c50367(
    value: typing.Optional[DataSnowflakeDynamicTablesLike],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f5cf660d24e28c0ee893a07e1b16d8716c15d29fcaea783c2b25461623ebbb(
    *,
    from_: typing.Optional[builtins.str] = None,
    rows: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f71393924907e767d848f40966740c188c63a4e539b751e9b42e0971e23786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416b98e4813c49e5a0c06bf9bbfa86376a4c7a32099d0382637f55b96c567cd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc6b446f838cda78847f0230c6071467ee36da2f81ce4f2d8713bae21c9077a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2dcc779a0c66b5a8d190bf6c62682e4915b35b06b53949ce1ea6f655f17cdb7(
    value: typing.Optional[DataSnowflakeDynamicTablesLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d761da99ad6422af641cd01c5ff1dba1a1433592061bfd00e173e3e616311e55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56264aca7bad85db11ea0f958753653c92cf00c3f5ab56d2e4be899c4d62065b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78043296771c6280f00c27da2dcc13baee055d9f6a8e206c123a3a3f874d84dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b5f000288b3986d070e05ba4fcaa515726677b43652c8a7c7f7082cb0a795b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243026d41c340ee1d20070be4a5816a60a5ca3e4190a6e40afeb6fa3057691bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a45962092dbde6bb36537525ab403791cb186744fa143eae26517c24044893(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84424c313a89cb3ae10bbfdfde1e3cc5b3655c1babeb5758ecf6aabc9f6480d9(
    value: typing.Optional[DataSnowflakeDynamicTablesRecords],
) -> None:
    """Type checking stubs"""
    pass
