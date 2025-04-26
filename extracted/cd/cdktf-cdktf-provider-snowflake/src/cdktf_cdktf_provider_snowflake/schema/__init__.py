r'''
# `snowflake_schema`

Refer to the Terraform Registry for docs: [`snowflake_schema`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema).
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


class Schema(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.Schema",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema snowflake_schema}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_volume: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_transient: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
        pipe_execution_paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_serialization_policy: typing.Optional[builtins.str] = None,
        suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
        task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
        trace_level: typing.Optional[builtins.str] = None,
        user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
        user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
        user_task_timeout_ms: typing.Optional[jsii.Number] = None,
        with_managed_access: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema snowflake_schema} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the schema. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#database Schema#database}
        :param name: Specifies the identifier for the schema; must be unique for the database in which the schema is created. When the name is ``PUBLIC``, during creation the provider checks if this schema has already been created and, in such case, ``ALTER`` is used to match the desired state. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#name Schema#name}
        :param catalog: The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#catalog Schema#catalog}
        :param comment: Specifies a comment for the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#comment Schema#comment}
        :param data_retention_time_in_days: Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database. For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#data_retention_time_in_days Schema#data_retention_time_in_days}
        :param default_ddl_collation: Specifies a default collation specification for all schemas and tables added to the database. It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#default_ddl_collation Schema#default_ddl_collation}
        :param enable_console_output: If true, enables stdout/stderr fast path logging for anonymous stored procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#enable_console_output Schema#enable_console_output}
        :param external_volume: The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#external_volume Schema#external_volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#id Schema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_transient: Specifies the schema as transient. Transient schemas do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#is_transient Schema#is_transient}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#log_level Schema#log_level}
        :param max_data_extension_time_in_days: Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale. For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#max_data_extension_time_in_days Schema#max_data_extension_time_in_days}
        :param pipe_execution_paused: Specifies whether to pause a running pipe, primarily in preparation for transferring ownership of the pipe to a different role. For more information, check `PIPE_EXECUTION_PAUSED docs <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#pipe_execution_paused Schema#pipe_execution_paused}
        :param quoted_identifiers_ignore_case: If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#quoted_identifiers_ignore_case Schema#quoted_identifiers_ignore_case}
        :param replace_invalid_characters: Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table. You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#replace_invalid_characters Schema#replace_invalid_characters}
        :param storage_serialization_policy: The storage serialization policy for Iceberg tables that use Snowflake as the catalog. Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#storage_serialization_policy Schema#storage_serialization_policy}
        :param suspend_task_after_num_failures: How many times a task must fail in a row before it is automatically suspended. 0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#suspend_task_after_num_failures Schema#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#task_auto_retry_attempts Schema#task_auto_retry_attempts}
        :param trace_level: Controls how trace events are ingested into the event table. Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#trace_level Schema#trace_level}
        :param user_task_managed_initial_warehouse_size: The initial size of warehouse to use for managed warehouses in the absence of history. For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_managed_initial_warehouse_size Schema#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_minimum_trigger_interval_in_seconds Schema#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_timeout_ms Schema#user_task_timeout_ms}
        :param with_managed_access: Specifies a managed schema. Managed access schemas centralize privilege management with the schema owner. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#with_managed_access Schema#with_managed_access}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7f31ce197ad346226677001c20e7651f4d3749ff745027f9ad6c25fc7a3a0c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SchemaConfig(
            database=database,
            name=name,
            catalog=catalog,
            comment=comment,
            data_retention_time_in_days=data_retention_time_in_days,
            default_ddl_collation=default_ddl_collation,
            enable_console_output=enable_console_output,
            external_volume=external_volume,
            id=id,
            is_transient=is_transient,
            log_level=log_level,
            max_data_extension_time_in_days=max_data_extension_time_in_days,
            pipe_execution_paused=pipe_execution_paused,
            quoted_identifiers_ignore_case=quoted_identifiers_ignore_case,
            replace_invalid_characters=replace_invalid_characters,
            storage_serialization_policy=storage_serialization_policy,
            suspend_task_after_num_failures=suspend_task_after_num_failures,
            task_auto_retry_attempts=task_auto_retry_attempts,
            trace_level=trace_level,
            user_task_managed_initial_warehouse_size=user_task_managed_initial_warehouse_size,
            user_task_minimum_trigger_interval_in_seconds=user_task_minimum_trigger_interval_in_seconds,
            user_task_timeout_ms=user_task_timeout_ms,
            with_managed_access=with_managed_access,
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
        '''Generates CDKTF code for importing a Schema resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Schema to import.
        :param import_from_id: The id of the existing Schema that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Schema to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d57c6e921930c6e5bd1e2ca4ebb9b6fb2c1967566585564047b68b6b1d3b1d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCatalog")
    def reset_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalog", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetDataRetentionTimeInDays")
    def reset_data_retention_time_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataRetentionTimeInDays", []))

    @jsii.member(jsii_name="resetDefaultDdlCollation")
    def reset_default_ddl_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDdlCollation", []))

    @jsii.member(jsii_name="resetEnableConsoleOutput")
    def reset_enable_console_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConsoleOutput", []))

    @jsii.member(jsii_name="resetExternalVolume")
    def reset_external_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalVolume", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsTransient")
    def reset_is_transient(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsTransient", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetMaxDataExtensionTimeInDays")
    def reset_max_data_extension_time_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDataExtensionTimeInDays", []))

    @jsii.member(jsii_name="resetPipeExecutionPaused")
    def reset_pipe_execution_paused(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipeExecutionPaused", []))

    @jsii.member(jsii_name="resetQuotedIdentifiersIgnoreCase")
    def reset_quoted_identifiers_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotedIdentifiersIgnoreCase", []))

    @jsii.member(jsii_name="resetReplaceInvalidCharacters")
    def reset_replace_invalid_characters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplaceInvalidCharacters", []))

    @jsii.member(jsii_name="resetStorageSerializationPolicy")
    def reset_storage_serialization_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageSerializationPolicy", []))

    @jsii.member(jsii_name="resetSuspendTaskAfterNumFailures")
    def reset_suspend_task_after_num_failures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspendTaskAfterNumFailures", []))

    @jsii.member(jsii_name="resetTaskAutoRetryAttempts")
    def reset_task_auto_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskAutoRetryAttempts", []))

    @jsii.member(jsii_name="resetTraceLevel")
    def reset_trace_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraceLevel", []))

    @jsii.member(jsii_name="resetUserTaskManagedInitialWarehouseSize")
    def reset_user_task_managed_initial_warehouse_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTaskManagedInitialWarehouseSize", []))

    @jsii.member(jsii_name="resetUserTaskMinimumTriggerIntervalInSeconds")
    def reset_user_task_minimum_trigger_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTaskMinimumTriggerIntervalInSeconds", []))

    @jsii.member(jsii_name="resetUserTaskTimeoutMs")
    def reset_user_task_timeout_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTaskTimeoutMs", []))

    @jsii.member(jsii_name="resetWithManagedAccess")
    def reset_with_managed_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithManagedAccess", []))

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
    @jsii.member(jsii_name="describeOutput")
    def describe_output(self) -> "SchemaDescribeOutputList":
        return typing.cast("SchemaDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "SchemaParametersList":
        return typing.cast("SchemaParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "SchemaShowOutputList":
        return typing.cast("SchemaShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

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
    @jsii.member(jsii_name="defaultDdlCollationInput")
    def default_ddl_collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDdlCollationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutputInput")
    def enable_console_output_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConsoleOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="externalVolumeInput")
    def external_volume_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isTransientInput")
    def is_transient_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isTransientInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDataExtensionTimeInDaysInput")
    def max_data_extension_time_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDataExtensionTimeInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pipeExecutionPausedInput")
    def pipe_execution_paused_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pipeExecutionPausedInput"))

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCaseInput")
    def quoted_identifiers_ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "quotedIdentifiersIgnoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceInvalidCharactersInput")
    def replace_invalid_characters_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replaceInvalidCharactersInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSerializationPolicyInput")
    def storage_serialization_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageSerializationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailuresInput")
    def suspend_task_after_num_failures_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "suspendTaskAfterNumFailuresInput"))

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttemptsInput")
    def task_auto_retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "taskAutoRetryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="traceLevelInput")
    def trace_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "traceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSizeInput")
    def user_task_managed_initial_warehouse_size_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userTaskManagedInitialWarehouseSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSecondsInput")
    def user_task_minimum_trigger_interval_in_seconds_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "userTaskMinimumTriggerIntervalInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMsInput")
    def user_task_timeout_ms_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "userTaskTimeoutMsInput"))

    @builtins.property
    @jsii.member(jsii_name="withManagedAccessInput")
    def with_managed_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "withManagedAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f405a71011bca0d673a8e7c933ab2296015d77e475a4eb515d09c566d13fb13d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4303f2fb3dcc73f9e9f08cb4a43bd40908b8599615d37cd2bfd72f3bb9243b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540939c259d622d5d57b56da95e10d5fc53869001992975fb42ed2423e56d423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDays")
    def data_retention_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataRetentionTimeInDays"))

    @data_retention_time_in_days.setter
    def data_retention_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdcf5c96591e0e4e0204ef55c5010c9d92c1195707363d93fa92c53f2c9d787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRetentionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDdlCollation")
    def default_ddl_collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDdlCollation"))

    @default_ddl_collation.setter
    def default_ddl_collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1310f051ab6497d0f3ffed01dccef53deab701252f880cafa0697bb415b0fe50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDdlCollation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConsoleOutput"))

    @enable_console_output.setter
    def enable_console_output(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3bd25dac56024202843349c94fdf0402d07c32a0b72e4bc26dfff952877a601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsoleOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalVolume")
    def external_volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalVolume"))

    @external_volume.setter
    def external_volume(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9594f55e0dfd0f0e83b3731367e173b67d1db61bd750554063094e4ed042102b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23502a2ef521a17f3b86cc41410c2e43a78f674f14df610498e4ab542a688db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isTransient")
    def is_transient(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isTransient"))

    @is_transient.setter
    def is_transient(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8adc46e74e9a3bc1e3007dd610cbd4703984330556e30ba5fb5d73885ccb36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isTransient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b6cc4484f3b39c9a2ac8ad548e553e4ecc64b71a28458aa3cebfdb5920894a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDataExtensionTimeInDays")
    def max_data_extension_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDataExtensionTimeInDays"))

    @max_data_extension_time_in_days.setter
    def max_data_extension_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89f0378038cc38d23fc01df17d2461312b95771c7ba20b78e381aa00fd23d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDataExtensionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03001625825ea7416588d2d1cbf8330d51720d54e02322e376ea1204a6877fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pipeExecutionPaused")
    def pipe_execution_paused(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pipeExecutionPaused"))

    @pipe_execution_paused.setter
    def pipe_execution_paused(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8bd592609be681a00dfb065089fa25c91d0b853fef09bdd1e4e48b0799df2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipeExecutionPaused", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCase")
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "quotedIdentifiersIgnoreCase"))

    @quoted_identifiers_ignore_case.setter
    def quoted_identifiers_ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2821b1d34127c97dbf2bd7c249c3a208697678dc7373b7bcd114427d667a4139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotedIdentifiersIgnoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replaceInvalidCharacters")
    def replace_invalid_characters(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replaceInvalidCharacters"))

    @replace_invalid_characters.setter
    def replace_invalid_characters(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5170d0f1a6822871eefee6fdd6d225ddf7a85c1a879e39fe8620d6a473636028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceInvalidCharacters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSerializationPolicy")
    def storage_serialization_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSerializationPolicy"))

    @storage_serialization_policy.setter
    def storage_serialization_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc57500dd69bdf7c6ca8bebc76c79496ae5a6a67e3548a36dc476b3e2b9e93e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSerializationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailures")
    def suspend_task_after_num_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendTaskAfterNumFailures"))

    @suspend_task_after_num_failures.setter
    def suspend_task_after_num_failures(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9c037fe90c44d88ef19c8563e77957fd5ac4df200c74147339de008de7cd2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendTaskAfterNumFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttempts")
    def task_auto_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskAutoRetryAttempts"))

    @task_auto_retry_attempts.setter
    def task_auto_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f635352101c45eaa0f8b191442d3fe973d1a61fa8c6c3c9977334ba0e34d489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskAutoRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f19f0eb3f13cf775b2bf115e9767b917ecc4be5ea5c4fdd81ea5e77d66a1803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSize")
    def user_task_managed_initial_warehouse_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTaskManagedInitialWarehouseSize"))

    @user_task_managed_initial_warehouse_size.setter
    def user_task_managed_initial_warehouse_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fb7baa40c2f9afbc07b8d100c6f2012ae0a98f0f6924564dc29bc0cf8bbab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskManagedInitialWarehouseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSeconds")
    def user_task_minimum_trigger_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskMinimumTriggerIntervalInSeconds"))

    @user_task_minimum_trigger_interval_in_seconds.setter
    def user_task_minimum_trigger_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2fd05acade805bfc0396c42a02e6871ddf538da781bd181e3b7321526a6f0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskMinimumTriggerIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMs")
    def user_task_timeout_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskTimeoutMs"))

    @user_task_timeout_ms.setter
    def user_task_timeout_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3220034706aff32307587960e0afc9aaee258299dd058720eba2533e8f2e3410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskTimeoutMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withManagedAccess")
    def with_managed_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "withManagedAccess"))

    @with_managed_access.setter
    def with_managed_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d151441dc7119ab6f871852d380a497face1df45aceb7b0bbb6ed29c3eaa86eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withManagedAccess", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaConfig",
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
        "catalog": "catalog",
        "comment": "comment",
        "data_retention_time_in_days": "dataRetentionTimeInDays",
        "default_ddl_collation": "defaultDdlCollation",
        "enable_console_output": "enableConsoleOutput",
        "external_volume": "externalVolume",
        "id": "id",
        "is_transient": "isTransient",
        "log_level": "logLevel",
        "max_data_extension_time_in_days": "maxDataExtensionTimeInDays",
        "pipe_execution_paused": "pipeExecutionPaused",
        "quoted_identifiers_ignore_case": "quotedIdentifiersIgnoreCase",
        "replace_invalid_characters": "replaceInvalidCharacters",
        "storage_serialization_policy": "storageSerializationPolicy",
        "suspend_task_after_num_failures": "suspendTaskAfterNumFailures",
        "task_auto_retry_attempts": "taskAutoRetryAttempts",
        "trace_level": "traceLevel",
        "user_task_managed_initial_warehouse_size": "userTaskManagedInitialWarehouseSize",
        "user_task_minimum_trigger_interval_in_seconds": "userTaskMinimumTriggerIntervalInSeconds",
        "user_task_timeout_ms": "userTaskTimeoutMs",
        "with_managed_access": "withManagedAccess",
    },
)
class SchemaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        catalog: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_volume: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_transient: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
        pipe_execution_paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_serialization_policy: typing.Optional[builtins.str] = None,
        suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
        task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
        trace_level: typing.Optional[builtins.str] = None,
        user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
        user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
        user_task_timeout_ms: typing.Optional[jsii.Number] = None,
        with_managed_access: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the schema. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#database Schema#database}
        :param name: Specifies the identifier for the schema; must be unique for the database in which the schema is created. When the name is ``PUBLIC``, during creation the provider checks if this schema has already been created and, in such case, ``ALTER`` is used to match the desired state. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#name Schema#name}
        :param catalog: The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#catalog Schema#catalog}
        :param comment: Specifies a comment for the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#comment Schema#comment}
        :param data_retention_time_in_days: Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database. For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#data_retention_time_in_days Schema#data_retention_time_in_days}
        :param default_ddl_collation: Specifies a default collation specification for all schemas and tables added to the database. It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#default_ddl_collation Schema#default_ddl_collation}
        :param enable_console_output: If true, enables stdout/stderr fast path logging for anonymous stored procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#enable_console_output Schema#enable_console_output}
        :param external_volume: The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#external_volume Schema#external_volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#id Schema#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_transient: Specifies the schema as transient. Transient schemas do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#is_transient Schema#is_transient}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#log_level Schema#log_level}
        :param max_data_extension_time_in_days: Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale. For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#max_data_extension_time_in_days Schema#max_data_extension_time_in_days}
        :param pipe_execution_paused: Specifies whether to pause a running pipe, primarily in preparation for transferring ownership of the pipe to a different role. For more information, check `PIPE_EXECUTION_PAUSED docs <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#pipe_execution_paused Schema#pipe_execution_paused}
        :param quoted_identifiers_ignore_case: If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#quoted_identifiers_ignore_case Schema#quoted_identifiers_ignore_case}
        :param replace_invalid_characters: Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table. You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#replace_invalid_characters Schema#replace_invalid_characters}
        :param storage_serialization_policy: The storage serialization policy for Iceberg tables that use Snowflake as the catalog. Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#storage_serialization_policy Schema#storage_serialization_policy}
        :param suspend_task_after_num_failures: How many times a task must fail in a row before it is automatically suspended. 0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#suspend_task_after_num_failures Schema#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#task_auto_retry_attempts Schema#task_auto_retry_attempts}
        :param trace_level: Controls how trace events are ingested into the event table. Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#trace_level Schema#trace_level}
        :param user_task_managed_initial_warehouse_size: The initial size of warehouse to use for managed warehouses in the absence of history. For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_managed_initial_warehouse_size Schema#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_minimum_trigger_interval_in_seconds Schema#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_timeout_ms Schema#user_task_timeout_ms}
        :param with_managed_access: Specifies a managed schema. Managed access schemas centralize privilege management with the schema owner. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#with_managed_access Schema#with_managed_access}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933b22d4f33ab3703f8c6e84f222b0c2ab1cdb3484c64b57dabf3d44d3591301)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument data_retention_time_in_days", value=data_retention_time_in_days, expected_type=type_hints["data_retention_time_in_days"])
            check_type(argname="argument default_ddl_collation", value=default_ddl_collation, expected_type=type_hints["default_ddl_collation"])
            check_type(argname="argument enable_console_output", value=enable_console_output, expected_type=type_hints["enable_console_output"])
            check_type(argname="argument external_volume", value=external_volume, expected_type=type_hints["external_volume"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_transient", value=is_transient, expected_type=type_hints["is_transient"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument max_data_extension_time_in_days", value=max_data_extension_time_in_days, expected_type=type_hints["max_data_extension_time_in_days"])
            check_type(argname="argument pipe_execution_paused", value=pipe_execution_paused, expected_type=type_hints["pipe_execution_paused"])
            check_type(argname="argument quoted_identifiers_ignore_case", value=quoted_identifiers_ignore_case, expected_type=type_hints["quoted_identifiers_ignore_case"])
            check_type(argname="argument replace_invalid_characters", value=replace_invalid_characters, expected_type=type_hints["replace_invalid_characters"])
            check_type(argname="argument storage_serialization_policy", value=storage_serialization_policy, expected_type=type_hints["storage_serialization_policy"])
            check_type(argname="argument suspend_task_after_num_failures", value=suspend_task_after_num_failures, expected_type=type_hints["suspend_task_after_num_failures"])
            check_type(argname="argument task_auto_retry_attempts", value=task_auto_retry_attempts, expected_type=type_hints["task_auto_retry_attempts"])
            check_type(argname="argument trace_level", value=trace_level, expected_type=type_hints["trace_level"])
            check_type(argname="argument user_task_managed_initial_warehouse_size", value=user_task_managed_initial_warehouse_size, expected_type=type_hints["user_task_managed_initial_warehouse_size"])
            check_type(argname="argument user_task_minimum_trigger_interval_in_seconds", value=user_task_minimum_trigger_interval_in_seconds, expected_type=type_hints["user_task_minimum_trigger_interval_in_seconds"])
            check_type(argname="argument user_task_timeout_ms", value=user_task_timeout_ms, expected_type=type_hints["user_task_timeout_ms"])
            check_type(argname="argument with_managed_access", value=with_managed_access, expected_type=type_hints["with_managed_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "name": name,
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
        if catalog is not None:
            self._values["catalog"] = catalog
        if comment is not None:
            self._values["comment"] = comment
        if data_retention_time_in_days is not None:
            self._values["data_retention_time_in_days"] = data_retention_time_in_days
        if default_ddl_collation is not None:
            self._values["default_ddl_collation"] = default_ddl_collation
        if enable_console_output is not None:
            self._values["enable_console_output"] = enable_console_output
        if external_volume is not None:
            self._values["external_volume"] = external_volume
        if id is not None:
            self._values["id"] = id
        if is_transient is not None:
            self._values["is_transient"] = is_transient
        if log_level is not None:
            self._values["log_level"] = log_level
        if max_data_extension_time_in_days is not None:
            self._values["max_data_extension_time_in_days"] = max_data_extension_time_in_days
        if pipe_execution_paused is not None:
            self._values["pipe_execution_paused"] = pipe_execution_paused
        if quoted_identifiers_ignore_case is not None:
            self._values["quoted_identifiers_ignore_case"] = quoted_identifiers_ignore_case
        if replace_invalid_characters is not None:
            self._values["replace_invalid_characters"] = replace_invalid_characters
        if storage_serialization_policy is not None:
            self._values["storage_serialization_policy"] = storage_serialization_policy
        if suspend_task_after_num_failures is not None:
            self._values["suspend_task_after_num_failures"] = suspend_task_after_num_failures
        if task_auto_retry_attempts is not None:
            self._values["task_auto_retry_attempts"] = task_auto_retry_attempts
        if trace_level is not None:
            self._values["trace_level"] = trace_level
        if user_task_managed_initial_warehouse_size is not None:
            self._values["user_task_managed_initial_warehouse_size"] = user_task_managed_initial_warehouse_size
        if user_task_minimum_trigger_interval_in_seconds is not None:
            self._values["user_task_minimum_trigger_interval_in_seconds"] = user_task_minimum_trigger_interval_in_seconds
        if user_task_timeout_ms is not None:
            self._values["user_task_timeout_ms"] = user_task_timeout_ms
        if with_managed_access is not None:
            self._values["with_managed_access"] = with_managed_access

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
        '''The database in which to create the schema.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#database Schema#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the schema;

        must be unique for the database in which the schema is created. When the name is ``PUBLIC``, during creation the provider checks if this schema has already been created and, in such case, ``ALTER`` is used to match the desired state. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#name Schema#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#catalog Schema#catalog}
        '''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#comment Schema#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_retention_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database.

        For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#data_retention_time_in_days Schema#data_retention_time_in_days}
        '''
        result = self._values.get("data_retention_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ddl_collation(self) -> typing.Optional[builtins.str]:
        '''Specifies a default collation specification for all schemas and tables added to the database.

        It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#default_ddl_collation Schema#default_ddl_collation}
        '''
        result = self._values.get("default_ddl_collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_console_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enables stdout/stderr fast path logging for anonymous stored procedures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#enable_console_output Schema#enable_console_output}
        '''
        result = self._values.get("enable_console_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_volume(self) -> typing.Optional[builtins.str]:
        '''The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#external_volume Schema#external_volume}
        '''
        result = self._values.get("external_volume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#id Schema#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_transient(self) -> typing.Optional[builtins.str]:
        '''Specifies the schema as transient.

        Transient schemas do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#is_transient Schema#is_transient}
        '''
        result = self._values.get("is_transient")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the severity level of messages that should be ingested and made available in the active event table.

        Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#log_level Schema#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_data_extension_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale.

        For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#max_data_extension_time_in_days Schema#max_data_extension_time_in_days}
        '''
        result = self._values.get("max_data_extension_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pipe_execution_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to pause a running pipe, primarily in preparation for transferring ownership of the pipe to a different role.

        For more information, check `PIPE_EXECUTION_PAUSED docs <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#pipe_execution_paused Schema#pipe_execution_paused}
        '''
        result = self._values.get("pipe_execution_paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#quoted_identifiers_ignore_case Schema#quoted_identifiers_ignore_case}
        '''
        result = self._values.get("quoted_identifiers_ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replace_invalid_characters(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table.

        You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#replace_invalid_characters Schema#replace_invalid_characters}
        '''
        result = self._values.get("replace_invalid_characters")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def storage_serialization_policy(self) -> typing.Optional[builtins.str]:
        '''The storage serialization policy for Iceberg tables that use Snowflake as the catalog.

        Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#storage_serialization_policy Schema#storage_serialization_policy}
        '''
        result = self._values.get("storage_serialization_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspend_task_after_num_failures(self) -> typing.Optional[jsii.Number]:
        '''How many times a task must fail in a row before it is automatically suspended.

        0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#suspend_task_after_num_failures Schema#suspend_task_after_num_failures}
        '''
        result = self._values.get("suspend_task_after_num_failures")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_auto_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#task_auto_retry_attempts Schema#task_auto_retry_attempts}
        '''
        result = self._values.get("task_auto_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Controls how trace events are ingested into the event table.

        Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#trace_level Schema#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_task_managed_initial_warehouse_size(self) -> typing.Optional[builtins.str]:
        '''The initial size of warehouse to use for managed warehouses in the absence of history.

        For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_managed_initial_warehouse_size Schema#user_task_managed_initial_warehouse_size}
        '''
        result = self._values.get("user_task_managed_initial_warehouse_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_task_minimum_trigger_interval_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Minimum amount of time between Triggered Task executions in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_minimum_trigger_interval_in_seconds Schema#user_task_minimum_trigger_interval_in_seconds}
        '''
        result = self._values.get("user_task_minimum_trigger_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_task_timeout_ms(self) -> typing.Optional[jsii.Number]:
        '''User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#user_task_timeout_ms Schema#user_task_timeout_ms}
        '''
        result = self._values.get("user_task_timeout_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def with_managed_access(self) -> typing.Optional[builtins.str]:
        '''Specifies a managed schema.

        Managed access schemas centralize privilege management with the schema owner. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/schema#with_managed_access Schema#with_managed_access}
        '''
        result = self._values.get("with_managed_access")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a3ea4af82aae38a56def9e25db866655de240ef17c279c262fb8881efd48d7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SchemaDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71768d1be60061ac75275364325db6001aed49185683b38a50daf2c034322a4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab20b86c1673dd5b6225b693390ebed0e85e8420fac0e24c9d4803c15e1445b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51c7654a5a39cae9c888744d07813777cb414648fde1f4be78e34ba7125d976b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__668a6aec86e29e6e89ef7117aa1660882c895567b31d49ad34a9d91bbb2cce04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5cccce4b523d4f8c76a2b01462a4300330479102f843659a1c348f91e67283)
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
    def internal_value(self) -> typing.Optional[SchemaDescribeOutput]:
        return typing.cast(typing.Optional[SchemaDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SchemaDescribeOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3769820019ebc8a49a0d881fc6fe5d5ea03243689ce6e0471350f88f3a6f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersCatalog",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersCatalog:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersCatalog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersCatalogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersCatalogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c05f705af33b920c36eecb17f23b4cd47b163cd7498ec165697ff441f9a9b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SchemaParametersCatalogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61c5a69439fac901efebec805d2970e10ef3d921fc2456ca9c2912a8003bb26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersCatalogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9877ac595b3351aea6e9529af9e4378d56f52d6475e4b3e38743cb04041085f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb2a926043e0bd21b92906468b67d2a464caefccea6069ca7d163555ecf430c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cecc036a58038aa44467ab99fc280aca24b73912459f6df9a05a2707f5da6a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersCatalogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersCatalogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8039ac32b38cdaa4a89d32964aa27d5809f784fbc732f275ed08fa25b06d5bcb)
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
    def internal_value(self) -> typing.Optional[SchemaParametersCatalog]:
        return typing.cast(typing.Optional[SchemaParametersCatalog], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SchemaParametersCatalog]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9bf9f08a93f503b183a293b42f9a2a448f66767e0af49d954832905de66ddfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersDataRetentionTimeInDays",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersDataRetentionTimeInDays:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersDataRetentionTimeInDays(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersDataRetentionTimeInDaysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersDataRetentionTimeInDaysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28aa5ebdd5e769ae571ec4a2e2090e7fbf79dc660175b759e7128c414ac974b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersDataRetentionTimeInDaysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc087873ba10ede3152eb848681b0d213b3386d074a1a88ee4bc187133a541c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersDataRetentionTimeInDaysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e52206ccf042b2a1415533c6373a0a40952f3bd0c4e275b960a279f080c64fdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47539afce804864e3061974822519a4e41123e84c7e812a14475110206b70ef9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aba227dec2c74e26c57578658fcaf0af45548fcfb3507b8bb10a1e2ea9cbcaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersDataRetentionTimeInDaysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersDataRetentionTimeInDaysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e7e95a0e176cf679f84574178347284af8ed45017d5fe84ada2c3f5110f3d7e)
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
    ) -> typing.Optional[SchemaParametersDataRetentionTimeInDays]:
        return typing.cast(typing.Optional[SchemaParametersDataRetentionTimeInDays], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersDataRetentionTimeInDays],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b46d618e2416fc3ba963b396c8d951aa187d2f282ad952163f0a629336e74cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersDefaultDdlCollation",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersDefaultDdlCollation:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersDefaultDdlCollation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersDefaultDdlCollationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersDefaultDdlCollationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34b154a200fdf52ef3988f52a9fcca661354e220ab313ffb73a90bbd28a69af4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersDefaultDdlCollationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88929d2268c123648d47333d8ce2d4f088747773be2a9183049ab61b8d7ac5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersDefaultDdlCollationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a5118ce2dc440ae2cd60ff53fd0efe4ea21e430aa6f1148c31bea85caf9b39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b617910d829b3b3c38cf509a14ba7b97df3d6d4fd66b55b128db069bbc4933d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33aaa3e30b385a65f2c0275198370304268b5f5f6a3f32f26edc7271ec10d0ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersDefaultDdlCollationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersDefaultDdlCollationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b54e9e60221f673e2a245fe234b210aa1ed8b154e2d6758f1491ab5012a74103)
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
    def internal_value(self) -> typing.Optional[SchemaParametersDefaultDdlCollation]:
        return typing.cast(typing.Optional[SchemaParametersDefaultDdlCollation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersDefaultDdlCollation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed9446596d54eaf2508d8ee43d718b3afe8d163272fadadf8eec1af6fa26f69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersEnableConsoleOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersEnableConsoleOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersEnableConsoleOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersEnableConsoleOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersEnableConsoleOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c543b74c1d8c6590114794b13a41efb3c4643e55a3aded0d4487171d3b439e7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersEnableConsoleOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1242def4fcf4c3b6e3e1493c9f759e861f7ccd7780338525e8fbb2a6cde481)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersEnableConsoleOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1b24d901d1af4773a0f674ad115885d9e1f3658760683310c73be7605b3161)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b4abae0325e063c2cd55bad3367b9801dd6accf06aa5d4d15e40934ed193cd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bb2fefd524692d7f1343790c20f99ad6e649baf058963b82ab1402c7f81c308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersEnableConsoleOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersEnableConsoleOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb86931b287f09e6196015997e8dcfbfd6434aaae73214ab6449e7d60608ab00)
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
    def internal_value(self) -> typing.Optional[SchemaParametersEnableConsoleOutput]:
        return typing.cast(typing.Optional[SchemaParametersEnableConsoleOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersEnableConsoleOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a022786b452041c4ef867af2a90ab5f532463367dce1bd23775b374d13adcc41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersExternalVolume",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersExternalVolume:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersExternalVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersExternalVolumeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersExternalVolumeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9afc994eb801fd982e2a1d071242c7214f6cd4fe1649c08005d484782e2fe15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersExternalVolumeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9f998efcd6f3a3ecaeb122821e37cac12a453377a475daef84011ec5c454e7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersExternalVolumeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467f51f2241e2ef0945c56075c45348b3a672d728f8906a8371c43c5de398497)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d2d148ca38fae4ee8e875c216612a07b3952a576525514cf806d35bd5dd4119)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bb4e9fa718e6288bac42c9afbee0cbd835a0ecd234ea3f5139932db0593003e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersExternalVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersExternalVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__833539217602c19f6ab3c14c72f9a3aa84da32352f1fa3d40244f568902fe6a7)
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
    def internal_value(self) -> typing.Optional[SchemaParametersExternalVolume]:
        return typing.cast(typing.Optional[SchemaParametersExternalVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersExternalVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd53de3bfb4cf610c3680f406a164d76ad0f8ad787780cd4e8dc1b3553eb39f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SchemaParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2db5a4246907894a3990b65478fd5ff8650ac617107a6b2c9831b3645569e2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SchemaParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433a676b56405759c51400a5a0216117dece558dc119553f08a6b8e39e349810)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fada3aa8647d7c86c73ac988b6d78e394f934662883813f95cb5b699be49680a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f3760319df603a0c9871272c4cc5f797718cb853e511a65a61b3d84284610dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__919f60a11f9ebf517c4020bf0a86bdecc72e463e49f4c22a8092d26d201f8814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f31263541782e2d01c8c63997bf78296a5624acc19f7f499d35ba35ac0c98616)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SchemaParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d5f51a5e0123e9b5b9a8a0dc17d24de459474cd36ed73691ec54981b7473b6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d4b849fd8d9d25c8263f6d217152f9477d9d02a389adf25cb99b74a4d17578)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbfdcf9d946f3368ae05e3bb29cd704b57c4242f15b6f67f069a68038131301)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6017565d77380d8d5e0a427d3bf2a80d658dfea610acdc4d6733e9ecac5e0001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6fe76a75c01319b3874be2e3d1520d91cb36b2c84647ecdf9a9c9f9ebe71566)
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
    def internal_value(self) -> typing.Optional[SchemaParametersLogLevel]:
        return typing.cast(typing.Optional[SchemaParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SchemaParametersLogLevel]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2527a56f6077d17ab79c40ca140c9aa2bc95ebfd390cadf7ce80f8fe99cc5557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersMaxDataExtensionTimeInDays",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersMaxDataExtensionTimeInDays:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersMaxDataExtensionTimeInDays(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersMaxDataExtensionTimeInDaysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersMaxDataExtensionTimeInDaysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dac181f8347e158d3879057a4cb9df4cf65283dafb386034d79afa2a3dcdfb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersMaxDataExtensionTimeInDaysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5541c208b09dfcb0a597f92e419a635cf11bdffb73f7d0bb1707d38a19c8b0bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersMaxDataExtensionTimeInDaysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8b1e59f54d40fbff2d7e80a5000d6ab6f1a4f0b69adf90702b8cfb6e5ff552)
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
            type_hints = typing.get_type_hints(_typecheckingstub__607030de9ceb39a7b7bf41ae76d8cf1e8d6475992713fdc79035ee49ba50924d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b88a602b0fe2db558c96c3d3e5e5d14a7b1801db2d3a7377467ba84df92d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersMaxDataExtensionTimeInDaysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersMaxDataExtensionTimeInDaysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c687d1d7441dad6ae5e2d1565d66f743eed097895a175206f2b69c1e37c38411)
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
    ) -> typing.Optional[SchemaParametersMaxDataExtensionTimeInDays]:
        return typing.cast(typing.Optional[SchemaParametersMaxDataExtensionTimeInDays], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersMaxDataExtensionTimeInDays],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c30a3f095036bd1d623bc1d3d3eaa632c096753002067be77a409e4cbf57f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SchemaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0a8688c90b05594922d8aaa2436fd5d5d23273193be8fa1985a0b84f7b8092d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> SchemaParametersCatalogList:
        return typing.cast(SchemaParametersCatalogList, jsii.get(self, "catalog"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDays")
    def data_retention_time_in_days(
        self,
    ) -> SchemaParametersDataRetentionTimeInDaysList:
        return typing.cast(SchemaParametersDataRetentionTimeInDaysList, jsii.get(self, "dataRetentionTimeInDays"))

    @builtins.property
    @jsii.member(jsii_name="defaultDdlCollation")
    def default_ddl_collation(self) -> SchemaParametersDefaultDdlCollationList:
        return typing.cast(SchemaParametersDefaultDdlCollationList, jsii.get(self, "defaultDdlCollation"))

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(self) -> SchemaParametersEnableConsoleOutputList:
        return typing.cast(SchemaParametersEnableConsoleOutputList, jsii.get(self, "enableConsoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="externalVolume")
    def external_volume(self) -> SchemaParametersExternalVolumeList:
        return typing.cast(SchemaParametersExternalVolumeList, jsii.get(self, "externalVolume"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> SchemaParametersLogLevelList:
        return typing.cast(SchemaParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="maxDataExtensionTimeInDays")
    def max_data_extension_time_in_days(
        self,
    ) -> SchemaParametersMaxDataExtensionTimeInDaysList:
        return typing.cast(SchemaParametersMaxDataExtensionTimeInDaysList, jsii.get(self, "maxDataExtensionTimeInDays"))

    @builtins.property
    @jsii.member(jsii_name="pipeExecutionPaused")
    def pipe_execution_paused(self) -> "SchemaParametersPipeExecutionPausedList":
        return typing.cast("SchemaParametersPipeExecutionPausedList", jsii.get(self, "pipeExecutionPaused"))

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCase")
    def quoted_identifiers_ignore_case(
        self,
    ) -> "SchemaParametersQuotedIdentifiersIgnoreCaseList":
        return typing.cast("SchemaParametersQuotedIdentifiersIgnoreCaseList", jsii.get(self, "quotedIdentifiersIgnoreCase"))

    @builtins.property
    @jsii.member(jsii_name="replaceInvalidCharacters")
    def replace_invalid_characters(
        self,
    ) -> "SchemaParametersReplaceInvalidCharactersList":
        return typing.cast("SchemaParametersReplaceInvalidCharactersList", jsii.get(self, "replaceInvalidCharacters"))

    @builtins.property
    @jsii.member(jsii_name="storageSerializationPolicy")
    def storage_serialization_policy(
        self,
    ) -> "SchemaParametersStorageSerializationPolicyList":
        return typing.cast("SchemaParametersStorageSerializationPolicyList", jsii.get(self, "storageSerializationPolicy"))

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailures")
    def suspend_task_after_num_failures(
        self,
    ) -> "SchemaParametersSuspendTaskAfterNumFailuresList":
        return typing.cast("SchemaParametersSuspendTaskAfterNumFailuresList", jsii.get(self, "suspendTaskAfterNumFailures"))

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttempts")
    def task_auto_retry_attempts(self) -> "SchemaParametersTaskAutoRetryAttemptsList":
        return typing.cast("SchemaParametersTaskAutoRetryAttemptsList", jsii.get(self, "taskAutoRetryAttempts"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "SchemaParametersTraceLevelList":
        return typing.cast("SchemaParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSize")
    def user_task_managed_initial_warehouse_size(
        self,
    ) -> "SchemaParametersUserTaskManagedInitialWarehouseSizeList":
        return typing.cast("SchemaParametersUserTaskManagedInitialWarehouseSizeList", jsii.get(self, "userTaskManagedInitialWarehouseSize"))

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSeconds")
    def user_task_minimum_trigger_interval_in_seconds(
        self,
    ) -> "SchemaParametersUserTaskMinimumTriggerIntervalInSecondsList":
        return typing.cast("SchemaParametersUserTaskMinimumTriggerIntervalInSecondsList", jsii.get(self, "userTaskMinimumTriggerIntervalInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMs")
    def user_task_timeout_ms(self) -> "SchemaParametersUserTaskTimeoutMsList":
        return typing.cast("SchemaParametersUserTaskTimeoutMsList", jsii.get(self, "userTaskTimeoutMs"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SchemaParameters]:
        return typing.cast(typing.Optional[SchemaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SchemaParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d188443c9c693cbde1a305c3df7618db677be532e1c21826d7e1b0a0c751c2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersPipeExecutionPaused",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersPipeExecutionPaused:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersPipeExecutionPaused(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersPipeExecutionPausedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersPipeExecutionPausedList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6de8b22a95d8d0a47431bcc9650ff35bd8fddc3e76d53c87a40b31cbe491c9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersPipeExecutionPausedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba6aa145c7467759a80fd7d7e8d686d573e9e0189a967ba50a9222f4d11caee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersPipeExecutionPausedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf224e31c7df2d06eec88df42aac35b96366b0a1791c81a67692e139348726f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66d711aff1586dd8aafae7a1d6b58363a304ff9ee7bf73521a1db9d1412a0a8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__651d59ff413b484fb4866cb60bcefcdc3d06e21677329f3d275218c15a72a34f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersPipeExecutionPausedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersPipeExecutionPausedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19c07949b129b707c62448e9a27775261d08f5917384091963d5b1c05b426a61)
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
    def internal_value(self) -> typing.Optional[SchemaParametersPipeExecutionPaused]:
        return typing.cast(typing.Optional[SchemaParametersPipeExecutionPaused], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersPipeExecutionPaused],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe1e3a3068061a995e5a3a882535e384789e07ece27fe072a39109a352b3c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersQuotedIdentifiersIgnoreCase",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersQuotedIdentifiersIgnoreCase:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersQuotedIdentifiersIgnoreCase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersQuotedIdentifiersIgnoreCaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersQuotedIdentifiersIgnoreCaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cbe04371197b220be4af4a578513088737f4632d4c7e9fc153b251f59d40926)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersQuotedIdentifiersIgnoreCaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a893895d88a9870981a2c370bcd87cda305f805df0c0406ce3c35e1ea69352)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersQuotedIdentifiersIgnoreCaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b568b5717887200e2652a78049b0c6bbe3d5e160492f0fc953f343e8925af6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a82667d5a324ee47c5e56de10c4117cfccab33d77838768e82f895f4ba62b58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d15945c73553ba97fb046a874efee6e5a3413a63628a50f93fe224e68796076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersQuotedIdentifiersIgnoreCaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersQuotedIdentifiersIgnoreCaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68bc4c24a43edc71d20d269ee1edf2decbc5f6bbeaf41ff921e5d0202c8e8691)
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
    ) -> typing.Optional[SchemaParametersQuotedIdentifiersIgnoreCase]:
        return typing.cast(typing.Optional[SchemaParametersQuotedIdentifiersIgnoreCase], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersQuotedIdentifiersIgnoreCase],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338dacbf33caf9f40c7a97740a31284911818ff1477de1ddff9be15e203c94e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersReplaceInvalidCharacters",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersReplaceInvalidCharacters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersReplaceInvalidCharacters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersReplaceInvalidCharactersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersReplaceInvalidCharactersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dbefdf6d7fad8aef9776767fae956df3cea4d5bf941e17b09da87bbda758cf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersReplaceInvalidCharactersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180a2c0e5ec6e1991f428779447666fd2a473c4391b9d221e30a4abd0b30f410)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersReplaceInvalidCharactersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e50c9710648889a00ba5246eb0cdb06204e972fdc1a2dd09e6c9b627c1eba84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44695e7e3e70830a0a6e90567ec805a89ae82ed9d6999401aa5ecc5406d73700)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ba09dcfaf872acb7acb7936cc15a9aadaeff41b62d90ca3dd3f3b03710c0212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersReplaceInvalidCharactersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersReplaceInvalidCharactersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f81d5a8a384fecd3b7ce981eda344fb38bde4eb037276685dfedfd6d5bd68bc3)
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
    ) -> typing.Optional[SchemaParametersReplaceInvalidCharacters]:
        return typing.cast(typing.Optional[SchemaParametersReplaceInvalidCharacters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersReplaceInvalidCharacters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397ad321a4e00d86aafa37cbd070f505ea1a56cbab794ef31d9c7ce47f25666d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersStorageSerializationPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersStorageSerializationPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersStorageSerializationPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersStorageSerializationPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersStorageSerializationPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c7b0cc64a4d063ea77f0dc15b9d084f9958efbf6bf9b06b198d4b19aefe6ce5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersStorageSerializationPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80dda0ef174d9e6d94aa7f28b32caf508323a2c833632dc73668a306543aca05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersStorageSerializationPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86214bc3879f469a89a0c8beaa3cb810b9d12ba5dda20e7dcf97c6fa6b76d46f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3ce5bffc2d99e84005aa33febf16dad84c8bb6bb32091930535aad4c6f1f0fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60065598c6639e57f9171208d4812bdfce27fcc4e766020a26c268c4d04d1317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersStorageSerializationPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersStorageSerializationPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22fe09ee249a77fd52d01169cb5f6fbd633a04e24a5f226b0680cd883d4e7e33)
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
    ) -> typing.Optional[SchemaParametersStorageSerializationPolicy]:
        return typing.cast(typing.Optional[SchemaParametersStorageSerializationPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersStorageSerializationPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a761f8ed1b00287c814a6b9ab1d1642fa1d513bffe19f1ff11caa5f3b9510abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersSuspendTaskAfterNumFailures",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersSuspendTaskAfterNumFailures:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersSuspendTaskAfterNumFailures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersSuspendTaskAfterNumFailuresList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersSuspendTaskAfterNumFailuresList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ced01df2fc03ecedd0b5c9d7b9f36c3dc6186701332477f52068344370ed9c09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersSuspendTaskAfterNumFailuresOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91dd992f59563e64d0d69f3e65adc3afc1a04c7cd5175ac7c88977b067a864ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersSuspendTaskAfterNumFailuresOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e9eb3213b902b81fb53fa5f1ff18346fd745be6e458eed29c49037bc80e491)
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
            type_hints = typing.get_type_hints(_typecheckingstub__570ca73ab02cbc4cf2320b62d904355c03e286deca4020ae66d3e8ee8e4ea9a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6d97d3ec80b20c3cc10c691807f111b03ecaa2db5ebc3d1810e49db9a4c8bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersSuspendTaskAfterNumFailuresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersSuspendTaskAfterNumFailuresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa5150b96112df29fe9e3f6dae84549833c61441fd649b2a58bb0ac50c47ed63)
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
    ) -> typing.Optional[SchemaParametersSuspendTaskAfterNumFailures]:
        return typing.cast(typing.Optional[SchemaParametersSuspendTaskAfterNumFailures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersSuspendTaskAfterNumFailures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1242aab8d62221b4ae8cfb99b0c450a1b561fb9c1f1fff2ca2c5e5b3a275c78a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersTaskAutoRetryAttempts",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersTaskAutoRetryAttempts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersTaskAutoRetryAttempts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersTaskAutoRetryAttemptsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersTaskAutoRetryAttemptsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ff4b201ef66168baed3b326d95e444328ca297c3e255107d098ab8cacad7802)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersTaskAutoRetryAttemptsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68124dc5d44c88da633ce5f2d58edb2540be0651d68e713217faecc1841ea5c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersTaskAutoRetryAttemptsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35333fb54d8137ccd90c91c0f1b7196e1c943620cfd0f9922e04f486b253264)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c1382d0ee3eb42c4a098e51f2818ec6e5d2cee5f934cb75695ce01ca0a36b31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8027446cf69dfe6b6bf39f07fe690368864ec9e16302970bb9be45ccb2a1b84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersTaskAutoRetryAttemptsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersTaskAutoRetryAttemptsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0f995fb06f19676b5e1564b805ee2207ebf6a1bb5214c9224ab38f8bc1f0a7)
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
    def internal_value(self) -> typing.Optional[SchemaParametersTaskAutoRetryAttempts]:
        return typing.cast(typing.Optional[SchemaParametersTaskAutoRetryAttempts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersTaskAutoRetryAttempts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95a7b6a7b430d48dc227ecc185a776088fd3dd84091c93ed6396d2fb40df8230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__236e01071b39ebd7fdf4dfc08c2e7446686d9a9877ad35f1c75fda11a11ceefb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SchemaParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ed9c152cc42a6c5ce00f96007ad1c2e89eb2fddb596afb7d59fb9f24ffe4aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62b8769e3a43c76ab65d6de56911d8c9cbd5354a930246d8bec4b4d9034929e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e582039d7a4c887488497e8ccc4893fe6d0aa96e59ae631ed35109d638693f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16a86bcf59eda8e0081a11738d5b61e4715200c48703f081c0c68d5de60d7253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__866bed11158170fdd39ec243c511cb98fa762f62d8ac4991e9775a3522730cdf)
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
    def internal_value(self) -> typing.Optional[SchemaParametersTraceLevel]:
        return typing.cast(typing.Optional[SchemaParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6e21bc11701e43a50ee034cb67d4155b01e2a6fe1b846ede19f319e1db6dcb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskManagedInitialWarehouseSize",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersUserTaskManagedInitialWarehouseSize:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersUserTaskManagedInitialWarehouseSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersUserTaskManagedInitialWarehouseSizeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskManagedInitialWarehouseSizeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac1b508c706c31664ec0ac23b4cecae532f7b605ff00d1c7b21631742dc7bc7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersUserTaskManagedInitialWarehouseSizeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f1f3e60ebfff3b9f00c9edcd20763c6a9b8c6a337fe34c80a9ca5ff3e54573)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersUserTaskManagedInitialWarehouseSizeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539308c310aeb5a82078e07906ddd843081209478abddad7285757607bfeac31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5165f678c0a9aaf993e0465235158dc3e815f877ff41fbac7da77c4e7ba0d302)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f58feb985df780bb347cd80c338f26b789081fba2ebeabde511ebb20603587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersUserTaskManagedInitialWarehouseSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskManagedInitialWarehouseSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11bc2078e96394509e682f17e8fe39454384eb725cb48ddae3b78b2e9320d541)
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
    ) -> typing.Optional[SchemaParametersUserTaskManagedInitialWarehouseSize]:
        return typing.cast(typing.Optional[SchemaParametersUserTaskManagedInitialWarehouseSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersUserTaskManagedInitialWarehouseSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c567b386085cf89ac742e9ba5b7cad4f8609af09744e953fcb227c6a0393694)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskMinimumTriggerIntervalInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersUserTaskMinimumTriggerIntervalInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersUserTaskMinimumTriggerIntervalInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersUserTaskMinimumTriggerIntervalInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskMinimumTriggerIntervalInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0099733b0624176758f2c49f60619378ecbec186a5cf5be9b05c067874f9021b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0b2a758cf7ccd0e585008347d7beb1a67783ba39f3053e2981811f837e4b54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed2860cc997636a3e14bda658ae5dae37961c33eb39adca1fabcc055537c7b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2401e5dd3a9b28e075110f5a30ea5558c5a50ed7f698d88d8e87e507fce8a07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aafdbded64f6d2481daf3cae18ae1653e4ce8cf05a53a593665df32304433c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c0472dba0f98bc245df5a4b27e2e1fcf28263a5c8b0c94058bac6f5c8e7e21)
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
    ) -> typing.Optional[SchemaParametersUserTaskMinimumTriggerIntervalInSeconds]:
        return typing.cast(typing.Optional[SchemaParametersUserTaskMinimumTriggerIntervalInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersUserTaskMinimumTriggerIntervalInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1769ed35742c028bba38822e559b49ec0e66a8da67342485f4f5ef3f98f388c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskTimeoutMs",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaParametersUserTaskTimeoutMs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaParametersUserTaskTimeoutMs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaParametersUserTaskTimeoutMsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskTimeoutMsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b2a6e954314275912b844beec8b4783a4ba844dd92a6ba88bec1f44ab3b5cad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SchemaParametersUserTaskTimeoutMsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47bede3c81f8033f4ff72a5bf06781e74f0d84d2b1cf7f93306a4641d05ac4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaParametersUserTaskTimeoutMsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291a99a9e1a7a1928e0571b249562ded886ffe81b75229279ac1833645be10d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1a649ef0076694450c15c38c916ad633000a4fb41b901bef4edf4e9f6ed8b87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a2bf76d2e18f735a73c72d068b922930625c4949500b5245214e2998da88c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaParametersUserTaskTimeoutMsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaParametersUserTaskTimeoutMsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52fb4df99e8a163cb46328d01c191e93c811a732110d86fd87d5c389750432f5)
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
    def internal_value(self) -> typing.Optional[SchemaParametersUserTaskTimeoutMs]:
        return typing.cast(typing.Optional[SchemaParametersUserTaskTimeoutMs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SchemaParametersUserTaskTimeoutMs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3c3adcc3c5d265353514d19688d67c72e92225a3c6fb0a6ee9c5cc59325a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.schema.SchemaShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class SchemaShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SchemaShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c64425a7d957a8b5915eaee240f8440334e66fbb79d7fab6d8671b8a993def7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SchemaShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fe5e7389b37bf91557ac1c2605cbdc8a66947a7f25121dc0cea0b7ebe41122)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SchemaShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d380472be4c77ecaa1a2e4f91519eb50206bdafd78ab0fe01618bd1d1c08aded)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f98c585ecaff07e8eb43b49bece50c5c370b0ac3bc14d6092f89b2c14549cd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99a46c9543aea28ea0d1f47b51d102075450b90c04959a767029832996b88e5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SchemaShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.schema.SchemaShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceaaee91875e6f7b3c880486135b1f80774e2a44cc0464de8889cd13298fd3df)
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
    def internal_value(self) -> typing.Optional[SchemaShowOutput]:
        return typing.cast(typing.Optional[SchemaShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SchemaShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed87313a32c41c76177a3af8022b338dfa462d5620d2aebc5abce2ba244b17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Schema",
    "SchemaConfig",
    "SchemaDescribeOutput",
    "SchemaDescribeOutputList",
    "SchemaDescribeOutputOutputReference",
    "SchemaParameters",
    "SchemaParametersCatalog",
    "SchemaParametersCatalogList",
    "SchemaParametersCatalogOutputReference",
    "SchemaParametersDataRetentionTimeInDays",
    "SchemaParametersDataRetentionTimeInDaysList",
    "SchemaParametersDataRetentionTimeInDaysOutputReference",
    "SchemaParametersDefaultDdlCollation",
    "SchemaParametersDefaultDdlCollationList",
    "SchemaParametersDefaultDdlCollationOutputReference",
    "SchemaParametersEnableConsoleOutput",
    "SchemaParametersEnableConsoleOutputList",
    "SchemaParametersEnableConsoleOutputOutputReference",
    "SchemaParametersExternalVolume",
    "SchemaParametersExternalVolumeList",
    "SchemaParametersExternalVolumeOutputReference",
    "SchemaParametersList",
    "SchemaParametersLogLevel",
    "SchemaParametersLogLevelList",
    "SchemaParametersLogLevelOutputReference",
    "SchemaParametersMaxDataExtensionTimeInDays",
    "SchemaParametersMaxDataExtensionTimeInDaysList",
    "SchemaParametersMaxDataExtensionTimeInDaysOutputReference",
    "SchemaParametersOutputReference",
    "SchemaParametersPipeExecutionPaused",
    "SchemaParametersPipeExecutionPausedList",
    "SchemaParametersPipeExecutionPausedOutputReference",
    "SchemaParametersQuotedIdentifiersIgnoreCase",
    "SchemaParametersQuotedIdentifiersIgnoreCaseList",
    "SchemaParametersQuotedIdentifiersIgnoreCaseOutputReference",
    "SchemaParametersReplaceInvalidCharacters",
    "SchemaParametersReplaceInvalidCharactersList",
    "SchemaParametersReplaceInvalidCharactersOutputReference",
    "SchemaParametersStorageSerializationPolicy",
    "SchemaParametersStorageSerializationPolicyList",
    "SchemaParametersStorageSerializationPolicyOutputReference",
    "SchemaParametersSuspendTaskAfterNumFailures",
    "SchemaParametersSuspendTaskAfterNumFailuresList",
    "SchemaParametersSuspendTaskAfterNumFailuresOutputReference",
    "SchemaParametersTaskAutoRetryAttempts",
    "SchemaParametersTaskAutoRetryAttemptsList",
    "SchemaParametersTaskAutoRetryAttemptsOutputReference",
    "SchemaParametersTraceLevel",
    "SchemaParametersTraceLevelList",
    "SchemaParametersTraceLevelOutputReference",
    "SchemaParametersUserTaskManagedInitialWarehouseSize",
    "SchemaParametersUserTaskManagedInitialWarehouseSizeList",
    "SchemaParametersUserTaskManagedInitialWarehouseSizeOutputReference",
    "SchemaParametersUserTaskMinimumTriggerIntervalInSeconds",
    "SchemaParametersUserTaskMinimumTriggerIntervalInSecondsList",
    "SchemaParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference",
    "SchemaParametersUserTaskTimeoutMs",
    "SchemaParametersUserTaskTimeoutMsList",
    "SchemaParametersUserTaskTimeoutMsOutputReference",
    "SchemaShowOutput",
    "SchemaShowOutputList",
    "SchemaShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__4a7f31ce197ad346226677001c20e7651f4d3749ff745027f9ad6c25fc7a3a0c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    name: builtins.str,
    catalog: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_volume: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_transient: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    pipe_execution_paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_serialization_policy: typing.Optional[builtins.str] = None,
    suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
    task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
    trace_level: typing.Optional[builtins.str] = None,
    user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
    user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
    user_task_timeout_ms: typing.Optional[jsii.Number] = None,
    with_managed_access: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0d57c6e921930c6e5bd1e2ca4ebb9b6fb2c1967566585564047b68b6b1d3b1d5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f405a71011bca0d673a8e7c933ab2296015d77e475a4eb515d09c566d13fb13d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4303f2fb3dcc73f9e9f08cb4a43bd40908b8599615d37cd2bfd72f3bb9243b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540939c259d622d5d57b56da95e10d5fc53869001992975fb42ed2423e56d423(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdcf5c96591e0e4e0204ef55c5010c9d92c1195707363d93fa92c53f2c9d787(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1310f051ab6497d0f3ffed01dccef53deab701252f880cafa0697bb415b0fe50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3bd25dac56024202843349c94fdf0402d07c32a0b72e4bc26dfff952877a601(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9594f55e0dfd0f0e83b3731367e173b67d1db61bd750554063094e4ed042102b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23502a2ef521a17f3b86cc41410c2e43a78f674f14df610498e4ab542a688db9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8adc46e74e9a3bc1e3007dd610cbd4703984330556e30ba5fb5d73885ccb36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b6cc4484f3b39c9a2ac8ad548e553e4ecc64b71a28458aa3cebfdb5920894a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89f0378038cc38d23fc01df17d2461312b95771c7ba20b78e381aa00fd23d1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03001625825ea7416588d2d1cbf8330d51720d54e02322e376ea1204a6877fa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8bd592609be681a00dfb065089fa25c91d0b853fef09bdd1e4e48b0799df2d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2821b1d34127c97dbf2bd7c249c3a208697678dc7373b7bcd114427d667a4139(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5170d0f1a6822871eefee6fdd6d225ddf7a85c1a879e39fe8620d6a473636028(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc57500dd69bdf7c6ca8bebc76c79496ae5a6a67e3548a36dc476b3e2b9e93e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9c037fe90c44d88ef19c8563e77957fd5ac4df200c74147339de008de7cd2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f635352101c45eaa0f8b191442d3fe973d1a61fa8c6c3c9977334ba0e34d489(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f19f0eb3f13cf775b2bf115e9767b917ecc4be5ea5c4fdd81ea5e77d66a1803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fb7baa40c2f9afbc07b8d100c6f2012ae0a98f0f6924564dc29bc0cf8bbab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2fd05acade805bfc0396c42a02e6871ddf538da781bd181e3b7321526a6f0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3220034706aff32307587960e0afc9aaee258299dd058720eba2533e8f2e3410(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d151441dc7119ab6f871852d380a497face1df45aceb7b0bbb6ed29c3eaa86eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933b22d4f33ab3703f8c6e84f222b0c2ab1cdb3484c64b57dabf3d44d3591301(
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
    catalog: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_volume: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_transient: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    pipe_execution_paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_serialization_policy: typing.Optional[builtins.str] = None,
    suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
    task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
    trace_level: typing.Optional[builtins.str] = None,
    user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
    user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
    user_task_timeout_ms: typing.Optional[jsii.Number] = None,
    with_managed_access: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3ea4af82aae38a56def9e25db866655de240ef17c279c262fb8881efd48d7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71768d1be60061ac75275364325db6001aed49185683b38a50daf2c034322a4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab20b86c1673dd5b6225b693390ebed0e85e8420fac0e24c9d4803c15e1445b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c7654a5a39cae9c888744d07813777cb414648fde1f4be78e34ba7125d976b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668a6aec86e29e6e89ef7117aa1660882c895567b31d49ad34a9d91bbb2cce04(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5cccce4b523d4f8c76a2b01462a4300330479102f843659a1c348f91e67283(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3769820019ebc8a49a0d881fc6fe5d5ea03243689ce6e0471350f88f3a6f1e(
    value: typing.Optional[SchemaDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c05f705af33b920c36eecb17f23b4cd47b163cd7498ec165697ff441f9a9b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61c5a69439fac901efebec805d2970e10ef3d921fc2456ca9c2912a8003bb26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9877ac595b3351aea6e9529af9e4378d56f52d6475e4b3e38743cb04041085f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2a926043e0bd21b92906468b67d2a464caefccea6069ca7d163555ecf430c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecc036a58038aa44467ab99fc280aca24b73912459f6df9a05a2707f5da6a56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8039ac32b38cdaa4a89d32964aa27d5809f784fbc732f275ed08fa25b06d5bcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9bf9f08a93f503b183a293b42f9a2a448f66767e0af49d954832905de66ddfe(
    value: typing.Optional[SchemaParametersCatalog],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28aa5ebdd5e769ae571ec4a2e2090e7fbf79dc660175b759e7128c414ac974b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc087873ba10ede3152eb848681b0d213b3386d074a1a88ee4bc187133a541c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52206ccf042b2a1415533c6373a0a40952f3bd0c4e275b960a279f080c64fdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47539afce804864e3061974822519a4e41123e84c7e812a14475110206b70ef9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aba227dec2c74e26c57578658fcaf0af45548fcfb3507b8bb10a1e2ea9cbcaf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7e95a0e176cf679f84574178347284af8ed45017d5fe84ada2c3f5110f3d7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b46d618e2416fc3ba963b396c8d951aa187d2f282ad952163f0a629336e74cd8(
    value: typing.Optional[SchemaParametersDataRetentionTimeInDays],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b154a200fdf52ef3988f52a9fcca661354e220ab313ffb73a90bbd28a69af4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88929d2268c123648d47333d8ce2d4f088747773be2a9183049ab61b8d7ac5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a5118ce2dc440ae2cd60ff53fd0efe4ea21e430aa6f1148c31bea85caf9b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b617910d829b3b3c38cf509a14ba7b97df3d6d4fd66b55b128db069bbc4933d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33aaa3e30b385a65f2c0275198370304268b5f5f6a3f32f26edc7271ec10d0ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54e9e60221f673e2a245fe234b210aa1ed8b154e2d6758f1491ab5012a74103(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed9446596d54eaf2508d8ee43d718b3afe8d163272fadadf8eec1af6fa26f69(
    value: typing.Optional[SchemaParametersDefaultDdlCollation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c543b74c1d8c6590114794b13a41efb3c4643e55a3aded0d4487171d3b439e7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1242def4fcf4c3b6e3e1493c9f759e861f7ccd7780338525e8fbb2a6cde481(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1b24d901d1af4773a0f674ad115885d9e1f3658760683310c73be7605b3161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4abae0325e063c2cd55bad3367b9801dd6accf06aa5d4d15e40934ed193cd8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb2fefd524692d7f1343790c20f99ad6e649baf058963b82ab1402c7f81c308(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb86931b287f09e6196015997e8dcfbfd6434aaae73214ab6449e7d60608ab00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a022786b452041c4ef867af2a90ab5f532463367dce1bd23775b374d13adcc41(
    value: typing.Optional[SchemaParametersEnableConsoleOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9afc994eb801fd982e2a1d071242c7214f6cd4fe1649c08005d484782e2fe15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9f998efcd6f3a3ecaeb122821e37cac12a453377a475daef84011ec5c454e7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467f51f2241e2ef0945c56075c45348b3a672d728f8906a8371c43c5de398497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2d148ca38fae4ee8e875c216612a07b3952a576525514cf806d35bd5dd4119(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb4e9fa718e6288bac42c9afbee0cbd835a0ecd234ea3f5139932db0593003e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833539217602c19f6ab3c14c72f9a3aa84da32352f1fa3d40244f568902fe6a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd53de3bfb4cf610c3680f406a164d76ad0f8ad787780cd4e8dc1b3553eb39f(
    value: typing.Optional[SchemaParametersExternalVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2db5a4246907894a3990b65478fd5ff8650ac617107a6b2c9831b3645569e2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433a676b56405759c51400a5a0216117dece558dc119553f08a6b8e39e349810(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fada3aa8647d7c86c73ac988b6d78e394f934662883813f95cb5b699be49680a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3760319df603a0c9871272c4cc5f797718cb853e511a65a61b3d84284610dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919f60a11f9ebf517c4020bf0a86bdecc72e463e49f4c22a8092d26d201f8814(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31263541782e2d01c8c63997bf78296a5624acc19f7f499d35ba35ac0c98616(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d5f51a5e0123e9b5b9a8a0dc17d24de459474cd36ed73691ec54981b7473b6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d4b849fd8d9d25c8263f6d217152f9477d9d02a389adf25cb99b74a4d17578(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbfdcf9d946f3368ae05e3bb29cd704b57c4242f15b6f67f069a68038131301(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6017565d77380d8d5e0a427d3bf2a80d658dfea610acdc4d6733e9ecac5e0001(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6fe76a75c01319b3874be2e3d1520d91cb36b2c84647ecdf9a9c9f9ebe71566(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2527a56f6077d17ab79c40ca140c9aa2bc95ebfd390cadf7ce80f8fe99cc5557(
    value: typing.Optional[SchemaParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dac181f8347e158d3879057a4cb9df4cf65283dafb386034d79afa2a3dcdfb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5541c208b09dfcb0a597f92e419a635cf11bdffb73f7d0bb1707d38a19c8b0bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8b1e59f54d40fbff2d7e80a5000d6ab6f1a4f0b69adf90702b8cfb6e5ff552(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607030de9ceb39a7b7bf41ae76d8cf1e8d6475992713fdc79035ee49ba50924d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b88a602b0fe2db558c96c3d3e5e5d14a7b1801db2d3a7377467ba84df92d4e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c687d1d7441dad6ae5e2d1565d66f743eed097895a175206f2b69c1e37c38411(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c30a3f095036bd1d623bc1d3d3eaa632c096753002067be77a409e4cbf57f8(
    value: typing.Optional[SchemaParametersMaxDataExtensionTimeInDays],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a8688c90b05594922d8aaa2436fd5d5d23273193be8fa1985a0b84f7b8092d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d188443c9c693cbde1a305c3df7618db677be532e1c21826d7e1b0a0c751c2e5(
    value: typing.Optional[SchemaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6de8b22a95d8d0a47431bcc9650ff35bd8fddc3e76d53c87a40b31cbe491c9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba6aa145c7467759a80fd7d7e8d686d573e9e0189a967ba50a9222f4d11caee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf224e31c7df2d06eec88df42aac35b96366b0a1791c81a67692e139348726f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d711aff1586dd8aafae7a1d6b58363a304ff9ee7bf73521a1db9d1412a0a8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651d59ff413b484fb4866cb60bcefcdc3d06e21677329f3d275218c15a72a34f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c07949b129b707c62448e9a27775261d08f5917384091963d5b1c05b426a61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe1e3a3068061a995e5a3a882535e384789e07ece27fe072a39109a352b3c67(
    value: typing.Optional[SchemaParametersPipeExecutionPaused],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cbe04371197b220be4af4a578513088737f4632d4c7e9fc153b251f59d40926(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a893895d88a9870981a2c370bcd87cda305f805df0c0406ce3c35e1ea69352(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b568b5717887200e2652a78049b0c6bbe3d5e160492f0fc953f343e8925af6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a82667d5a324ee47c5e56de10c4117cfccab33d77838768e82f895f4ba62b58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d15945c73553ba97fb046a874efee6e5a3413a63628a50f93fe224e68796076(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68bc4c24a43edc71d20d269ee1edf2decbc5f6bbeaf41ff921e5d0202c8e8691(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338dacbf33caf9f40c7a97740a31284911818ff1477de1ddff9be15e203c94e5(
    value: typing.Optional[SchemaParametersQuotedIdentifiersIgnoreCase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dbefdf6d7fad8aef9776767fae956df3cea4d5bf941e17b09da87bbda758cf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180a2c0e5ec6e1991f428779447666fd2a473c4391b9d221e30a4abd0b30f410(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e50c9710648889a00ba5246eb0cdb06204e972fdc1a2dd09e6c9b627c1eba84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44695e7e3e70830a0a6e90567ec805a89ae82ed9d6999401aa5ecc5406d73700(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba09dcfaf872acb7acb7936cc15a9aadaeff41b62d90ca3dd3f3b03710c0212(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81d5a8a384fecd3b7ce981eda344fb38bde4eb037276685dfedfd6d5bd68bc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397ad321a4e00d86aafa37cbd070f505ea1a56cbab794ef31d9c7ce47f25666d(
    value: typing.Optional[SchemaParametersReplaceInvalidCharacters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7b0cc64a4d063ea77f0dc15b9d084f9958efbf6bf9b06b198d4b19aefe6ce5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80dda0ef174d9e6d94aa7f28b32caf508323a2c833632dc73668a306543aca05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86214bc3879f469a89a0c8beaa3cb810b9d12ba5dda20e7dcf97c6fa6b76d46f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ce5bffc2d99e84005aa33febf16dad84c8bb6bb32091930535aad4c6f1f0fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60065598c6639e57f9171208d4812bdfce27fcc4e766020a26c268c4d04d1317(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fe09ee249a77fd52d01169cb5f6fbd633a04e24a5f226b0680cd883d4e7e33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a761f8ed1b00287c814a6b9ab1d1642fa1d513bffe19f1ff11caa5f3b9510abb(
    value: typing.Optional[SchemaParametersStorageSerializationPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced01df2fc03ecedd0b5c9d7b9f36c3dc6186701332477f52068344370ed9c09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91dd992f59563e64d0d69f3e65adc3afc1a04c7cd5175ac7c88977b067a864ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e9eb3213b902b81fb53fa5f1ff18346fd745be6e458eed29c49037bc80e491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570ca73ab02cbc4cf2320b62d904355c03e286deca4020ae66d3e8ee8e4ea9a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d97d3ec80b20c3cc10c691807f111b03ecaa2db5ebc3d1810e49db9a4c8bff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5150b96112df29fe9e3f6dae84549833c61441fd649b2a58bb0ac50c47ed63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1242aab8d62221b4ae8cfb99b0c450a1b561fb9c1f1fff2ca2c5e5b3a275c78a(
    value: typing.Optional[SchemaParametersSuspendTaskAfterNumFailures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff4b201ef66168baed3b326d95e444328ca297c3e255107d098ab8cacad7802(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68124dc5d44c88da633ce5f2d58edb2540be0651d68e713217faecc1841ea5c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35333fb54d8137ccd90c91c0f1b7196e1c943620cfd0f9922e04f486b253264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1382d0ee3eb42c4a098e51f2818ec6e5d2cee5f934cb75695ce01ca0a36b31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8027446cf69dfe6b6bf39f07fe690368864ec9e16302970bb9be45ccb2a1b84(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0f995fb06f19676b5e1564b805ee2207ebf6a1bb5214c9224ab38f8bc1f0a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a7b6a7b430d48dc227ecc185a776088fd3dd84091c93ed6396d2fb40df8230(
    value: typing.Optional[SchemaParametersTaskAutoRetryAttempts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236e01071b39ebd7fdf4dfc08c2e7446686d9a9877ad35f1c75fda11a11ceefb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ed9c152cc42a6c5ce00f96007ad1c2e89eb2fddb596afb7d59fb9f24ffe4aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62b8769e3a43c76ab65d6de56911d8c9cbd5354a930246d8bec4b4d9034929e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e582039d7a4c887488497e8ccc4893fe6d0aa96e59ae631ed35109d638693f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a86bcf59eda8e0081a11738d5b61e4715200c48703f081c0c68d5de60d7253(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866bed11158170fdd39ec243c511cb98fa762f62d8ac4991e9775a3522730cdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e21bc11701e43a50ee034cb67d4155b01e2a6fe1b846ede19f319e1db6dcb8(
    value: typing.Optional[SchemaParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1b508c706c31664ec0ac23b4cecae532f7b605ff00d1c7b21631742dc7bc7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f1f3e60ebfff3b9f00c9edcd20763c6a9b8c6a337fe34c80a9ca5ff3e54573(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539308c310aeb5a82078e07906ddd843081209478abddad7285757607bfeac31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5165f678c0a9aaf993e0465235158dc3e815f877ff41fbac7da77c4e7ba0d302(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f58feb985df780bb347cd80c338f26b789081fba2ebeabde511ebb20603587(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11bc2078e96394509e682f17e8fe39454384eb725cb48ddae3b78b2e9320d541(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c567b386085cf89ac742e9ba5b7cad4f8609af09744e953fcb227c6a0393694(
    value: typing.Optional[SchemaParametersUserTaskManagedInitialWarehouseSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0099733b0624176758f2c49f60619378ecbec186a5cf5be9b05c067874f9021b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0b2a758cf7ccd0e585008347d7beb1a67783ba39f3053e2981811f837e4b54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed2860cc997636a3e14bda658ae5dae37961c33eb39adca1fabcc055537c7b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2401e5dd3a9b28e075110f5a30ea5558c5a50ed7f698d88d8e87e507fce8a07(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafdbded64f6d2481daf3cae18ae1653e4ce8cf05a53a593665df32304433c88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c0472dba0f98bc245df5a4b27e2e1fcf28263a5c8b0c94058bac6f5c8e7e21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1769ed35742c028bba38822e559b49ec0e66a8da67342485f4f5ef3f98f388c(
    value: typing.Optional[SchemaParametersUserTaskMinimumTriggerIntervalInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2a6e954314275912b844beec8b4783a4ba844dd92a6ba88bec1f44ab3b5cad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47bede3c81f8033f4ff72a5bf06781e74f0d84d2b1cf7f93306a4641d05ac4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291a99a9e1a7a1928e0571b249562ded886ffe81b75229279ac1833645be10d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a649ef0076694450c15c38c916ad633000a4fb41b901bef4edf4e9f6ed8b87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2bf76d2e18f735a73c72d068b922930625c4949500b5245214e2998da88c75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fb4df99e8a163cb46328d01c191e93c811a732110d86fd87d5c389750432f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3c3adcc3c5d265353514d19688d67c72e92225a3c6fb0a6ee9c5cc59325a1e(
    value: typing.Optional[SchemaParametersUserTaskTimeoutMs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c64425a7d957a8b5915eaee240f8440334e66fbb79d7fab6d8671b8a993def7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fe5e7389b37bf91557ac1c2605cbdc8a66947a7f25121dc0cea0b7ebe41122(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d380472be4c77ecaa1a2e4f91519eb50206bdafd78ab0fe01618bd1d1c08aded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f98c585ecaff07e8eb43b49bece50c5c370b0ac3bc14d6092f89b2c14549cd4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a46c9543aea28ea0d1f47b51d102075450b90c04959a767029832996b88e5a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceaaee91875e6f7b3c880486135b1f80774e2a44cc0464de8889cd13298fd3df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed87313a32c41c76177a3af8022b338dfa462d5620d2aebc5abce2ba244b17a(
    value: typing.Optional[SchemaShowOutput],
) -> None:
    """Type checking stubs"""
    pass
