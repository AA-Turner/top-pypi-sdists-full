r'''
# `snowflake_account_parameter`

Refer to the Terraform Registry for docs: [`snowflake_account_parameter`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter).
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


class AccountParameter(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.accountParameter.AccountParameter",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter snowflake_account_parameter}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key: builtins.str,
        value: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter snowflake_account_parameter} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key: Name of account parameter. Valid values are (case-insensitive): ``ALLOW_CLIENT_MFA_CACHING`` | ``ALLOW_ID_TOKEN`` | ``CLIENT_ENCRYPTION_KEY_SIZE`` | ``CORTEX_ENABLED_CROSS_REGION`` | ``ENABLE_IDENTIFIER_FIRST_LOGIN`` | ``ENABLE_INTERNAL_STAGES_PRIVATELINK`` | ``ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_IMAGE_REPOSITORY`` | ``ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_SPCS_BLOCK_STORAGE`` | ``ENABLE_UNHANDLED_EXCEPTIONS_REPORTING`` | ``ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES`` | ``EVENT_TABLE`` | ``EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST`` | ``INITIAL_REPLICATION_SIZE_LIMIT_IN_TB`` | ``MIN_DATA_RETENTION_TIME_IN_DAYS`` | ``NETWORK_POLICY`` | ``OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST`` | ``PERIODIC_DATA_REKEYING`` | ``PREVENT_LOAD_FROM_INLINE_URL`` | ``PREVENT_UNLOAD_TO_INLINE_URL`` | ``REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION`` | ``REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION`` | ``SSO_LOGIN_PAGE`` | ``ABORT_DETACHED_QUERY`` | ``ACTIVE_PYTHON_PROFILER`` | ``AUTOCOMMIT`` | ``BINARY_INPUT_FORMAT`` | ``BINARY_OUTPUT_FORMAT`` | ``CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS`` | ``CLIENT_MEMORY_LIMIT`` | ``CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX`` | ``CLIENT_METADATA_USE_SESSION_DATABASE`` | ``CLIENT_PREFETCH_THREADS`` | ``CLIENT_RESULT_CHUNK_SIZE`` | ``CLIENT_SESSION_KEEP_ALIVE`` | ``CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY`` | ``CLIENT_TIMESTAMP_TYPE_MAPPING`` | ``ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION`` | ``CLIENT_RESULT_COLUMN_CASE_INSENSITIVE`` | ``CSV_TIMESTAMP_FORMAT`` | ``DATE_INPUT_FORMAT`` | ``DATE_OUTPUT_FORMAT`` | ``ERROR_ON_NONDETERMINISTIC_MERGE`` | ``ERROR_ON_NONDETERMINISTIC_UPDATE`` | ``GEOGRAPHY_OUTPUT_FORMAT`` | ``GEOMETRY_OUTPUT_FORMAT`` | ``HYBRID_TABLE_LOCK_TIMEOUT`` | ``JDBC_TREAT_DECIMAL_AS_INT`` | ``JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC`` | ``JDBC_USE_SESSION_TIMEZONE`` | ``JSON_INDENT`` | ``JS_TREAT_INTEGER_AS_BIGINT`` | ``LOCK_TIMEOUT`` | ``MULTI_STATEMENT_COUNT`` | ``NOORDER_SEQUENCE_AS_DEFAULT`` | ``ODBC_TREAT_DECIMAL_AS_INT`` | ``PYTHON_PROFILER_MODULES`` | ``PYTHON_PROFILER_TARGET_STAGE`` | ``QUERY_TAG`` | ``QUOTED_IDENTIFIERS_IGNORE_CASE`` | ``ROWS_PER_RESULTSET`` | ``S3_STAGE_VPCE_DNS_NAME`` | ``SEARCH_PATH`` | ``SIMULATED_DATA_SHARING_CONSUMER`` | ``STATEMENT_TIMEOUT_IN_SECONDS`` | ``STRICT_JSON_OUTPUT`` | ``TIME_INPUT_FORMAT`` | ``TIME_OUTPUT_FORMAT`` | ``TIMESTAMP_DAY_IS_ALWAYS_24H`` | ``TIMESTAMP_INPUT_FORMAT`` | ``TIMESTAMP_LTZ_OUTPUT_FORMAT`` | ``TIMESTAMP_NTZ_OUTPUT_FORMAT`` | ``TIMESTAMP_OUTPUT_FORMAT`` | ``TIMESTAMP_TYPE_MAPPING`` | ``TIMESTAMP_TZ_OUTPUT_FORMAT`` | ``TIMEZONE`` | ``TRANSACTION_ABORT_ON_ERROR`` | ``TRANSACTION_DEFAULT_ISOLATION_LEVEL`` | ``TWO_DIGIT_CENTURY_START`` | ``UNSUPPORTED_DDL_ACTION`` | ``USE_CACHED_RESULT`` | ``WEEK_OF_YEAR_POLICY`` | ``WEEK_START`` | ``CATALOG`` | ``DATA_RETENTION_TIME_IN_DAYS`` | ``DEFAULT_DDL_COLLATION`` | ``EXTERNAL_VOLUME`` | ``LOG_LEVEL`` | ``MAX_CONCURRENCY_LEVEL`` | ``MAX_DATA_EXTENSION_TIME_IN_DAYS`` | ``PIPE_EXECUTION_PAUSED`` | ``PREVENT_UNLOAD_TO_INTERNAL_STAGES`` | ``REPLACE_INVALID_CHARACTERS`` | ``STATEMENT_QUEUED_TIMEOUT_IN_SECONDS`` | ``STORAGE_SERIALIZATION_POLICY`` | ``SHARE_RESTRICTIONS`` | ``SUSPEND_TASK_AFTER_NUM_FAILURES`` | ``TRACE_LEVEL`` | ``USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE`` | ``USER_TASK_TIMEOUT_MS`` | ``TASK_AUTO_RETRY_ATTEMPTS`` | ``USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS`` | ``METRIC_LEVEL`` | ``ENABLE_CONSOLE_OUTPUT`` | ``ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR`` | ``ENABLE_PERSONAL_DATABASE``. Deprecated parameters are not supported in the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#key AccountParameter#key}
        :param value: Value of account parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation. The parameter values are validated in Snowflake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#value AccountParameter#value}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#id AccountParameter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e1c8bcfc617dc9ee4c85210e2a8ddd077f7df278b9fc50e5127723a5300857)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccountParameterConfig(
            key=key,
            value=value,
            id=id,
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
        '''Generates CDKTF code for importing a AccountParameter resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccountParameter to import.
        :param import_from_id: The id of the existing AccountParameter that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccountParameter to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7d50df001ca735f739d13943f3e8429b237f22fcb084f836d727395318f738)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c170f9edc63ddf58b3d3a74edfab00be1a67171fce2c6e5e1f4c3d07f65897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758db68834df2babcbf8e60161f2654304518d311e4ff020b655aec1c1cc9ec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15fddce3705096ac8d3a07b1d1cbabe3b99f5e8a47b51f3556d5af22e600f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.accountParameter.AccountParameterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key": "key",
        "value": "value",
        "id": "id",
    },
)
class AccountParameterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key: builtins.str,
        value: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key: Name of account parameter. Valid values are (case-insensitive): ``ALLOW_CLIENT_MFA_CACHING`` | ``ALLOW_ID_TOKEN`` | ``CLIENT_ENCRYPTION_KEY_SIZE`` | ``CORTEX_ENABLED_CROSS_REGION`` | ``ENABLE_IDENTIFIER_FIRST_LOGIN`` | ``ENABLE_INTERNAL_STAGES_PRIVATELINK`` | ``ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_IMAGE_REPOSITORY`` | ``ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_SPCS_BLOCK_STORAGE`` | ``ENABLE_UNHANDLED_EXCEPTIONS_REPORTING`` | ``ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES`` | ``EVENT_TABLE`` | ``EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST`` | ``INITIAL_REPLICATION_SIZE_LIMIT_IN_TB`` | ``MIN_DATA_RETENTION_TIME_IN_DAYS`` | ``NETWORK_POLICY`` | ``OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST`` | ``PERIODIC_DATA_REKEYING`` | ``PREVENT_LOAD_FROM_INLINE_URL`` | ``PREVENT_UNLOAD_TO_INLINE_URL`` | ``REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION`` | ``REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION`` | ``SSO_LOGIN_PAGE`` | ``ABORT_DETACHED_QUERY`` | ``ACTIVE_PYTHON_PROFILER`` | ``AUTOCOMMIT`` | ``BINARY_INPUT_FORMAT`` | ``BINARY_OUTPUT_FORMAT`` | ``CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS`` | ``CLIENT_MEMORY_LIMIT`` | ``CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX`` | ``CLIENT_METADATA_USE_SESSION_DATABASE`` | ``CLIENT_PREFETCH_THREADS`` | ``CLIENT_RESULT_CHUNK_SIZE`` | ``CLIENT_SESSION_KEEP_ALIVE`` | ``CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY`` | ``CLIENT_TIMESTAMP_TYPE_MAPPING`` | ``ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION`` | ``CLIENT_RESULT_COLUMN_CASE_INSENSITIVE`` | ``CSV_TIMESTAMP_FORMAT`` | ``DATE_INPUT_FORMAT`` | ``DATE_OUTPUT_FORMAT`` | ``ERROR_ON_NONDETERMINISTIC_MERGE`` | ``ERROR_ON_NONDETERMINISTIC_UPDATE`` | ``GEOGRAPHY_OUTPUT_FORMAT`` | ``GEOMETRY_OUTPUT_FORMAT`` | ``HYBRID_TABLE_LOCK_TIMEOUT`` | ``JDBC_TREAT_DECIMAL_AS_INT`` | ``JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC`` | ``JDBC_USE_SESSION_TIMEZONE`` | ``JSON_INDENT`` | ``JS_TREAT_INTEGER_AS_BIGINT`` | ``LOCK_TIMEOUT`` | ``MULTI_STATEMENT_COUNT`` | ``NOORDER_SEQUENCE_AS_DEFAULT`` | ``ODBC_TREAT_DECIMAL_AS_INT`` | ``PYTHON_PROFILER_MODULES`` | ``PYTHON_PROFILER_TARGET_STAGE`` | ``QUERY_TAG`` | ``QUOTED_IDENTIFIERS_IGNORE_CASE`` | ``ROWS_PER_RESULTSET`` | ``S3_STAGE_VPCE_DNS_NAME`` | ``SEARCH_PATH`` | ``SIMULATED_DATA_SHARING_CONSUMER`` | ``STATEMENT_TIMEOUT_IN_SECONDS`` | ``STRICT_JSON_OUTPUT`` | ``TIME_INPUT_FORMAT`` | ``TIME_OUTPUT_FORMAT`` | ``TIMESTAMP_DAY_IS_ALWAYS_24H`` | ``TIMESTAMP_INPUT_FORMAT`` | ``TIMESTAMP_LTZ_OUTPUT_FORMAT`` | ``TIMESTAMP_NTZ_OUTPUT_FORMAT`` | ``TIMESTAMP_OUTPUT_FORMAT`` | ``TIMESTAMP_TYPE_MAPPING`` | ``TIMESTAMP_TZ_OUTPUT_FORMAT`` | ``TIMEZONE`` | ``TRANSACTION_ABORT_ON_ERROR`` | ``TRANSACTION_DEFAULT_ISOLATION_LEVEL`` | ``TWO_DIGIT_CENTURY_START`` | ``UNSUPPORTED_DDL_ACTION`` | ``USE_CACHED_RESULT`` | ``WEEK_OF_YEAR_POLICY`` | ``WEEK_START`` | ``CATALOG`` | ``DATA_RETENTION_TIME_IN_DAYS`` | ``DEFAULT_DDL_COLLATION`` | ``EXTERNAL_VOLUME`` | ``LOG_LEVEL`` | ``MAX_CONCURRENCY_LEVEL`` | ``MAX_DATA_EXTENSION_TIME_IN_DAYS`` | ``PIPE_EXECUTION_PAUSED`` | ``PREVENT_UNLOAD_TO_INTERNAL_STAGES`` | ``REPLACE_INVALID_CHARACTERS`` | ``STATEMENT_QUEUED_TIMEOUT_IN_SECONDS`` | ``STORAGE_SERIALIZATION_POLICY`` | ``SHARE_RESTRICTIONS`` | ``SUSPEND_TASK_AFTER_NUM_FAILURES`` | ``TRACE_LEVEL`` | ``USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE`` | ``USER_TASK_TIMEOUT_MS`` | ``TASK_AUTO_RETRY_ATTEMPTS`` | ``USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS`` | ``METRIC_LEVEL`` | ``ENABLE_CONSOLE_OUTPUT`` | ``ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR`` | ``ENABLE_PERSONAL_DATABASE``. Deprecated parameters are not supported in the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#key AccountParameter#key}
        :param value: Value of account parameter, as a string. Constraints are the same as those for the parameters in Snowflake documentation. The parameter values are validated in Snowflake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#value AccountParameter#value}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#id AccountParameter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f30368a2decefeef326c84acef3b1f38dc36402249a428320a3a17a06b78fd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
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
    def key(self) -> builtins.str:
        '''Name of account parameter.

        Valid values are (case-insensitive): ``ALLOW_CLIENT_MFA_CACHING`` | ``ALLOW_ID_TOKEN`` | ``CLIENT_ENCRYPTION_KEY_SIZE`` | ``CORTEX_ENABLED_CROSS_REGION`` | ``ENABLE_IDENTIFIER_FIRST_LOGIN`` | ``ENABLE_INTERNAL_STAGES_PRIVATELINK`` | ``ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_IMAGE_REPOSITORY`` | ``ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_SPCS_BLOCK_STORAGE`` | ``ENABLE_UNHANDLED_EXCEPTIONS_REPORTING`` | ``ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES`` | ``EVENT_TABLE`` | ``EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST`` | ``INITIAL_REPLICATION_SIZE_LIMIT_IN_TB`` | ``MIN_DATA_RETENTION_TIME_IN_DAYS`` | ``NETWORK_POLICY`` | ``OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST`` | ``PERIODIC_DATA_REKEYING`` | ``PREVENT_LOAD_FROM_INLINE_URL`` | ``PREVENT_UNLOAD_TO_INLINE_URL`` | ``REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION`` | ``REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION`` | ``SSO_LOGIN_PAGE`` | ``ABORT_DETACHED_QUERY`` | ``ACTIVE_PYTHON_PROFILER`` | ``AUTOCOMMIT`` | ``BINARY_INPUT_FORMAT`` | ``BINARY_OUTPUT_FORMAT`` | ``CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS`` | ``CLIENT_MEMORY_LIMIT`` | ``CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX`` | ``CLIENT_METADATA_USE_SESSION_DATABASE`` | ``CLIENT_PREFETCH_THREADS`` | ``CLIENT_RESULT_CHUNK_SIZE`` | ``CLIENT_SESSION_KEEP_ALIVE`` | ``CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY`` | ``CLIENT_TIMESTAMP_TYPE_MAPPING`` | ``ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION`` | ``CLIENT_RESULT_COLUMN_CASE_INSENSITIVE`` | ``CSV_TIMESTAMP_FORMAT`` | ``DATE_INPUT_FORMAT`` | ``DATE_OUTPUT_FORMAT`` | ``ERROR_ON_NONDETERMINISTIC_MERGE`` | ``ERROR_ON_NONDETERMINISTIC_UPDATE`` | ``GEOGRAPHY_OUTPUT_FORMAT`` | ``GEOMETRY_OUTPUT_FORMAT`` | ``HYBRID_TABLE_LOCK_TIMEOUT`` | ``JDBC_TREAT_DECIMAL_AS_INT`` | ``JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC`` | ``JDBC_USE_SESSION_TIMEZONE`` | ``JSON_INDENT`` | ``JS_TREAT_INTEGER_AS_BIGINT`` | ``LOCK_TIMEOUT`` | ``MULTI_STATEMENT_COUNT`` | ``NOORDER_SEQUENCE_AS_DEFAULT`` | ``ODBC_TREAT_DECIMAL_AS_INT`` | ``PYTHON_PROFILER_MODULES`` | ``PYTHON_PROFILER_TARGET_STAGE`` | ``QUERY_TAG`` | ``QUOTED_IDENTIFIERS_IGNORE_CASE`` | ``ROWS_PER_RESULTSET`` | ``S3_STAGE_VPCE_DNS_NAME`` | ``SEARCH_PATH`` | ``SIMULATED_DATA_SHARING_CONSUMER`` | ``STATEMENT_TIMEOUT_IN_SECONDS`` | ``STRICT_JSON_OUTPUT`` | ``TIME_INPUT_FORMAT`` | ``TIME_OUTPUT_FORMAT`` | ``TIMESTAMP_DAY_IS_ALWAYS_24H`` | ``TIMESTAMP_INPUT_FORMAT`` | ``TIMESTAMP_LTZ_OUTPUT_FORMAT`` | ``TIMESTAMP_NTZ_OUTPUT_FORMAT`` | ``TIMESTAMP_OUTPUT_FORMAT`` | ``TIMESTAMP_TYPE_MAPPING`` | ``TIMESTAMP_TZ_OUTPUT_FORMAT`` | ``TIMEZONE`` | ``TRANSACTION_ABORT_ON_ERROR`` | ``TRANSACTION_DEFAULT_ISOLATION_LEVEL`` | ``TWO_DIGIT_CENTURY_START`` | ``UNSUPPORTED_DDL_ACTION`` | ``USE_CACHED_RESULT`` | ``WEEK_OF_YEAR_POLICY`` | ``WEEK_START`` | ``CATALOG`` | ``DATA_RETENTION_TIME_IN_DAYS`` | ``DEFAULT_DDL_COLLATION`` | ``EXTERNAL_VOLUME`` | ``LOG_LEVEL`` | ``MAX_CONCURRENCY_LEVEL`` | ``MAX_DATA_EXTENSION_TIME_IN_DAYS`` | ``PIPE_EXECUTION_PAUSED`` | ``PREVENT_UNLOAD_TO_INTERNAL_STAGES`` | ``REPLACE_INVALID_CHARACTERS`` | ``STATEMENT_QUEUED_TIMEOUT_IN_SECONDS`` | ``STORAGE_SERIALIZATION_POLICY`` | ``SHARE_RESTRICTIONS`` | ``SUSPEND_TASK_AFTER_NUM_FAILURES`` | ``TRACE_LEVEL`` | ``USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE`` | ``USER_TASK_TIMEOUT_MS`` | ``TASK_AUTO_RETRY_ATTEMPTS`` | ``USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS`` | ``METRIC_LEVEL`` | ``ENABLE_CONSOLE_OUTPUT`` | ``ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR`` | ``ENABLE_PERSONAL_DATABASE``. Deprecated parameters are not supported in the provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#key AccountParameter#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of account parameter, as a string.

        Constraints are the same as those for the parameters in Snowflake documentation. The parameter values are validated in Snowflake.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#value AccountParameter#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/account_parameter#id AccountParameter#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountParameterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccountParameter",
    "AccountParameterConfig",
]

publication.publish()

def _typecheckingstub__34e1c8bcfc617dc9ee4c85210e2a8ddd077f7df278b9fc50e5127723a5300857(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key: builtins.str,
    value: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__fa7d50df001ca735f739d13943f3e8429b237f22fcb084f836d727395318f738(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c170f9edc63ddf58b3d3a74edfab00be1a67171fce2c6e5e1f4c3d07f65897(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758db68834df2babcbf8e60161f2654304518d311e4ff020b655aec1c1cc9ec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15fddce3705096ac8d3a07b1d1cbabe3b99f5e8a47b51f3556d5af22e600f31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f30368a2decefeef326c84acef3b1f38dc36402249a428320a3a17a06b78fd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: builtins.str,
    value: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
