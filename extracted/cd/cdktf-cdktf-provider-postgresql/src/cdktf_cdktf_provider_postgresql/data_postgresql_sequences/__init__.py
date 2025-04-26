r'''
# `data_postgresql_sequences`

Refer to the Terraform Registry for docs: [`data_postgresql_sequences`](https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences).
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


class DataPostgresqlSequences(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-postgresql.dataPostgresqlSequences.DataPostgresqlSequences",
):
    '''Represents a {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences postgresql_sequences}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        id: typing.Optional[builtins.str] = None,
        like_all_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        like_any_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_like_all_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        regex_pattern: typing.Optional[builtins.str] = None,
        schemas: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences postgresql_sequences} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The PostgreSQL database which will be queried for sequence names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#database DataPostgresqlSequences#database}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#id DataPostgresqlSequences#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param like_all_patterns: Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL LIKE ALL operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#like_all_patterns DataPostgresqlSequences#like_all_patterns}
        :param like_any_patterns: Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL LIKE ANY operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#like_any_patterns DataPostgresqlSequences#like_any_patterns}
        :param not_like_all_patterns: Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL NOT LIKE ALL operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#not_like_all_patterns DataPostgresqlSequences#not_like_all_patterns}
        :param regex_pattern: Expression which will be pattern matched against sequence names in the query using the PostgreSQL ~ (regular expression match) operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#regex_pattern DataPostgresqlSequences#regex_pattern}
        :param schemas: The PostgreSQL schema(s) which will be queried for sequence names. Queries all schemas in the database by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#schemas DataPostgresqlSequences#schemas}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7692c5ecc27c55ac98f301112426cfcb219b134d38e5889345ccca5a83607ad1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataPostgresqlSequencesConfig(
            database=database,
            id=id,
            like_all_patterns=like_all_patterns,
            like_any_patterns=like_any_patterns,
            not_like_all_patterns=not_like_all_patterns,
            regex_pattern=regex_pattern,
            schemas=schemas,
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
        '''Generates CDKTF code for importing a DataPostgresqlSequences resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataPostgresqlSequences to import.
        :param import_from_id: The id of the existing DataPostgresqlSequences that should be imported. Refer to the {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataPostgresqlSequences to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ace9388a1f89438ea522ebcbba935be5e5aac684203812214cd6baa8d4b061e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLikeAllPatterns")
    def reset_like_all_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLikeAllPatterns", []))

    @jsii.member(jsii_name="resetLikeAnyPatterns")
    def reset_like_any_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLikeAnyPatterns", []))

    @jsii.member(jsii_name="resetNotLikeAllPatterns")
    def reset_not_like_all_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotLikeAllPatterns", []))

    @jsii.member(jsii_name="resetRegexPattern")
    def reset_regex_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegexPattern", []))

    @jsii.member(jsii_name="resetSchemas")
    def reset_schemas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemas", []))

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
    @jsii.member(jsii_name="sequences")
    def sequences(self) -> "DataPostgresqlSequencesSequencesList":
        return typing.cast("DataPostgresqlSequencesSequencesList", jsii.get(self, "sequences"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="likeAllPatternsInput")
    def like_all_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "likeAllPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="likeAnyPatternsInput")
    def like_any_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "likeAnyPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="notLikeAllPatternsInput")
    def not_like_all_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notLikeAllPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="regexPatternInput")
    def regex_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="schemasInput")
    def schemas_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "schemasInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0905445aabb6dcec8e5c7f60d798138c7223d70084e3b930fb39a5929abe9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4678104855c1cf310b787290f24f33ebcd60c8ec6f5f9dc11465f6de35c53a81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="likeAllPatterns")
    def like_all_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "likeAllPatterns"))

    @like_all_patterns.setter
    def like_all_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e41c708fb02f06f3d1c737d1a78de1767ab897243367046abc354702811e687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "likeAllPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="likeAnyPatterns")
    def like_any_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "likeAnyPatterns"))

    @like_any_patterns.setter
    def like_any_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e904fa063c345749407747cdfe996f36ac89a6cda7d65cb68dacf0cd11b55353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "likeAnyPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notLikeAllPatterns")
    def not_like_all_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notLikeAllPatterns"))

    @not_like_all_patterns.setter
    def not_like_all_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e96bab950b445b664d603157691caddeecbe012f70afd2b12d55c64a1ea78a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notLikeAllPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regexPattern")
    def regex_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regexPattern"))

    @regex_pattern.setter
    def regex_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83580b49b1826791ab1a5cd1293ac451a12e29deadce5796d8b4bf2115064c26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schemas")
    def schemas(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "schemas"))

    @schemas.setter
    def schemas(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c2fda4f1e58cff5f355052ecebd09180f336a8e5aae4ace0343c6378a764149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemas", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-postgresql.dataPostgresqlSequences.DataPostgresqlSequencesConfig",
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
        "id": "id",
        "like_all_patterns": "likeAllPatterns",
        "like_any_patterns": "likeAnyPatterns",
        "not_like_all_patterns": "notLikeAllPatterns",
        "regex_pattern": "regexPattern",
        "schemas": "schemas",
    },
)
class DataPostgresqlSequencesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: typing.Optional[builtins.str] = None,
        like_all_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        like_any_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_like_all_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        regex_pattern: typing.Optional[builtins.str] = None,
        schemas: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The PostgreSQL database which will be queried for sequence names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#database DataPostgresqlSequences#database}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#id DataPostgresqlSequences#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param like_all_patterns: Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL LIKE ALL operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#like_all_patterns DataPostgresqlSequences#like_all_patterns}
        :param like_any_patterns: Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL LIKE ANY operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#like_any_patterns DataPostgresqlSequences#like_any_patterns}
        :param not_like_all_patterns: Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL NOT LIKE ALL operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#not_like_all_patterns DataPostgresqlSequences#not_like_all_patterns}
        :param regex_pattern: Expression which will be pattern matched against sequence names in the query using the PostgreSQL ~ (regular expression match) operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#regex_pattern DataPostgresqlSequences#regex_pattern}
        :param schemas: The PostgreSQL schema(s) which will be queried for sequence names. Queries all schemas in the database by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#schemas DataPostgresqlSequences#schemas}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619e1c8023bf202cca3b151256dddd6d991091b7529ba0a0aa0e4adad84ecf35)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument like_all_patterns", value=like_all_patterns, expected_type=type_hints["like_all_patterns"])
            check_type(argname="argument like_any_patterns", value=like_any_patterns, expected_type=type_hints["like_any_patterns"])
            check_type(argname="argument not_like_all_patterns", value=not_like_all_patterns, expected_type=type_hints["not_like_all_patterns"])
            check_type(argname="argument regex_pattern", value=regex_pattern, expected_type=type_hints["regex_pattern"])
            check_type(argname="argument schemas", value=schemas, expected_type=type_hints["schemas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
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
        if id is not None:
            self._values["id"] = id
        if like_all_patterns is not None:
            self._values["like_all_patterns"] = like_all_patterns
        if like_any_patterns is not None:
            self._values["like_any_patterns"] = like_any_patterns
        if not_like_all_patterns is not None:
            self._values["not_like_all_patterns"] = not_like_all_patterns
        if regex_pattern is not None:
            self._values["regex_pattern"] = regex_pattern
        if schemas is not None:
            self._values["schemas"] = schemas

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
        '''The PostgreSQL database which will be queried for sequence names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#database DataPostgresqlSequences#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#id DataPostgresqlSequences#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def like_all_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL LIKE ALL operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#like_all_patterns DataPostgresqlSequences#like_all_patterns}
        '''
        result = self._values.get("like_all_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def like_any_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL LIKE ANY operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#like_any_patterns DataPostgresqlSequences#like_any_patterns}
        '''
        result = self._values.get("like_any_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_like_all_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Expression(s) which will be pattern matched against sequence names in the query using the PostgreSQL NOT LIKE ALL operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#not_like_all_patterns DataPostgresqlSequences#not_like_all_patterns}
        '''
        result = self._values.get("not_like_all_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def regex_pattern(self) -> typing.Optional[builtins.str]:
        '''Expression which will be pattern matched against sequence names in the query using the PostgreSQL ~ (regular expression match) operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#regex_pattern DataPostgresqlSequences#regex_pattern}
        '''
        result = self._values.get("regex_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schemas(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The PostgreSQL schema(s) which will be queried for sequence names. Queries all schemas in the database by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs/data-sources/sequences#schemas DataPostgresqlSequences#schemas}
        '''
        result = self._values.get("schemas")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPostgresqlSequencesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-postgresql.dataPostgresqlSequences.DataPostgresqlSequencesSequences",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataPostgresqlSequencesSequences:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPostgresqlSequencesSequences(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataPostgresqlSequencesSequencesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-postgresql.dataPostgresqlSequences.DataPostgresqlSequencesSequencesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce482489577c08d60dd5f2ca2444bcb8d7667541865e63dbf5af2ce98399558c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataPostgresqlSequencesSequencesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd90d5d2b55fd44a23f0ce260a0f974132e9129ce714b48b11b631665291030)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataPostgresqlSequencesSequencesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e7bccc4f031d84a92439de8213be594b8db31bdc1296b5b1b6ee526c91b5fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a43fe8e061dc91d33861117239149e45ffc429e9c215bcb9ffbd3a91246452b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e18e018fbe0d96f9d735ebb35e964d00fa4fa4a24c6ee63facd9a0fc9c97e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataPostgresqlSequencesSequencesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-postgresql.dataPostgresqlSequences.DataPostgresqlSequencesSequencesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf19ba9a0eac680172cdfe5b4d526ead57133f8139cdfd057d0e1535e638ffa5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @builtins.property
    @jsii.member(jsii_name="objectName")
    def object_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectName"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataPostgresqlSequencesSequences]:
        return typing.cast(typing.Optional[DataPostgresqlSequencesSequences], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPostgresqlSequencesSequences],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24768a99aa4e7aedecf3cfefef4cb1d93232d9a4c6d3bd0a72887cdd522a59c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataPostgresqlSequences",
    "DataPostgresqlSequencesConfig",
    "DataPostgresqlSequencesSequences",
    "DataPostgresqlSequencesSequencesList",
    "DataPostgresqlSequencesSequencesOutputReference",
]

