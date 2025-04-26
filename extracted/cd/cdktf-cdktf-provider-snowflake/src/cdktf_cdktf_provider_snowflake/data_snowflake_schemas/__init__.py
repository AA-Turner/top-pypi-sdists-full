r'''
# `data_snowflake_schemas`

Refer to the Terraform Registry for docs: [`data_snowflake_schemas`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas).
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


class DataSnowflakeSchemas(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemas",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas snowflake_schemas}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        in_: typing.Optional[typing.Union["DataSnowflakeSchemasIn", typing.Dict[builtins.str, typing.Any]]] = None,
        like: typing.Optional[builtins.str] = None,
        limit: typing.Optional[typing.Union["DataSnowflakeSchemasLimit", typing.Dict[builtins.str, typing.Any]]] = None,
        starts_with: typing.Optional[builtins.str] = None,
        with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_parameters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas snowflake_schemas} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#id DataSnowflakeSchemas#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_: in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#in DataSnowflakeSchemas#in}
        :param like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#like DataSnowflakeSchemas#like}
        :param limit: limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#limit DataSnowflakeSchemas#limit}
        :param starts_with: Filters the output with **case-sensitive** characters indicating the beginning of the object name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#starts_with DataSnowflakeSchemas#starts_with}
        :param with_describe: Runs DESC SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the description field. By default this value is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#with_describe DataSnowflakeSchemas#with_describe}
        :param with_parameters: Runs SHOW PARAMETERS FOR SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the parameters field as a map. By default this value is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#with_parameters DataSnowflakeSchemas#with_parameters}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1757e962bec44e228d5ccc3956a105599a4f8ccbc277f4b8d8593c5c4ea3f286)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataSnowflakeSchemasConfig(
            id=id,
            in_=in_,
            like=like,
            limit=limit,
            starts_with=starts_with,
            with_describe=with_describe,
            with_parameters=with_parameters,
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
        '''Generates CDKTF code for importing a DataSnowflakeSchemas resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataSnowflakeSchemas to import.
        :param import_from_id: The id of the existing DataSnowflakeSchemas that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataSnowflakeSchemas to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442d4769be3167219e19bc264851ae514627e68564cd28314168051c947fc794)
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
        application: typing.Optional[builtins.str] = None,
        application_package: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: Returns records for the entire account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#account DataSnowflakeSchemas#account}
        :param application: Returns records for the specified application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#application DataSnowflakeSchemas#application}
        :param application_package: Returns records for the specified application package. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#application_package DataSnowflakeSchemas#application_package}
        :param database: Returns records for the current database in use or for a specified database (db_name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#database DataSnowflakeSchemas#database}
        '''
        value = DataSnowflakeSchemasIn(
            account=account,
            application=application,
            application_package=application_package,
            database=database,
        )

        return typing.cast(None, jsii.invoke(self, "putIn", [value]))

    @jsii.member(jsii_name="putLimit")
    def put_limit(
        self,
        *,
        rows: jsii.Number,
        from_: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rows: The maximum number of rows to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#rows DataSnowflakeSchemas#rows}
        :param from_: Specifies a **case-sensitive** pattern that is used to match object name. After the first match, the limit on the number of rows will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#from DataSnowflakeSchemas#from}
        '''
        value = DataSnowflakeSchemasLimit(rows=rows, from_=from_)

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

    @jsii.member(jsii_name="resetWithDescribe")
    def reset_with_describe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithDescribe", []))

    @jsii.member(jsii_name="resetWithParameters")
    def reset_with_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithParameters", []))

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
    def in_(self) -> "DataSnowflakeSchemasInOutputReference":
        return typing.cast("DataSnowflakeSchemasInOutputReference", jsii.get(self, "in"))

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> "DataSnowflakeSchemasLimitOutputReference":
        return typing.cast("DataSnowflakeSchemasLimitOutputReference", jsii.get(self, "limit"))

    @builtins.property
    @jsii.member(jsii_name="schemas")
    def schemas(self) -> "DataSnowflakeSchemasSchemasList":
        return typing.cast("DataSnowflakeSchemasSchemasList", jsii.get(self, "schemas"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inInput")
    def in_input(self) -> typing.Optional["DataSnowflakeSchemasIn"]:
        return typing.cast(typing.Optional["DataSnowflakeSchemasIn"], jsii.get(self, "inInput"))

    @builtins.property
    @jsii.member(jsii_name="likeInput")
    def like_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "likeInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional["DataSnowflakeSchemasLimit"]:
        return typing.cast(typing.Optional["DataSnowflakeSchemasLimit"], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="startsWithInput")
    def starts_with_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startsWithInput"))

    @builtins.property
    @jsii.member(jsii_name="withDescribeInput")
    def with_describe_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withDescribeInput"))

    @builtins.property
    @jsii.member(jsii_name="withParametersInput")
    def with_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d2f8a3e3f8786b4a08ff3d9dad97d3735d41e5c679aa0ce0f3510115c8bb01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="like")
    def like(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "like"))

    @like.setter
    def like(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74cc0ddb386115d7c0d109382e04237ff8c728985513a0b5121858bd7ad55a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "like", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startsWith")
    def starts_with(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startsWith"))

    @starts_with.setter
    def starts_with(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a0cfeb1f2d3ae33676429665c598715211596597e330d45fd163f1b6150bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startsWith", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withDescribe")
    def with_describe(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withDescribe"))

    @with_describe.setter
    def with_describe(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c34dc04b482c7d0d76469f6ee28cefcb04c031e0d0ea465e45445b3754fb4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withDescribe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withParameters")
    def with_parameters(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withParameters"))

    @with_parameters.setter
    def with_parameters(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baaf1e33c386261c6772a18ba712303016f9f7af56a9c6f3f4286ff456a0c27f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withParameters", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasConfig",
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
        "with_describe": "withDescribe",
        "with_parameters": "withParameters",
    },
)
class DataSnowflakeSchemasConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        in_: typing.Optional[typing.Union["DataSnowflakeSchemasIn", typing.Dict[builtins.str, typing.Any]]] = None,
        like: typing.Optional[builtins.str] = None,
        limit: typing.Optional[typing.Union["DataSnowflakeSchemasLimit", typing.Dict[builtins.str, typing.Any]]] = None,
        starts_with: typing.Optional[builtins.str] = None,
        with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        with_parameters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#id DataSnowflakeSchemas#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_: in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#in DataSnowflakeSchemas#in}
        :param like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#like DataSnowflakeSchemas#like}
        :param limit: limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#limit DataSnowflakeSchemas#limit}
        :param starts_with: Filters the output with **case-sensitive** characters indicating the beginning of the object name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#starts_with DataSnowflakeSchemas#starts_with}
        :param with_describe: Runs DESC SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the description field. By default this value is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#with_describe DataSnowflakeSchemas#with_describe}
        :param with_parameters: Runs SHOW PARAMETERS FOR SCHEMA for each schema returned by SHOW SCHEMAS. The output of describe is saved to the parameters field as a map. By default this value is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#with_parameters DataSnowflakeSchemas#with_parameters}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(in_, dict):
            in_ = DataSnowflakeSchemasIn(**in_)
        if isinstance(limit, dict):
            limit = DataSnowflakeSchemasLimit(**limit)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b62844619df9b3e8f3b49871e60137209b0b36bf956b2a21bb8a56705c11d5)
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
            check_type(argname="argument with_describe", value=with_describe, expected_type=type_hints["with_describe"])
            check_type(argname="argument with_parameters", value=with_parameters, expected_type=type_hints["with_parameters"])
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
        if with_describe is not None:
            self._values["with_describe"] = with_describe
        if with_parameters is not None:
            self._values["with_parameters"] = with_parameters

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#id DataSnowflakeSchemas#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_(self) -> typing.Optional["DataSnowflakeSchemasIn"]:
        '''in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#in DataSnowflakeSchemas#in}
        '''
        result = self._values.get("in_")
        return typing.cast(typing.Optional["DataSnowflakeSchemasIn"], result)

    @builtins.property
    def like(self) -> typing.Optional[builtins.str]:
        '''Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#like DataSnowflakeSchemas#like}
        '''
        result = self._values.get("like")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional["DataSnowflakeSchemasLimit"]:
        '''limit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#limit DataSnowflakeSchemas#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional["DataSnowflakeSchemasLimit"], result)

    @builtins.property
    def starts_with(self) -> typing.Optional[builtins.str]:
        '''Filters the output with **case-sensitive** characters indicating the beginning of the object name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#starts_with DataSnowflakeSchemas#starts_with}
        '''
        result = self._values.get("starts_with")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_describe(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runs DESC SCHEMA for each schema returned by SHOW SCHEMAS.

        The output of describe is saved to the description field. By default this value is set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#with_describe DataSnowflakeSchemas#with_describe}
        '''
        result = self._values.get("with_describe")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def with_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runs SHOW PARAMETERS FOR SCHEMA for each schema returned by SHOW SCHEMAS.

        The output of describe is saved to the parameters field as a map. By default this value is set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#with_parameters DataSnowflakeSchemas#with_parameters}
        '''
        result = self._values.get("with_parameters")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasIn",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "application": "application",
        "application_package": "applicationPackage",
        "database": "database",
    },
)
class DataSnowflakeSchemasIn:
    def __init__(
        self,
        *,
        account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        application: typing.Optional[builtins.str] = None,
        application_package: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: Returns records for the entire account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#account DataSnowflakeSchemas#account}
        :param application: Returns records for the specified application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#application DataSnowflakeSchemas#application}
        :param application_package: Returns records for the specified application package. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#application_package DataSnowflakeSchemas#application_package}
        :param database: Returns records for the current database in use or for a specified database (db_name). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#database DataSnowflakeSchemas#database}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86eb905be5f6e289c0e5d7d0fa8403dddd1b0b8f491a0a04f71ff75ab9e04f3b)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument application_package", value=application_package, expected_type=type_hints["application_package"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if application is not None:
            self._values["application"] = application
        if application_package is not None:
            self._values["application_package"] = application_package
        if database is not None:
            self._values["database"] = database

    @builtins.property
    def account(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Returns records for the entire account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#account DataSnowflakeSchemas#account}
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def application(self) -> typing.Optional[builtins.str]:
        '''Returns records for the specified application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#application DataSnowflakeSchemas#application}
        '''
        result = self._values.get("application")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_package(self) -> typing.Optional[builtins.str]:
        '''Returns records for the specified application package.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#application_package DataSnowflakeSchemas#application_package}
        '''
        result = self._values.get("application_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Returns records for the current database in use or for a specified database (db_name).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#database DataSnowflakeSchemas#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01675740148bffdb4d56a3042ad626929675f275c00828043c48c07dc86ce73c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccount")
    def reset_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccount", []))

    @jsii.member(jsii_name="resetApplication")
    def reset_application(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplication", []))

    @jsii.member(jsii_name="resetApplicationPackage")
    def reset_application_package(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationPackage", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @builtins.property
    @jsii.member(jsii_name="accountInput")
    def account_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "accountInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationInput")
    def application_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationPackageInput")
    def application_package_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationPackageInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f5da20b2cf527b6cd2ed59475d8ff194803e54f926d804fc4084aac7d998881b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "account", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @application.setter
    def application(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a027c4806504a3787df0654ae5ae09de9cd25980dd2c8e2ff1444537f3ebc4d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "application", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationPackage")
    def application_package(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationPackage"))

    @application_package.setter
    def application_package(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160b097b10685ba983e1a49e2e284cd4f5f591a9f24d4321c4084d8d3af3d420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationPackage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f906aa6fad594632b095014515e2ba43ad9d04774236462c1db2d896e340285a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeSchemasIn]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasIn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataSnowflakeSchemasIn]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0760097bbb2b60a404683a1a10b4ec9bbdda156892b072d3b2e0dcdcc109290c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasLimit",
    jsii_struct_bases=[],
    name_mapping={"rows": "rows", "from_": "from"},
)
class DataSnowflakeSchemasLimit:
    def __init__(
        self,
        *,
        rows: jsii.Number,
        from_: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rows: The maximum number of rows to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#rows DataSnowflakeSchemas#rows}
        :param from_: Specifies a **case-sensitive** pattern that is used to match object name. After the first match, the limit on the number of rows will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#from DataSnowflakeSchemas#from}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd7d16bb665887cfa1ddd3b73ebd3003ca56c4a976ea4c358041573ff4e2221)
            check_type(argname="argument rows", value=rows, expected_type=type_hints["rows"])
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rows": rows,
        }
        if from_ is not None:
            self._values["from_"] = from_

    @builtins.property
    def rows(self) -> jsii.Number:
        '''The maximum number of rows to return.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#rows DataSnowflakeSchemas#rows}
        '''
        result = self._values.get("rows")
        assert result is not None, "Required property 'rows' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def from_(self) -> typing.Optional[builtins.str]:
        '''Specifies a **case-sensitive** pattern that is used to match object name.

        After the first match, the limit on the number of rows will be applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/schemas#from DataSnowflakeSchemas#from}
        '''
        result = self._values.get("from_")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4e618c8d439c71d0b28793019da6f4837977c5dd4c4556181eb3759ed7735b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFrom")
    def reset_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrom", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ec7261a1ec933693b72a21c8a55937e71b7f8335aa472e6ea46b05371b7753dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rows")
    def rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rows"))

    @rows.setter
    def rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4f97495f73df2f569d05c5d523f69743d75c9f4583c611631a982706e635b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeSchemasLimit]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataSnowflakeSchemasLimit]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b45efe109dc11de1e7eb89010fce8e61a46428bb2a7d9243292824aad72c11e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemas",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemas:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f115871c4c3c52a69151336940082a529edaab0e55088c542ab704430e3a210)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acf8360000ee4842dc0cfac7b01ad998028e844cd86258bb90000db492a399a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276d4f9c695abd1ea05a405e3385477cccf2ccdb7b1ee7f91166c8b11a80c6a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0bf3da7067e590c3c9ef9749a78cbdd7cd7716296c7abce2363fc1c50319bb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b709c44c5ee7adaa67f097c1f82f018ceb4e6a07ffc5aca606c961f353169293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__797f1553421d804bd093df1154ef00835a40e893d9c4185b84313ade5525fffb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasDescribeOutput]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abc76ef62cc53045f2af4393f522644375d9f4df421bc6ba253d3c32a9bf088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1491a8c71d9de2f8932d045398ed6ca5694f5644639375b1ef9ae89e0940ee34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataSnowflakeSchemasSchemasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08daf666eb271265cc1006b7c459f868068cd37b5a703d7085c5259c70cf0f14)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4175a286023c58be8c9829d6b74150ed677171c5125edf470d7d0df94771d507)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccbab471305a7c4fc89b6a466079717373c8d7733a047278dc72f18f32246fb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33a1b7b82aa6ebbcaa7b048ecbfbf2b4eabc34fdecc592d1eccd34971f3a9143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7be112ee0b45a669930ac54b14a018ff79152e2bf9f57f1848939676e9832769)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="describeOutput")
    def describe_output(self) -> DataSnowflakeSchemasSchemasDescribeOutputList:
        return typing.cast(DataSnowflakeSchemasSchemasDescribeOutputList, jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "DataSnowflakeSchemasSchemasParametersList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "DataSnowflakeSchemasSchemasShowOutputList":
        return typing.cast("DataSnowflakeSchemasSchemasShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeSchemasSchemas]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemas], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemas],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c62a9e3f9d9f1b50cb5cac76fa9a2f7c9499d7a4bc964b8a9e36313cec3d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersCatalog",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersCatalog:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersCatalog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersCatalogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersCatalogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d117b1b073a460d5647c2ea71f673038a900e83b24cc5795f4361a835270568)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersCatalogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e151122a671db6772afdf92764bbfa4c16ce295e48c118f8e54ee59603e283)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersCatalogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8acb7e079c2c8d43ba2281a99ba268e493c6fcd9b90f8c7b4d609559958a54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d74e8ae3029116aef03b62bd9c70e333ba4454edb8dd3203c8102026ca87e50b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e266b4d36ada712d695be4199c49cd58f8879bb5361b1bf1861672c9dce914a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersCatalogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersCatalogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b6dd779c114f8252b5499bfd33323685ba4d1ff451445d7c4c4b7198e76e8d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersCatalog]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersCatalog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersCatalog],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70bb78bd1e1219f2f3967753039e3011c05c589566a44e4589d021bd2d1a6998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDays",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDays:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDays(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__726e508f2ddccea6c47d9b73d5c429add90e249e8c77da9abf2d2eac9664a314)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c07251c9419c8ebddf012f1c28672182610683ea53081460aeb587850fae1e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bf108b08c9f25c4998e9af413f04b1ade44435e286390d9d8e2a0f45cef9e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9b3c129d0311b7c8139365aabcd8758224e4267c9a5960f710041dd41502429)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e223c1ff0e5306ab5307dc8722ef0ae0e1c0554cfd156bff31e848b69a6e6f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18a8cff4cc414110b5be7e7eaa8508dd6c7981bf896abedf5f3ac65a6d9595ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDays]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDays], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDays],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b65a6753ba9066c20ea85ca672381883d3df10d6a30209df3a3b6d397c21a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersDefaultDdlCollation",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersDefaultDdlCollation:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersDefaultDdlCollation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersDefaultDdlCollationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersDefaultDdlCollationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd4fcbeeea049f8513af5711302e1f57ecadc48d4a9d1637402624589b74ab57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersDefaultDdlCollationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7750ecc95252b94c32607ede1be0d8bc74ecbdd5fe86476c52bc4608f061f44b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersDefaultDdlCollationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0dd238a787a4123b49e284a7d2d780bf6bc1be09f74fbb73064e5688bf7f5fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeabcfb064d9cae72711c335ecc3d1aabefa5fd9590b054b468c41b25fd7fb46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d6d4842bb51f2f06c1de06b4b868b95a17c38b71c81ef920fdcfc33eeb15484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersDefaultDdlCollationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersDefaultDdlCollationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d8ef67632df69ea1dc37023d5493f398ec347c6c5208d5e9b9014b3507935a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersDefaultDdlCollation]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersDefaultDdlCollation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersDefaultDdlCollation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889f5e93ccd9bc2ec4eea88a2c7d5c31bac3a89623abb0bc93a08fabfee95b57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersEnableConsoleOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersEnableConsoleOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersEnableConsoleOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersEnableConsoleOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersEnableConsoleOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__344ba471b9cd9043555d5265efdfa9e478bb2607ddbd5a5daf943ea30bea926c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersEnableConsoleOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11da1075128b33cb879e6595dda54499a3766a458b7c0a50d78e4e6f43894c0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersEnableConsoleOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9364362b85c7238b72f7df4428a1087bfd6a8748dfc138e4129fb1135ab11656)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2c863b671a114ff32a2d0fd7ef1f8d5fdb62e9de849de4d9bbdcdf273e6040c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8942a31d8a7252117839f58863898e4eff534ca9587e3dec192e60cdad83ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersEnableConsoleOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersEnableConsoleOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72f85241f0b276c72b803ad318d6377845f469680328ea88c68e15327642f32f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersEnableConsoleOutput]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersEnableConsoleOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersEnableConsoleOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522ac21535033b28823ed97e590a14216b5100d2f9bd00fef75a29cba7bc3764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersExternalVolume",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersExternalVolume:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersExternalVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersExternalVolumeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersExternalVolumeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca824d6432f504c9255982d3330ec7a7bf872c61dccce809f6c166dc98a743ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersExternalVolumeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e83843519ee05d8d1ec88ae887298686d1e99c4b196369475bb3d746a4fc1c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersExternalVolumeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c9ef714a5a47e9cc122b6eef4a8d7172dbfea577d73a2cbf5f979bbc407aef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b1f010af9efeb80d2e9aa020761809754460c71ef99af9b334d04ed01cacc2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d342f4e375636d53b95f4273cf9ad778a8f76f2bda39b593268f684c9a4766ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersExternalVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersExternalVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99b3f04aece87dc9904e7d9c56840d49a042730ea1278603345052cf286162b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersExternalVolume]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersExternalVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersExternalVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2840544fd925fbd2658b6e66033cfe05db7df9b5bca139026ecedc614830435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fef31056b2cfd3a4de25f6f7a69d3398aa9e94f3141d83af77e31bccf8ec77c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30074ba30d1e06c16019aeb0fdd69cefe54744dc312e05a1dce035f7dfe876bd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6fb0e7eafca2e6653fbf860cb930264ccf18f33addb89107baedd843e08a19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__933b6c9a5fff42de923ec1e5dd8cdb51ab66312949574391950ac332e3d8ed49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4050332d1c0b256af5692fe1de4412495cab7fd1f60348bae39abab0b1d7d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79f4feaff5bc30b5e08c953abae947c5d017c3da57ee7f4eeb097d6d4a58e415)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c56a56c333896abc56565b6bb3c9dcc55732275a3be63e5efffb32b6006fcfc6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8933def9b75f7f9d5a0a00ed5750082b26ea5bb7f829cf4a01c3af21121728a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97929cee3dc03382b420d878fdbf548173d9a78142db2f1bc736e3e5e1e05a7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62dd36d27644b3efad850506e37bba2e9ae406556b8eab0bf44660eb85cfab20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ab65188da172f6df0cd681a9eebef69b15d9549e205226a6e052a9db4036df8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersLogLevel]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersLogLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cad4aaf8a4e40853bbb1f0b9acc3e7032f3a767a55eeea5c10d93700f751b0d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDays",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDays:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDays(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7923bab2c62d5647dada161f9e1160b2b6b57b860bbca58ae7c64efdd7e8d92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd0cbadc88fc2b12cd6a0bb3550a8f7e2d521bf72abfa92af642ae727b1636c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae3c02c7122e8a8560a564ed2b21dac3252c2827653f63f3b766362dd066524)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a204e75609ef3e5b829873c0ddc4b2ede350f4d02006d645aa481ebb5a9bace5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0076400489d1c00d25fc559dd869949f3dd077b3955f79aea64e372810d15e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab4205f5cda6d6216587d53ca37875b3194be1399dd8e295a2228be1058a6a8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDays]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDays], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDays],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8679e87053c438b717d6fbdd6106f3719365fb968de820ecad3e8ffa86ce6b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c4036d0967a10e7b030e833112524fc3706b4c6ed27d401e3f025713f05194)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> DataSnowflakeSchemasSchemasParametersCatalogList:
        return typing.cast(DataSnowflakeSchemasSchemasParametersCatalogList, jsii.get(self, "catalog"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDays")
    def data_retention_time_in_days(
        self,
    ) -> DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysList:
        return typing.cast(DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysList, jsii.get(self, "dataRetentionTimeInDays"))

    @builtins.property
    @jsii.member(jsii_name="defaultDdlCollation")
    def default_ddl_collation(
        self,
    ) -> DataSnowflakeSchemasSchemasParametersDefaultDdlCollationList:
        return typing.cast(DataSnowflakeSchemasSchemasParametersDefaultDdlCollationList, jsii.get(self, "defaultDdlCollation"))

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(
        self,
    ) -> DataSnowflakeSchemasSchemasParametersEnableConsoleOutputList:
        return typing.cast(DataSnowflakeSchemasSchemasParametersEnableConsoleOutputList, jsii.get(self, "enableConsoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="externalVolume")
    def external_volume(
        self,
    ) -> DataSnowflakeSchemasSchemasParametersExternalVolumeList:
        return typing.cast(DataSnowflakeSchemasSchemasParametersExternalVolumeList, jsii.get(self, "externalVolume"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> DataSnowflakeSchemasSchemasParametersLogLevelList:
        return typing.cast(DataSnowflakeSchemasSchemasParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="maxDataExtensionTimeInDays")
    def max_data_extension_time_in_days(
        self,
    ) -> DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysList:
        return typing.cast(DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysList, jsii.get(self, "maxDataExtensionTimeInDays"))

    @builtins.property
    @jsii.member(jsii_name="pipeExecutionPaused")
    def pipe_execution_paused(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersPipeExecutionPausedList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersPipeExecutionPausedList", jsii.get(self, "pipeExecutionPaused"))

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCase")
    def quoted_identifiers_ignore_case(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseList", jsii.get(self, "quotedIdentifiersIgnoreCase"))

    @builtins.property
    @jsii.member(jsii_name="replaceInvalidCharacters")
    def replace_invalid_characters(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersList", jsii.get(self, "replaceInvalidCharacters"))

    @builtins.property
    @jsii.member(jsii_name="storageSerializationPolicy")
    def storage_serialization_policy(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyList", jsii.get(self, "storageSerializationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailures")
    def suspend_task_after_num_failures(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresList", jsii.get(self, "suspendTaskAfterNumFailures"))

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttempts")
    def task_auto_retry_attempts(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsList", jsii.get(self, "taskAutoRetryAttempts"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "DataSnowflakeSchemasSchemasParametersTraceLevelList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSize")
    def user_task_managed_initial_warehouse_size(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeList", jsii.get(self, "userTaskManagedInitialWarehouseSize"))

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSeconds")
    def user_task_minimum_trigger_interval_in_seconds(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsList", jsii.get(self, "userTaskMinimumTriggerIntervalInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMs")
    def user_task_timeout_ms(
        self,
    ) -> "DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsList":
        return typing.cast("DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsList", jsii.get(self, "userTaskTimeoutMs"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeSchemasSchemasParameters]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a139499b243b630ddf0e234ccfbfc2de4cc01a1625cb6690f950b28179c07b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersPipeExecutionPaused",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersPipeExecutionPaused:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersPipeExecutionPaused(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersPipeExecutionPausedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersPipeExecutionPausedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e0345cacc95c559d8eee427f3f8c5908c220dbf606ff081cd42fa592597f07b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersPipeExecutionPausedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e3a3c25d8b362110982139cb754a904d7ff94e663e59aa93e063c82b8d6fd6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersPipeExecutionPausedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10154f32412e43adc3093f999c3bd7c8cb31c3169d2793d774bc6088ae83a36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__919892da496b4b9a1a75f07acb594e7fb349a5fc1deb1d0f74e64b87c81c97e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7013993d90f7795c9f991a65e903f255ea6ce325d89b3c3a0456b7a354c2cafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersPipeExecutionPausedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersPipeExecutionPausedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47cfabe95929f85cb025ba7cfd565b2fa2b997843b5dd86fdc6747daafe8d15a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersPipeExecutionPaused]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersPipeExecutionPaused], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersPipeExecutionPaused],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22122e04b2531b5564c95ee8b911fcbd6c76dc827e6f5e7f20a925468bcc162f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCase",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCase:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abd472644e12a5c95147ccc1fc8bf4958fbe6956a12522d65e0bc660d5465b95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c345d6a054c4cf6b2a8600802018854699f1efacc313a69e9e157539a5a238bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa0d52138bb23ee0298f00bbc2dc2eea8f40f69d2db15f97b98da57f61b9f8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f4deae69cd581e070489ddd8900cd5ceb9362667fd59a69c1b0b73c0b0cccac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4d59be24ae28058cb1b607f718c75cc51e738869bb52fe049c58f92fdd258b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03a7d52edd1e009026c83866aeb2e575f7ac8120c1f27e17f3d813bf5143c42c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCase]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCase], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCase],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e7074a7af23938430345212f695084ecc7ae490b97f861ca47d939582a8ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersReplaceInvalidCharacters",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersReplaceInvalidCharacters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersReplaceInvalidCharacters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6859509c5275997e530d7b7a8e7ae326be5f50c5ce72db9edc3761c0b9868c07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c872cc1d70b0aeb2f538468ab71594db038eaabf7b77c811d037dc9a520b85)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd6bd429f962795516fea300316bc05e8c132cb63b5c4308affdf2055ce292c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ce95912731c2a017177185c9cb90bd7108eba4b70f1e0efbc8eb89a1850e497)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0acc892562bb9ad9ff455a816f723ed64a81e678d49bb994ff55cbaab16f976c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20dd9dd95f265b18aa22a36af1b151e334dabbf6f3cac5bbe50001b424372ca1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersReplaceInvalidCharacters]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersReplaceInvalidCharacters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersReplaceInvalidCharacters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d6345cf639ce1ad23b7995ec23276a68cdca8de7d2659a6ec2b47b3b831850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersStorageSerializationPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersStorageSerializationPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersStorageSerializationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48dca80ceb10de548d666e3227fd4ffce0b2e451058a4075fd1f7f9aa8c2fab1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d360df4e5d2a28a3164d5208965f209c4341d347c6a1e7ce22d45a0dabca10c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f31b768cb3bc27c308ab222f5c754c64fc4d33a2e31e51f127efe5b40531900)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15b3592f38fe6d34fe8e66bace5d071ed14d23ebd0a45a3bfabeb69ea6494292)
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
            type_hints = typing.get_type_hints(_typecheckingstub__886cb9441cd635a86053dc1375cfdaad7f8f085ceba8af193c839a665aab6050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dcb387c59005593e6177e67e496f256cb49ee7e5ca43541c255ad0a8e62525d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersStorageSerializationPolicy]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersStorageSerializationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersStorageSerializationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f881ecbfa579f22d546a33c2ada908e7ba6793d29b99b81e8fd9d986e74128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailures",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailures:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__500d8f622a4a28147fa20d79ce34f93a535a08ff6aa5aa2b1383934c1e853891)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e8bb8d92c4d57eaebc9bed8ce91148f7803bbd1187559eaeb3fafde977d817)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b56cfc4a694dfb959ddf09af688e179467f18ec0fddf65ec05515bc26b8c0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae66e2ff0217b284e5b8362ee03fa0079447b8a7621d4016476379ea65ea8dde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8aad999bccb1c4107137d3233c677fb5b3150dfdf59ef88150eceadaa9e97395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3e3de32b0e747505815529745fbc8277051812b6eb1332c657db9e5ee8fcfe7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailures]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c457b0baf901178d0b8ee13a1cea61002553f4d82bbef287df7797fa5f0c64d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttempts",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttempts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttempts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b80557eeacdfb4906fed9d2b6004f0e39f32fb0c544507fa7f12840161a86c9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47688beca4022284818d1316ebc4d5a9b4da42b36e67a4e5ce7a97298badd065)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b713d5f092c2f22d9523a505b10ccdc3e6e95bad5e52d64b9e8a54462728bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22185d238ea25506afffc52ffeda99166ea4c137f420b78919d74c8fc7caea7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05eaa48d44094461ee5bc18e5217a9f072768a33006750306a604f6be3e397c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37d6d0c0c8239ec2230b58995d316cbea534261e182c35b947ba120206d016e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttempts]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttempts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttempts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd62c81ce5d07e46eca33679e0f340cdfa1b94ef11ba572941ec72768b1d31a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__befc5d70918adcb902168ec4f1748480392a2f310a59e506690a72f16cdb98d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2551e33f3e16eaf0c8dd0bb26ec1d8b45c4014a98960f928f7b2278c56b5d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61de037dd4138f84ef26263315cf93162f9eed7b554bbf91da067666018b7c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__700f7db0cbdc226e129f48fc3308952ef8e8062a6cc08eacf871fcba24e3fec4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdf073686123ce8272d16b76e264384891641e6b91e2082e0f2559aec6fc1f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8a69b5d8b9e72516df8adb2fda9e7b821077e86ea21357752711b41b6effaf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersTraceLevel]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76efe09fcbfaa01dda03229e8ab816bccb938bc9d830bf29aa951d165d643909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSize",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSize:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__229974d0e1b46f393d98e639cc3cfb6d9c1aa1b41919771a4ff5871ef483fd18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9eb3aeedcc32c4cd66499f1374741ec6e642ab3a901a396578610ea7021bbb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c038c762788bb252de709690dc85fff66226139a5dbe7325e610da7318a0611c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be0ff91fdd017ff8793de35046f85ea42fe68509328f44f7da3c58ca54ac5254)
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
            type_hints = typing.get_type_hints(_typecheckingstub__574cbe89613d75f30704d17fd2d68543ab96fb8f2a06cdbd17e84b94e31ebcf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ad1a81ee7decaaf61f57ea4e1e3dd8a092adfa2cf91bfccdef771f88ee78a58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSize]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f0a63078bb0f1aee00e244f8c1899c6d16dcc9db67749751981a630be8abaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d58b9635d3609a119bb19a859f42ecd6e9a7572f42c73c9d914c8c85b7284cf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12bd69b3d1abece13119e08b9fad53c10882eb57040296578a160724e4907454)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc095cc888d0b96287ce645ad4ffed818a9a4ad7c6bf0b7c698930efa2ff409)
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
            type_hints = typing.get_type_hints(_typecheckingstub__285ff532d2d28a6e61db95602a6254153d59da5d8057d06bb7caca5a49fe0c2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13e46cffdb282f8b5b561a4fe31bf844a63b6da7e837c3096c9391be55980ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25176bf0fb32b053d91ace3ae6cf095072d121d07101b6d23ddfd30525bdb17e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSeconds]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1747983c72e7aa132319a7c70287bd172cbcc921256b18f4676e5f326b5d0cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMs",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0d6aec76324486a485819fd604de0ff91a4b8a17d6067cbab4692ccb2fa0615)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e920d8cfbb7805fa6784e42de8b11db32b319766ffe9c7b0117d025af01eb814)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18c566f6b9461be8ee884b01e8fd5313a29be9683788f7c66ce16f835c2e68a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a53e2031acd19c7ce19e183ed916be77010de236b7e6c1b0a072b0cbd9cd0cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5f52dec8c69c9a9189d97f6379b098690325bf10c585bc483448088d3465e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f40112a6c7b56556892bed0d35314f052c17c11d7b781f41f757109baf91f49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMs]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee40293b52b45db4609ef6ca9aab38eb13738c366d99ccb51b3a5cd4d63241c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeSchemasSchemasShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeSchemasSchemasShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeSchemasSchemasShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f49aff93902fa6213c2776fe802c8660b236229205084561806a9f014a8a77d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeSchemasSchemasShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f47890f268bfd5fb0468eafa573ec9cb7abf10eddd49a41e8a74d558c28d934)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeSchemasSchemasShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e529151138779e93455b74522b56c6dfed19934e50cd0ca2b529b722153560)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb34e1612437960c58e82fc97a58e1b84e248f413156a199f6c908e96363a1ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c8618d32569aaf4c5c00a99769e6faff5335de904fb412c7c5f34dc3119c024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeSchemasSchemasShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeSchemas.DataSnowflakeSchemasSchemasShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2a4672f93a00abf998753edae6c298071dd77a03ddd4acb5216ae186eccd30c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
    @jsii.member(jsii_name="droppedOn")
    def dropped_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "droppedOn"))

    @builtins.property
    @jsii.member(jsii_name="isCurrent")
    def is_current(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isCurrent"))

    @builtins.property
    @jsii.member(jsii_name="isDefault")
    def is_default(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isDefault"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="ownerRoleType")
    def owner_role_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerRoleType"))

    @builtins.property
    @jsii.member(jsii_name="retentionTime")
    def retention_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeSchemasSchemasShowOutput]:
        return typing.cast(typing.Optional[DataSnowflakeSchemasSchemasShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeSchemasSchemasShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2188e34b057dc84a346f6e1cde5fd4c2839ce1bedebe2e01555c266c9a6ec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataSnowflakeSchemas",
    "DataSnowflakeSchemasConfig",
    "DataSnowflakeSchemasIn",
    "DataSnowflakeSchemasInOutputReference",
    "DataSnowflakeSchemasLimit",
    "DataSnowflakeSchemasLimitOutputReference",
    "DataSnowflakeSchemasSchemas",
    "DataSnowflakeSchemasSchemasDescribeOutput",
    "DataSnowflakeSchemasSchemasDescribeOutputList",
    "DataSnowflakeSchemasSchemasDescribeOutputOutputReference",
    "DataSnowflakeSchemasSchemasList",
    "DataSnowflakeSchemasSchemasOutputReference",
    "DataSnowflakeSchemasSchemasParameters",
    "DataSnowflakeSchemasSchemasParametersCatalog",
    "DataSnowflakeSchemasSchemasParametersCatalogList",
    "DataSnowflakeSchemasSchemasParametersCatalogOutputReference",
    "DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDays",
    "DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysList",
    "DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDaysOutputReference",
    "DataSnowflakeSchemasSchemasParametersDefaultDdlCollation",
    "DataSnowflakeSchemasSchemasParametersDefaultDdlCollationList",
    "DataSnowflakeSchemasSchemasParametersDefaultDdlCollationOutputReference",
    "DataSnowflakeSchemasSchemasParametersEnableConsoleOutput",
    "DataSnowflakeSchemasSchemasParametersEnableConsoleOutputList",
    "DataSnowflakeSchemasSchemasParametersEnableConsoleOutputOutputReference",
    "DataSnowflakeSchemasSchemasParametersExternalVolume",
    "DataSnowflakeSchemasSchemasParametersExternalVolumeList",
    "DataSnowflakeSchemasSchemasParametersExternalVolumeOutputReference",
    "DataSnowflakeSchemasSchemasParametersList",
    "DataSnowflakeSchemasSchemasParametersLogLevel",
    "DataSnowflakeSchemasSchemasParametersLogLevelList",
    "DataSnowflakeSchemasSchemasParametersLogLevelOutputReference",
    "DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDays",
    "DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysList",
    "DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDaysOutputReference",
    "DataSnowflakeSchemasSchemasParametersOutputReference",
    "DataSnowflakeSchemasSchemasParametersPipeExecutionPaused",
    "DataSnowflakeSchemasSchemasParametersPipeExecutionPausedList",
    "DataSnowflakeSchemasSchemasParametersPipeExecutionPausedOutputReference",
    "DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCase",
    "DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseList",
    "DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCaseOutputReference",
    "DataSnowflakeSchemasSchemasParametersReplaceInvalidCharacters",
    "DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersList",
    "DataSnowflakeSchemasSchemasParametersReplaceInvalidCharactersOutputReference",
    "DataSnowflakeSchemasSchemasParametersStorageSerializationPolicy",
    "DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyList",
    "DataSnowflakeSchemasSchemasParametersStorageSerializationPolicyOutputReference",
    "DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailures",
    "DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresList",
    "DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailuresOutputReference",
    "DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttempts",
    "DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsList",
    "DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttemptsOutputReference",
    "DataSnowflakeSchemasSchemasParametersTraceLevel",
    "DataSnowflakeSchemasSchemasParametersTraceLevelList",
    "DataSnowflakeSchemasSchemasParametersTraceLevelOutputReference",
    "DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSize",
    "DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeList",
    "DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSizeOutputReference",
    "DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSeconds",
    "DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsList",
    "DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference",
    "DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMs",
    "DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsList",
    "DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMsOutputReference",
    "DataSnowflakeSchemasSchemasShowOutput",
    "DataSnowflakeSchemasSchemasShowOutputList",
    "DataSnowflakeSchemasSchemasShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__1757e962bec44e228d5ccc3956a105599a4f8ccbc277f4b8d8593c5c4ea3f286(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    in_: typing.Optional[typing.Union[DataSnowflakeSchemasIn, typing.Dict[builtins.str, typing.Any]]] = None,
    like: typing.Optional[builtins.str] = None,
    limit: typing.Optional[typing.Union[DataSnowflakeSchemasLimit, typing.Dict[builtins.str, typing.Any]]] = None,
    starts_with: typing.Optional[builtins.str] = None,
    with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_parameters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__442d4769be3167219e19bc264851ae514627e68564cd28314168051c947fc794(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d2f8a3e3f8786b4a08ff3d9dad97d3735d41e5c679aa0ce0f3510115c8bb01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cc0ddb386115d7c0d109382e04237ff8c728985513a0b5121858bd7ad55a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a0cfeb1f2d3ae33676429665c598715211596597e330d45fd163f1b6150bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c34dc04b482c7d0d76469f6ee28cefcb04c031e0d0ea465e45445b3754fb4e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baaf1e33c386261c6772a18ba712303016f9f7af56a9c6f3f4286ff456a0c27f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b62844619df9b3e8f3b49871e60137209b0b36bf956b2a21bb8a56705c11d5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    in_: typing.Optional[typing.Union[DataSnowflakeSchemasIn, typing.Dict[builtins.str, typing.Any]]] = None,
    like: typing.Optional[builtins.str] = None,
    limit: typing.Optional[typing.Union[DataSnowflakeSchemasLimit, typing.Dict[builtins.str, typing.Any]]] = None,
    starts_with: typing.Optional[builtins.str] = None,
    with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    with_parameters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86eb905be5f6e289c0e5d7d0fa8403dddd1b0b8f491a0a04f71ff75ab9e04f3b(
    *,
    account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    application: typing.Optional[builtins.str] = None,
    application_package: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01675740148bffdb4d56a3042ad626929675f275c00828043c48c07dc86ce73c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5da20b2cf527b6cd2ed59475d8ff194803e54f926d804fc4084aac7d998881b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a027c4806504a3787df0654ae5ae09de9cd25980dd2c8e2ff1444537f3ebc4d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160b097b10685ba983e1a49e2e284cd4f5f591a9f24d4321c4084d8d3af3d420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f906aa6fad594632b095014515e2ba43ad9d04774236462c1db2d896e340285a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0760097bbb2b60a404683a1a10b4ec9bbdda156892b072d3b2e0dcdcc109290c(
    value: typing.Optional[DataSnowflakeSchemasIn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd7d16bb665887cfa1ddd3b73ebd3003ca56c4a976ea4c358041573ff4e2221(
    *,
    rows: jsii.Number,
    from_: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e618c8d439c71d0b28793019da6f4837977c5dd4c4556181eb3759ed7735b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7261a1ec933693b72a21c8a55937e71b7f8335aa472e6ea46b05371b7753dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4f97495f73df2f569d05c5d523f69743d75c9f4583c611631a982706e635b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b45efe109dc11de1e7eb89010fce8e61a46428bb2a7d9243292824aad72c11e(
    value: typing.Optional[DataSnowflakeSchemasLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f115871c4c3c52a69151336940082a529edaab0e55088c542ab704430e3a210(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acf8360000ee4842dc0cfac7b01ad998028e844cd86258bb90000db492a399a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276d4f9c695abd1ea05a405e3385477cccf2ccdb7b1ee7f91166c8b11a80c6a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0bf3da7067e590c3c9ef9749a78cbdd7cd7716296c7abce2363fc1c50319bb4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b709c44c5ee7adaa67f097c1f82f018ceb4e6a07ffc5aca606c961f353169293(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797f1553421d804bd093df1154ef00835a40e893d9c4185b84313ade5525fffb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abc76ef62cc53045f2af4393f522644375d9f4df421bc6ba253d3c32a9bf088(
    value: typing.Optional[DataSnowflakeSchemasSchemasDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1491a8c71d9de2f8932d045398ed6ca5694f5644639375b1ef9ae89e0940ee34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08daf666eb271265cc1006b7c459f868068cd37b5a703d7085c5259c70cf0f14(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4175a286023c58be8c9829d6b74150ed677171c5125edf470d7d0df94771d507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbab471305a7c4fc89b6a466079717373c8d7733a047278dc72f18f32246fb7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a1b7b82aa6ebbcaa7b048ecbfbf2b4eabc34fdecc592d1eccd34971f3a9143(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be112ee0b45a669930ac54b14a018ff79152e2bf9f57f1848939676e9832769(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c62a9e3f9d9f1b50cb5cac76fa9a2f7c9499d7a4bc964b8a9e36313cec3d44(
    value: typing.Optional[DataSnowflakeSchemasSchemas],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d117b1b073a460d5647c2ea71f673038a900e83b24cc5795f4361a835270568(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e151122a671db6772afdf92764bbfa4c16ce295e48c118f8e54ee59603e283(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8acb7e079c2c8d43ba2281a99ba268e493c6fcd9b90f8c7b4d609559958a54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74e8ae3029116aef03b62bd9c70e333ba4454edb8dd3203c8102026ca87e50b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e266b4d36ada712d695be4199c49cd58f8879bb5361b1bf1861672c9dce914a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6dd779c114f8252b5499bfd33323685ba4d1ff451445d7c4c4b7198e76e8d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70bb78bd1e1219f2f3967753039e3011c05c589566a44e4589d021bd2d1a6998(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersCatalog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726e508f2ddccea6c47d9b73d5c429add90e249e8c77da9abf2d2eac9664a314(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c07251c9419c8ebddf012f1c28672182610683ea53081460aeb587850fae1e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bf108b08c9f25c4998e9af413f04b1ade44435e286390d9d8e2a0f45cef9e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b3c129d0311b7c8139365aabcd8758224e4267c9a5960f710041dd41502429(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e223c1ff0e5306ab5307dc8722ef0ae0e1c0554cfd156bff31e848b69a6e6f57(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a8cff4cc414110b5be7e7eaa8508dd6c7981bf896abedf5f3ac65a6d9595ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b65a6753ba9066c20ea85ca672381883d3df10d6a30209df3a3b6d397c21a9(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersDataRetentionTimeInDays],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4fcbeeea049f8513af5711302e1f57ecadc48d4a9d1637402624589b74ab57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7750ecc95252b94c32607ede1be0d8bc74ecbdd5fe86476c52bc4608f061f44b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dd238a787a4123b49e284a7d2d780bf6bc1be09f74fbb73064e5688bf7f5fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeabcfb064d9cae72711c335ecc3d1aabefa5fd9590b054b468c41b25fd7fb46(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6d4842bb51f2f06c1de06b4b868b95a17c38b71c81ef920fdcfc33eeb15484(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8ef67632df69ea1dc37023d5493f398ec347c6c5208d5e9b9014b3507935a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889f5e93ccd9bc2ec4eea88a2c7d5c31bac3a89623abb0bc93a08fabfee95b57(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersDefaultDdlCollation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344ba471b9cd9043555d5265efdfa9e478bb2607ddbd5a5daf943ea30bea926c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11da1075128b33cb879e6595dda54499a3766a458b7c0a50d78e4e6f43894c0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9364362b85c7238b72f7df4428a1087bfd6a8748dfc138e4129fb1135ab11656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c863b671a114ff32a2d0fd7ef1f8d5fdb62e9de849de4d9bbdcdf273e6040c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8942a31d8a7252117839f58863898e4eff534ca9587e3dec192e60cdad83ff5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f85241f0b276c72b803ad318d6377845f469680328ea88c68e15327642f32f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522ac21535033b28823ed97e590a14216b5100d2f9bd00fef75a29cba7bc3764(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersEnableConsoleOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca824d6432f504c9255982d3330ec7a7bf872c61dccce809f6c166dc98a743ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e83843519ee05d8d1ec88ae887298686d1e99c4b196369475bb3d746a4fc1c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c9ef714a5a47e9cc122b6eef4a8d7172dbfea577d73a2cbf5f979bbc407aef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1f010af9efeb80d2e9aa020761809754460c71ef99af9b334d04ed01cacc2a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d342f4e375636d53b95f4273cf9ad778a8f76f2bda39b593268f684c9a4766ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b3f04aece87dc9904e7d9c56840d49a042730ea1278603345052cf286162b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2840544fd925fbd2658b6e66033cfe05db7df9b5bca139026ecedc614830435(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersExternalVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef31056b2cfd3a4de25f6f7a69d3398aa9e94f3141d83af77e31bccf8ec77c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30074ba30d1e06c16019aeb0fdd69cefe54744dc312e05a1dce035f7dfe876bd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6fb0e7eafca2e6653fbf860cb930264ccf18f33addb89107baedd843e08a19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933b6c9a5fff42de923ec1e5dd8cdb51ab66312949574391950ac332e3d8ed49(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4050332d1c0b256af5692fe1de4412495cab7fd1f60348bae39abab0b1d7d61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f4feaff5bc30b5e08c953abae947c5d017c3da57ee7f4eeb097d6d4a58e415(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56a56c333896abc56565b6bb3c9dcc55732275a3be63e5efffb32b6006fcfc6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8933def9b75f7f9d5a0a00ed5750082b26ea5bb7f829cf4a01c3af21121728a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97929cee3dc03382b420d878fdbf548173d9a78142db2f1bc736e3e5e1e05a7b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62dd36d27644b3efad850506e37bba2e9ae406556b8eab0bf44660eb85cfab20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab65188da172f6df0cd681a9eebef69b15d9549e205226a6e052a9db4036df8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cad4aaf8a4e40853bbb1f0b9acc3e7032f3a767a55eeea5c10d93700f751b0d6(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7923bab2c62d5647dada161f9e1160b2b6b57b860bbca58ae7c64efdd7e8d92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd0cbadc88fc2b12cd6a0bb3550a8f7e2d521bf72abfa92af642ae727b1636c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae3c02c7122e8a8560a564ed2b21dac3252c2827653f63f3b766362dd066524(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a204e75609ef3e5b829873c0ddc4b2ede350f4d02006d645aa481ebb5a9bace5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0076400489d1c00d25fc559dd869949f3dd077b3955f79aea64e372810d15e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4205f5cda6d6216587d53ca37875b3194be1399dd8e295a2228be1058a6a8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8679e87053c438b717d6fbdd6106f3719365fb968de820ecad3e8ffa86ce6b7(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersMaxDataExtensionTimeInDays],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c4036d0967a10e7b030e833112524fc3706b4c6ed27d401e3f025713f05194(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a139499b243b630ddf0e234ccfbfc2de4cc01a1625cb6690f950b28179c07b(
    value: typing.Optional[DataSnowflakeSchemasSchemasParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0345cacc95c559d8eee427f3f8c5908c220dbf606ff081cd42fa592597f07b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e3a3c25d8b362110982139cb754a904d7ff94e663e59aa93e063c82b8d6fd6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10154f32412e43adc3093f999c3bd7c8cb31c3169d2793d774bc6088ae83a36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919892da496b4b9a1a75f07acb594e7fb349a5fc1deb1d0f74e64b87c81c97e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7013993d90f7795c9f991a65e903f255ea6ce325d89b3c3a0456b7a354c2cafc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47cfabe95929f85cb025ba7cfd565b2fa2b997843b5dd86fdc6747daafe8d15a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22122e04b2531b5564c95ee8b911fcbd6c76dc827e6f5e7f20a925468bcc162f(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersPipeExecutionPaused],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd472644e12a5c95147ccc1fc8bf4958fbe6956a12522d65e0bc660d5465b95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c345d6a054c4cf6b2a8600802018854699f1efacc313a69e9e157539a5a238bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa0d52138bb23ee0298f00bbc2dc2eea8f40f69d2db15f97b98da57f61b9f8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4deae69cd581e070489ddd8900cd5ceb9362667fd59a69c1b0b73c0b0cccac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d59be24ae28058cb1b607f718c75cc51e738869bb52fe049c58f92fdd258b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a7d52edd1e009026c83866aeb2e575f7ac8120c1f27e17f3d813bf5143c42c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e7074a7af23938430345212f695084ecc7ae490b97f861ca47d939582a8ab0(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersQuotedIdentifiersIgnoreCase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6859509c5275997e530d7b7a8e7ae326be5f50c5ce72db9edc3761c0b9868c07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c872cc1d70b0aeb2f538468ab71594db038eaabf7b77c811d037dc9a520b85(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd6bd429f962795516fea300316bc05e8c132cb63b5c4308affdf2055ce292c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce95912731c2a017177185c9cb90bd7108eba4b70f1e0efbc8eb89a1850e497(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acc892562bb9ad9ff455a816f723ed64a81e678d49bb994ff55cbaab16f976c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dd9dd95f265b18aa22a36af1b151e334dabbf6f3cac5bbe50001b424372ca1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d6345cf639ce1ad23b7995ec23276a68cdca8de7d2659a6ec2b47b3b831850(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersReplaceInvalidCharacters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48dca80ceb10de548d666e3227fd4ffce0b2e451058a4075fd1f7f9aa8c2fab1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d360df4e5d2a28a3164d5208965f209c4341d347c6a1e7ce22d45a0dabca10c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f31b768cb3bc27c308ab222f5c754c64fc4d33a2e31e51f127efe5b40531900(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b3592f38fe6d34fe8e66bace5d071ed14d23ebd0a45a3bfabeb69ea6494292(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886cb9441cd635a86053dc1375cfdaad7f8f085ceba8af193c839a665aab6050(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcb387c59005593e6177e67e496f256cb49ee7e5ca43541c255ad0a8e62525d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f881ecbfa579f22d546a33c2ada908e7ba6793d29b99b81e8fd9d986e74128(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersStorageSerializationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500d8f622a4a28147fa20d79ce34f93a535a08ff6aa5aa2b1383934c1e853891(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e8bb8d92c4d57eaebc9bed8ce91148f7803bbd1187559eaeb3fafde977d817(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b56cfc4a694dfb959ddf09af688e179467f18ec0fddf65ec05515bc26b8c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae66e2ff0217b284e5b8362ee03fa0079447b8a7621d4016476379ea65ea8dde(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aad999bccb1c4107137d3233c677fb5b3150dfdf59ef88150eceadaa9e97395(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e3de32b0e747505815529745fbc8277051812b6eb1332c657db9e5ee8fcfe7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c457b0baf901178d0b8ee13a1cea61002553f4d82bbef287df7797fa5f0c64d(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersSuspendTaskAfterNumFailures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80557eeacdfb4906fed9d2b6004f0e39f32fb0c544507fa7f12840161a86c9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47688beca4022284818d1316ebc4d5a9b4da42b36e67a4e5ce7a97298badd065(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b713d5f092c2f22d9523a505b10ccdc3e6e95bad5e52d64b9e8a54462728bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22185d238ea25506afffc52ffeda99166ea4c137f420b78919d74c8fc7caea7f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05eaa48d44094461ee5bc18e5217a9f072768a33006750306a604f6be3e397c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d6d0c0c8239ec2230b58995d316cbea534261e182c35b947ba120206d016e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd62c81ce5d07e46eca33679e0f340cdfa1b94ef11ba572941ec72768b1d31a(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersTaskAutoRetryAttempts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befc5d70918adcb902168ec4f1748480392a2f310a59e506690a72f16cdb98d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2551e33f3e16eaf0c8dd0bb26ec1d8b45c4014a98960f928f7b2278c56b5d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61de037dd4138f84ef26263315cf93162f9eed7b554bbf91da067666018b7c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700f7db0cbdc226e129f48fc3308952ef8e8062a6cc08eacf871fcba24e3fec4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdf073686123ce8272d16b76e264384891641e6b91e2082e0f2559aec6fc1f35(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a69b5d8b9e72516df8adb2fda9e7b821077e86ea21357752711b41b6effaf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76efe09fcbfaa01dda03229e8ab816bccb938bc9d830bf29aa951d165d643909(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229974d0e1b46f393d98e639cc3cfb6d9c1aa1b41919771a4ff5871ef483fd18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9eb3aeedcc32c4cd66499f1374741ec6e642ab3a901a396578610ea7021bbb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c038c762788bb252de709690dc85fff66226139a5dbe7325e610da7318a0611c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0ff91fdd017ff8793de35046f85ea42fe68509328f44f7da3c58ca54ac5254(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574cbe89613d75f30704d17fd2d68543ab96fb8f2a06cdbd17e84b94e31ebcf6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad1a81ee7decaaf61f57ea4e1e3dd8a092adfa2cf91bfccdef771f88ee78a58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f0a63078bb0f1aee00e244f8c1899c6d16dcc9db67749751981a630be8abaf(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskManagedInitialWarehouseSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58b9635d3609a119bb19a859f42ecd6e9a7572f42c73c9d914c8c85b7284cf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12bd69b3d1abece13119e08b9fad53c10882eb57040296578a160724e4907454(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc095cc888d0b96287ce645ad4ffed818a9a4ad7c6bf0b7c698930efa2ff409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285ff532d2d28a6e61db95602a6254153d59da5d8057d06bb7caca5a49fe0c2d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e46cffdb282f8b5b561a4fe31bf844a63b6da7e837c3096c9391be55980ea1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25176bf0fb32b053d91ace3ae6cf095072d121d07101b6d23ddfd30525bdb17e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1747983c72e7aa132319a7c70287bd172cbcc921256b18f4676e5f326b5d0cc8(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskMinimumTriggerIntervalInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d6aec76324486a485819fd604de0ff91a4b8a17d6067cbab4692ccb2fa0615(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e920d8cfbb7805fa6784e42de8b11db32b319766ffe9c7b0117d025af01eb814(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18c566f6b9461be8ee884b01e8fd5313a29be9683788f7c66ce16f835c2e68a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a53e2031acd19c7ce19e183ed916be77010de236b7e6c1b0a072b0cbd9cd0cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f52dec8c69c9a9189d97f6379b098690325bf10c585bc483448088d3465e25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f40112a6c7b56556892bed0d35314f052c17c11d7b781f41f757109baf91f49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee40293b52b45db4609ef6ca9aab38eb13738c366d99ccb51b3a5cd4d63241c9(
    value: typing.Optional[DataSnowflakeSchemasSchemasParametersUserTaskTimeoutMs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49aff93902fa6213c2776fe802c8660b236229205084561806a9f014a8a77d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f47890f268bfd5fb0468eafa573ec9cb7abf10eddd49a41e8a74d558c28d934(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e529151138779e93455b74522b56c6dfed19934e50cd0ca2b529b722153560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb34e1612437960c58e82fc97a58e1b84e248f413156a199f6c908e96363a1ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8618d32569aaf4c5c00a99769e6faff5335de904fb412c7c5f34dc3119c024(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a4672f93a00abf998753edae6c298071dd77a03ddd4acb5216ae186eccd30c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2188e34b057dc84a346f6e1cde5fd4c2839ce1bedebe2e01555c266c9a6ec7(
    value: typing.Optional[DataSnowflakeSchemasSchemasShowOutput],
) -> None:
    """Type checking stubs"""
    pass
