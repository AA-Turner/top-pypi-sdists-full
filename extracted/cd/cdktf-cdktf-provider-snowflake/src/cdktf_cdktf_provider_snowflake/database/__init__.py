r'''
# `snowflake_database`

Refer to the Terraform Registry for docs: [`snowflake_database`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database).
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


class Database(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.database.Database",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database snowflake_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        drop_public_schema_on_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_volume: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_transient: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replication: typing.Optional[typing.Union["DatabaseReplication", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database snowflake_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Specifies the identifier for the database; must be unique for your account. As a best practice for `Database Replication and Failover <https://docs.snowflake.com/en/user-guide/db-replication-intro>`_, it is recommended to give each secondary database the same name as its primary database. This practice supports referencing fully-qualified objects (i.e. '..') by other objects in the same database, such as querying a fully-qualified table name in a view. If a secondary database has a different name from the primary database, then these object references would break in the secondary database. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#name Database#name}
        :param catalog: The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#catalog Database#catalog}
        :param comment: Specifies a comment for the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#comment Database#comment}
        :param data_retention_time_in_days: Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database. For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#data_retention_time_in_days Database#data_retention_time_in_days}
        :param default_ddl_collation: Specifies a default collation specification for all schemas and tables added to the database. It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#default_ddl_collation Database#default_ddl_collation}
        :param drop_public_schema_on_creation: Specifies whether to drop public schema on creation or not. Modifying the parameter after database is already created won't have any effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#drop_public_schema_on_creation Database#drop_public_schema_on_creation}
        :param enable_console_output: If true, enables stdout/stderr fast path logging for anonymous stored procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#enable_console_output Database#enable_console_output}
        :param external_volume: The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#external_volume Database#external_volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#id Database#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_transient: Specifies the database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#is_transient Database#is_transient}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#log_level Database#log_level}
        :param max_data_extension_time_in_days: Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale. For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#max_data_extension_time_in_days Database#max_data_extension_time_in_days}
        :param quoted_identifiers_ignore_case: If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#quoted_identifiers_ignore_case Database#quoted_identifiers_ignore_case}
        :param replace_invalid_characters: Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table. You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#replace_invalid_characters Database#replace_invalid_characters}
        :param replication: replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#replication Database#replication}
        :param storage_serialization_policy: The storage serialization policy for Iceberg tables that use Snowflake as the catalog. Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#storage_serialization_policy Database#storage_serialization_policy}
        :param suspend_task_after_num_failures: How many times a task must fail in a row before it is automatically suspended. 0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#suspend_task_after_num_failures Database#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#task_auto_retry_attempts Database#task_auto_retry_attempts}
        :param trace_level: Controls how trace events are ingested into the event table. Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#trace_level Database#trace_level}
        :param user_task_managed_initial_warehouse_size: The initial size of warehouse to use for managed warehouses in the absence of history. For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_managed_initial_warehouse_size Database#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_minimum_trigger_interval_in_seconds Database#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_timeout_ms Database#user_task_timeout_ms}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15a50f89eb08aece66579f840c6fa677da88eecbc745d8303f4003e46439abf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DatabaseConfig(
            name=name,
            catalog=catalog,
            comment=comment,
            data_retention_time_in_days=data_retention_time_in_days,
            default_ddl_collation=default_ddl_collation,
            drop_public_schema_on_creation=drop_public_schema_on_creation,
            enable_console_output=enable_console_output,
            external_volume=external_volume,
            id=id,
            is_transient=is_transient,
            log_level=log_level,
            max_data_extension_time_in_days=max_data_extension_time_in_days,
            quoted_identifiers_ignore_case=quoted_identifiers_ignore_case,
            replace_invalid_characters=replace_invalid_characters,
            replication=replication,
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
        '''Generates CDKTF code for importing a Database resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Database to import.
        :param import_from_id: The id of the existing Database that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Database to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77891cb77202232aa5fdff4adeab90ba3a5bb42678747f900a74c6a3daa469f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putReplication")
    def put_replication(
        self,
        *,
        enable_to_account: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseReplicationEnableToAccount", typing.Dict[builtins.str, typing.Any]]]],
        ignore_edition_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_to_account: enable_to_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#enable_to_account Database#enable_to_account}
        :param ignore_edition_check: Allows replicating data to accounts on lower editions in either of the following scenarios: 1. The primary database is in a Business Critical (or higher) account but one or more of the accounts approved for replication are on lower editions. Business Critical Edition is intended for Snowflake accounts with extremely sensitive data. 2. The primary database is in a Business Critical (or higher) account and a signed business associate agreement is in place to store PHI data in the account per HIPAA and HITRUST regulations, but no such agreement is in place for one or more of the accounts approved for replication, regardless if they are Business Critical (or higher) accounts. Both scenarios are prohibited by default in an effort to help prevent account administrators for Business Critical (or higher) accounts from inadvertently replicating sensitive data to accounts on lower editions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#ignore_edition_check Database#ignore_edition_check}
        '''
        value = DatabaseReplication(
            enable_to_account=enable_to_account,
            ignore_edition_check=ignore_edition_check,
        )

        return typing.cast(None, jsii.invoke(self, "putReplication", [value]))

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

    @jsii.member(jsii_name="resetDropPublicSchemaOnCreation")
    def reset_drop_public_schema_on_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropPublicSchemaOnCreation", []))

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

    @jsii.member(jsii_name="resetReplication")
    def reset_replication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplication", []))

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
    @jsii.member(jsii_name="replication")
    def replication(self) -> "DatabaseReplicationOutputReference":
        return typing.cast("DatabaseReplicationOutputReference", jsii.get(self, "replication"))

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
    @jsii.member(jsii_name="dropPublicSchemaOnCreationInput")
    def drop_public_schema_on_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropPublicSchemaOnCreationInput"))

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
    @jsii.member(jsii_name="replicationInput")
    def replication_input(self) -> typing.Optional["DatabaseReplication"]:
        return typing.cast(typing.Optional["DatabaseReplication"], jsii.get(self, "replicationInput"))

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
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f309e0e1018d51444b8f2afa705855d5ca326852a42242415a4f8a9a197edba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e2a89dc8f0fc5f4ebbf143fe2e8f7040b61e3933fbac91752a1ed3b7e53e18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDays")
    def data_retention_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataRetentionTimeInDays"))

    @data_retention_time_in_days.setter
    def data_retention_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca2c028304080fa7ff570057044330e7d313c3be453bcf132c534f78bf04959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRetentionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDdlCollation")
    def default_ddl_collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDdlCollation"))

    @default_ddl_collation.setter
    def default_ddl_collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ef76a5d17a3dae9ed5724e03411a1c64dbfde6ab45e79c1deb00854d95aa98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDdlCollation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dropPublicSchemaOnCreation")
    def drop_public_schema_on_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropPublicSchemaOnCreation"))

    @drop_public_schema_on_creation.setter
    def drop_public_schema_on_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e53bdc1ef24de42393b2819101ee8a214358f28a563b749ad5bf37cecd1e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropPublicSchemaOnCreation", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__7de99fa10800fb2fc8f4c25056c98e5a376c4522fa62dc100064fbe1bec7835f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsoleOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalVolume")
    def external_volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalVolume"))

    @external_volume.setter
    def external_volume(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7415dcaabccd7a229632856cdfe9a4fbd8f773501b44bd5a3bd97b44e0197d82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd1d980fc53ae3767f84154ae86a1f0f7561231ff3245856409f992ab3ca540)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43c2a7b99e3b917074cd9fbd8d72667638938c3856367106165056bde52ffda8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isTransient", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f616d4976048c49ec40fa3661a4b513b4ffcc948022260ccff0a37e1764274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDataExtensionTimeInDays")
    def max_data_extension_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDataExtensionTimeInDays"))

    @max_data_extension_time_in_days.setter
    def max_data_extension_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c628d88e1ca4bf1b1ed180cb42db69c2051e46dd4b62ecf86b72d5deb8b4200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDataExtensionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbccc96209c6e09ec18d2d3fc2bf18fc780c674c489bd1dee20dac62996024d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30667c5f6b701dc74caa58b77c80f903502c3c111e029a6e9c3787b3d9d41ffa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__387fd8556e8c1ae5976c2167b9d8fadf022fc6e3e1acf2f3104ec86dd40034f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceInvalidCharacters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSerializationPolicy")
    def storage_serialization_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSerializationPolicy"))

    @storage_serialization_policy.setter
    def storage_serialization_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae374394ea2270fc09f92f5ef9a66ad054bda9979169704635c1cc5a0a2af6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSerializationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailures")
    def suspend_task_after_num_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendTaskAfterNumFailures"))

    @suspend_task_after_num_failures.setter
    def suspend_task_after_num_failures(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c12beae95b66965d287f3af9adfad9ac15a7826d12ec77795b8b18274fbdc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendTaskAfterNumFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttempts")
    def task_auto_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskAutoRetryAttempts"))

    @task_auto_retry_attempts.setter
    def task_auto_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f497ba4d7ef61f6b034ab97e09a77688c2fc3e9345d7fa37f4129daf90f7c5e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskAutoRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af3a0b7cbd3f8fa9a3d0c6909b7bcbc9bf8358dc690abfd807a2c5ba31d2c4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSize")
    def user_task_managed_initial_warehouse_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTaskManagedInitialWarehouseSize"))

    @user_task_managed_initial_warehouse_size.setter
    def user_task_managed_initial_warehouse_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7988b50cbe076cda8dca3408ec8cee6d1cf370f151d071be0f2ebc172303b2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskManagedInitialWarehouseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSeconds")
    def user_task_minimum_trigger_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskMinimumTriggerIntervalInSeconds"))

    @user_task_minimum_trigger_interval_in_seconds.setter
    def user_task_minimum_trigger_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce42b54e786aad937cdd7e034bcd27bbde1e8c18a3b24cb3bed72907875ceacd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskMinimumTriggerIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMs")
    def user_task_timeout_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskTimeoutMs"))

    @user_task_timeout_ms.setter
    def user_task_timeout_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40ed1e11565dfd6c6281d687c85e775c307a45a2004f678d3aa6bc924e36bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskTimeoutMs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.database.DatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "catalog": "catalog",
        "comment": "comment",
        "data_retention_time_in_days": "dataRetentionTimeInDays",
        "default_ddl_collation": "defaultDdlCollation",
        "drop_public_schema_on_creation": "dropPublicSchemaOnCreation",
        "enable_console_output": "enableConsoleOutput",
        "external_volume": "externalVolume",
        "id": "id",
        "is_transient": "isTransient",
        "log_level": "logLevel",
        "max_data_extension_time_in_days": "maxDataExtensionTimeInDays",
        "quoted_identifiers_ignore_case": "quotedIdentifiersIgnoreCase",
        "replace_invalid_characters": "replaceInvalidCharacters",
        "replication": "replication",
        "storage_serialization_policy": "storageSerializationPolicy",
        "suspend_task_after_num_failures": "suspendTaskAfterNumFailures",
        "task_auto_retry_attempts": "taskAutoRetryAttempts",
        "trace_level": "traceLevel",
        "user_task_managed_initial_warehouse_size": "userTaskManagedInitialWarehouseSize",
        "user_task_minimum_trigger_interval_in_seconds": "userTaskMinimumTriggerIntervalInSeconds",
        "user_task_timeout_ms": "userTaskTimeoutMs",
    },
)
class DatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        drop_public_schema_on_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_volume: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        is_transient: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replication: typing.Optional[typing.Union["DatabaseReplication", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Specifies the identifier for the database; must be unique for your account. As a best practice for `Database Replication and Failover <https://docs.snowflake.com/en/user-guide/db-replication-intro>`_, it is recommended to give each secondary database the same name as its primary database. This practice supports referencing fully-qualified objects (i.e. '..') by other objects in the same database, such as querying a fully-qualified table name in a view. If a secondary database has a different name from the primary database, then these object references would break in the secondary database. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#name Database#name}
        :param catalog: The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#catalog Database#catalog}
        :param comment: Specifies a comment for the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#comment Database#comment}
        :param data_retention_time_in_days: Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database. For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#data_retention_time_in_days Database#data_retention_time_in_days}
        :param default_ddl_collation: Specifies a default collation specification for all schemas and tables added to the database. It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#default_ddl_collation Database#default_ddl_collation}
        :param drop_public_schema_on_creation: Specifies whether to drop public schema on creation or not. Modifying the parameter after database is already created won't have any effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#drop_public_schema_on_creation Database#drop_public_schema_on_creation}
        :param enable_console_output: If true, enables stdout/stderr fast path logging for anonymous stored procedures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#enable_console_output Database#enable_console_output}
        :param external_volume: The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#external_volume Database#external_volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#id Database#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_transient: Specifies the database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#is_transient Database#is_transient}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#log_level Database#log_level}
        :param max_data_extension_time_in_days: Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale. For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#max_data_extension_time_in_days Database#max_data_extension_time_in_days}
        :param quoted_identifiers_ignore_case: If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#quoted_identifiers_ignore_case Database#quoted_identifiers_ignore_case}
        :param replace_invalid_characters: Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table. You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#replace_invalid_characters Database#replace_invalid_characters}
        :param replication: replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#replication Database#replication}
        :param storage_serialization_policy: The storage serialization policy for Iceberg tables that use Snowflake as the catalog. Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#storage_serialization_policy Database#storage_serialization_policy}
        :param suspend_task_after_num_failures: How many times a task must fail in a row before it is automatically suspended. 0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#suspend_task_after_num_failures Database#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#task_auto_retry_attempts Database#task_auto_retry_attempts}
        :param trace_level: Controls how trace events are ingested into the event table. Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#trace_level Database#trace_level}
        :param user_task_managed_initial_warehouse_size: The initial size of warehouse to use for managed warehouses in the absence of history. For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_managed_initial_warehouse_size Database#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_minimum_trigger_interval_in_seconds Database#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_timeout_ms Database#user_task_timeout_ms}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(replication, dict):
            replication = DatabaseReplication(**replication)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb9ea0f5460322c2aa412891dea0477deedf7145dc8a299456e1d66c88827d3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument data_retention_time_in_days", value=data_retention_time_in_days, expected_type=type_hints["data_retention_time_in_days"])
            check_type(argname="argument default_ddl_collation", value=default_ddl_collation, expected_type=type_hints["default_ddl_collation"])
            check_type(argname="argument drop_public_schema_on_creation", value=drop_public_schema_on_creation, expected_type=type_hints["drop_public_schema_on_creation"])
            check_type(argname="argument enable_console_output", value=enable_console_output, expected_type=type_hints["enable_console_output"])
            check_type(argname="argument external_volume", value=external_volume, expected_type=type_hints["external_volume"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_transient", value=is_transient, expected_type=type_hints["is_transient"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument max_data_extension_time_in_days", value=max_data_extension_time_in_days, expected_type=type_hints["max_data_extension_time_in_days"])
            check_type(argname="argument quoted_identifiers_ignore_case", value=quoted_identifiers_ignore_case, expected_type=type_hints["quoted_identifiers_ignore_case"])
            check_type(argname="argument replace_invalid_characters", value=replace_invalid_characters, expected_type=type_hints["replace_invalid_characters"])
            check_type(argname="argument replication", value=replication, expected_type=type_hints["replication"])
            check_type(argname="argument storage_serialization_policy", value=storage_serialization_policy, expected_type=type_hints["storage_serialization_policy"])
            check_type(argname="argument suspend_task_after_num_failures", value=suspend_task_after_num_failures, expected_type=type_hints["suspend_task_after_num_failures"])
            check_type(argname="argument task_auto_retry_attempts", value=task_auto_retry_attempts, expected_type=type_hints["task_auto_retry_attempts"])
            check_type(argname="argument trace_level", value=trace_level, expected_type=type_hints["trace_level"])
            check_type(argname="argument user_task_managed_initial_warehouse_size", value=user_task_managed_initial_warehouse_size, expected_type=type_hints["user_task_managed_initial_warehouse_size"])
            check_type(argname="argument user_task_minimum_trigger_interval_in_seconds", value=user_task_minimum_trigger_interval_in_seconds, expected_type=type_hints["user_task_minimum_trigger_interval_in_seconds"])
            check_type(argname="argument user_task_timeout_ms", value=user_task_timeout_ms, expected_type=type_hints["user_task_timeout_ms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if drop_public_schema_on_creation is not None:
            self._values["drop_public_schema_on_creation"] = drop_public_schema_on_creation
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
        if replication is not None:
            self._values["replication"] = replication
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
    def name(self) -> builtins.str:
        '''Specifies the identifier for the database;

        must be unique for your account. As a best practice for `Database Replication and Failover <https://docs.snowflake.com/en/user-guide/db-replication-intro>`_, it is recommended to give each secondary database the same name as its primary database. This practice supports referencing fully-qualified objects (i.e. '..') by other objects in the same database, such as querying a fully-qualified table name in a view. If a secondary database has a different name from the primary database, then these object references would break in the secondary database. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#name Database#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''The database parameter that specifies the default catalog to use for Iceberg tables. For more information, see `CATALOG <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#catalog Database#catalog}
        '''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#comment Database#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_retention_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the default Time Travel retention time for all schemas created in the database.

        For more details, see `Understanding & Using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#data_retention_time_in_days Database#data_retention_time_in_days}
        '''
        result = self._values.get("data_retention_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_ddl_collation(self) -> typing.Optional[builtins.str]:
        '''Specifies a default collation specification for all schemas and tables added to the database.

        It can be overridden on schema or table level. For more information, see `collation specification <https://docs.snowflake.com/en/sql-reference/collation#label-collation-specification>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#default_ddl_collation Database#default_ddl_collation}
        '''
        result = self._values.get("default_ddl_collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def drop_public_schema_on_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to drop public schema on creation or not.

        Modifying the parameter after database is already created won't have any effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#drop_public_schema_on_creation Database#drop_public_schema_on_creation}
        '''
        result = self._values.get("drop_public_schema_on_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_console_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, enables stdout/stderr fast path logging for anonymous stored procedures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#enable_console_output Database#enable_console_output}
        '''
        result = self._values.get("enable_console_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_volume(self) -> typing.Optional[builtins.str]:
        '''The database parameter that specifies the default external volume to use for Iceberg tables. For more information, see `EXTERNAL_VOLUME <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#external_volume Database#external_volume}
        '''
        result = self._values.get("external_volume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#id Database#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#is_transient Database#is_transient}
        '''
        result = self._values.get("is_transient")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the severity level of messages that should be ingested and made available in the active event table.

        Valid options are: [TRACE DEBUG INFO WARN ERROR FATAL OFF]. Messages at the specified level (and at more severe levels) are ingested. For more information, see `LOG_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#log_level Database#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_data_extension_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale.

        For a detailed description of this parameter, see `MAX_DATA_EXTENSION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters.html#label-max-data-extension-time-in-days>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#max_data_extension_time_in_days Database#max_data_extension_time_in_days}
        '''
        result = self._values.get("max_data_extension_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the case of quoted identifiers is ignored. For more information, see `QUOTED_IDENTIFIERS_IGNORE_CASE <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#quoted_identifiers_ignore_case Database#quoted_identifiers_ignore_case}
        '''
        result = self._values.get("quoted_identifiers_ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replace_invalid_characters(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an Iceberg table.

        You can only set this parameter for tables that use an external Iceberg catalog. For more information, see `REPLACE_INVALID_CHARACTERS <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#replace_invalid_characters Database#replace_invalid_characters}
        '''
        result = self._values.get("replace_invalid_characters")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replication(self) -> typing.Optional["DatabaseReplication"]:
        '''replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#replication Database#replication}
        '''
        result = self._values.get("replication")
        return typing.cast(typing.Optional["DatabaseReplication"], result)

    @builtins.property
    def storage_serialization_policy(self) -> typing.Optional[builtins.str]:
        '''The storage serialization policy for Iceberg tables that use Snowflake as the catalog.

        Valid options are: [COMPATIBLE OPTIMIZED]. COMPATIBLE: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines. OPTIMIZED: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake. For more information, see `STORAGE_SERIALIZATION_POLICY <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#storage_serialization_policy Database#storage_serialization_policy}
        '''
        result = self._values.get("storage_serialization_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspend_task_after_num_failures(self) -> typing.Optional[jsii.Number]:
        '''How many times a task must fail in a row before it is automatically suspended.

        0 disables auto-suspending. For more information, see `SUSPEND_TASK_AFTER_NUM_FAILURES <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#suspend_task_after_num_failures Database#suspend_task_after_num_failures}
        '''
        result = self._values.get("suspend_task_after_num_failures")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_auto_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Maximum automatic retries allowed for a user task. For more information, see `TASK_AUTO_RETRY_ATTEMPTS <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#task_auto_retry_attempts Database#task_auto_retry_attempts}
        '''
        result = self._values.get("task_auto_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Controls how trace events are ingested into the event table.

        Valid options are: [ALWAYS ON_EVENT OFF]. For information about levels, see `TRACE_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters.html#label-trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#trace_level Database#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_task_managed_initial_warehouse_size(self) -> typing.Optional[builtins.str]:
        '''The initial size of warehouse to use for managed warehouses in the absence of history.

        For more information, see `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_managed_initial_warehouse_size Database#user_task_managed_initial_warehouse_size}
        '''
        result = self._values.get("user_task_managed_initial_warehouse_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_task_minimum_trigger_interval_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Minimum amount of time between Triggered Task executions in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_minimum_trigger_interval_in_seconds Database#user_task_minimum_trigger_interval_in_seconds}
        '''
        result = self._values.get("user_task_minimum_trigger_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_task_timeout_ms(self) -> typing.Optional[jsii.Number]:
        '''User task execution timeout in milliseconds. For more information, see `USER_TASK_TIMEOUT_MS <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#user_task_timeout_ms Database#user_task_timeout_ms}
        '''
        result = self._values.get("user_task_timeout_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.database.DatabaseReplication",
    jsii_struct_bases=[],
    name_mapping={
        "enable_to_account": "enableToAccount",
        "ignore_edition_check": "ignoreEditionCheck",
    },
)
class DatabaseReplication:
    def __init__(
        self,
        *,
        enable_to_account: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseReplicationEnableToAccount", typing.Dict[builtins.str, typing.Any]]]],
        ignore_edition_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_to_account: enable_to_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#enable_to_account Database#enable_to_account}
        :param ignore_edition_check: Allows replicating data to accounts on lower editions in either of the following scenarios: 1. The primary database is in a Business Critical (or higher) account but one or more of the accounts approved for replication are on lower editions. Business Critical Edition is intended for Snowflake accounts with extremely sensitive data. 2. The primary database is in a Business Critical (or higher) account and a signed business associate agreement is in place to store PHI data in the account per HIPAA and HITRUST regulations, but no such agreement is in place for one or more of the accounts approved for replication, regardless if they are Business Critical (or higher) accounts. Both scenarios are prohibited by default in an effort to help prevent account administrators for Business Critical (or higher) accounts from inadvertently replicating sensitive data to accounts on lower editions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#ignore_edition_check Database#ignore_edition_check}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d8fe52074244d27751ea6941f76b0092ada9d1a95d3405ec863597bf12fb44)
            check_type(argname="argument enable_to_account", value=enable_to_account, expected_type=type_hints["enable_to_account"])
            check_type(argname="argument ignore_edition_check", value=ignore_edition_check, expected_type=type_hints["ignore_edition_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_to_account": enable_to_account,
        }
        if ignore_edition_check is not None:
            self._values["ignore_edition_check"] = ignore_edition_check

    @builtins.property
    def enable_to_account(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseReplicationEnableToAccount"]]:
        '''enable_to_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#enable_to_account Database#enable_to_account}
        '''
        result = self._values.get("enable_to_account")
        assert result is not None, "Required property 'enable_to_account' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseReplicationEnableToAccount"]], result)

    @builtins.property
    def ignore_edition_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allows replicating data to accounts on lower editions in either of the following scenarios: 1.

        The primary database is in a Business Critical (or higher) account but one or more of the accounts approved for replication are on lower editions. Business Critical Edition is intended for Snowflake accounts with extremely sensitive data. 2. The primary database is in a Business Critical (or higher) account and a signed business associate agreement is in place to store PHI data in the account per HIPAA and HITRUST regulations, but no such agreement is in place for one or more of the accounts approved for replication, regardless if they are Business Critical (or higher) accounts. Both scenarios are prohibited by default in an effort to help prevent account administrators for Business Critical (or higher) accounts from inadvertently replicating sensitive data to accounts on lower editions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#ignore_edition_check Database#ignore_edition_check}
        '''
        result = self._values.get("ignore_edition_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.database.DatabaseReplicationEnableToAccount",
    jsii_struct_bases=[],
    name_mapping={
        "account_identifier": "accountIdentifier",
        "with_failover": "withFailover",
    },
)
class DatabaseReplicationEnableToAccount:
    def __init__(
        self,
        *,
        account_identifier: builtins.str,
        with_failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param account_identifier: Specifies account identifier for which replication should be enabled. The account identifiers should be in the form of ``"<organization_name>"."<account_name>"``. For more information about this resource, see `docs <./account>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#account_identifier Database#account_identifier}
        :param with_failover: Specifies if failover should be enabled for the specified account identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#with_failover Database#with_failover}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96e1b40a6ab70351b39483fefdf7f09990b1b7613be1d137b6da7861a4f1234)
            check_type(argname="argument account_identifier", value=account_identifier, expected_type=type_hints["account_identifier"])
            check_type(argname="argument with_failover", value=with_failover, expected_type=type_hints["with_failover"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_identifier": account_identifier,
        }
        if with_failover is not None:
            self._values["with_failover"] = with_failover

    @builtins.property
    def account_identifier(self) -> builtins.str:
        '''Specifies account identifier for which replication should be enabled.

        The account identifiers should be in the form of ``"<organization_name>"."<account_name>"``. For more information about this resource, see `docs <./account>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#account_identifier Database#account_identifier}
        '''
        result = self._values.get("account_identifier")
        assert result is not None, "Required property 'account_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def with_failover(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if failover should be enabled for the specified account identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/database#with_failover Database#with_failover}
        '''
        result = self._values.get("with_failover")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseReplicationEnableToAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseReplicationEnableToAccountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.database.DatabaseReplicationEnableToAccountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b4ac0816e60076ca2b6be3f42b59a47a4c5c9dd1ae4b934f8f8c3a08f03dc17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseReplicationEnableToAccountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1836b755365329ae64f53a80b1aa64c0dd0ed90ca939ceb09ac9947a7af3897)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseReplicationEnableToAccountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f38afd329f74f78f8ab97fd41fe2ba171580a558a07cba206f9583678c4e4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abfdf749f7a512f77f93c7a5b362254ec453751edf1cf5e621ba8aafbbaa7907)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8c8204423a534fd8864370b3798809ffa3797647536b9f4738b6c34854bc1da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseReplicationEnableToAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseReplicationEnableToAccount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseReplicationEnableToAccount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0b358cffd9d05116c0183acf4ea2b53a5b9448ee0584eb4549b3494d41467f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseReplicationEnableToAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.database.DatabaseReplicationEnableToAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b14e785a181922a08c6d223ea1ae142b8a604a1fa0576f51390e819156d537e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWithFailover")
    def reset_with_failover(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithFailover", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdentifierInput")
    def account_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="withFailoverInput")
    def with_failover_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withFailoverInput"))

    @builtins.property
    @jsii.member(jsii_name="accountIdentifier")
    def account_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountIdentifier"))

    @account_identifier.setter
    def account_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e7a600fde73b76f876e689b0d04db9838ddeaa4a32ed12c37a7de176e1eadc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="withFailover")
    def with_failover(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withFailover"))

    @with_failover.setter
    def with_failover(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5f19b61c4404e20585a912f29eb7bd13ef3e27c8b01f87eb5b7d655260e840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withFailover", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseReplicationEnableToAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseReplicationEnableToAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseReplicationEnableToAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cebd1617a8b58d4f1fed0d4dce5df11ed787c27e0e80d636cdff6e266403653c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DatabaseReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.database.DatabaseReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e07d0f188a06a03623471363f31b6371ee0bbae0c9d714bb904914d708b376e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnableToAccount")
    def put_enable_to_account(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseReplicationEnableToAccount, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8092aa4c8319a3e2cc1517ac370bc66b16afb90cfabdcdab84fb9c0f868b5f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnableToAccount", [value]))

    @jsii.member(jsii_name="resetIgnoreEditionCheck")
    def reset_ignore_edition_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreEditionCheck", []))

    @builtins.property
    @jsii.member(jsii_name="enableToAccount")
    def enable_to_account(self) -> DatabaseReplicationEnableToAccountList:
        return typing.cast(DatabaseReplicationEnableToAccountList, jsii.get(self, "enableToAccount"))

    @builtins.property
    @jsii.member(jsii_name="enableToAccountInput")
    def enable_to_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseReplicationEnableToAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseReplicationEnableToAccount]]], jsii.get(self, "enableToAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreEditionCheckInput")
    def ignore_edition_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreEditionCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreEditionCheck")
    def ignore_edition_check(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreEditionCheck"))

    @ignore_edition_check.setter
    def ignore_edition_check(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f9326d956d1612762ee5381a19039996b73c1736fdf303c121c5588d0dcf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreEditionCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatabaseReplication]:
        return typing.cast(typing.Optional[DatabaseReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DatabaseReplication]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03836f781862a4babad8fc4f9dfd4673603c00c4bf5247604afab5b2b41e1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Database",
    "DatabaseConfig",
    "DatabaseReplication",
    "DatabaseReplicationEnableToAccount",
    "DatabaseReplicationEnableToAccountList",
    "DatabaseReplicationEnableToAccountOutputReference",
    "DatabaseReplicationOutputReference",
]

publication.publish()

def _typecheckingstub__b15a50f89eb08aece66579f840c6fa677da88eecbc745d8303f4003e46439abf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    catalog: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    drop_public_schema_on_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_volume: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_transient: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replication: typing.Optional[typing.Union[DatabaseReplication, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e77891cb77202232aa5fdff4adeab90ba3a5bb42678747f900a74c6a3daa469f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f309e0e1018d51444b8f2afa705855d5ca326852a42242415a4f8a9a197edba5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2a89dc8f0fc5f4ebbf143fe2e8f7040b61e3933fbac91752a1ed3b7e53e18a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca2c028304080fa7ff570057044330e7d313c3be453bcf132c534f78bf04959(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ef76a5d17a3dae9ed5724e03411a1c64dbfde6ab45e79c1deb00854d95aa98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e53bdc1ef24de42393b2819101ee8a214358f28a563b749ad5bf37cecd1e25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de99fa10800fb2fc8f4c25056c98e5a376c4522fa62dc100064fbe1bec7835f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7415dcaabccd7a229632856cdfe9a4fbd8f773501b44bd5a3bd97b44e0197d82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd1d980fc53ae3767f84154ae86a1f0f7561231ff3245856409f992ab3ca540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c2a7b99e3b917074cd9fbd8d72667638938c3856367106165056bde52ffda8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f616d4976048c49ec40fa3661a4b513b4ffcc948022260ccff0a37e1764274(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c628d88e1ca4bf1b1ed180cb42db69c2051e46dd4b62ecf86b72d5deb8b4200(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbccc96209c6e09ec18d2d3fc2bf18fc780c674c489bd1dee20dac62996024d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30667c5f6b701dc74caa58b77c80f903502c3c111e029a6e9c3787b3d9d41ffa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387fd8556e8c1ae5976c2167b9d8fadf022fc6e3e1acf2f3104ec86dd40034f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae374394ea2270fc09f92f5ef9a66ad054bda9979169704635c1cc5a0a2af6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c12beae95b66965d287f3af9adfad9ac15a7826d12ec77795b8b18274fbdc1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f497ba4d7ef61f6b034ab97e09a77688c2fc3e9345d7fa37f4129daf90f7c5e2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af3a0b7cbd3f8fa9a3d0c6909b7bcbc9bf8358dc690abfd807a2c5ba31d2c4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7988b50cbe076cda8dca3408ec8cee6d1cf370f151d071be0f2ebc172303b2e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce42b54e786aad937cdd7e034bcd27bbde1e8c18a3b24cb3bed72907875ceacd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40ed1e11565dfd6c6281d687c85e775c307a45a2004f678d3aa6bc924e36bc6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb9ea0f5460322c2aa412891dea0477deedf7145dc8a299456e1d66c88827d3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    catalog: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    drop_public_schema_on_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_volume: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    is_transient: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replication: typing.Optional[typing.Union[DatabaseReplication, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f4d8fe52074244d27751ea6941f76b0092ada9d1a95d3405ec863597bf12fb44(
    *,
    enable_to_account: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseReplicationEnableToAccount, typing.Dict[builtins.str, typing.Any]]]],
    ignore_edition_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96e1b40a6ab70351b39483fefdf7f09990b1b7613be1d137b6da7861a4f1234(
    *,
    account_identifier: builtins.str,
    with_failover: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4ac0816e60076ca2b6be3f42b59a47a4c5c9dd1ae4b934f8f8c3a08f03dc17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1836b755365329ae64f53a80b1aa64c0dd0ed90ca939ceb09ac9947a7af3897(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f38afd329f74f78f8ab97fd41fe2ba171580a558a07cba206f9583678c4e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfdf749f7a512f77f93c7a5b362254ec453751edf1cf5e621ba8aafbbaa7907(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c8204423a534fd8864370b3798809ffa3797647536b9f4738b6c34854bc1da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0b358cffd9d05116c0183acf4ea2b53a5b9448ee0584eb4549b3494d41467f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseReplicationEnableToAccount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b14e785a181922a08c6d223ea1ae142b8a604a1fa0576f51390e819156d537e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e7a600fde73b76f876e689b0d04db9838ddeaa4a32ed12c37a7de176e1eadc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5f19b61c4404e20585a912f29eb7bd13ef3e27c8b01f87eb5b7d655260e840(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebd1617a8b58d4f1fed0d4dce5df11ed787c27e0e80d636cdff6e266403653c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseReplicationEnableToAccount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e07d0f188a06a03623471363f31b6371ee0bbae0c9d714bb904914d708b376e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8092aa4c8319a3e2cc1517ac370bc66b16afb90cfabdcdab84fb9c0f868b5f96(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseReplicationEnableToAccount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f9326d956d1612762ee5381a19039996b73c1736fdf303c121c5588d0dcf94(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03836f781862a4babad8fc4f9dfd4673603c00c4bf5247604afab5b2b41e1b5(
    value: typing.Optional[DatabaseReplication],
) -> None:
    """Type checking stubs"""
    pass