publication.publish()

def _typecheckingstub__7692c5ecc27c55ac98f301112426cfcb219b134d38e5889345ccca5a83607ad1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    id: typing.Optional[builtins.str] = None,
    like_all_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    like_any_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_like_all_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    regex_pattern: typing.Optional[builtins.str] = None,
    schemas: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__0ace9388a1f89438ea522ebcbba935be5e5aac684203812214cd6baa8d4b061e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0905445aabb6dcec8e5c7f60d798138c7223d70084e3b930fb39a5929abe9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4678104855c1cf310b787290f24f33ebcd60c8ec6f5f9dc11465f6de35c53a81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e41c708fb02f06f3d1c737d1a78de1767ab897243367046abc354702811e687(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e904fa063c345749407747cdfe996f36ac89a6cda7d65cb68dacf0cd11b55353(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e96bab950b445b664d603157691caddeecbe012f70afd2b12d55c64a1ea78a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83580b49b1826791ab1a5cd1293ac451a12e29deadce5796d8b4bf2115064c26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2fda4f1e58cff5f355052ecebd09180f336a8e5aae4ace0343c6378a764149(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619e1c8023bf202cca3b151256dddd6d991091b7529ba0a0aa0e4adad84ecf35(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    id: typing.Optional[builtins.str] = None,
    like_all_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    like_any_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_like_all_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    regex_pattern: typing.Optional[builtins.str] = None,
    schemas: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce482489577c08d60dd5f2ca2444bcb8d7667541865e63dbf5af2ce98399558c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd90d5d2b55fd44a23f0ce260a0f974132e9129ce714b48b11b631665291030(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e7bccc4f031d84a92439de8213be594b8db31bdc1296b5b1b6ee526c91b5fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43fe8e061dc91d33861117239149e45ffc429e9c215bcb9ffbd3a91246452b3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e18e018fbe0d96f9d735ebb35e964d00fa4fa4a24c6ee63facd9a0fc9c97e02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf19ba9a0eac680172cdfe5b4d526ead57133f8139cdfd057d0e1535e638ffa5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24768a99aa4e7aedecf3cfefef4cb1d93232d9a4c6d3bd0a72887cdd522a59c(
    value: typing.Optional[DataPostgresqlSequencesSequences],
) -> None:
    """Type checking stubs"""
    pass
