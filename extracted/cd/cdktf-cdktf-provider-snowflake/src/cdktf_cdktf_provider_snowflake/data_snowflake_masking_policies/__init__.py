r'''
# `data_snowflake_masking_policies`

Refer to the Terraform Registry for docs: [`data_snowflake_masking_policies`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies).
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


class DataSnowflakeMaskingPolicies(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPolicies",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies snowflake_masking_policies}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        in_: typing.Optional[typing.Union["DataSnowflakeMaskingPoliciesIn", typing.Dict[builtins.str, typing.Any]]] = None,
        like: typing.Optional[builtins.str] = None,
        limit: typing.Optional[typing.Union["DataSnowflakeMaskingPoliciesLimit", typing.Dict[builtins.str, typing.Any]]] = None,
        with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies snowflake_masking_policies} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#id DataSnowflakeMaskingPolicies#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_: in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#in DataSnowflakeMaskingPolicies#in}
        :param like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#like DataSnowflakeMaskingPolicies#like}
        :param limit: limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#limit DataSnowflakeMaskingPolicies#limit}
        :param with_describe: Runs DESC MASKING POLICY for each masking policy returned by SHOW MASKING POLICIES. The output of describe is saved to the description field. By default this value is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#with_describe DataSnowflakeMaskingPolicies#with_describe}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e658bc06274a818821e98bbfed314b4e3fef98e94f5c1fd96d6d723c6d6a41e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataSnowflakeMaskingPoliciesConfig(
            id=id,
            in_=in_,
            like=like,
            limit=limit,
            with_describe=with_describe,
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
        '''Generates CDKTF code for importing a DataSnowflakeMaskingPolicies resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataSnowflakeMaskingPolicies to import.
        :param import_from_id: The id of the existing DataSnowflakeMaskingPolicies that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataSnowflakeMaskingPolicies to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18069110b5713112c684611c01faef0ea3c5de829812b9abeb02d68cae01795d)
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
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: Returns records for the entire account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#account DataSnowflakeMaskingPolicies#account}
        :param application: Returns records for the specified application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#application DataSnowflakeMaskingPolicies#application}
        :param application_package: Returns records for the specified application package. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#application_package DataSnowflakeMaskingPolicies#application_package}
        :param database: Returns records for the current database in use or for a specified database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#database DataSnowflakeMaskingPolicies#database}
        :param schema: Returns records for the current schema in use or a specified schema. Use fully qualified name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#schema DataSnowflakeMaskingPolicies#schema}
        '''
        value = DataSnowflakeMaskingPoliciesIn(
            account=account,
            application=application,
            application_package=application_package,
            database=database,
            schema=schema,
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
        :param rows: The maximum number of rows to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#rows DataSnowflakeMaskingPolicies#rows}
        :param from_: Specifies a **case-sensitive** pattern that is used to match object name. After the first match, the limit on the number of rows will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#from DataSnowflakeMaskingPolicies#from}
        '''
        value = DataSnowflakeMaskingPoliciesLimit(rows=rows, from_=from_)

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

    @jsii.member(jsii_name="resetWithDescribe")
    def reset_with_describe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithDescribe", []))

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
    def in_(self) -> "DataSnowflakeMaskingPoliciesInOutputReference":
        return typing.cast("DataSnowflakeMaskingPoliciesInOutputReference", jsii.get(self, "in"))

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> "DataSnowflakeMaskingPoliciesLimitOutputReference":
        return typing.cast("DataSnowflakeMaskingPoliciesLimitOutputReference", jsii.get(self, "limit"))

    @builtins.property
    @jsii.member(jsii_name="maskingPolicies")
    def masking_policies(self) -> "DataSnowflakeMaskingPoliciesMaskingPoliciesList":
        return typing.cast("DataSnowflakeMaskingPoliciesMaskingPoliciesList", jsii.get(self, "maskingPolicies"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inInput")
    def in_input(self) -> typing.Optional["DataSnowflakeMaskingPoliciesIn"]:
        return typing.cast(typing.Optional["DataSnowflakeMaskingPoliciesIn"], jsii.get(self, "inInput"))

    @builtins.property
    @jsii.member(jsii_name="likeInput")
    def like_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "likeInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional["DataSnowflakeMaskingPoliciesLimit"]:
        return typing.cast(typing.Optional["DataSnowflakeMaskingPoliciesLimit"], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="withDescribeInput")
    def with_describe_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withDescribeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f929e03b013649a4323e7dbe294f82bc76759e3b5e8b97a5b526bc59254fff51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="like")
    def like(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "like"))

    @like.setter
    def like(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a50c22f54824c8b9bbe9caed8bc7012eee3615511d726c8a37ce2078dc6b3fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "like", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__9b1422d8cab95ddb5f5f3a5397d472bf8d11088f97f3b0df65bcfa93196310ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withDescribe", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesConfig",
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
        "with_describe": "withDescribe",
    },
)
class DataSnowflakeMaskingPoliciesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        in_: typing.Optional[typing.Union["DataSnowflakeMaskingPoliciesIn", typing.Dict[builtins.str, typing.Any]]] = None,
        like: typing.Optional[builtins.str] = None,
        limit: typing.Optional[typing.Union["DataSnowflakeMaskingPoliciesLimit", typing.Dict[builtins.str, typing.Any]]] = None,
        with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#id DataSnowflakeMaskingPolicies#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param in_: in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#in DataSnowflakeMaskingPolicies#in}
        :param like: Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#like DataSnowflakeMaskingPolicies#like}
        :param limit: limit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#limit DataSnowflakeMaskingPolicies#limit}
        :param with_describe: Runs DESC MASKING POLICY for each masking policy returned by SHOW MASKING POLICIES. The output of describe is saved to the description field. By default this value is set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#with_describe DataSnowflakeMaskingPolicies#with_describe}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(in_, dict):
            in_ = DataSnowflakeMaskingPoliciesIn(**in_)
        if isinstance(limit, dict):
            limit = DataSnowflakeMaskingPoliciesLimit(**limit)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9880836cff2e0b8a96c44d0926200e5b94ef5e9e8b4f1d3b7f915fe203247409)
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
            check_type(argname="argument with_describe", value=with_describe, expected_type=type_hints["with_describe"])
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
        if with_describe is not None:
            self._values["with_describe"] = with_describe

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#id DataSnowflakeMaskingPolicies#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_(self) -> typing.Optional["DataSnowflakeMaskingPoliciesIn"]:
        '''in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#in DataSnowflakeMaskingPolicies#in}
        '''
        result = self._values.get("in_")
        return typing.cast(typing.Optional["DataSnowflakeMaskingPoliciesIn"], result)

    @builtins.property
    def like(self) -> typing.Optional[builtins.str]:
        '''Filters the output with **case-insensitive** pattern, with support for SQL wildcard characters (``%`` and ``_``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#like DataSnowflakeMaskingPolicies#like}
        '''
        result = self._values.get("like")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit(self) -> typing.Optional["DataSnowflakeMaskingPoliciesLimit"]:
        '''limit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#limit DataSnowflakeMaskingPolicies#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional["DataSnowflakeMaskingPoliciesLimit"], result)

    @builtins.property
    def with_describe(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runs DESC MASKING POLICY for each masking policy returned by SHOW MASKING POLICIES.

        The output of describe is saved to the description field. By default this value is set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#with_describe DataSnowflakeMaskingPolicies#with_describe}
        '''
        result = self._values.get("with_describe")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeMaskingPoliciesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesIn",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "application": "application",
        "application_package": "applicationPackage",
        "database": "database",
        "schema": "schema",
    },
)
class DataSnowflakeMaskingPoliciesIn:
    def __init__(
        self,
        *,
        account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        application: typing.Optional[builtins.str] = None,
        application_package: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: Returns records for the entire account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#account DataSnowflakeMaskingPolicies#account}
        :param application: Returns records for the specified application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#application DataSnowflakeMaskingPolicies#application}
        :param application_package: Returns records for the specified application package. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#application_package DataSnowflakeMaskingPolicies#application_package}
        :param database: Returns records for the current database in use or for a specified database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#database DataSnowflakeMaskingPolicies#database}
        :param schema: Returns records for the current schema in use or a specified schema. Use fully qualified name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#schema DataSnowflakeMaskingPolicies#schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bc5b8bde8731b5e812f35a2c684cd59e60d9e00689f4cc566a2657d45978dc)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument application_package", value=application_package, expected_type=type_hints["application_package"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if application is not None:
            self._values["application"] = application
        if application_package is not None:
            self._values["application_package"] = application_package
        if database is not None:
            self._values["database"] = database
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def account(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Returns records for the entire account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#account DataSnowflakeMaskingPolicies#account}
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def application(self) -> typing.Optional[builtins.str]:
        '''Returns records for the specified application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#application DataSnowflakeMaskingPolicies#application}
        '''
        result = self._values.get("application")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_package(self) -> typing.Optional[builtins.str]:
        '''Returns records for the specified application package.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#application_package DataSnowflakeMaskingPolicies#application_package}
        '''
        result = self._values.get("application_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Returns records for the current database in use or for a specified database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#database DataSnowflakeMaskingPolicies#database}
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Returns records for the current schema in use or a specified schema. Use fully qualified name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#schema DataSnowflakeMaskingPolicies#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeMaskingPoliciesIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeMaskingPoliciesInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78230646f17d9ab08b9857886f2e2133d8e68985966a37df92f39a29e9b3fc2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39339aad841cd29082d867a57536115eec66bbebb0c6456bbc5789530e28d521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "account", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @application.setter
    def application(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eda486744199d6567ab1f7c60cbea4da0b2a4b77e7218bf80f64364e450c102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "application", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationPackage")
    def application_package(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationPackage"))

    @application_package.setter
    def application_package(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5898b1c24cdca37363f1af7e983fbc993ec57c4beff6d3c0f8f4552f3b3b35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationPackage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2702b8dedfa84de88e19acf525dac5b883701018c47055185a0dbf1ac8c5e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb53032a4c64fba0cff194261286e0b100eef1382b853f0ec2437da7861e79d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeMaskingPoliciesIn]:
        return typing.cast(typing.Optional[DataSnowflakeMaskingPoliciesIn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeMaskingPoliciesIn],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ae08581cc060441555f87a80f822b6a015b20a66692b5b01442be8ab333fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesLimit",
    jsii_struct_bases=[],
    name_mapping={"rows": "rows", "from_": "from"},
)
class DataSnowflakeMaskingPoliciesLimit:
    def __init__(
        self,
        *,
        rows: jsii.Number,
        from_: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rows: The maximum number of rows to return. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#rows DataSnowflakeMaskingPolicies#rows}
        :param from_: Specifies a **case-sensitive** pattern that is used to match object name. After the first match, the limit on the number of rows will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#from DataSnowflakeMaskingPolicies#from}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e56a342c0b92f1854690b25501c959ba035ffc5731e68205c100a8902464c4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#rows DataSnowflakeMaskingPolicies#rows}
        '''
        result = self._values.get("rows")
        assert result is not None, "Required property 'rows' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def from_(self) -> typing.Optional[builtins.str]:
        '''Specifies a **case-sensitive** pattern that is used to match object name.

        After the first match, the limit on the number of rows will be applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/data-sources/masking_policies#from DataSnowflakeMaskingPolicies#from}
        '''
        result = self._values.get("from_")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeMaskingPoliciesLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeMaskingPoliciesLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8c96391245b7bed6709fc32f964a3cde9447a80187d90e1f365a2a024d5f7ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbc489fd5f98e3aabe0718079fc54d28c0943c7d38433d53bf8742452e575e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "from", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rows")
    def rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rows"))

    @rows.setter
    def rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e471d9d9d16ed500235a713ccbaf18deb2da5b836eed533548852c17d649709e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataSnowflakeMaskingPoliciesLimit]:
        return typing.cast(typing.Optional[DataSnowflakeMaskingPoliciesLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeMaskingPoliciesLimit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628df38ef2109c30634074aec5aee9018667d2932df3d5adbc3da3c89dd8ee24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPolicies",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeMaskingPoliciesMaskingPolicies:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeMaskingPoliciesMaskingPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3422c863f93854da59eb901a2a735848096c51af88c6147e00b071afb223f176)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346f0b5c04850f17951c22b624bd98aa2c6ac289968887030feac07bb6663850)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2331a002a6c6f9ff49bd45e45fcb7a083a715e53393d39adc93a57169dbe2725)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23e05efd75400ed2562ae2de356ca7ac9ea112584b48b26645b9a32e8d231f48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__642a6c2151fccb4a7636948dcdcbd671e6ca3f345ab4761d7b68a2b92df4107f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__053b0af5d8af2c8c78baebd007f705cf052beb18c5db47b005049d17a2966554)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @builtins.property
    @jsii.member(jsii_name="signature")
    def signature(
        self,
    ) -> "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureList":
        return typing.cast("DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureList", jsii.get(self, "signature"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutput]:
        return typing.cast(typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44856c432044a705ad6421ebf5df72044b196ed15c78bf6e621079bc4520b49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignature",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignature:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignature(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e21822139b3bc29ac2ef330d9b40f8a9b09b9c6f3690676395ef96687455ceb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e412aa4522568bbc97ad58773d9d584a35a31b07059a0ca390578ff1a509bdcd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5e4970e9049a3eebf424e26570d010e5cabc199fff1779652fabb16544da61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c998540372424f21c5e9bc9038acf35099e1484dbd9c828833c588416a74661a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcc41fab1079e16f123751174ed119601b1936e3cf7972e764ace7332bc5938c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d56a57d742ea202521734703d25a8d1889de74829f2fecda946f471e04ce074)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignature]:
        return typing.cast(typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignature], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignature],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f863ee42577f9c377c0d64bdf7fcb29a6865a5890e59a4696fc94f32880e0e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeMaskingPoliciesMaskingPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e3cde1666b58c0bb27c58ae3488669f956f98ce86dec26c299a5c1b883f8b61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeMaskingPoliciesMaskingPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792ca10860b14ba84fc6e139eb6c6b8437e019e11aaa8d0836d1cd516ee3bc6b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeMaskingPoliciesMaskingPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666feb6c3cb19d205314b6be339bae12ea48659c33c8fff71f65b136a5452181)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b667cab393f4f79b85a75eae72b26eae3b637f41d0d9f3b867c5fede36d3221)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60d8d230c8f91d2b1db0392060ab22a255bf9996c072e874c857819a4fc8882b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeMaskingPoliciesMaskingPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a4a27a6e3bef42012f995b0b3d1375682a124ceeebb5509e5cede718aaa8a8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="describeOutput")
    def describe_output(
        self,
    ) -> DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputList:
        return typing.cast(DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputList, jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(
        self,
    ) -> "DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputList":
        return typing.cast("DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeMaskingPoliciesMaskingPolicies]:
        return typing.cast(typing.Optional[DataSnowflakeMaskingPoliciesMaskingPolicies], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeMaskingPoliciesMaskingPolicies],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e684eb64c7c2c5a3b8d1c849641013fa110821881fa7bb537909acb2f7acc34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81a9da36a5ce3c6d29329e3074de59e3eba5a86a407f6bdf41686024e7a1d19d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b963b8869d2084918a1f86af7663e8d58a6e5d488a15e0d2794a95376c2fd0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c91c4806255083bfc36cd85003abef37db6c0c332bda17b2191671ee8cbab0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae491efb1b2bce4be9c994f71285634e9226a661b0f51f3e46b6048df232ffdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b9913ed2a1ecd768ef02a2eec1536ca112ddb27b6bab266c201849182ea7416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.dataSnowflakeMaskingPolicies.DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4c12100c49a1361330c90d3467fea895850fe00430d53e8659a6ce253c211ea)
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
    @jsii.member(jsii_name="exemptOtherPolicies")
    def exempt_other_policies(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "exemptOtherPolicies"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

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
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutput]:
        return typing.cast(typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c441d09aca7da03f86ec02f3c4198a8f4b92483b06b184941c508f32e7bdfe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataSnowflakeMaskingPolicies",
    "DataSnowflakeMaskingPoliciesConfig",
    "DataSnowflakeMaskingPoliciesIn",
    "DataSnowflakeMaskingPoliciesInOutputReference",
    "DataSnowflakeMaskingPoliciesLimit",
    "DataSnowflakeMaskingPoliciesLimitOutputReference",
    "DataSnowflakeMaskingPoliciesMaskingPolicies",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutput",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputList",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputOutputReference",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignature",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureList",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignatureOutputReference",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesList",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesOutputReference",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutput",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputList",
    "DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__e658bc06274a818821e98bbfed314b4e3fef98e94f5c1fd96d6d723c6d6a41e8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    in_: typing.Optional[typing.Union[DataSnowflakeMaskingPoliciesIn, typing.Dict[builtins.str, typing.Any]]] = None,
    like: typing.Optional[builtins.str] = None,
    limit: typing.Optional[typing.Union[DataSnowflakeMaskingPoliciesLimit, typing.Dict[builtins.str, typing.Any]]] = None,
    with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__18069110b5713112c684611c01faef0ea3c5de829812b9abeb02d68cae01795d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f929e03b013649a4323e7dbe294f82bc76759e3b5e8b97a5b526bc59254fff51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50c22f54824c8b9bbe9caed8bc7012eee3615511d726c8a37ce2078dc6b3fdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1422d8cab95ddb5f5f3a5397d472bf8d11088f97f3b0df65bcfa93196310ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9880836cff2e0b8a96c44d0926200e5b94ef5e9e8b4f1d3b7f915fe203247409(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    in_: typing.Optional[typing.Union[DataSnowflakeMaskingPoliciesIn, typing.Dict[builtins.str, typing.Any]]] = None,
    like: typing.Optional[builtins.str] = None,
    limit: typing.Optional[typing.Union[DataSnowflakeMaskingPoliciesLimit, typing.Dict[builtins.str, typing.Any]]] = None,
    with_describe: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bc5b8bde8731b5e812f35a2c684cd59e60d9e00689f4cc566a2657d45978dc(
    *,
    account: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    application: typing.Optional[builtins.str] = None,
    application_package: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78230646f17d9ab08b9857886f2e2133d8e68985966a37df92f39a29e9b3fc2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39339aad841cd29082d867a57536115eec66bbebb0c6456bbc5789530e28d521(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eda486744199d6567ab1f7c60cbea4da0b2a4b77e7218bf80f64364e450c102(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5898b1c24cdca37363f1af7e983fbc993ec57c4beff6d3c0f8f4552f3b3b35f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2702b8dedfa84de88e19acf525dac5b883701018c47055185a0dbf1ac8c5e39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb53032a4c64fba0cff194261286e0b100eef1382b853f0ec2437da7861e79d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ae08581cc060441555f87a80f822b6a015b20a66692b5b01442be8ab333fd0(
    value: typing.Optional[DataSnowflakeMaskingPoliciesIn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e56a342c0b92f1854690b25501c959ba035ffc5731e68205c100a8902464c4(
    *,
    rows: jsii.Number,
    from_: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c96391245b7bed6709fc32f964a3cde9447a80187d90e1f365a2a024d5f7ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc489fd5f98e3aabe0718079fc54d28c0943c7d38433d53bf8742452e575e55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e471d9d9d16ed500235a713ccbaf18deb2da5b836eed533548852c17d649709e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628df38ef2109c30634074aec5aee9018667d2932df3d5adbc3da3c89dd8ee24(
    value: typing.Optional[DataSnowflakeMaskingPoliciesLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3422c863f93854da59eb901a2a735848096c51af88c6147e00b071afb223f176(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346f0b5c04850f17951c22b624bd98aa2c6ac289968887030feac07bb6663850(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2331a002a6c6f9ff49bd45e45fcb7a083a715e53393d39adc93a57169dbe2725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e05efd75400ed2562ae2de356ca7ac9ea112584b48b26645b9a32e8d231f48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642a6c2151fccb4a7636948dcdcbd671e6ca3f345ab4761d7b68a2b92df4107f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053b0af5d8af2c8c78baebd007f705cf052beb18c5db47b005049d17a2966554(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44856c432044a705ad6421ebf5df72044b196ed15c78bf6e621079bc4520b49(
    value: typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21822139b3bc29ac2ef330d9b40f8a9b09b9c6f3690676395ef96687455ceb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e412aa4522568bbc97ad58773d9d584a35a31b07059a0ca390578ff1a509bdcd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5e4970e9049a3eebf424e26570d010e5cabc199fff1779652fabb16544da61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c998540372424f21c5e9bc9038acf35099e1484dbd9c828833c588416a74661a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc41fab1079e16f123751174ed119601b1936e3cf7972e764ace7332bc5938c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d56a57d742ea202521734703d25a8d1889de74829f2fecda946f471e04ce074(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f863ee42577f9c377c0d64bdf7fcb29a6865a5890e59a4696fc94f32880e0e1(
    value: typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesDescribeOutputSignature],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3cde1666b58c0bb27c58ae3488669f956f98ce86dec26c299a5c1b883f8b61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792ca10860b14ba84fc6e139eb6c6b8437e019e11aaa8d0836d1cd516ee3bc6b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666feb6c3cb19d205314b6be339bae12ea48659c33c8fff71f65b136a5452181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b667cab393f4f79b85a75eae72b26eae3b637f41d0d9f3b867c5fede36d3221(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d8d230c8f91d2b1db0392060ab22a255bf9996c072e874c857819a4fc8882b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4a27a6e3bef42012f995b0b3d1375682a124ceeebb5509e5cede718aaa8a8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e684eb64c7c2c5a3b8d1c849641013fa110821881fa7bb537909acb2f7acc34(
    value: typing.Optional[DataSnowflakeMaskingPoliciesMaskingPolicies],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a9da36a5ce3c6d29329e3074de59e3eba5a86a407f6bdf41686024e7a1d19d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b963b8869d2084918a1f86af7663e8d58a6e5d488a15e0d2794a95376c2fd0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c91c4806255083bfc36cd85003abef37db6c0c332bda17b2191671ee8cbab0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae491efb1b2bce4be9c994f71285634e9226a661b0f51f3e46b6048df232ffdd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9913ed2a1ecd768ef02a2eec1536ca112ddb27b6bab266c201849182ea7416(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c12100c49a1361330c90d3467fea895850fe00430d53e8659a6ce253c211ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c441d09aca7da03f86ec02f3c4198a8f4b92483b06b184941c508f32e7bdfe5(
    value: typing.Optional[DataSnowflakeMaskingPoliciesMaskingPoliciesShowOutput],
) -> None:
    """Type checking stubs"""
    pass
