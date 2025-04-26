r'''
# `snowflake_secondary_database`

Refer to the Terraform Registry for docs: [`snowflake_secondary_database`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database).
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


class SecondaryDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.secondaryDatabase.SecondaryDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database snowflake_secondary_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        as_replica_of: builtins.str,
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_volume: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_transient: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_serialization_policy: typing.Optional[builtins.str] = None,
        suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
        task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
        trace_level: typing.Optional[builtins.str] = None,
        user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
        user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
        user_task_timeout_ms: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database snowflake_secondary_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param as_replica_of: A fully qualified path to a database to create a replica from. A fully qualified path follows the format of ``"<organization_name>"."<account_name>"."<database_name>"``. For more information about this resource, see `docs <./database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#as_replica_of SecondaryDatabase#as_replica_of}
        :param name: Specifies the identifier for the database; must be unique for your account. As a best practice for `Database Replication and Failover <https://docs.snowflake.com/en/user-guide/db-replication-intro>`_, it is recommended to give each secondary database the same name as its primary database. This practice supports referencing fully-qualified objects (i.e. '..') by other objects in the same database, such as querying a fully-qualified table name in a view. If a secondary database has a different name from the primary database, then these object references would break in the secondary database. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#name SecondaryDatabase#name}
        :param catalog: The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#catalog SecondaryDatabase#catalog}
        :param comment: Specifies a comment for the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#comment SecondaryDatabase#comment}
        :param data_retention_time_in_days: Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database. For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#data_retention_time_in_days SecondaryDatabase#data_retention_time_in_days}
        :param default_ddl_collation: Specifies a default collation specification for all schemas and tables added to the database. It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#default_ddl_collation SecondaryDatabase#default_ddl_collation}
        :param enable_console_output: If true, enables stdout/stderr fast path logging for anonymous stored procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#enable_console_output SecondaryDatabase#enable_console_output}
        :param external_volume: The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#external_volume SecondaryDatabase#external_volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#id SecondaryDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_transient: Specifies the database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#is_transient SecondaryDatabase#is_transient}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#log_level SecondaryDatabase#log_level}
        :param max_data_extension_time_in_days: Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale. For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#max_data_extension_time_in_days SecondaryDatabase#max_data_extension_time_in_days}
        :param quoted_identifiers_ignore_case: If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#quoted_identifiers_ignore_case SecondaryDatabase#quoted_identifiers_ignore_case}
        :param replace_invalid_characters: Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table. You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#replace_invalid_characters SecondaryDatabase#replace_invalid_characters}
        :param storage_serialization_policy: The storage serialization policy for Iceberg tables that use Snowflake as the catalog. Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#storage_serialization_policy SecondaryDatabase#storage_serialization_policy}
        :param suspend_task_after_num_failures: How many times a task must fail in a row before it is automatically suspended. 0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#suspend_task_after_num_failures SecondaryDatabase#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#task_auto_retry_attempts SecondaryDatabase#task_auto_retry_attempts}
        :param trace_level: Controls how trace events are ingested into the event table. Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#trace_level SecondaryDatabase#trace_level}
        :param user_task_managed_initial_warehouse_size: The initial size of warehouse to use for managed warehouses in the absence of history. For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_managed_initial_warehouse_size SecondaryDatabase#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_minimum_trigger_interval_in_seconds SecondaryDatabase#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_timeout_ms SecondaryDatabase#user_task_timeout_ms}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89e27d03be3c5d664f520f7df681f5cc94c844a524def1b59c8581d5b9d7c3e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SecondaryDatabaseConfig(
            as_replica_of=as_replica_of,
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
            quoted_identifiers_ignore_case=quoted_identifiers_ignore_case,
            replace_invalid_characters=replace_invalid_characters,
            storage_serialization_policy=storage_serialization_policy,
            suspend_task_after_num_failures=suspend_task_after_num_failures,
            task_auto_retry_attempts=task_auto_retry_attempts,
            trace_level=trace_level,
            user_task_managed_initial_warehouse_size=user_task_managed_initial_warehouse_size,
            user_task_minimum_trigger_interval_in_seconds=user_task_minimum_trigger_interval_in_seconds,
            user_task_timeout_ms=user_task_timeout_ms,
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
        '''Generates CDKTF code for importing a SecondaryDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SecondaryDatabase to import.
        :param import_from_id: The id of the existing SecondaryDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SecondaryDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60e154b0a460a0aaf2c06d30667508dba449e73dcabe9ba21b0d00e42e43a19b)
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
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="asReplicaOfInput")
    def as_replica_of_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "asReplicaOfInput"))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

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
    def is_transient_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isTransientInput"))

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
    @jsii.member(jsii_name="asReplicaOf")
    def as_replica_of(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "asReplicaOf"))

    @as_replica_of.setter
    def as_replica_of(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5945be344282713b659ce8eda55a7502d59b7b95625358b63f997a6ecabaf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asReplicaOf", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b93cf5b66e397c77236b4d7260a8092b8b8ec96afc99999929c74b1678a884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c6dbdc81fa64103882cf9304f79dbf1be2e4947225b1185c873fc65698f85c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDays")
    def data_retention_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataRetentionTimeInDays"))

    @data_retention_time_in_days.setter
    def data_retention_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370fd6ae269f5053ff730f61399233bfaf11ccbce4655f3f969b6b81221795e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRetentionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDdlCollation")
    def default_ddl_collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDdlCollation"))

    @default_ddl_collation.setter
    def default_ddl_collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3844cfbad76b0f9f9405a06a419a69b598a8fad446f34340f65016ec44ab4aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__151173a260cea8355d94afea9b51f4768e8230a15a139fca27f1a119306aac47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsoleOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalVolume")
    def external_volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalVolume"))

    @external_volume.setter
    def external_volume(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f10736c1e74876a4bdea3e41291a1090391540e16f799e8c637a8fbb895454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e8c25fbbd6ae6edd2b083cc2689fdb9557ba568984afb3606a9c086a43266c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isTransient")
    def is_transient(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isTransient"))

    @is_transient.setter
    def is_transient(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2126b81a158e6394e812deb96e64d3aa1cf5d0715d38e542f9720558a3e03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isTransient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda464daf2d27d309a106c2636a20d72d98cfc1d48dc6ed5c8ddc286e74ee5c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDataExtensionTimeInDays")
    def max_data_extension_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDataExtensionTimeInDays"))

    @max_data_extension_time_in_days.setter
    def max_data_extension_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618aa2d2a787c350ab3d7e5bdbfd8f2f9d27318b7192a1a91cd8781db22f50e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDataExtensionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b829bb1b709aed938ee12b4abc8b24271722656b69581eb6e3fac0ed074c2fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__82abec0e262429fa4f21898635ad998e63f59158cc4e7e81fd3331cf85bca832)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6abdbf730e3294a10c33a8ec87a6069c9158e0e7c8abdd9863742651e20f6993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceInvalidCharacters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSerializationPolicy")
    def storage_serialization_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSerializationPolicy"))

    @storage_serialization_policy.setter
    def storage_serialization_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e832dd68e8d514f133f6318114d4eac87b7214590d7f344ec1492ab4c74b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSerializationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailures")
    def suspend_task_after_num_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendTaskAfterNumFailures"))

    @suspend_task_after_num_failures.setter
    def suspend_task_after_num_failures(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2242b3d2ba1dd36812efde1e9f3b69c0516bf0891f711534154de50dd1c1512f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendTaskAfterNumFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttempts")
    def task_auto_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskAutoRetryAttempts"))

    @task_auto_retry_attempts.setter
    def task_auto_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078ed8948aaccf58ee95797b98d9e597590a75c2a2a1a31bff2596177767de7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskAutoRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30f06a79eb1be547f0c8f471dce4725d9ebe144ffd412114b7c32d84c988355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSize")
    def user_task_managed_initial_warehouse_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTaskManagedInitialWarehouseSize"))

    @user_task_managed_initial_warehouse_size.setter
    def user_task_managed_initial_warehouse_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3057222a07f2eef28c7ad5932f235bf84b2a02a023d349411136df9e94ec6029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskManagedInitialWarehouseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSeconds")
    def user_task_minimum_trigger_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskMinimumTriggerIntervalInSeconds"))

    @user_task_minimum_trigger_interval_in_seconds.setter
    def user_task_minimum_trigger_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc07e912da06f5ad47a64862fbb92d6cba4edd49f30ac28e6cb7a4145779e21b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskMinimumTriggerIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMs")
    def user_task_timeout_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskTimeoutMs"))

    @user_task_timeout_ms.setter
    def user_task_timeout_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700c3fe4e4b83daa5b51e00d66a29bd07279c4f7978dbaf2d83d7afe6032cbac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskTimeoutMs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.secondaryDatabase.SecondaryDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "as_replica_of": "asReplicaOf",
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
        "quoted_identifiers_ignore_case": "quotedIdentifiersIgnoreCase",
        "replace_invalid_characters": "replaceInvalidCharacters",
        "storage_serialization_policy": "storageSerializationPolicy",
        "suspend_task_after_num_failures": "suspendTaskAfterNumFailures",
        "task_auto_retry_attempts": "taskAutoRetryAttempts",
        "trace_level": "traceLevel",
        "user_task_managed_initial_warehouse_size": "userTaskManagedInitialWarehouseSize",
        "user_task_minimum_trigger_interval_in_seconds": "userTaskMinimumTriggerIntervalInSeconds",
        "user_task_timeout_ms": "userTaskTimeoutMs",
    },
)
class SecondaryDatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        as_replica_of: builtins.str,
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_volume: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_transient: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_serialization_policy: typing.Optional[builtins.str] = None,
        suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
        task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
        trace_level: typing.Optional[builtins.str] = None,
        user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
        user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
        user_task_timeout_ms: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param as_replica_of: A fully qualified path to a database to create a replica from. A fully qualified path follows the format of ``"<organization_name>"."<account_name>"."<database_name>"``. For more information about this resource, see `docs <./database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#as_replica_of SecondaryDatabase#as_replica_of}
        :param name: Specifies the identifier for the database; must be unique for your account. As a best practice for `Database Replication and Failover <https://docs.snowflake.com/en/user-guide/db-replication-intro>`_, it is recommended to give each secondary database the same name as its primary database. This practice supports referencing fully-qualified objects (i.e. '..') by other objects in the same database, such as querying a fully-qualified table name in a view. If a secondary database has a different name from the primary database, then these object references would break in the secondary database. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#name SecondaryDatabase#name}
        :param catalog: The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#catalog SecondaryDatabase#catalog}
        :param comment: Specifies a comment for the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#comment SecondaryDatabase#comment}
        :param data_retention_time_in_days: Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database. For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#data_retention_time_in_days SecondaryDatabase#data_retention_time_in_days}
        :param default_ddl_collation: Specifies a default collation specification for all schemas and tables added to the database. It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#default_ddl_collation SecondaryDatabase#default_ddl_collation}
        :param enable_console_output: If true, enables stdout/stderr fast path logging for anonymous stored procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#enable_console_output SecondaryDatabase#enable_console_output}
        :param external_volume: The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#external_volume SecondaryDatabase#external_volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#id SecondaryDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_transient: Specifies the database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#is_transient SecondaryDatabase#is_transient}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#log_level SecondaryDatabase#log_level}
        :param max_data_extension_time_in_days: Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale. For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#max_data_extension_time_in_days SecondaryDatabase#max_data_extension_time_in_days}
        :param quoted_identifiers_ignore_case: If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#quoted_identifiers_ignore_case SecondaryDatabase#quoted_identifiers_ignore_case}
        :param replace_invalid_characters: Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table. You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#replace_invalid_characters SecondaryDatabase#replace_invalid_characters}
        :param storage_serialization_policy: The storage serialization policy for Iceberg tables that use Snowflake as the catalog. Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#storage_serialization_policy SecondaryDatabase#storage_serialization_policy}
        :param suspend_task_after_num_failures: How many times a task must fail in a row before it is automatically suspended. 0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#suspend_task_after_num_failures SecondaryDatabase#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#task_auto_retry_attempts SecondaryDatabase#task_auto_retry_attempts}
        :param trace_level: Controls how trace events are ingested into the event table. Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#trace_level SecondaryDatabase#trace_level}
        :param user_task_managed_initial_warehouse_size: The initial size of warehouse to use for managed warehouses in the absence of history. For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_managed_initial_warehouse_size SecondaryDatabase#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_minimum_trigger_interval_in_seconds SecondaryDatabase#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_timeout_ms SecondaryDatabase#user_task_timeout_ms}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474313f467e7319a382c708ef0748e82b899118d40d161bc54b79ebc7a54bb8b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument as_replica_of", value=as_replica_of, expected_type=type_hints["as_replica_of"])
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
            check_type(argname="argument quoted_identifiers_ignore_case", value=quoted_identifiers_ignore_case, expected_type=type_hints["quoted_identifiers_ignore_case"])
            check_type(argname="argument replace_invalid_characters", value=replace_invalid_characters, expected_type=type_hints["replace_invalid_characters"])
            check_type(argname="argument storage_serialization_policy", value=storage_serialization_policy, expected_type=type_hints["storage_serialization_policy"])
            check_type(argname="argument suspend_task_after_num_failures", value=suspend_task_after_num_failures, expected_type=type_hints["suspend_task_after_num_failures"])
            check_type(argname="argument task_auto_retry_attempts", value=task_auto_retry_attempts, expected_type=type_hints["task_auto_retry_attempts"])
            check_type(argname="argument trace_level", value=trace_level, expected_type=type_hints["trace_level"])
            check_type(argname="argument user_task_managed_initial_warehouse_size", value=user_task_managed_initial_warehouse_size, expected_type=type_hints["user_task_managed_initial_warehouse_size"])
            check_type(argname="argument user_task_minimum_trigger_interval_in_seconds", value=user_task_minimum_trigger_interval_in_seconds, expected_type=type_hints["user_task_minimum_trigger_interval_in_seconds"])
            check_type(argname="argument user_task_timeout_ms", value=user_task_timeout_ms, expected_type=type_hints["user_task_timeout_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "as_replica_of": as_replica_of,
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
    def as_replica_of(self) -> builtins.str:
        '''A fully qualified path to a database to create a replica from.

        A fully qualified path follows the format of ``"<organization_name>"."<account_name>"."<database_name>"``. For more information about this resource, see `docs <./database>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#as_replica_of SecondaryDatabase#as_replica_of}
        '''
        result = self._values.get("as_replica_of")
        assert result is not None, "Required property 'as_replica_of' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the database;

        must be unique for your account. As a best practice for `Database Replication and Failover <https://docs.snowflake.com/en/user-guide/db-replication-intro>`_, it is recommended to give each secondary database the same name as its primary database. This practice supports referencing fully-qualified objects (i.e. '..') by other objects in the same database, such as querying a fully-qualified table name in a view. If a secondary database has a different name from the primary database, then these object references would break in the secondary database. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#name SecondaryDatabase#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#catalog SecondaryDatabase#catalog}
        '''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#comment SecondaryDatabase#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_retention_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database.

        For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#data_retention_time_in_days SecondaryDatabase#data_retention_time_in_days}
        '''
        result = self._values.get("data_retention_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ddl_collation(self) -> typing.Optional[builtins.str]:
        '''Specifies a default collation specification for all schemas and tables added to the database.

        It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#default_ddl_collation SecondaryDatabase#default_ddl_collation}
        '''
        result = self._values.get("default_ddl_collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_console_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enables stdout/stderr fast path logging for anonymous stored procedures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#enable_console_output SecondaryDatabase#enable_console_output}
        '''
        result = self._values.get("enable_console_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_volume(self) -> typing.Optional[builtins.str]:
        '''The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#external_volume SecondaryDatabase#external_volume}
        '''
        result = self._values.get("external_volume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#id SecondaryDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_transient(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the database as transient.

        Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#is_transient SecondaryDatabase#is_transient}
        '''
        result = self._values.get("is_transient")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the severity level of messages that should be ingested and made available in the active event table.

        Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#log_level SecondaryDatabase#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_data_extension_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale.

        For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#max_data_extension_time_in_days SecondaryDatabase#max_data_extension_time_in_days}
        '''
        result = self._values.get("max_data_extension_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#quoted_identifiers_ignore_case SecondaryDatabase#quoted_identifiers_ignore_case}
        '''
        result = self._values.get("quoted_identifiers_ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replace_invalid_characters(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table.

        You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#replace_invalid_characters SecondaryDatabase#replace_invalid_characters}
        '''
        result = self._values.get("replace_invalid_characters")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def storage_serialization_policy(self) -> typing.Optional[builtins.str]:
        '''The storage serialization policy for Iceberg tables that use Snowflake as the catalog.

        Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#storage_serialization_policy SecondaryDatabase#storage_serialization_policy}
        '''
        result = self._values.get("storage_serialization_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspend_task_after_num_failures(self) -> typing.Optional[jsii.Number]:
        '''How many times a task must fail in a row before it is automatically suspended.

        0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#suspend_task_after_num_failures SecondaryDatabase#suspend_task_after_num_failures}
        '''
        result = self._values.get("suspend_task_after_num_failures")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_auto_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#task_auto_retry_attempts SecondaryDatabase#task_auto_retry_attempts}
        '''
        result = self._values.get("task_auto_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Controls how trace events are ingested into the event table.

        Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#trace_level SecondaryDatabase#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_task_managed_initial_warehouse_size(self) -> typing.Optional[builtins.str]:
        '''The initial size of warehouse to use for managed warehouses in the absence of history.

        For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_managed_initial_warehouse_size SecondaryDatabase#user_task_managed_initial_warehouse_size}
        '''
        result = self._values.get("user_task_managed_initial_warehouse_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_task_minimum_trigger_interval_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Minimum amount of time between Triggered Task executions in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_minimum_trigger_interval_in_seconds SecondaryDatabase#user_task_minimum_trigger_interval_in_seconds}
        '''
        result = self._values.get("user_task_minimum_trigger_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_task_timeout_ms(self) -> typing.Optional[jsii.Number]:
        '''User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/secondary_database#user_task_timeout_ms SecondaryDatabase#user_task_timeout_ms}
        '''
        result = self._values.get("user_task_timeout_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecondaryDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecondaryDatabase",
    "SecondaryDatabaseConfig",
]

publication.publish()

def _typecheckingstub__a89e27d03be3c5d664f520f7df681f5cc94c844a524def1b59c8581d5b9d7c3e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    as_replica_of: builtins.str,
    name: builtins.str,
    catalog: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_volume: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_transient: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_serialization_policy: typing.Optional[builtins.str] = None,
    suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
    task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
    trace_level: typing.Optional[builtins.str] = None,
    user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
    user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
    user_task_timeout_ms: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__60e154b0a460a0aaf2c06d30667508dba449e73dcabe9ba21b0d00e42e43a19b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5945be344282713b659ce8eda55a7502d59b7b95625358b63f997a6ecabaf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b93cf5b66e397c77236b4d7260a8092b8b8ec96afc99999929c74b1678a884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c6dbdc81fa64103882cf9304f79dbf1be2e4947225b1185c873fc65698f85c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370fd6ae269f5053ff730f61399233bfaf11ccbce4655f3f969b6b81221795e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3844cfbad76b0f9f9405a06a419a69b598a8fad446f34340f65016ec44ab4aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151173a260cea8355d94afea9b51f4768e8230a15a139fca27f1a119306aac47(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f10736c1e74876a4bdea3e41291a1090391540e16f799e8c637a8fbb895454(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e8c25fbbd6ae6edd2b083cc2689fdb9557ba568984afb3606a9c086a43266c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2126b81a158e6394e812deb96e64d3aa1cf5d0715d38e542f9720558a3e03c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda464daf2d27d309a106c2636a20d72d98cfc1d48dc6ed5c8ddc286e74ee5c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618aa2d2a787c350ab3d7e5bdbfd8f2f9d27318b7192a1a91cd8781db22f50e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b829bb1b709aed938ee12b4abc8b24271722656b69581eb6e3fac0ed074c2fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82abec0e262429fa4f21898635ad998e63f59158cc4e7e81fd3331cf85bca832(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abdbf730e3294a10c33a8ec87a6069c9158e0e7c8abdd9863742651e20f6993(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e832dd68e8d514f133f6318114d4eac87b7214590d7f344ec1492ab4c74b37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2242b3d2ba1dd36812efde1e9f3b69c0516bf0891f711534154de50dd1c1512f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078ed8948aaccf58ee95797b98d9e597590a75c2a2a1a31bff2596177767de7a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30f06a79eb1be547f0c8f471dce4725d9ebe144ffd412114b7c32d84c988355(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3057222a07f2eef28c7ad5932f235bf84b2a02a023d349411136df9e94ec6029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc07e912da06f5ad47a64862fbb92d6cba4edd49f30ac28e6cb7a4145779e21b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700c3fe4e4b83daa5b51e00d66a29bd07279c4f7978dbaf2d83d7afe6032cbac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474313f467e7319a382c708ef0748e82b899118d40d161bc54b79ebc7a54bb8b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    as_replica_of: builtins.str,
    name: builtins.str,
    catalog: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_volume: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_transient: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_serialization_policy: typing.Optional[builtins.str] = None,
    suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
    task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
    trace_level: typing.Optional[builtins.str] = None,
    user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
    user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
    user_task_timeout_ms: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
