r'''
# `snowflake_task`

Refer to the Terraform Registry for docs: [`snowflake_task`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task).
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


class Task(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.Task",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task snowflake_task}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        sql_statement: builtins.str,
        started: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        after: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_overlapping_execution: typing.Optional[builtins.str] = None,
        autocommit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        binary_input_format: typing.Optional[builtins.str] = None,
        binary_output_format: typing.Optional[builtins.str] = None,
        client_memory_limit: typing.Optional[jsii.Number] = None,
        client_metadata_request_use_connection_ctx: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_prefetch_threads: typing.Optional[jsii.Number] = None,
        client_result_chunk_size: typing.Optional[jsii.Number] = None,
        client_result_column_case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_session_keep_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_session_keep_alive_heartbeat_frequency: typing.Optional[jsii.Number] = None,
        client_timestamp_type_mapping: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        config: typing.Optional[builtins.str] = None,
        date_input_format: typing.Optional[builtins.str] = None,
        date_output_format: typing.Optional[builtins.str] = None,
        enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_integration: typing.Optional[builtins.str] = None,
        error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        finalize: typing.Optional[builtins.str] = None,
        geography_output_format: typing.Optional[builtins.str] = None,
        geometry_output_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_indent: typing.Optional[jsii.Number] = None,
        lock_timeout: typing.Optional[jsii.Number] = None,
        log_level: typing.Optional[builtins.str] = None,
        multi_statement_count: typing.Optional[jsii.Number] = None,
        noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_tag: typing.Optional[builtins.str] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rows_per_resultset: typing.Optional[jsii.Number] = None,
        s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["TaskSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        search_path: typing.Optional[builtins.str] = None,
        statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
        task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
        time_input_format: typing.Optional[builtins.str] = None,
        time_output_format: typing.Optional[builtins.str] = None,
        timestamp_day_is_always24_h: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timestamp_input_format: typing.Optional[builtins.str] = None,
        timestamp_ltz_output_format: typing.Optional[builtins.str] = None,
        timestamp_ntz_output_format: typing.Optional[builtins.str] = None,
        timestamp_output_format: typing.Optional[builtins.str] = None,
        timestamp_type_mapping: typing.Optional[builtins.str] = None,
        timestamp_tz_output_format: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
        trace_level: typing.Optional[builtins.str] = None,
        transaction_abort_on_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transaction_default_isolation_level: typing.Optional[builtins.str] = None,
        two_digit_century_start: typing.Optional[jsii.Number] = None,
        unsupported_ddl_action: typing.Optional[builtins.str] = None,
        use_cached_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
        user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
        user_task_timeout_ms: typing.Optional[jsii.Number] = None,
        warehouse: typing.Optional[builtins.str] = None,
        week_of_year_policy: typing.Optional[jsii.Number] = None,
        week_start: typing.Optional[jsii.Number] = None,
        when: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task snowflake_task} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the task. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#database Task#database}
        :param name: Specifies the identifier for the task; must be unique for the database and schema in which the task is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#name Task#name}
        :param schema: The schema in which to create the task. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#schema Task#schema}
        :param sql_statement: Any single SQL statement, or a call to a stored procedure, executed when the task runs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#sql_statement Task#sql_statement}
        :param started: Specifies if the task should be started or suspended. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#started Task#started}
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#abort_detached_query Task#abort_detached_query}
        :param after: Specifies one or more predecessor tasks for the current task. Use this option to `create a DAG <https://docs.snowflake.com/en/user-guide/tasks-graphs.html#label-task-dag>`_ of tasks or add this task to an existing DAG. A DAG is a series of tasks that starts with a scheduled root task and is linked together by dependencies. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#after Task#after}
        :param allow_overlapping_execution: By default, Snowflake ensures that only one instance of a particular DAG is allowed to run at a time, setting the parameter value to TRUE permits DAG runs to overlap. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#allow_overlapping_execution Task#allow_overlapping_execution}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#autocommit Task#autocommit}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#binary_input_format Task#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#binary_output_format Task#binary_output_format}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_memory_limit Task#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_metadata_request_use_connection_ctx Task#client_metadata_request_use_connection_ctx}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_prefetch_threads Task#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_result_chunk_size Task#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_result_column_case_insensitive Task#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_session_keep_alive Task#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_session_keep_alive_heartbeat_frequency Task#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_timestamp_type_mapping Task#client_timestamp_type_mapping}
        :param comment: Specifies a comment for the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#comment Task#comment}
        :param config: Specifies a string representation of key value pairs that can be accessed by all tasks in the task graph. Must be in JSON format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#config Task#config}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#date_input_format Task#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#date_output_format Task#date_output_format}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#enable_unload_physical_type_optimization Task#enable_unload_physical_type_optimization}
        :param error_integration: Specifies the name of the notification integration used for error notifications. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./notification_integration>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_integration Task#error_integration}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_on_nondeterministic_merge Task#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_on_nondeterministic_update Task#error_on_nondeterministic_update}
        :param finalize: Specifies the name of a root task that the finalizer task is associated with. Finalizer tasks run after all other tasks in the task graph run to completion. You can define the SQL of a finalizer task to handle notifications and the release and cleanup of resources that a task graph uses. For more information, see `Release and cleanup of task graphs <https://docs.snowflake.com/en/user-guide/tasks-graphs.html#label-finalizer-task>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#finalize Task#finalize}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#geography_output_format Task#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#geometry_output_format Task#geometry_output_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#id Task#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#jdbc_treat_timestamp_ntz_as_utc Task#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#jdbc_use_session_timezone Task#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#json_indent Task#json_indent}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#lock_timeout Task#lock_timeout}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#log_level Task#log_level}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#multi_statement_count Task#multi_statement_count}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#noorder_sequence_as_default Task#noorder_sequence_as_default}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#odbc_treat_decimal_as_int Task#odbc_treat_decimal_as_int}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#query_tag Task#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#quoted_identifiers_ignore_case Task#quoted_identifiers_ignore_case}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#rows_per_resultset Task#rows_per_resultset}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#s3_stage_vpce_dns_name Task#s3_stage_vpce_dns_name}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#schedule Task#schedule}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#search_path Task#search_path}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#statement_queued_timeout_in_seconds Task#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#statement_timeout_in_seconds Task#statement_timeout_in_seconds}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#strict_json_output Task#strict_json_output}
        :param suspend_task_after_num_failures: Specifies the number of consecutive failed task runs after which the current task is suspended automatically. The default is 0 (no automatic suspension). For more information, check `SUSPEND_TASK_AFTER_NUM_FAILURES docs <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#suspend_task_after_num_failures Task#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Specifies the number of automatic task graph retry attempts. If any task graphs complete in a FAILED state, Snowflake can automatically retry the task graphs from the last task in the graph that failed. For more information, check `TASK_AUTO_RETRY_ATTEMPTS docs <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#task_auto_retry_attempts Task#task_auto_retry_attempts}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#time_input_format Task#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#time_output_format Task#time_output_format}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_day_is_always_24h Task#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_input_format Task#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_ltz_output_format Task#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_ntz_output_format Task#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_output_format Task#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_type_mapping Task#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_tz_output_format Task#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timezone Task#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#trace_level Task#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#transaction_abort_on_error Task#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#transaction_default_isolation_level Task#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#two_digit_century_start Task#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#unsupported_ddl_action Task#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#use_cached_result Task#use_cached_result}
        :param user_task_managed_initial_warehouse_size: Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size. Once a task has successfully completed a few runs, Snowflake ignores this parameter setting. Valid values are (case-insensitive): %s. (Conflicts with warehouse). For more information about warehouses, see `docs <./warehouse>`_. For more information, check `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_managed_initial_warehouse_size Task#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds For more information, check `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-minimum-trigger-interval-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_minimum_trigger_interval_in_seconds Task#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: Specifies the time limit on a single run of the task before it times out (in milliseconds). For more information, check `USER_TASK_TIMEOUT_MS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_timeout_ms Task#user_task_timeout_ms}
        :param warehouse: The warehouse the task will use. Omit this parameter to use Snowflake-managed compute resources for runs of this task. Due to Snowflake limitations warehouse identifier can consist of only upper-cased letters. (Conflicts with user_task_managed_initial_warehouse_size) For more information about this resource, see `docs <./warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#warehouse Task#warehouse}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#week_of_year_policy Task#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#week_start Task#week_start}
        :param when: Specifies a Boolean SQL expression; multiple conditions joined with AND/OR are supported. When a task is triggered (based on its SCHEDULE or AFTER setting), it validates the conditions of the expression to determine whether to execute. If the conditions of the expression are not met, then the task skips the current run. Any tasks that identify this task as a predecessor also don’t run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#when Task#when}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ea4604358bdf109eaf78f231f37e685f614aef5f8076778e9130b15f8df16b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = TaskConfig(
            database=database,
            name=name,
            schema=schema,
            sql_statement=sql_statement,
            started=started,
            abort_detached_query=abort_detached_query,
            after=after,
            allow_overlapping_execution=allow_overlapping_execution,
            autocommit=autocommit,
            binary_input_format=binary_input_format,
            binary_output_format=binary_output_format,
            client_memory_limit=client_memory_limit,
            client_metadata_request_use_connection_ctx=client_metadata_request_use_connection_ctx,
            client_prefetch_threads=client_prefetch_threads,
            client_result_chunk_size=client_result_chunk_size,
            client_result_column_case_insensitive=client_result_column_case_insensitive,
            client_session_keep_alive=client_session_keep_alive,
            client_session_keep_alive_heartbeat_frequency=client_session_keep_alive_heartbeat_frequency,
            client_timestamp_type_mapping=client_timestamp_type_mapping,
            comment=comment,
            config=config,
            date_input_format=date_input_format,
            date_output_format=date_output_format,
            enable_unload_physical_type_optimization=enable_unload_physical_type_optimization,
            error_integration=error_integration,
            error_on_nondeterministic_merge=error_on_nondeterministic_merge,
            error_on_nondeterministic_update=error_on_nondeterministic_update,
            finalize=finalize,
            geography_output_format=geography_output_format,
            geometry_output_format=geometry_output_format,
            id=id,
            jdbc_treat_timestamp_ntz_as_utc=jdbc_treat_timestamp_ntz_as_utc,
            jdbc_use_session_timezone=jdbc_use_session_timezone,
            json_indent=json_indent,
            lock_timeout=lock_timeout,
            log_level=log_level,
            multi_statement_count=multi_statement_count,
            noorder_sequence_as_default=noorder_sequence_as_default,
            odbc_treat_decimal_as_int=odbc_treat_decimal_as_int,
            query_tag=query_tag,
            quoted_identifiers_ignore_case=quoted_identifiers_ignore_case,
            rows_per_resultset=rows_per_resultset,
            s3_stage_vpce_dns_name=s3_stage_vpce_dns_name,
            schedule=schedule,
            search_path=search_path,
            statement_queued_timeout_in_seconds=statement_queued_timeout_in_seconds,
            statement_timeout_in_seconds=statement_timeout_in_seconds,
            strict_json_output=strict_json_output,
            suspend_task_after_num_failures=suspend_task_after_num_failures,
            task_auto_retry_attempts=task_auto_retry_attempts,
            time_input_format=time_input_format,
            time_output_format=time_output_format,
            timestamp_day_is_always24_h=timestamp_day_is_always24_h,
            timestamp_input_format=timestamp_input_format,
            timestamp_ltz_output_format=timestamp_ltz_output_format,
            timestamp_ntz_output_format=timestamp_ntz_output_format,
            timestamp_output_format=timestamp_output_format,
            timestamp_type_mapping=timestamp_type_mapping,
            timestamp_tz_output_format=timestamp_tz_output_format,
            timezone=timezone,
            trace_level=trace_level,
            transaction_abort_on_error=transaction_abort_on_error,
            transaction_default_isolation_level=transaction_default_isolation_level,
            two_digit_century_start=two_digit_century_start,
            unsupported_ddl_action=unsupported_ddl_action,
            use_cached_result=use_cached_result,
            user_task_managed_initial_warehouse_size=user_task_managed_initial_warehouse_size,
            user_task_minimum_trigger_interval_in_seconds=user_task_minimum_trigger_interval_in_seconds,
            user_task_timeout_ms=user_task_timeout_ms,
            warehouse=warehouse,
            week_of_year_policy=week_of_year_policy,
            week_start=week_start,
            when=when,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Task resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Task to import.
        :param import_from_id: The id of the existing Task that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Task to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d8c59b01adbf5f8e29e6c733dbd841414111ef772ca196ca2e258f5461e7d29)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        minutes: typing.Optional[jsii.Number] = None,
        using_cron: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minutes: Specifies an interval (in minutes) of wait time inserted between runs of the task. Accepts positive integers only. (conflicts with ``using_cron``) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#minutes Task#minutes}
        :param using_cron: Specifies a cron expression and time zone for periodically running the task. Supports a subset of standard cron utility syntax. (conflicts with ``minutes``) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#using_cron Task#using_cron}
        '''
        value = TaskSchedule(minutes=minutes, using_cron=using_cron)

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetAbortDetachedQuery")
    def reset_abort_detached_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbortDetachedQuery", []))

    @jsii.member(jsii_name="resetAfter")
    def reset_after(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAfter", []))

    @jsii.member(jsii_name="resetAllowOverlappingExecution")
    def reset_allow_overlapping_execution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowOverlappingExecution", []))

    @jsii.member(jsii_name="resetAutocommit")
    def reset_autocommit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutocommit", []))

    @jsii.member(jsii_name="resetBinaryInputFormat")
    def reset_binary_input_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryInputFormat", []))

    @jsii.member(jsii_name="resetBinaryOutputFormat")
    def reset_binary_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryOutputFormat", []))

    @jsii.member(jsii_name="resetClientMemoryLimit")
    def reset_client_memory_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientMemoryLimit", []))

    @jsii.member(jsii_name="resetClientMetadataRequestUseConnectionCtx")
    def reset_client_metadata_request_use_connection_ctx(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientMetadataRequestUseConnectionCtx", []))

    @jsii.member(jsii_name="resetClientPrefetchThreads")
    def reset_client_prefetch_threads(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientPrefetchThreads", []))

    @jsii.member(jsii_name="resetClientResultChunkSize")
    def reset_client_result_chunk_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientResultChunkSize", []))

    @jsii.member(jsii_name="resetClientResultColumnCaseInsensitive")
    def reset_client_result_column_case_insensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientResultColumnCaseInsensitive", []))

    @jsii.member(jsii_name="resetClientSessionKeepAlive")
    def reset_client_session_keep_alive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSessionKeepAlive", []))

    @jsii.member(jsii_name="resetClientSessionKeepAliveHeartbeatFrequency")
    def reset_client_session_keep_alive_heartbeat_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSessionKeepAliveHeartbeatFrequency", []))

    @jsii.member(jsii_name="resetClientTimestampTypeMapping")
    def reset_client_timestamp_type_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTimestampTypeMapping", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetDateInputFormat")
    def reset_date_input_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateInputFormat", []))

    @jsii.member(jsii_name="resetDateOutputFormat")
    def reset_date_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateOutputFormat", []))

    @jsii.member(jsii_name="resetEnableUnloadPhysicalTypeOptimization")
    def reset_enable_unload_physical_type_optimization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUnloadPhysicalTypeOptimization", []))

    @jsii.member(jsii_name="resetErrorIntegration")
    def reset_error_integration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorIntegration", []))

    @jsii.member(jsii_name="resetErrorOnNondeterministicMerge")
    def reset_error_on_nondeterministic_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOnNondeterministicMerge", []))

    @jsii.member(jsii_name="resetErrorOnNondeterministicUpdate")
    def reset_error_on_nondeterministic_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOnNondeterministicUpdate", []))

    @jsii.member(jsii_name="resetFinalize")
    def reset_finalize(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFinalize", []))

    @jsii.member(jsii_name="resetGeographyOutputFormat")
    def reset_geography_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeographyOutputFormat", []))

    @jsii.member(jsii_name="resetGeometryOutputFormat")
    def reset_geometry_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeometryOutputFormat", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJdbcTreatTimestampNtzAsUtc")
    def reset_jdbc_treat_timestamp_ntz_as_utc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJdbcTreatTimestampNtzAsUtc", []))

    @jsii.member(jsii_name="resetJdbcUseSessionTimezone")
    def reset_jdbc_use_session_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJdbcUseSessionTimezone", []))

    @jsii.member(jsii_name="resetJsonIndent")
    def reset_json_indent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonIndent", []))

    @jsii.member(jsii_name="resetLockTimeout")
    def reset_lock_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockTimeout", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetMultiStatementCount")
    def reset_multi_statement_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiStatementCount", []))

    @jsii.member(jsii_name="resetNoorderSequenceAsDefault")
    def reset_noorder_sequence_as_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoorderSequenceAsDefault", []))

    @jsii.member(jsii_name="resetOdbcTreatDecimalAsInt")
    def reset_odbc_treat_decimal_as_int(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOdbcTreatDecimalAsInt", []))

    @jsii.member(jsii_name="resetQueryTag")
    def reset_query_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryTag", []))

    @jsii.member(jsii_name="resetQuotedIdentifiersIgnoreCase")
    def reset_quoted_identifiers_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotedIdentifiersIgnoreCase", []))

    @jsii.member(jsii_name="resetRowsPerResultset")
    def reset_rows_per_resultset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowsPerResultset", []))

    @jsii.member(jsii_name="resetS3StageVpceDnsName")
    def reset_s3_stage_vpce_dns_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3StageVpceDnsName", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetSearchPath")
    def reset_search_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchPath", []))

    @jsii.member(jsii_name="resetStatementQueuedTimeoutInSeconds")
    def reset_statement_queued_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementQueuedTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetStatementTimeoutInSeconds")
    def reset_statement_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetStrictJsonOutput")
    def reset_strict_json_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictJsonOutput", []))

    @jsii.member(jsii_name="resetSuspendTaskAfterNumFailures")
    def reset_suspend_task_after_num_failures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspendTaskAfterNumFailures", []))

    @jsii.member(jsii_name="resetTaskAutoRetryAttempts")
    def reset_task_auto_retry_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskAutoRetryAttempts", []))

    @jsii.member(jsii_name="resetTimeInputFormat")
    def reset_time_input_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeInputFormat", []))

    @jsii.member(jsii_name="resetTimeOutputFormat")
    def reset_time_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeOutputFormat", []))

    @jsii.member(jsii_name="resetTimestampDayIsAlways24H")
    def reset_timestamp_day_is_always24_h(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampDayIsAlways24H", []))

    @jsii.member(jsii_name="resetTimestampInputFormat")
    def reset_timestamp_input_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampInputFormat", []))

    @jsii.member(jsii_name="resetTimestampLtzOutputFormat")
    def reset_timestamp_ltz_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampLtzOutputFormat", []))

    @jsii.member(jsii_name="resetTimestampNtzOutputFormat")
    def reset_timestamp_ntz_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampNtzOutputFormat", []))

    @jsii.member(jsii_name="resetTimestampOutputFormat")
    def reset_timestamp_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampOutputFormat", []))

    @jsii.member(jsii_name="resetTimestampTypeMapping")
    def reset_timestamp_type_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampTypeMapping", []))

    @jsii.member(jsii_name="resetTimestampTzOutputFormat")
    def reset_timestamp_tz_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampTzOutputFormat", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @jsii.member(jsii_name="resetTraceLevel")
    def reset_trace_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraceLevel", []))

    @jsii.member(jsii_name="resetTransactionAbortOnError")
    def reset_transaction_abort_on_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransactionAbortOnError", []))

    @jsii.member(jsii_name="resetTransactionDefaultIsolationLevel")
    def reset_transaction_default_isolation_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransactionDefaultIsolationLevel", []))

    @jsii.member(jsii_name="resetTwoDigitCenturyStart")
    def reset_two_digit_century_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwoDigitCenturyStart", []))

    @jsii.member(jsii_name="resetUnsupportedDdlAction")
    def reset_unsupported_ddl_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnsupportedDdlAction", []))

    @jsii.member(jsii_name="resetUseCachedResult")
    def reset_use_cached_result(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCachedResult", []))

    @jsii.member(jsii_name="resetUserTaskManagedInitialWarehouseSize")
    def reset_user_task_managed_initial_warehouse_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTaskManagedInitialWarehouseSize", []))

    @jsii.member(jsii_name="resetUserTaskMinimumTriggerIntervalInSeconds")
    def reset_user_task_minimum_trigger_interval_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTaskMinimumTriggerIntervalInSeconds", []))

    @jsii.member(jsii_name="resetUserTaskTimeoutMs")
    def reset_user_task_timeout_ms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTaskTimeoutMs", []))

    @jsii.member(jsii_name="resetWarehouse")
    def reset_warehouse(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarehouse", []))

    @jsii.member(jsii_name="resetWeekOfYearPolicy")
    def reset_week_of_year_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekOfYearPolicy", []))

    @jsii.member(jsii_name="resetWeekStart")
    def reset_week_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekStart", []))

    @jsii.member(jsii_name="resetWhen")
    def reset_when(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhen", []))

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
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "TaskParametersList":
        return typing.cast("TaskParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "TaskScheduleOutputReference":
        return typing.cast("TaskScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "TaskShowOutputList":
        return typing.cast("TaskShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="abortDetachedQueryInput")
    def abort_detached_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "abortDetachedQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="afterInput")
    def after_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "afterInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOverlappingExecutionInput")
    def allow_overlapping_execution_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowOverlappingExecutionInput"))

    @builtins.property
    @jsii.member(jsii_name="autocommitInput")
    def autocommit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autocommitInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormatInput")
    def binary_input_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryInputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormatInput")
    def binary_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimitInput")
    def client_memory_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientMemoryLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="clientMetadataRequestUseConnectionCtxInput")
    def client_metadata_request_use_connection_ctx_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientMetadataRequestUseConnectionCtxInput"))

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreadsInput")
    def client_prefetch_threads_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientPrefetchThreadsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSizeInput")
    def client_result_chunk_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientResultChunkSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="clientResultColumnCaseInsensitiveInput")
    def client_result_column_case_insensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientResultColumnCaseInsensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequencyInput")
    def client_session_keep_alive_heartbeat_frequency_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientSessionKeepAliveHeartbeatFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveInput")
    def client_session_keep_alive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientSessionKeepAliveInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMappingInput")
    def client_timestamp_type_mapping_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientTimestampTypeMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="dateInputFormatInput")
    def date_input_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateInputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormatInput")
    def date_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="enableUnloadPhysicalTypeOptimizationInput")
    def enable_unload_physical_type_optimization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableUnloadPhysicalTypeOptimizationInput"))

    @builtins.property
    @jsii.member(jsii_name="errorIntegrationInput")
    def error_integration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "errorIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicMergeInput")
    def error_on_nondeterministic_merge_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "errorOnNondeterministicMergeInput"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicUpdateInput")
    def error_on_nondeterministic_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "errorOnNondeterministicUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="finalizeInput")
    def finalize_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "finalizeInput"))

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormatInput")
    def geography_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geographyOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormatInput")
    def geometry_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geometryOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatTimestampNtzAsUtcInput")
    def jdbc_treat_timestamp_ntz_as_utc_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jdbcTreatTimestampNtzAsUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="jdbcUseSessionTimezoneInput")
    def jdbc_use_session_timezone_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jdbcUseSessionTimezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonIndentInput")
    def json_indent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jsonIndentInput"))

    @builtins.property
    @jsii.member(jsii_name="lockTimeoutInput")
    def lock_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lockTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="multiStatementCountInput")
    def multi_statement_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "multiStatementCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="noorderSequenceAsDefaultInput")
    def noorder_sequence_as_default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noorderSequenceAsDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="odbcTreatDecimalAsIntInput")
    def odbc_treat_decimal_as_int_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "odbcTreatDecimalAsIntInput"))

    @builtins.property
    @jsii.member(jsii_name="queryTagInput")
    def query_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryTagInput"))

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCaseInput")
    def quoted_identifiers_ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "quotedIdentifiersIgnoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultsetInput")
    def rows_per_resultset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowsPerResultsetInput"))

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsNameInput")
    def s3_stage_vpce_dns_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3StageVpceDnsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional["TaskSchedule"]:
        return typing.cast(typing.Optional["TaskSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="searchPathInput")
    def search_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchPathInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlStatementInput")
    def sql_statement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlStatementInput"))

    @builtins.property
    @jsii.member(jsii_name="startedInput")
    def started_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startedInput"))

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSecondsInput")
    def statement_queued_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statementQueuedTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSecondsInput")
    def statement_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statementTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="strictJsonOutputInput")
    def strict_json_output_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictJsonOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailuresInput")
    def suspend_task_after_num_failures_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "suspendTaskAfterNumFailuresInput"))

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttemptsInput")
    def task_auto_retry_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "taskAutoRetryAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInputFormatInput")
    def time_input_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeInputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormatInput")
    def time_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampDayIsAlways24HInput")
    def timestamp_day_is_always24_h_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timestampDayIsAlways24HInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormatInput")
    def timestamp_input_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampInputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormatInput")
    def timestamp_ltz_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampLtzOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormatInput")
    def timestamp_ntz_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampNtzOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormatInput")
    def timestamp_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMappingInput")
    def timestamp_type_mapping_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampTypeMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormatInput")
    def timestamp_tz_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampTzOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="traceLevelInput")
    def trace_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "traceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="transactionAbortOnErrorInput")
    def transaction_abort_on_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "transactionAbortOnErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevelInput")
    def transaction_default_isolation_level_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transactionDefaultIsolationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStartInput")
    def two_digit_century_start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "twoDigitCenturyStartInput"))

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlActionInput")
    def unsupported_ddl_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unsupportedDdlActionInput"))

    @builtins.property
    @jsii.member(jsii_name="useCachedResultInput")
    def use_cached_result_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCachedResultInput"))

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
    @jsii.member(jsii_name="warehouseInput")
    def warehouse_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicyInput")
    def week_of_year_policy_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekOfYearPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="weekStartInput")
    def week_start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekStartInput"))

    @builtins.property
    @jsii.member(jsii_name="whenInput")
    def when_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whenInput"))

    @builtins.property
    @jsii.member(jsii_name="abortDetachedQuery")
    def abort_detached_query(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "abortDetachedQuery"))

    @abort_detached_query.setter
    def abort_detached_query(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000dc1c40e67a220428cb96bf7cb09cc4f0b3f8b178495941a23748443f2b9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "abortDetachedQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="after")
    def after(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "after"))

    @after.setter
    def after(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4f67b7c6aaa0dff726ba8906da170893801767daeb8594a67d27e29b4a8211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "after", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowOverlappingExecution")
    def allow_overlapping_execution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowOverlappingExecution"))

    @allow_overlapping_execution.setter
    def allow_overlapping_execution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6f45ea20a892361fea1f1a00ce23bf3fa2158ed4ff73473407f678b7e4d1966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOverlappingExecution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autocommit")
    def autocommit(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autocommit"))

    @autocommit.setter
    def autocommit(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed52bd51ac39c4b02d53c556e031440abd97026a9813f0f4d71ee7da5f7566c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocommit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryInputFormat"))

    @binary_input_format.setter
    def binary_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb3125f305c8280b29149705d01db0c20dc8e93219d3dc24ea42f2e8340677c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryOutputFormat"))

    @binary_output_format.setter
    def binary_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6221c4f6b0416e4042d00c83a22b85a3ecafe8ac94944b89106f15924fb6b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientMemoryLimit"))

    @client_memory_limit.setter
    def client_memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637c700d5d2b0467139b55d791050aadd034c177fad3f91bfd15085056fe1262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientMemoryLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientMetadataRequestUseConnectionCtx")
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientMetadataRequestUseConnectionCtx"))

    @client_metadata_request_use_connection_ctx.setter
    def client_metadata_request_use_connection_ctx(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c2b3628ddb0842c8296d0637c79e644fb4cacacc65e2448278e75e0484e4a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientMetadataRequestUseConnectionCtx", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientPrefetchThreads"))

    @client_prefetch_threads.setter
    def client_prefetch_threads(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db7243d99e12980fefad990de332880bffc74402e08c00fab52e763b84a2f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientPrefetchThreads", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientResultChunkSize"))

    @client_result_chunk_size.setter
    def client_result_chunk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4426fe8bd4ea007f4bf825b078e48b46ef67bef7682434b7cfb3877223fa7051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientResultChunkSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientResultColumnCaseInsensitive")
    def client_result_column_case_insensitive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientResultColumnCaseInsensitive"))

    @client_result_column_case_insensitive.setter
    def client_result_column_case_insensitive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ede84d56e4d6345bea8ec7b80845f6dae914c663e7fd56a8208cb4fe21101e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientResultColumnCaseInsensitive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAlive")
    def client_session_keep_alive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientSessionKeepAlive"))

    @client_session_keep_alive.setter
    def client_session_keep_alive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096b788c9067ad872c6182ac1120ac72584777021f5995063cd8fd3bf7bda767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAlive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @client_session_keep_alive_heartbeat_frequency.setter
    def client_session_keep_alive_heartbeat_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f305f4838a9b6608d2d740d284bacf14b8ca8427177adfa6cd59e3c5ea17d92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAliveHeartbeatFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTimestampTypeMapping"))

    @client_timestamp_type_mapping.setter
    def client_timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c41cf9c392fc1149452d56c573fe7287d2eca8c4e1a3486cda39ddb8d9199f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a460ab85bdbee1b5b7d1afc2c85e737dcbf0fc049e53145eb43bcf5ac51fd64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "config"))

    @config.setter
    def config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca4e11acc7de6bd00451df8fbf84eac47525d1714900ae902cc1060fd1e02e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4663644f15e776aad0efb661ea515bf94c94a51357321a4b8454a61781655a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateInputFormat"))

    @date_input_format.setter
    def date_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f1cac5d5f949f3297141adab2d85cd48cf30efd15ee98b27acb135491cd2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateOutputFormat"))

    @date_output_format.setter
    def date_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0844e07ffc28c29dd33f773b5657e1b2bcceeab2630f9209c5916db978a8c86f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableUnloadPhysicalTypeOptimization")
    def enable_unload_physical_type_optimization(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableUnloadPhysicalTypeOptimization"))

    @enable_unload_physical_type_optimization.setter
    def enable_unload_physical_type_optimization(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__198f2f6903193d6a7867ce2c2f7cfa327e45bcb384ed7d5f048bb100b388a253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUnloadPhysicalTypeOptimization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="errorIntegration")
    def error_integration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorIntegration"))

    @error_integration.setter
    def error_integration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5eb20156b6371eea9d6150bb1904bc23049ba1e4170cbe9d97564bce3a4e32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorIntegration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicMerge")
    def error_on_nondeterministic_merge(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "errorOnNondeterministicMerge"))

    @error_on_nondeterministic_merge.setter
    def error_on_nondeterministic_merge(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a7091ea763a511d0d7d6aac91eda8352f48fe2589b2bd4970fe3d965dd677c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOnNondeterministicMerge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicUpdate")
    def error_on_nondeterministic_update(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "errorOnNondeterministicUpdate"))

    @error_on_nondeterministic_update.setter
    def error_on_nondeterministic_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4576b68bcacf1e201400094ec87872eaa692bea1479646881536e16f1a28fd43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOnNondeterministicUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finalize")
    def finalize(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finalize"))

    @finalize.setter
    def finalize(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6bd797b10149b6858ff3ecc12eb82c34e81a754d8875c454c85b378455749b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finalize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geographyOutputFormat"))

    @geography_output_format.setter
    def geography_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e490da0ad04f55ea72041d7a7ad70366be71fb10ec1458179fdd8d3470228b4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geographyOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geometryOutputFormat"))

    @geometry_output_format.setter
    def geometry_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4951d580bd17faa92961cd864065c0d972b1263d273f9cecbbb46f26833251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geometryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64b3bfe9c82317b45a085e9ac53577abd6c2d6c42bdfb4c9b5a38702f7a0cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatTimestampNtzAsUtc")
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jdbcTreatTimestampNtzAsUtc"))

    @jdbc_treat_timestamp_ntz_as_utc.setter
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ac4d350619dd24a2df0476718884e5b07c97761bee49d3b873fc39eaa1106f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jdbcTreatTimestampNtzAsUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jdbcUseSessionTimezone")
    def jdbc_use_session_timezone(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jdbcUseSessionTimezone"))

    @jdbc_use_session_timezone.setter
    def jdbc_use_session_timezone(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1cb3fe994d311b435fa9733c740e6910e4457cd2446b8ec938e4dee945fadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jdbcUseSessionTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jsonIndent"))

    @json_indent.setter
    def json_indent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9088a2bfd5b64fdef999d452642bac369812724888d5443e0d6a811612d20c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonIndent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockTimeout"))

    @lock_timeout.setter
    def lock_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77dc909823397116bcec8bf4058a0c3d831731a64c6654e469de7778f61082a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7d3f0253acb1f5642fcf01ea794f431e15e17feeb9546638fb8fb92f8ebe0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiStatementCount"))

    @multi_statement_count.setter
    def multi_statement_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd863124f4692ee7860b1a2f8572a8bf5706309cbf4d47417627dd312bd18a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiStatementCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35fdd161201488a3a65a8e3aab9a6810d45e1ad46cfb37cb179a616f85b3e1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noorderSequenceAsDefault")
    def noorder_sequence_as_default(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noorderSequenceAsDefault"))

    @noorder_sequence_as_default.setter
    def noorder_sequence_as_default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d858bcc23f60fbf7a6a0b24fbb2c8b2dbdf262eb00106f6362ea9b9c4198ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noorderSequenceAsDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="odbcTreatDecimalAsInt")
    def odbc_treat_decimal_as_int(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "odbcTreatDecimalAsInt"))

    @odbc_treat_decimal_as_int.setter
    def odbc_treat_decimal_as_int(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0386968c6965db3e232384ec2c509510c8c2c9927a27b1c1b1ee48c70fd05b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbcTreatDecimalAsInt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryTag"))

    @query_tag.setter
    def query_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e7118930856f5db3d6bde5a565811b5df317631b0a7659cb14b9318004a10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryTag", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__730207da9e10b233dc9d9524d84398699ee9ce108e3404547f68d2ddce288601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotedIdentifiersIgnoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsPerResultset"))

    @rows_per_resultset.setter
    def rows_per_resultset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00807a2ad95e96d76a8de34990f5922868042c1def5f3151dab6afafe4cf52eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsPerResultset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3StageVpceDnsName"))

    @s3_stage_vpce_dns_name.setter
    def s3_stage_vpce_dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c38ac74489a1ec15385297f1da9fb6cab68e86b4ff99d32f35fb97db4bdf60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3StageVpceDnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e414d304fb0b5b56fb9ac7ec2de77f79a7b509fa1f0697c776dea0112c26c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchPath"))

    @search_path.setter
    def search_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0382c4ecb9752bb2d404bb8295857c938035307b2c7f2aac086835abd53c2ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlStatement")
    def sql_statement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlStatement"))

    @sql_statement.setter
    def sql_statement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b278cd40c077dc3d408636838637868d09b900fc1e63409db65d40e5f8eccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlStatement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="started")
    def started(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "started"))

    @started.setter
    def started(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2c8180e858236070f21334babaa6826e34132ad5e9ef981b98c88efd8ea3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "started", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @statement_queued_timeout_in_seconds.setter
    def statement_queued_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b77066bf27a18c21232146e79a30afa5f555f4c9c73cdd00dec8db4189eff31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementQueuedTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementTimeoutInSeconds"))

    @statement_timeout_in_seconds.setter
    def statement_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5076d5b136a93294ea4e10e6fbabf3ffbea61a0341d3949102a6edd7124e1905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictJsonOutput")
    def strict_json_output(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strictJsonOutput"))

    @strict_json_output.setter
    def strict_json_output(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd951c73ffeac27ee48f6969a8faf00a10ba7a28a77ec39a4e2e711ba15a8d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictJsonOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailures")
    def suspend_task_after_num_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendTaskAfterNumFailures"))

    @suspend_task_after_num_failures.setter
    def suspend_task_after_num_failures(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad29a4348b00843adeb8c03ba026e9b3d51c0836d9305968bd9ee4d7f94eafa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendTaskAfterNumFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttempts")
    def task_auto_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskAutoRetryAttempts"))

    @task_auto_retry_attempts.setter
    def task_auto_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52bca2a91426ae6aa44865eb3a71e7907326767ce8f3ccec2026eebc1f4b86d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskAutoRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeInputFormat"))

    @time_input_format.setter
    def time_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b581dcb2e7530c942a1a6ad84af489e87a2814b2c3c9f152c57e943e8b9639aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeOutputFormat"))

    @time_output_format.setter
    def time_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe052aea7752fcdd72fb7dd7b1d0103df9e610e8a1335817a87dbcfeab9a307a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampDayIsAlways24H")
    def timestamp_day_is_always24_h(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "timestampDayIsAlways24H"))

    @timestamp_day_is_always24_h.setter
    def timestamp_day_is_always24_h(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5634334e9aa811ca6f8d622a3a5dc3741abf7a0eb417e0e9c7268262560dc45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampDayIsAlways24H", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampInputFormat"))

    @timestamp_input_format.setter
    def timestamp_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd0903e2eeff55e572b23adfaca726d4e6d850adec915af400f8e399ea92906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampLtzOutputFormat"))

    @timestamp_ltz_output_format.setter
    def timestamp_ltz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe9df6c5acb0e33d40236e196b2b34532c165d35e1090b33e2b10e2e99cb0f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampLtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampNtzOutputFormat"))

    @timestamp_ntz_output_format.setter
    def timestamp_ntz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e082ebbc26fba6b74675e7c9ec2209f78a6a1ed2c4c85023763284954ecac0b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampNtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampOutputFormat"))

    @timestamp_output_format.setter
    def timestamp_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9873af85c6b305a81d64bfd17f65f9c31a6cedf227ff5a94d7ddafdf2a6482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTypeMapping"))

    @timestamp_type_mapping.setter
    def timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7b96a56b63f2be0a18f9a3c27842bc65fe61a1b4272dc7f17f5e328bc9fc06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTzOutputFormat"))

    @timestamp_tz_output_format.setter
    def timestamp_tz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a911059dd442fb2a8451d221477348274fdcef94eae305732e61bbdc31d96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ec267cdb3bf89086e0b3b233c7a10f302e50a6bb0af429d3cfa1b9c4a6cc28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2137c00e4dbf8fb4ac0355c7fabc854bc2048550ec268ba1d418f40c811014ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionAbortOnError")
    def transaction_abort_on_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "transactionAbortOnError"))

    @transaction_abort_on_error.setter
    def transaction_abort_on_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7319289576ada8bc907fbc2906c172d1c7a48672a0b6e72c974c6a2af6a9e9a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionAbortOnError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transactionDefaultIsolationLevel"))

    @transaction_default_isolation_level.setter
    def transaction_default_isolation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb42aa5f9aff9bacd6f35feb1f06cdd0f75a8f9f838893199bd881acf7219c2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionDefaultIsolationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "twoDigitCenturyStart"))

    @two_digit_century_start.setter
    def two_digit_century_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ecf00a9cd7649614468d946e85905c33d4005e58a9c6e22cc5e6ec858cfdd14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twoDigitCenturyStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unsupportedDdlAction"))

    @unsupported_ddl_action.setter
    def unsupported_ddl_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4021c53075a65661455c9d1937e82d1119341d5e9c76991c0ef9a5973ff9e315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unsupportedDdlAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCachedResult")
    def use_cached_result(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCachedResult"))

    @use_cached_result.setter
    def use_cached_result(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d580b67262ca576ca41c00b5da866b277ada6ad11f923c715f72ebe6407642c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCachedResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSize")
    def user_task_managed_initial_warehouse_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTaskManagedInitialWarehouseSize"))

    @user_task_managed_initial_warehouse_size.setter
    def user_task_managed_initial_warehouse_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd215a5b4794e793060b5f7cdaed15f6c4510f3c30f92263bf2dc02b2d7cc17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskManagedInitialWarehouseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSeconds")
    def user_task_minimum_trigger_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskMinimumTriggerIntervalInSeconds"))

    @user_task_minimum_trigger_interval_in_seconds.setter
    def user_task_minimum_trigger_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474e3cc0338e5e932ed3e8030f12840ba1aa42a2cea8d796e5ad564c4f67d77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskMinimumTriggerIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMs")
    def user_task_timeout_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskTimeoutMs"))

    @user_task_timeout_ms.setter
    def user_task_timeout_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6add217094f96be1fdbd877c03c3acfb12531a10388192bbfa81d39cd144bd42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskTimeoutMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouse")
    def warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouse"))

    @warehouse.setter
    def warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6240dc59b88cc8128ed2cadcd5ef1616adff3e1f28ea512a868bf98f628315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOfYearPolicy"))

    @week_of_year_policy.setter
    def week_of_year_policy(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3723ec57d593cb2af888a59c1cd076164c70c199db20322e7aa5607e02e7f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfYearPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekStart"))

    @week_start.setter
    def week_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960350664d9ace313b147091fb63f8cae0d4d0389be8fd90869f821d27af750a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="when")
    def when(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "when"))

    @when.setter
    def when(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cca6129d7883e1890cfab97ecfe18908703485c2bb1ddb9f98ca4f633a8dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "when", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskConfig",
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
        "sql_statement": "sqlStatement",
        "started": "started",
        "abort_detached_query": "abortDetachedQuery",
        "after": "after",
        "allow_overlapping_execution": "allowOverlappingExecution",
        "autocommit": "autocommit",
        "binary_input_format": "binaryInputFormat",
        "binary_output_format": "binaryOutputFormat",
        "client_memory_limit": "clientMemoryLimit",
        "client_metadata_request_use_connection_ctx": "clientMetadataRequestUseConnectionCtx",
        "client_prefetch_threads": "clientPrefetchThreads",
        "client_result_chunk_size": "clientResultChunkSize",
        "client_result_column_case_insensitive": "clientResultColumnCaseInsensitive",
        "client_session_keep_alive": "clientSessionKeepAlive",
        "client_session_keep_alive_heartbeat_frequency": "clientSessionKeepAliveHeartbeatFrequency",
        "client_timestamp_type_mapping": "clientTimestampTypeMapping",
        "comment": "comment",
        "config": "config",
        "date_input_format": "dateInputFormat",
        "date_output_format": "dateOutputFormat",
        "enable_unload_physical_type_optimization": "enableUnloadPhysicalTypeOptimization",
        "error_integration": "errorIntegration",
        "error_on_nondeterministic_merge": "errorOnNondeterministicMerge",
        "error_on_nondeterministic_update": "errorOnNondeterministicUpdate",
        "finalize": "finalize",
        "geography_output_format": "geographyOutputFormat",
        "geometry_output_format": "geometryOutputFormat",
        "id": "id",
        "jdbc_treat_timestamp_ntz_as_utc": "jdbcTreatTimestampNtzAsUtc",
        "jdbc_use_session_timezone": "jdbcUseSessionTimezone",
        "json_indent": "jsonIndent",
        "lock_timeout": "lockTimeout",
        "log_level": "logLevel",
        "multi_statement_count": "multiStatementCount",
        "noorder_sequence_as_default": "noorderSequenceAsDefault",
        "odbc_treat_decimal_as_int": "odbcTreatDecimalAsInt",
        "query_tag": "queryTag",
        "quoted_identifiers_ignore_case": "quotedIdentifiersIgnoreCase",
        "rows_per_resultset": "rowsPerResultset",
        "s3_stage_vpce_dns_name": "s3StageVpceDnsName",
        "schedule": "schedule",
        "search_path": "searchPath",
        "statement_queued_timeout_in_seconds": "statementQueuedTimeoutInSeconds",
        "statement_timeout_in_seconds": "statementTimeoutInSeconds",
        "strict_json_output": "strictJsonOutput",
        "suspend_task_after_num_failures": "suspendTaskAfterNumFailures",
        "task_auto_retry_attempts": "taskAutoRetryAttempts",
        "time_input_format": "timeInputFormat",
        "time_output_format": "timeOutputFormat",
        "timestamp_day_is_always24_h": "timestampDayIsAlways24H",
        "timestamp_input_format": "timestampInputFormat",
        "timestamp_ltz_output_format": "timestampLtzOutputFormat",
        "timestamp_ntz_output_format": "timestampNtzOutputFormat",
        "timestamp_output_format": "timestampOutputFormat",
        "timestamp_type_mapping": "timestampTypeMapping",
        "timestamp_tz_output_format": "timestampTzOutputFormat",
        "timezone": "timezone",
        "trace_level": "traceLevel",
        "transaction_abort_on_error": "transactionAbortOnError",
        "transaction_default_isolation_level": "transactionDefaultIsolationLevel",
        "two_digit_century_start": "twoDigitCenturyStart",
        "unsupported_ddl_action": "unsupportedDdlAction",
        "use_cached_result": "useCachedResult",
        "user_task_managed_initial_warehouse_size": "userTaskManagedInitialWarehouseSize",
        "user_task_minimum_trigger_interval_in_seconds": "userTaskMinimumTriggerIntervalInSeconds",
        "user_task_timeout_ms": "userTaskTimeoutMs",
        "warehouse": "warehouse",
        "week_of_year_policy": "weekOfYearPolicy",
        "week_start": "weekStart",
        "when": "when",
    },
)
class TaskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        sql_statement: builtins.str,
        started: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        after: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_overlapping_execution: typing.Optional[builtins.str] = None,
        autocommit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        binary_input_format: typing.Optional[builtins.str] = None,
        binary_output_format: typing.Optional[builtins.str] = None,
        client_memory_limit: typing.Optional[jsii.Number] = None,
        client_metadata_request_use_connection_ctx: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_prefetch_threads: typing.Optional[jsii.Number] = None,
        client_result_chunk_size: typing.Optional[jsii.Number] = None,
        client_result_column_case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_session_keep_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_session_keep_alive_heartbeat_frequency: typing.Optional[jsii.Number] = None,
        client_timestamp_type_mapping: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        config: typing.Optional[builtins.str] = None,
        date_input_format: typing.Optional[builtins.str] = None,
        date_output_format: typing.Optional[builtins.str] = None,
        enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_integration: typing.Optional[builtins.str] = None,
        error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        finalize: typing.Optional[builtins.str] = None,
        geography_output_format: typing.Optional[builtins.str] = None,
        geometry_output_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_indent: typing.Optional[jsii.Number] = None,
        lock_timeout: typing.Optional[jsii.Number] = None,
        log_level: typing.Optional[builtins.str] = None,
        multi_statement_count: typing.Optional[jsii.Number] = None,
        noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_tag: typing.Optional[builtins.str] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rows_per_resultset: typing.Optional[jsii.Number] = None,
        s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["TaskSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        search_path: typing.Optional[builtins.str] = None,
        statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
        task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
        time_input_format: typing.Optional[builtins.str] = None,
        time_output_format: typing.Optional[builtins.str] = None,
        timestamp_day_is_always24_h: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timestamp_input_format: typing.Optional[builtins.str] = None,
        timestamp_ltz_output_format: typing.Optional[builtins.str] = None,
        timestamp_ntz_output_format: typing.Optional[builtins.str] = None,
        timestamp_output_format: typing.Optional[builtins.str] = None,
        timestamp_type_mapping: typing.Optional[builtins.str] = None,
        timestamp_tz_output_format: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
        trace_level: typing.Optional[builtins.str] = None,
        transaction_abort_on_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transaction_default_isolation_level: typing.Optional[builtins.str] = None,
        two_digit_century_start: typing.Optional[jsii.Number] = None,
        unsupported_ddl_action: typing.Optional[builtins.str] = None,
        use_cached_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
        user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
        user_task_timeout_ms: typing.Optional[jsii.Number] = None,
        warehouse: typing.Optional[builtins.str] = None,
        week_of_year_policy: typing.Optional[jsii.Number] = None,
        week_start: typing.Optional[jsii.Number] = None,
        when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the task. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#database Task#database}
        :param name: Specifies the identifier for the task; must be unique for the database and schema in which the task is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#name Task#name}
        :param schema: The schema in which to create the task. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#schema Task#schema}
        :param sql_statement: Any single SQL statement, or a call to a stored procedure, executed when the task runs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#sql_statement Task#sql_statement}
        :param started: Specifies if the task should be started or suspended. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#started Task#started}
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#abort_detached_query Task#abort_detached_query}
        :param after: Specifies one or more predecessor tasks for the current task. Use this option to `create a DAG <https://docs.snowflake.com/en/user-guide/tasks-graphs.html#label-task-dag>`_ of tasks or add this task to an existing DAG. A DAG is a series of tasks that starts with a scheduled root task and is linked together by dependencies. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#after Task#after}
        :param allow_overlapping_execution: By default, Snowflake ensures that only one instance of a particular DAG is allowed to run at a time, setting the parameter value to TRUE permits DAG runs to overlap. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#allow_overlapping_execution Task#allow_overlapping_execution}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#autocommit Task#autocommit}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#binary_input_format Task#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#binary_output_format Task#binary_output_format}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_memory_limit Task#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_metadata_request_use_connection_ctx Task#client_metadata_request_use_connection_ctx}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_prefetch_threads Task#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_result_chunk_size Task#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_result_column_case_insensitive Task#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_session_keep_alive Task#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_session_keep_alive_heartbeat_frequency Task#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_timestamp_type_mapping Task#client_timestamp_type_mapping}
        :param comment: Specifies a comment for the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#comment Task#comment}
        :param config: Specifies a string representation of key value pairs that can be accessed by all tasks in the task graph. Must be in JSON format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#config Task#config}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#date_input_format Task#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#date_output_format Task#date_output_format}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#enable_unload_physical_type_optimization Task#enable_unload_physical_type_optimization}
        :param error_integration: Specifies the name of the notification integration used for error notifications. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./notification_integration>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_integration Task#error_integration}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_on_nondeterministic_merge Task#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_on_nondeterministic_update Task#error_on_nondeterministic_update}
        :param finalize: Specifies the name of a root task that the finalizer task is associated with. Finalizer tasks run after all other tasks in the task graph run to completion. You can define the SQL of a finalizer task to handle notifications and the release and cleanup of resources that a task graph uses. For more information, see `Release and cleanup of task graphs <https://docs.snowflake.com/en/user-guide/tasks-graphs.html#label-finalizer-task>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#finalize Task#finalize}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#geography_output_format Task#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#geometry_output_format Task#geometry_output_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#id Task#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#jdbc_treat_timestamp_ntz_as_utc Task#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#jdbc_use_session_timezone Task#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#json_indent Task#json_indent}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#lock_timeout Task#lock_timeout}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#log_level Task#log_level}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#multi_statement_count Task#multi_statement_count}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#noorder_sequence_as_default Task#noorder_sequence_as_default}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#odbc_treat_decimal_as_int Task#odbc_treat_decimal_as_int}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#query_tag Task#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#quoted_identifiers_ignore_case Task#quoted_identifiers_ignore_case}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#rows_per_resultset Task#rows_per_resultset}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#s3_stage_vpce_dns_name Task#s3_stage_vpce_dns_name}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#schedule Task#schedule}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#search_path Task#search_path}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#statement_queued_timeout_in_seconds Task#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#statement_timeout_in_seconds Task#statement_timeout_in_seconds}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#strict_json_output Task#strict_json_output}
        :param suspend_task_after_num_failures: Specifies the number of consecutive failed task runs after which the current task is suspended automatically. The default is 0 (no automatic suspension). For more information, check `SUSPEND_TASK_AFTER_NUM_FAILURES docs <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#suspend_task_after_num_failures Task#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Specifies the number of automatic task graph retry attempts. If any task graphs complete in a FAILED state, Snowflake can automatically retry the task graphs from the last task in the graph that failed. For more information, check `TASK_AUTO_RETRY_ATTEMPTS docs <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#task_auto_retry_attempts Task#task_auto_retry_attempts}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#time_input_format Task#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#time_output_format Task#time_output_format}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_day_is_always_24h Task#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_input_format Task#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_ltz_output_format Task#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_ntz_output_format Task#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_output_format Task#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_type_mapping Task#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_tz_output_format Task#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timezone Task#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#trace_level Task#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#transaction_abort_on_error Task#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#transaction_default_isolation_level Task#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#two_digit_century_start Task#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#unsupported_ddl_action Task#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#use_cached_result Task#use_cached_result}
        :param user_task_managed_initial_warehouse_size: Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size. Once a task has successfully completed a few runs, Snowflake ignores this parameter setting. Valid values are (case-insensitive): %s. (Conflicts with warehouse). For more information about warehouses, see `docs <./warehouse>`_. For more information, check `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_managed_initial_warehouse_size Task#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds For more information, check `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-minimum-trigger-interval-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_minimum_trigger_interval_in_seconds Task#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: Specifies the time limit on a single run of the task before it times out (in milliseconds). For more information, check `USER_TASK_TIMEOUT_MS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_timeout_ms Task#user_task_timeout_ms}
        :param warehouse: The warehouse the task will use. Omit this parameter to use Snowflake-managed compute resources for runs of this task. Due to Snowflake limitations warehouse identifier can consist of only upper-cased letters. (Conflicts with user_task_managed_initial_warehouse_size) For more information about this resource, see `docs <./warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#warehouse Task#warehouse}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#week_of_year_policy Task#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#week_start Task#week_start}
        :param when: Specifies a Boolean SQL expression; multiple conditions joined with AND/OR are supported. When a task is triggered (based on its SCHEDULE or AFTER setting), it validates the conditions of the expression to determine whether to execute. If the conditions of the expression are not met, then the task skips the current run. Any tasks that identify this task as a predecessor also don’t run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#when Task#when}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(schedule, dict):
            schedule = TaskSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b33c946381b3c9a032b7570564a1e2078f7d125b95b09f4d234e236ac1b576)
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
            check_type(argname="argument sql_statement", value=sql_statement, expected_type=type_hints["sql_statement"])
            check_type(argname="argument started", value=started, expected_type=type_hints["started"])
            check_type(argname="argument abort_detached_query", value=abort_detached_query, expected_type=type_hints["abort_detached_query"])
            check_type(argname="argument after", value=after, expected_type=type_hints["after"])
            check_type(argname="argument allow_overlapping_execution", value=allow_overlapping_execution, expected_type=type_hints["allow_overlapping_execution"])
            check_type(argname="argument autocommit", value=autocommit, expected_type=type_hints["autocommit"])
            check_type(argname="argument binary_input_format", value=binary_input_format, expected_type=type_hints["binary_input_format"])
            check_type(argname="argument binary_output_format", value=binary_output_format, expected_type=type_hints["binary_output_format"])
            check_type(argname="argument client_memory_limit", value=client_memory_limit, expected_type=type_hints["client_memory_limit"])
            check_type(argname="argument client_metadata_request_use_connection_ctx", value=client_metadata_request_use_connection_ctx, expected_type=type_hints["client_metadata_request_use_connection_ctx"])
            check_type(argname="argument client_prefetch_threads", value=client_prefetch_threads, expected_type=type_hints["client_prefetch_threads"])
            check_type(argname="argument client_result_chunk_size", value=client_result_chunk_size, expected_type=type_hints["client_result_chunk_size"])
            check_type(argname="argument client_result_column_case_insensitive", value=client_result_column_case_insensitive, expected_type=type_hints["client_result_column_case_insensitive"])
            check_type(argname="argument client_session_keep_alive", value=client_session_keep_alive, expected_type=type_hints["client_session_keep_alive"])
            check_type(argname="argument client_session_keep_alive_heartbeat_frequency", value=client_session_keep_alive_heartbeat_frequency, expected_type=type_hints["client_session_keep_alive_heartbeat_frequency"])
            check_type(argname="argument client_timestamp_type_mapping", value=client_timestamp_type_mapping, expected_type=type_hints["client_timestamp_type_mapping"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument date_input_format", value=date_input_format, expected_type=type_hints["date_input_format"])
            check_type(argname="argument date_output_format", value=date_output_format, expected_type=type_hints["date_output_format"])
            check_type(argname="argument enable_unload_physical_type_optimization", value=enable_unload_physical_type_optimization, expected_type=type_hints["enable_unload_physical_type_optimization"])
            check_type(argname="argument error_integration", value=error_integration, expected_type=type_hints["error_integration"])
            check_type(argname="argument error_on_nondeterministic_merge", value=error_on_nondeterministic_merge, expected_type=type_hints["error_on_nondeterministic_merge"])
            check_type(argname="argument error_on_nondeterministic_update", value=error_on_nondeterministic_update, expected_type=type_hints["error_on_nondeterministic_update"])
            check_type(argname="argument finalize", value=finalize, expected_type=type_hints["finalize"])
            check_type(argname="argument geography_output_format", value=geography_output_format, expected_type=type_hints["geography_output_format"])
            check_type(argname="argument geometry_output_format", value=geometry_output_format, expected_type=type_hints["geometry_output_format"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jdbc_treat_timestamp_ntz_as_utc", value=jdbc_treat_timestamp_ntz_as_utc, expected_type=type_hints["jdbc_treat_timestamp_ntz_as_utc"])
            check_type(argname="argument jdbc_use_session_timezone", value=jdbc_use_session_timezone, expected_type=type_hints["jdbc_use_session_timezone"])
            check_type(argname="argument json_indent", value=json_indent, expected_type=type_hints["json_indent"])
            check_type(argname="argument lock_timeout", value=lock_timeout, expected_type=type_hints["lock_timeout"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument multi_statement_count", value=multi_statement_count, expected_type=type_hints["multi_statement_count"])
            check_type(argname="argument noorder_sequence_as_default", value=noorder_sequence_as_default, expected_type=type_hints["noorder_sequence_as_default"])
            check_type(argname="argument odbc_treat_decimal_as_int", value=odbc_treat_decimal_as_int, expected_type=type_hints["odbc_treat_decimal_as_int"])
            check_type(argname="argument query_tag", value=query_tag, expected_type=type_hints["query_tag"])
            check_type(argname="argument quoted_identifiers_ignore_case", value=quoted_identifiers_ignore_case, expected_type=type_hints["quoted_identifiers_ignore_case"])
            check_type(argname="argument rows_per_resultset", value=rows_per_resultset, expected_type=type_hints["rows_per_resultset"])
            check_type(argname="argument s3_stage_vpce_dns_name", value=s3_stage_vpce_dns_name, expected_type=type_hints["s3_stage_vpce_dns_name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument search_path", value=search_path, expected_type=type_hints["search_path"])
            check_type(argname="argument statement_queued_timeout_in_seconds", value=statement_queued_timeout_in_seconds, expected_type=type_hints["statement_queued_timeout_in_seconds"])
            check_type(argname="argument statement_timeout_in_seconds", value=statement_timeout_in_seconds, expected_type=type_hints["statement_timeout_in_seconds"])
            check_type(argname="argument strict_json_output", value=strict_json_output, expected_type=type_hints["strict_json_output"])
            check_type(argname="argument suspend_task_after_num_failures", value=suspend_task_after_num_failures, expected_type=type_hints["suspend_task_after_num_failures"])
            check_type(argname="argument task_auto_retry_attempts", value=task_auto_retry_attempts, expected_type=type_hints["task_auto_retry_attempts"])
            check_type(argname="argument time_input_format", value=time_input_format, expected_type=type_hints["time_input_format"])
            check_type(argname="argument time_output_format", value=time_output_format, expected_type=type_hints["time_output_format"])
            check_type(argname="argument timestamp_day_is_always24_h", value=timestamp_day_is_always24_h, expected_type=type_hints["timestamp_day_is_always24_h"])
            check_type(argname="argument timestamp_input_format", value=timestamp_input_format, expected_type=type_hints["timestamp_input_format"])
            check_type(argname="argument timestamp_ltz_output_format", value=timestamp_ltz_output_format, expected_type=type_hints["timestamp_ltz_output_format"])
            check_type(argname="argument timestamp_ntz_output_format", value=timestamp_ntz_output_format, expected_type=type_hints["timestamp_ntz_output_format"])
            check_type(argname="argument timestamp_output_format", value=timestamp_output_format, expected_type=type_hints["timestamp_output_format"])
            check_type(argname="argument timestamp_type_mapping", value=timestamp_type_mapping, expected_type=type_hints["timestamp_type_mapping"])
            check_type(argname="argument timestamp_tz_output_format", value=timestamp_tz_output_format, expected_type=type_hints["timestamp_tz_output_format"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument trace_level", value=trace_level, expected_type=type_hints["trace_level"])
            check_type(argname="argument transaction_abort_on_error", value=transaction_abort_on_error, expected_type=type_hints["transaction_abort_on_error"])
            check_type(argname="argument transaction_default_isolation_level", value=transaction_default_isolation_level, expected_type=type_hints["transaction_default_isolation_level"])
            check_type(argname="argument two_digit_century_start", value=two_digit_century_start, expected_type=type_hints["two_digit_century_start"])
            check_type(argname="argument unsupported_ddl_action", value=unsupported_ddl_action, expected_type=type_hints["unsupported_ddl_action"])
            check_type(argname="argument use_cached_result", value=use_cached_result, expected_type=type_hints["use_cached_result"])
            check_type(argname="argument user_task_managed_initial_warehouse_size", value=user_task_managed_initial_warehouse_size, expected_type=type_hints["user_task_managed_initial_warehouse_size"])
            check_type(argname="argument user_task_minimum_trigger_interval_in_seconds", value=user_task_minimum_trigger_interval_in_seconds, expected_type=type_hints["user_task_minimum_trigger_interval_in_seconds"])
            check_type(argname="argument user_task_timeout_ms", value=user_task_timeout_ms, expected_type=type_hints["user_task_timeout_ms"])
            check_type(argname="argument warehouse", value=warehouse, expected_type=type_hints["warehouse"])
            check_type(argname="argument week_of_year_policy", value=week_of_year_policy, expected_type=type_hints["week_of_year_policy"])
            check_type(argname="argument week_start", value=week_start, expected_type=type_hints["week_start"])
            check_type(argname="argument when", value=when, expected_type=type_hints["when"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "name": name,
            "schema": schema,
            "sql_statement": sql_statement,
            "started": started,
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
        if abort_detached_query is not None:
            self._values["abort_detached_query"] = abort_detached_query
        if after is not None:
            self._values["after"] = after
        if allow_overlapping_execution is not None:
            self._values["allow_overlapping_execution"] = allow_overlapping_execution
        if autocommit is not None:
            self._values["autocommit"] = autocommit
        if binary_input_format is not None:
            self._values["binary_input_format"] = binary_input_format
        if binary_output_format is not None:
            self._values["binary_output_format"] = binary_output_format
        if client_memory_limit is not None:
            self._values["client_memory_limit"] = client_memory_limit
        if client_metadata_request_use_connection_ctx is not None:
            self._values["client_metadata_request_use_connection_ctx"] = client_metadata_request_use_connection_ctx
        if client_prefetch_threads is not None:
            self._values["client_prefetch_threads"] = client_prefetch_threads
        if client_result_chunk_size is not None:
            self._values["client_result_chunk_size"] = client_result_chunk_size
        if client_result_column_case_insensitive is not None:
            self._values["client_result_column_case_insensitive"] = client_result_column_case_insensitive
        if client_session_keep_alive is not None:
            self._values["client_session_keep_alive"] = client_session_keep_alive
        if client_session_keep_alive_heartbeat_frequency is not None:
            self._values["client_session_keep_alive_heartbeat_frequency"] = client_session_keep_alive_heartbeat_frequency
        if client_timestamp_type_mapping is not None:
            self._values["client_timestamp_type_mapping"] = client_timestamp_type_mapping
        if comment is not None:
            self._values["comment"] = comment
        if config is not None:
            self._values["config"] = config
        if date_input_format is not None:
            self._values["date_input_format"] = date_input_format
        if date_output_format is not None:
            self._values["date_output_format"] = date_output_format
        if enable_unload_physical_type_optimization is not None:
            self._values["enable_unload_physical_type_optimization"] = enable_unload_physical_type_optimization
        if error_integration is not None:
            self._values["error_integration"] = error_integration
        if error_on_nondeterministic_merge is not None:
            self._values["error_on_nondeterministic_merge"] = error_on_nondeterministic_merge
        if error_on_nondeterministic_update is not None:
            self._values["error_on_nondeterministic_update"] = error_on_nondeterministic_update
        if finalize is not None:
            self._values["finalize"] = finalize
        if geography_output_format is not None:
            self._values["geography_output_format"] = geography_output_format
        if geometry_output_format is not None:
            self._values["geometry_output_format"] = geometry_output_format
        if id is not None:
            self._values["id"] = id
        if jdbc_treat_timestamp_ntz_as_utc is not None:
            self._values["jdbc_treat_timestamp_ntz_as_utc"] = jdbc_treat_timestamp_ntz_as_utc
        if jdbc_use_session_timezone is not None:
            self._values["jdbc_use_session_timezone"] = jdbc_use_session_timezone
        if json_indent is not None:
            self._values["json_indent"] = json_indent
        if lock_timeout is not None:
            self._values["lock_timeout"] = lock_timeout
        if log_level is not None:
            self._values["log_level"] = log_level
        if multi_statement_count is not None:
            self._values["multi_statement_count"] = multi_statement_count
        if noorder_sequence_as_default is not None:
            self._values["noorder_sequence_as_default"] = noorder_sequence_as_default
        if odbc_treat_decimal_as_int is not None:
            self._values["odbc_treat_decimal_as_int"] = odbc_treat_decimal_as_int
        if query_tag is not None:
            self._values["query_tag"] = query_tag
        if quoted_identifiers_ignore_case is not None:
            self._values["quoted_identifiers_ignore_case"] = quoted_identifiers_ignore_case
        if rows_per_resultset is not None:
            self._values["rows_per_resultset"] = rows_per_resultset
        if s3_stage_vpce_dns_name is not None:
            self._values["s3_stage_vpce_dns_name"] = s3_stage_vpce_dns_name
        if schedule is not None:
            self._values["schedule"] = schedule
        if search_path is not None:
            self._values["search_path"] = search_path
        if statement_queued_timeout_in_seconds is not None:
            self._values["statement_queued_timeout_in_seconds"] = statement_queued_timeout_in_seconds
        if statement_timeout_in_seconds is not None:
            self._values["statement_timeout_in_seconds"] = statement_timeout_in_seconds
        if strict_json_output is not None:
            self._values["strict_json_output"] = strict_json_output
        if suspend_task_after_num_failures is not None:
            self._values["suspend_task_after_num_failures"] = suspend_task_after_num_failures
        if task_auto_retry_attempts is not None:
            self._values["task_auto_retry_attempts"] = task_auto_retry_attempts
        if time_input_format is not None:
            self._values["time_input_format"] = time_input_format
        if time_output_format is not None:
            self._values["time_output_format"] = time_output_format
        if timestamp_day_is_always24_h is not None:
            self._values["timestamp_day_is_always24_h"] = timestamp_day_is_always24_h
        if timestamp_input_format is not None:
            self._values["timestamp_input_format"] = timestamp_input_format
        if timestamp_ltz_output_format is not None:
            self._values["timestamp_ltz_output_format"] = timestamp_ltz_output_format
        if timestamp_ntz_output_format is not None:
            self._values["timestamp_ntz_output_format"] = timestamp_ntz_output_format
        if timestamp_output_format is not None:
            self._values["timestamp_output_format"] = timestamp_output_format
        if timestamp_type_mapping is not None:
            self._values["timestamp_type_mapping"] = timestamp_type_mapping
        if timestamp_tz_output_format is not None:
            self._values["timestamp_tz_output_format"] = timestamp_tz_output_format
        if timezone is not None:
            self._values["timezone"] = timezone
        if trace_level is not None:
            self._values["trace_level"] = trace_level
        if transaction_abort_on_error is not None:
            self._values["transaction_abort_on_error"] = transaction_abort_on_error
        if transaction_default_isolation_level is not None:
            self._values["transaction_default_isolation_level"] = transaction_default_isolation_level
        if two_digit_century_start is not None:
            self._values["two_digit_century_start"] = two_digit_century_start
        if unsupported_ddl_action is not None:
            self._values["unsupported_ddl_action"] = unsupported_ddl_action
        if use_cached_result is not None:
            self._values["use_cached_result"] = use_cached_result
        if user_task_managed_initial_warehouse_size is not None:
            self._values["user_task_managed_initial_warehouse_size"] = user_task_managed_initial_warehouse_size
        if user_task_minimum_trigger_interval_in_seconds is not None:
            self._values["user_task_minimum_trigger_interval_in_seconds"] = user_task_minimum_trigger_interval_in_seconds
        if user_task_timeout_ms is not None:
            self._values["user_task_timeout_ms"] = user_task_timeout_ms
        if warehouse is not None:
            self._values["warehouse"] = warehouse
        if week_of_year_policy is not None:
            self._values["week_of_year_policy"] = week_of_year_policy
        if week_start is not None:
            self._values["week_start"] = week_start
        if when is not None:
            self._values["when"] = when

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
        '''The database in which to create the task.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#database Task#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the task;

        must be unique for the database and schema in which the task is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#name Task#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the task.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#schema Task#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_statement(self) -> builtins.str:
        '''Any single SQL statement, or a call to a stored procedure, executed when the task runs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#sql_statement Task#sql_statement}
        '''
        result = self._values.get("sql_statement")
        assert result is not None, "Required property 'sql_statement' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def started(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Specifies if the task should be started or suspended.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#started Task#started}
        '''
        result = self._values.get("started")
        assert result is not None, "Required property 'started' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def abort_detached_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#abort_detached_query Task#abort_detached_query}
        '''
        result = self._values.get("abort_detached_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def after(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies one or more predecessor tasks for the current task.

        Use this option to `create a DAG <https://docs.snowflake.com/en/user-guide/tasks-graphs.html#label-task-dag>`_ of tasks or add this task to an existing DAG. A DAG is a series of tasks that starts with a scheduled root task and is linked together by dependencies. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#after Task#after}
        '''
        result = self._values.get("after")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_overlapping_execution(self) -> typing.Optional[builtins.str]:
        '''By default, Snowflake ensures that only one instance of a particular DAG is allowed to run at a time, setting the parameter value to TRUE permits DAG runs to overlap.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#allow_overlapping_execution Task#allow_overlapping_execution}
        '''
        result = self._values.get("allow_overlapping_execution")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def autocommit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether autocommit is enabled for the session.

        Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#autocommit Task#autocommit}
        '''
        result = self._values.get("autocommit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def binary_input_format(self) -> typing.Optional[builtins.str]:
        '''The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#binary_input_format Task#binary_input_format}
        '''
        result = self._values.get("binary_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_output_format(self) -> typing.Optional[builtins.str]:
        '''The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#binary_output_format Task#binary_output_format}
        '''
        result = self._values.get("binary_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_memory_limit(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB).

        For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_memory_limit Task#client_memory_limit}
        '''
        result = self._values.get("client_memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema.

        The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_metadata_request_use_connection_ctx Task#client_metadata_request_use_connection_ctx}
        '''
        result = self._values.get("client_metadata_request_use_connection_ctx")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_prefetch_threads(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the number of threads used by the client to pre-fetch large result sets.

        The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_prefetch_threads Task#client_prefetch_threads}
        '''
        result = self._values.get("client_prefetch_threads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_chunk_size(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB).

        The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_result_chunk_size Task#client_result_chunk_size}
        '''
        result = self._values.get("client_result_chunk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_column_case_insensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_result_column_case_insensitive Task#client_result_column_case_insensitive}
        '''
        result = self._values.get("client_result_column_case_insensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to force a user to log in again after a period of inactivity in the session.

        For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_session_keep_alive Task#client_session_keep_alive}
        '''
        result = self._values.get("client_session_keep_alive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_session_keep_alive_heartbeat_frequency Task#client_session_keep_alive_heartbeat_frequency}
        '''
        result = self._values.get("client_session_keep_alive_heartbeat_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#client_timestamp_type_mapping Task#client_timestamp_type_mapping}
        '''
        result = self._values.get("client_timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the task.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#comment Task#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(self) -> typing.Optional[builtins.str]:
        '''Specifies a string representation of key value pairs that can be accessed by all tasks in the task graph.

        Must be in JSON format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#config Task#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#date_input_format Task#date_input_format}
        '''
        result = self._values.get("date_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#date_output_format Task#date_output_format}
        '''
        result = self._values.get("date_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_unload_physical_type_optimization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#enable_unload_physical_type_optimization Task#enable_unload_physical_type_optimization}
        '''
        result = self._values.get("enable_unload_physical_type_optimization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_integration(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the notification integration used for error notifications.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information about this resource, see `docs <./notification_integration>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_integration Task#error_integration}
        '''
        result = self._values.get("error_integration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error_on_nondeterministic_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_on_nondeterministic_merge Task#error_on_nondeterministic_merge}
        '''
        result = self._values.get("error_on_nondeterministic_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#error_on_nondeterministic_update Task#error_on_nondeterministic_update}
        '''
        result = self._values.get("error_on_nondeterministic_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def finalize(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of a root task that the finalizer task is associated with.

        Finalizer tasks run after all other tasks in the task graph run to completion. You can define the SQL of a finalizer task to handle notifications and the release and cleanup of resources that a task graph uses. For more information, see `Release and cleanup of task graphs <https://docs.snowflake.com/en/user-guide/tasks-graphs.html#label-finalizer-task>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#finalize Task#finalize}
        '''
        result = self._values.get("finalize")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geography_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#geography_output_format Task#geography_output_format}
        '''
        result = self._values.get("geography_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geometry_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#geometry_output_format Task#geometry_output_format}
        '''
        result = self._values.get("geometry_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#id Task#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#jdbc_treat_timestamp_ntz_as_utc Task#jdbc_treat_timestamp_ntz_as_utc}
        '''
        result = self._values.get("jdbc_treat_timestamp_ntz_as_utc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_use_session_timezone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#jdbc_use_session_timezone Task#jdbc_use_session_timezone}
        '''
        result = self._values.get("jdbc_use_session_timezone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def json_indent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of blank spaces to indent each new element in JSON output in the session.

        Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#json_indent Task#json_indent}
        '''
        result = self._values.get("json_indent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lock_timeout(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement.

        For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#lock_timeout Task#lock_timeout}
        '''
        result = self._values.get("lock_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the severity level of messages that should be ingested and made available in the active event table.

        Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#log_level Task#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_statement_count(self) -> typing.Optional[jsii.Number]:
        '''Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#multi_statement_count Task#multi_statement_count}
        '''
        result = self._values.get("multi_statement_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def noorder_sequence_as_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column.

        The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#noorder_sequence_as_default Task#noorder_sequence_as_default}
        '''
        result = self._values.get("noorder_sequence_as_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def odbc_treat_decimal_as_int(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#odbc_treat_decimal_as_int Task#odbc_treat_decimal_as_int}
        '''
        result = self._values.get("odbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_tag(self) -> typing.Optional[builtins.str]:
        '''Optional string that can be used to tag queries and other SQL statements executed within a session.

        The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#query_tag Task#query_tag}
        '''
        result = self._values.get("query_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters.

        By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#quoted_identifiers_ignore_case Task#quoted_identifiers_ignore_case}
        '''
        result = self._values.get("quoted_identifiers_ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rows_per_resultset(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of rows returned in a result set.

        A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#rows_per_resultset Task#rows_per_resultset}
        '''
        result = self._values.get("rows_per_resultset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3_stage_vpce_dns_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the DNS name of an Amazon S3 interface endpoint.

        Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#s3_stage_vpce_dns_name Task#s3_stage_vpce_dns_name}
        '''
        result = self._values.get("s3_stage_vpce_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional["TaskSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#schedule Task#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["TaskSchedule"], result)

    @builtins.property
    def search_path(self) -> typing.Optional[builtins.str]:
        '''Specifies the path to search to resolve unqualified object names in queries.

        For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#search_path Task#search_path}
        '''
        result = self._values.get("search_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_queued_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#statement_queued_timeout_in_seconds Task#statement_queued_timeout_in_seconds}
        '''
        result = self._values.get("statement_queued_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statement_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#statement_timeout_in_seconds Task#statement_timeout_in_seconds}
        '''
        result = self._values.get("statement_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strict_json_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#strict_json_output Task#strict_json_output}
        '''
        result = self._values.get("strict_json_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suspend_task_after_num_failures(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of consecutive failed task runs after which the current task is suspended automatically.

        The default is 0 (no automatic suspension). For more information, check `SUSPEND_TASK_AFTER_NUM_FAILURES docs <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#suspend_task_after_num_failures Task#suspend_task_after_num_failures}
        '''
        result = self._values.get("suspend_task_after_num_failures")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_auto_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of automatic task graph retry attempts.

        If any task graphs complete in a FAILED state, Snowflake can automatically retry the task graphs from the last task in the graph that failed. For more information, check `TASK_AUTO_RETRY_ATTEMPTS docs <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#task_auto_retry_attempts Task#task_auto_retry_attempts}
        '''
        result = self._values.get("task_auto_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#time_input_format Task#time_input_format}
        '''
        result = self._values.get("time_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#time_output_format Task#time_output_format}
        '''
        result = self._values.get("time_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_day_is_always24_h(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_day_is_always_24h Task#timestamp_day_is_always_24h}
        '''
        result = self._values.get("timestamp_day_is_always24_h")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timestamp_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_input_format Task#timestamp_input_format}
        '''
        result = self._values.get("timestamp_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ltz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_LTZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_ltz_output_format Task#timestamp_ltz_output_format}
        '''
        result = self._values.get("timestamp_ltz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ntz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_ntz_output_format Task#timestamp_ntz_output_format}
        '''
        result = self._values.get("timestamp_ntz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_output_format Task#timestamp_output_format}
        '''
        result = self._values.get("timestamp_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_type_mapping Task#timestamp_type_mapping}
        '''
        result = self._values.get("timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_tz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_TZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timestamp_tz_output_format Task#timestamp_tz_output_format}
        '''
        result = self._values.get("timestamp_tz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone for the session.

        You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#timezone Task#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Controls how trace events are ingested into the event table.

        For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#trace_level Task#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_abort_on_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error.

        For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#transaction_abort_on_error Task#transaction_abort_on_error}
        '''
        result = self._values.get("transaction_abort_on_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transaction_default_isolation_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#transaction_default_isolation_level Task#transaction_default_isolation_level}
        '''
        result = self._values.get("transaction_default_isolation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def two_digit_century_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#two_digit_century_start Task#two_digit_century_start}
        '''
        result = self._values.get("two_digit_century_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unsupported_ddl_action(self) -> typing.Optional[builtins.str]:
        '''Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#unsupported_ddl_action Task#unsupported_ddl_action}
        '''
        result = self._values.get("unsupported_ddl_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_cached_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to reuse persisted query results, if available, when a matching query is submitted.

        For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#use_cached_result Task#use_cached_result}
        '''
        result = self._values.get("use_cached_result")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_task_managed_initial_warehouse_size(self) -> typing.Optional[builtins.str]:
        '''Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size.

        Once a task has successfully completed a few runs, Snowflake ignores this parameter setting. Valid values are (case-insensitive): %s. (Conflicts with warehouse). For more information about warehouses, see `docs <./warehouse>`_. For more information, check `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_managed_initial_warehouse_size Task#user_task_managed_initial_warehouse_size}
        '''
        result = self._values.get("user_task_managed_initial_warehouse_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_task_minimum_trigger_interval_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Minimum amount of time between Triggered Task executions in seconds For more information, check `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-minimum-trigger-interval-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_minimum_trigger_interval_in_seconds Task#user_task_minimum_trigger_interval_in_seconds}
        '''
        result = self._values.get("user_task_minimum_trigger_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_task_timeout_ms(self) -> typing.Optional[jsii.Number]:
        '''Specifies the time limit on a single run of the task before it times out (in milliseconds).

        For more information, check `USER_TASK_TIMEOUT_MS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#user_task_timeout_ms Task#user_task_timeout_ms}
        '''
        result = self._values.get("user_task_timeout_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warehouse(self) -> typing.Optional[builtins.str]:
        '''The warehouse the task will use.

        Omit this parameter to use Snowflake-managed compute resources for runs of this task. Due to Snowflake limitations warehouse identifier can consist of only upper-cased letters. (Conflicts with user_task_managed_initial_warehouse_size) For more information about this resource, see `docs <./warehouse>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#warehouse Task#warehouse}
        '''
        result = self._values.get("warehouse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_of_year_policy(self) -> typing.Optional[jsii.Number]:
        '''Specifies how the weeks in a given year are computed.

        ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#week_of_year_policy Task#week_of_year_policy}
        '''
        result = self._values.get("week_of_year_policy")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the first day of the week (used by week-related date functions).

        ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#week_start Task#week_start}
        '''
        result = self._values.get("week_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def when(self) -> typing.Optional[builtins.str]:
        '''Specifies a Boolean SQL expression;

        multiple conditions joined with AND/OR are supported. When a task is triggered (based on its SCHEDULE or AFTER setting), it validates the conditions of the expression to determine whether to execute. If the conditions of the expression are not met, then the task skips the current run. Any tasks that identify this task as a predecessor also don’t run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#when Task#when}
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersAbortDetachedQuery",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersAbortDetachedQuery:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersAbortDetachedQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersAbortDetachedQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersAbortDetachedQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b73aae876d930fd857f18e2d0bdedd651d71fd07c4606e368a04e551f713dc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersAbortDetachedQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9835c44ab36dc7d9b2dac3f39a662ccfc2b1c4aa0bb4b41c485b579041fde813)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersAbortDetachedQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40a872971f2652c809c91399a61c3a69a15e342874a9fdd6017f2b6c434f746)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db1ac5e89fc2cf3a232bc41e2114865145fd9f8ce4d25a700f1bba1fa9457405)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2e3c8bac0e9ec6fc98cfe6d02f2d2f86d7425c38e16146c4186efbe3b31091e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersAbortDetachedQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersAbortDetachedQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08f16f43b0554e0ddc8f9c02c79247c3d760774cf982fc4e10de97ea145129d6)
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
    def internal_value(self) -> typing.Optional[TaskParametersAbortDetachedQuery]:
        return typing.cast(typing.Optional[TaskParametersAbortDetachedQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersAbortDetachedQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6e3431b861831c6b090342368c246c97754beff2c969fd360145bac4305293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersAutocommit",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersAutocommit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersAutocommit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersAutocommitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersAutocommitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49bae18e3f800aaabadbc176d8822ab63284b3d93d10669043224984b662c0c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersAutocommitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fa5dce3862c534d03d6d4cf431d39b9e0ed0cf991b84ffd9213e2f88d87f28)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersAutocommitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317d602b83630bdeb58be9cc0314f3c65d7e76e290497399a5a9d89925b823cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02ccdf42a58d5bc497fec8bb3927a2cfc08fc851ecc39ba4e1418156d012e928)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53f60107b9c838ae02da6a92e4b6aa7547711a5fc3a1f3d28d0d9034ce99d761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersAutocommitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersAutocommitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa45f18596a3c7ded5511cd629fa663ddda1590251c7d9ea778f3de888b9cf4e)
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
    def internal_value(self) -> typing.Optional[TaskParametersAutocommit]:
        return typing.cast(typing.Optional[TaskParametersAutocommit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersAutocommit]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3277c03ac9a70baeda04be60bb2a1d01a615aa83b1d59cb1f21083be52091a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersBinaryInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersBinaryInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersBinaryInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersBinaryInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersBinaryInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fb2e4e1ffe6542bc9ac4cfb666e84480a2b3af9d43ca0e40ebf45c992d365d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersBinaryInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325b8a92290e4220702502464f8cd7f0066475e34adf5dd39409af0f20780e67)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersBinaryInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc4aa6896663095300d91c45aad3f917cda5cd147ca69517a96cbd526b108ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47413068cfafc9ef79e611f0e695af4227c2987d701363ef5d4217cfb088a36f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bceefe509e2fe709e07958a7c4c882b69195c01da20dd124586790dae907e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersBinaryInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersBinaryInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edb3f30d80f4c17f59c58348fef1a795a8b9fdf6894d49a329fb3264a3330ca6)
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
    def internal_value(self) -> typing.Optional[TaskParametersBinaryInputFormat]:
        return typing.cast(typing.Optional[TaskParametersBinaryInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersBinaryInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2368add5ea53b9ec9fa8ee602f84db353283827e9a49a7645315fcb2f2f91ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersBinaryOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersBinaryOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersBinaryOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersBinaryOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersBinaryOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__610fe7b1b5c2c613df7a224fad12444beb088e4ca599bc425c1d2154ed0ec964)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersBinaryOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62af58a233e07eadf7e237d33446813ba0b45469388e69e76f3f5defe3a2104a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersBinaryOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8180ba36fffb792d4591ccbb04e08bd42fe72598746c615be6b55841be5ee05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91ff0f94fc5f322ea83824eded186c65d884cf7954de449b5454cfadcb170dc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70223987389a978d7d27afd0053d90a159b9104d8ba721780e4bcadaf6b7b27d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersBinaryOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersBinaryOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d3be9088a67955be8d5746c399bdff88e6dd13a4680341ea009a614d03f3305)
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
    def internal_value(self) -> typing.Optional[TaskParametersBinaryOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersBinaryOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersBinaryOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53dade3bb7c15c732eaeae0e1bb99c845240baf734e3ab664f45d519e97e615e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientMemoryLimit",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersClientMemoryLimit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersClientMemoryLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersClientMemoryLimitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientMemoryLimitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__836625564fc549c8fcf95639ea7c06da9a536dcfb1443f683b458afd80b4c7c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersClientMemoryLimitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5324e1499806813c076ed46516fab84899d6852cab25e700043ab2a8b5e5dbd5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersClientMemoryLimitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0642437bf9f5bbb2d628040684d96e869e231cf3dacbd592b68190f83887b6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cacf24ba596cf009f6e293d4c6d3230f14fb6488aadbb73c4ced333f8dab24c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e3a55701363519a2dc21bfbb28dac5d800f286ccdb79bb2e57c9593b83b1230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientMemoryLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientMemoryLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2242bc2449b370e1c0a4b87bedfbf990cf7be425771a442df61865c2c99a5a4)
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
    def internal_value(self) -> typing.Optional[TaskParametersClientMemoryLimit]:
        return typing.cast(typing.Optional[TaskParametersClientMemoryLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersClientMemoryLimit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34b0e90db1fe54ce47170a0caf1ace878139768368797830a40d86f4ae6f322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientMetadataRequestUseConnectionCtx",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersClientMetadataRequestUseConnectionCtx:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersClientMetadataRequestUseConnectionCtx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersClientMetadataRequestUseConnectionCtxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientMetadataRequestUseConnectionCtxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30052684102c32a4989c72acac5f69fb2ac90e7a1b71f6de9316830df85c7012)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersClientMetadataRequestUseConnectionCtxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc40c08c756d6b74e3efe7ec9dc14c26911b2db1de198b4483c5f52c8395a87)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersClientMetadataRequestUseConnectionCtxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ed5c28cadb0291cf8c4d07bac2b9ac3ae5162524eabc84976a28c73b3d7027)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a24ec2bddba93b2f10eaa92ef723e6a926a9fe0b125fc5c1e89e5df80858b1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24ae83d023a89c5b91952e27335c44cb3b95fcfd623c12d975f82e1bf4e60e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientMetadataRequestUseConnectionCtxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientMetadataRequestUseConnectionCtxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed34180e0ab48409ef54f206c7017603cb81b0014b29a53a19fc41a50ebdca2)
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
    ) -> typing.Optional[TaskParametersClientMetadataRequestUseConnectionCtx]:
        return typing.cast(typing.Optional[TaskParametersClientMetadataRequestUseConnectionCtx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersClientMetadataRequestUseConnectionCtx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7029d02d57177bfe31d48ccc05583d4563cfc5e7182dfd011432668b9b6089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientPrefetchThreads",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersClientPrefetchThreads:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersClientPrefetchThreads(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersClientPrefetchThreadsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientPrefetchThreadsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c5d145c191878a9f845c5a8346d095da7c45cce65f30a9bcd3faf6bd539e673)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersClientPrefetchThreadsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b66fc6fe2b7eb4ed50cf5de30a53753322adb512fff4d897f4fe190a83ee76)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersClientPrefetchThreadsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381b2cd38b968643947ac27b269c0ad914dc782c756fbf6a2806942123b46d45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c08bce8ae9bfa40a9ec0224993bd88c357c46c66d31a797dfb77a16be772dd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44631ac96ee3128d73351ae5d6fe682fe7f80095891b1e971aa97183bbaca846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientPrefetchThreadsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientPrefetchThreadsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e24b3944e9a0aa38160760828b91042bc0a12095fdc01e63f804db9fa2051dfa)
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
    def internal_value(self) -> typing.Optional[TaskParametersClientPrefetchThreads]:
        return typing.cast(typing.Optional[TaskParametersClientPrefetchThreads], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersClientPrefetchThreads],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6099059751e45d55692821b44adc72c68f42fe60fa4dc2e3e61580bbc459d75a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientResultChunkSize",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersClientResultChunkSize:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersClientResultChunkSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersClientResultChunkSizeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientResultChunkSizeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__caf61ed870be8ebbf53ec0a14158b44322fb2ae01e59343a5254b6f8f123a309)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersClientResultChunkSizeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2598331c1f41b12f2dfd8fea4df6d8256456054aa2283adb89ccc13fb9739de9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersClientResultChunkSizeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b967d7150f26aeb84f01086d8a89f4eef8822d9e9ad1a4a4969f8e033124cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaaaceb48cebb79152d6541f915f25eb6419149e96d19624be717d64c0e24c53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d62b717c931cf9b02eee450949ea464a0e08a6dba8a77ac43502e7b62e86e727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientResultChunkSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientResultChunkSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a84f82293bffd3b6e29d1d176d6f8695f102be4d963cc5a1681ff800e4356e9d)
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
    def internal_value(self) -> typing.Optional[TaskParametersClientResultChunkSize]:
        return typing.cast(typing.Optional[TaskParametersClientResultChunkSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersClientResultChunkSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437585183697a07751a74105f879e3518a0e4a5b92901d804d8672a2149df978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientResultColumnCaseInsensitive",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersClientResultColumnCaseInsensitive:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersClientResultColumnCaseInsensitive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersClientResultColumnCaseInsensitiveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientResultColumnCaseInsensitiveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6660bb318a88147b12534e6a8f3199596e7ec2bda4850f61cb61629e2b183526)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersClientResultColumnCaseInsensitiveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce59af7d84f22943e604e9fa2822ed88b27ed71b573307f6f76fccb9dc58c5f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersClientResultColumnCaseInsensitiveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7002a515c91f14315b395eeae0ff15755ce3a44a2a3573a16b7ac62909a699e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebef6f5b410c909ba01e20d7cfcd76a979ab3a9c724f84282c208286965a0bcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b2f0545293940e5e83735ceef84fddbb05ae97521e870fa3669507d56dfedfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientResultColumnCaseInsensitiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientResultColumnCaseInsensitiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__856db7bd94503897839b658989d73d1dad347ba8f8afe30515aec08fbe2e342b)
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
    ) -> typing.Optional[TaskParametersClientResultColumnCaseInsensitive]:
        return typing.cast(typing.Optional[TaskParametersClientResultColumnCaseInsensitive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersClientResultColumnCaseInsensitive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29d5ab59a766a83b5a3761a71b4147611d83f2f4e058da8d748e9e8c7863342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientSessionKeepAlive",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersClientSessionKeepAlive:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersClientSessionKeepAlive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientSessionKeepAliveHeartbeatFrequency",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersClientSessionKeepAliveHeartbeatFrequency:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersClientSessionKeepAliveHeartbeatFrequency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersClientSessionKeepAliveHeartbeatFrequencyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientSessionKeepAliveHeartbeatFrequencyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f5ef0e33fa366abd5ac4bb40365d5c3d364ba82298507b34f7451efcf51dc57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc08b8df2727ee5d52f05c0a58873d03ce779b5b164c1eb40b23ff381b680f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02e6848a31faaaf204a460d3c40ee31f582317a4db616df82ff6fc121249b22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96bfc1fa4c2b4c51d6d1b7a200be03f4ea257f7f9b5c79553461e522d8cb3ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d500be8a94feb9511fc3eb38ed78bc5689b6208e2d6f711ec7b451cfa8d3aef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f93fb817e02951b89845c3fe67a082bbc8f816dd0c5ee39b66a3eef207e03e1)
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
    ) -> typing.Optional[TaskParametersClientSessionKeepAliveHeartbeatFrequency]:
        return typing.cast(typing.Optional[TaskParametersClientSessionKeepAliveHeartbeatFrequency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersClientSessionKeepAliveHeartbeatFrequency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__550bbd467444b1d438a63a664aa10498d4a597bf35814c0fafebe3cca2b59406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientSessionKeepAliveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientSessionKeepAliveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5db656afe468fdce86b1c0877367188992f23f5a034b631c9698c1ca3656f0e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersClientSessionKeepAliveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31781fb8d007b093570184055de66afa2c33565d36197454f97ff84dc4401619)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersClientSessionKeepAliveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e2992061ca1143290f75d2fe6cb14b3179b8bcf562a94f98db6f58580e13fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4f417797690915f72e25804e28f5716681b5688c96adbe280e6ac0a14b7a0bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8c606712197fe5e54f6e8376fa1a6306628fed4ae45058d7f924422bfdf9e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientSessionKeepAliveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientSessionKeepAliveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a34dd74774294e9f750483df19b66c7678b5b0f583f8ad49c4e41b24e4a59904)
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
    def internal_value(self) -> typing.Optional[TaskParametersClientSessionKeepAlive]:
        return typing.cast(typing.Optional[TaskParametersClientSessionKeepAlive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersClientSessionKeepAlive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b7bf0665734583851f1c8c7c84839f16e387eec0f438ee20dd67dd6d44dbab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientTimestampTypeMapping",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersClientTimestampTypeMapping:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersClientTimestampTypeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersClientTimestampTypeMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientTimestampTypeMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d439b35530ab5c7caf4ca592950309ce933f86f1df661795111fd1f0f93e27b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersClientTimestampTypeMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfec196b003a9bc4fd465ce739e4a375db338b525113f81fca924349208110e0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersClientTimestampTypeMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4caa0c4c6d1bd3e06dfdcb5a33bc2a18b1bc230fd1178a2e99166986b61639d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3265fcdd7bbfa4de0ee8e26745ce5ce3c19803431ddf02393992050750f43cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b740384b5746b04783874e95792a6eb6fd75f9afe98affb5ee79874940a5b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersClientTimestampTypeMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersClientTimestampTypeMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46a88275756662a4ab51c7b73484a42191f889afa671809be2d75555a8e4a56b)
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
    ) -> typing.Optional[TaskParametersClientTimestampTypeMapping]:
        return typing.cast(typing.Optional[TaskParametersClientTimestampTypeMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersClientTimestampTypeMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fde68bf8add1ef0c5e6f720d56d760e4bc1993514c3e817269fd9a529730ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersDateInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersDateInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersDateInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersDateInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersDateInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59635f7368a8dd21cfe8724c7505024034fa5493cd5c924147876bb96db079e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersDateInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895d09a7d4bff99570ec666f15094d701cb7f866ba41200428f2a8460a0644db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersDateInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84224647ffcab3ed7aa9d7b11af387a0ebc15e8c26ee396789e1d977b18d380)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac109e62a2b58de7cf52a8e2c6c6d8e3c3499c30d0b8a636a65746083f002d2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3af6d8104c3046e2a81abde1f66a0703d5a144037072bb64c7de66bfac8f028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersDateInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersDateInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37582a44b56236f69fabf4e8be8f9e62eed2169db7190a9998a90b2f7937fc0b)
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
    def internal_value(self) -> typing.Optional[TaskParametersDateInputFormat]:
        return typing.cast(typing.Optional[TaskParametersDateInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersDateInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1364ff2558e20da90b1916825b0b4894c947d8ef7a668aa5388fe48cee91bfe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersDateOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersDateOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersDateOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersDateOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersDateOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c186a60bd835fb85e0196ee37c003fc3369b636359d122502d16815c1b90bda)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersDateOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9741a68a39adc6d2ed421475bb595e4ad8f97ca8d2c4d3fa07504c3dc864278)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersDateOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448c719799eae775338b4af4356f044b56082f57cdf2e029fa4d130c6ed4a5f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef2976bdd03d71f49dce622c06a3b370131f24e537e3658d033f948c5b30c347)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8207e982556d19d88e583049102ecdc5f918b1105fdde9345960f1daab2e24bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersDateOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersDateOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f7191ac06455205646fb259df6d5adc7c5321cb40ff008ccf5ad8ed75db0505)
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
    def internal_value(self) -> typing.Optional[TaskParametersDateOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersDateOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersDateOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03e9dbb44510e1f0636c84e1e826269fd7553af0f44e758dd838e78a51fdb40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersEnableUnloadPhysicalTypeOptimization",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersEnableUnloadPhysicalTypeOptimization:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersEnableUnloadPhysicalTypeOptimization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersEnableUnloadPhysicalTypeOptimizationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersEnableUnloadPhysicalTypeOptimizationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88ebb70ad88a3cc5b9d3a0a2f38b33f4f84e817f25f4aeeb15ebd4cedf8cfa9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersEnableUnloadPhysicalTypeOptimizationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fefc6b0287a6b22a59d3bfa31b1456e14e3eae19a2f372c97ed239bf4c83f074)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersEnableUnloadPhysicalTypeOptimizationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a8367611a38d43eb682b09d0a90a08e1d1869053f7ed0309036dc298e763f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5691f04aef9e8b7973c5c3d32de7b64606838fd8c0f24773adef1c2662fd9874)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc410b98c233be28b42045c018a7b1b8edb2e143d13c4e245043840e4b6dae3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersEnableUnloadPhysicalTypeOptimizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersEnableUnloadPhysicalTypeOptimizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a7f7dd302b3e56798831fdd3c2952995a870858c7c98159eef3dfd75fb668fb)
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
    ) -> typing.Optional[TaskParametersEnableUnloadPhysicalTypeOptimization]:
        return typing.cast(typing.Optional[TaskParametersEnableUnloadPhysicalTypeOptimization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersEnableUnloadPhysicalTypeOptimization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23607c3174479f6dab808e336fc60368a0705cb8cd1cf921c12d55ebf66a6ae0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersErrorOnNondeterministicMerge",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersErrorOnNondeterministicMerge:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersErrorOnNondeterministicMerge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersErrorOnNondeterministicMergeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersErrorOnNondeterministicMergeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e870dabae361a29c178c915483b85e71d163e76ec837d9c98a099837510c395)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersErrorOnNondeterministicMergeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd24910b308f2119888921c632c0f02d0824ef3a92ac2d9088293bf023882fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersErrorOnNondeterministicMergeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92024ae81ccc5d14613e31d76c0df63ce23c051d029094fcf3bdff594dbd1c5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81f278e5b5698a9fc0c72246cdb2a2b01274d47e1658b4b0ab9702317c24ee0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6efe069994f2d920799020ef77db4c615b52495e7fb9e702f3d9c5661505468e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersErrorOnNondeterministicMergeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersErrorOnNondeterministicMergeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ed78497a0686d79ec5c4c6e5dfee9cec2e6369180d06e577f7004b7de6f07dd)
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
    ) -> typing.Optional[TaskParametersErrorOnNondeterministicMerge]:
        return typing.cast(typing.Optional[TaskParametersErrorOnNondeterministicMerge], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersErrorOnNondeterministicMerge],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4b23e31b47a52b6876e60a263ce23708cd5b90b4446e9490b1767e7552e4d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersErrorOnNondeterministicUpdate",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersErrorOnNondeterministicUpdate:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersErrorOnNondeterministicUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersErrorOnNondeterministicUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersErrorOnNondeterministicUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5da3a384338fea73e085f127b8d790fbc13088e557cc83066606df35e0d7e973)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersErrorOnNondeterministicUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307b5699e15999b8b29d1b8298ce2459fba33e4b36432e159e19f68fb1a97079)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersErrorOnNondeterministicUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76cead59c8c110157d2cd2359aa7adc3d1417a4eaa6b8b48720ab2205caefa43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37b24ab3f04c13f5513d37e9d6a41df15afa209285da185b6d4674024a3a64ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac7cb3d0cf83ce486eeee55275b1072a9b668704f35005ebd06378f01ed2e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersErrorOnNondeterministicUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersErrorOnNondeterministicUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5158d1250437228c49682041aef384f9edba20f8ed9a01b2e96d0ee65e8ce149)
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
    ) -> typing.Optional[TaskParametersErrorOnNondeterministicUpdate]:
        return typing.cast(typing.Optional[TaskParametersErrorOnNondeterministicUpdate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersErrorOnNondeterministicUpdate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020ce17dffdbc0df461957c5bf0c2e397f35205c15bf41a3b1ac72266ec6ecee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersGeographyOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersGeographyOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersGeographyOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersGeographyOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersGeographyOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64c6cb63905dcda889fdbdb2d921ec1317db872929cc99409fe8950a51a3e2bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersGeographyOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e296bf94f551230278383543d1f5d350d12e841bf798210d5aa1852284dfe5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersGeographyOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511a8097851716a61e8fbad4979bee7f30c1e4daeec9c3c985557c390232a319)
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
            type_hints = typing.get_type_hints(_typecheckingstub__443d36ac6c456bf54a1c1675391a131c5133802d24d3fa41c92c174f9c17cc29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e190a8ab710fb238661dfddfdab9ea8d384a16f793853f30f8edca5949137a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersGeographyOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersGeographyOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6990534faa5a192a6d0e9a36a1224eb04d11b2e4897d9b359712b8d224cc4286)
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
    def internal_value(self) -> typing.Optional[TaskParametersGeographyOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersGeographyOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersGeographyOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75104ca1758987bebe8372d507f9d5c25c2577871a50eaad65d1e241f01699a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersGeometryOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersGeometryOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersGeometryOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersGeometryOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersGeometryOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__191ef3972bb76e492bc6cd792b4eb5bd139f5412778e7b8c2e60e9a618e57402)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersGeometryOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a89792f8aa61f41568de0ce855dc78e02f28ced766323e9ae8fe9b27e88b378)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersGeometryOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1548bc6482d96c97f1c283b7f1ce49a4f28d49fc68ecb1fb6254115a341a83b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24fc37ea824739324f4d88f7e830a7afd96477ce2786457ea766ec8117a02806)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40a7f87f9bd6b7c4e677f08955c9f763229802e3ee740d2b4a5ebd3b19d24c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersGeometryOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersGeometryOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__339d92b5bf783df3a4a6d7ed5ecc02474799f99fe73217fbebd3598b7ee55dff)
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
    def internal_value(self) -> typing.Optional[TaskParametersGeometryOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersGeometryOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersGeometryOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__558e1db1844d8600bc4ef112756094c09e2d0ede4fe4a431b73731676b72937e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJdbcTreatTimestampNtzAsUtc",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersJdbcTreatTimestampNtzAsUtc:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersJdbcTreatTimestampNtzAsUtc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersJdbcTreatTimestampNtzAsUtcList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJdbcTreatTimestampNtzAsUtcList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96133c47d6f3b7c30455f78e44c8dc5803805744f7e9e784059006b1eafb6269)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersJdbcTreatTimestampNtzAsUtcOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97310ee6a2e9815320af973c5df53e103450d34b53d4a7cd757ba1058644f09)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersJdbcTreatTimestampNtzAsUtcOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c56abb447b23e12e0475039b118bbafb6a03022c93d23b467865f9ba6ec13c40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf0e96fc3bddcc3d5845aba94896783e0dd34c0637d81b460a3a504b83d39c25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cc47922c4175cd0916d2a1818863013756db5b1489a5af858971da65b09e038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersJdbcTreatTimestampNtzAsUtcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJdbcTreatTimestampNtzAsUtcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec64a26c2f50763cfd23eca3b373fbc4d364d6719c6ff985c6b136a0b13bc097)
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
    ) -> typing.Optional[TaskParametersJdbcTreatTimestampNtzAsUtc]:
        return typing.cast(typing.Optional[TaskParametersJdbcTreatTimestampNtzAsUtc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersJdbcTreatTimestampNtzAsUtc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6588920269acb5747f61b728f79451939149cceec7b4bc33db1b5f600b3b7c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJdbcUseSessionTimezone",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersJdbcUseSessionTimezone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersJdbcUseSessionTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersJdbcUseSessionTimezoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJdbcUseSessionTimezoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cf73227def480b608a60293a5bf2476396736148a0b42fe037231090af20329)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersJdbcUseSessionTimezoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142c1ea92719b176be45f3d4b0f397626e42ceec1e8e4f746776e740bb0d76c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersJdbcUseSessionTimezoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d481456244f2b175af24d2901d4bd05aff0a0cbd1715ff637a5ab3cb02f457)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3475cea6802cdd08c97b7ee9e8a49292192a737ab91145a6fa763ba2e55a9c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1cd1c020ae84c427352e5b94438343094ea679a498c92ae7df356c7bffe5d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersJdbcUseSessionTimezoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJdbcUseSessionTimezoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84b335497dbf2f9aeeee980781e5decd5d881c48ae26718d02766089587992a3)
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
    def internal_value(self) -> typing.Optional[TaskParametersJdbcUseSessionTimezone]:
        return typing.cast(typing.Optional[TaskParametersJdbcUseSessionTimezone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersJdbcUseSessionTimezone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f22a981a1ac2b6ca11f01bde44f3b3396a0f9e14f43b707531f138933c1187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJsonIndent",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersJsonIndent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersJsonIndent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersJsonIndentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJsonIndentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c24e45df5f1de03492e86fffd66f5dee55c5034684ff22d1d574909f3e2be1ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersJsonIndentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5211b1203ce89f3c22eba8861ef5db116adae2c5658d7572fc57a2375160fc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersJsonIndentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cd8d9af1da69322d24cf4772513e2e3fd124a5de2fb061a89e2be2b00c5873)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22eb1e9e35bbfaa9ec776fb752247fa74f93dfdc62c940726dad136dc0cc9bea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1313286a3a968ef53791e57cfb3433529b702f2c81f999a1ce41d09d0d4014d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersJsonIndentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersJsonIndentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47177963c61f164a71d965657429b576fa4ecd212d86da33cfa3d9ce18770dcc)
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
    def internal_value(self) -> typing.Optional[TaskParametersJsonIndent]:
        return typing.cast(typing.Optional[TaskParametersJsonIndent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersJsonIndent]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbc07b70fd347a0ae7bac55595130ee8ce4ff30d1d898c8e33bb502a9c3dc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TaskParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ad4d666962efa13e5719a0b8899867dc4d81a7b6270f4da5bdbe73f31e27511)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e424510baf56c0a1b3d948c982829b66917a2bc902c8e6a14fd4403145f9bb19)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10769265213fa68d98b2c1a68037c62e269821aea96f81f108eee88cc3a4a775)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e030a7460a7bd72162f4eb2acfbad9f37b4625017c4a0bc834b4183f5dc3b93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ebecafac458d6b2425fb4b4d77dad7e89662746879f22653df778073372508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersLockTimeout",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersLockTimeout:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersLockTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersLockTimeoutList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersLockTimeoutList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8685a351c60ecc68fa5e7a197ef65d3807e9f11f2859a2dfe3b8b069809e0690)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersLockTimeoutOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2efd9f4d89a5658f17e1b0e45133d7c39bde1164619ed32e1f910a11a3496a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersLockTimeoutOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c830d30fecad8231f6b15a05446c102c91c3d7112f6dc2df246200c8720ab406)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a80b4afcf6e657c185e926a354b566b0f3b0bf6162bd8b8351864e4b325f3d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abcf7ff796a73cd9577e4fc54248256cf9a7fc8bc5fa20d0eabad0f6350a00a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersLockTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersLockTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b995ed4092664a06ad7a0584a66b8e400cd67ccb0083b61b1101f73b6eea1450)
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
    def internal_value(self) -> typing.Optional[TaskParametersLockTimeout]:
        return typing.cast(typing.Optional[TaskParametersLockTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersLockTimeout]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abef5311eec7e0ce6290286965666aeedd9e54185a3615c1d1056d1cbeda314c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__829eef6be32c389bde0a2266617c2fe771c0bc2f548955e944da0c84c5c28ab7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c029610a9fddb29afd2f34c9b3da34f4628e388beba10a32d3eaefb4a26af28d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd32f17a43502964abd271955af63959bc2ee219cbad0d06c6bf9bbea53490f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8267044404839c94d13619b93d9dfd55960063e4368a23229f7dab54763b435f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63c0192801d039c65817a476b33476204cdc541bf6f23f82515a6a2ad404dabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b75e5c8225dd7d7cd6480f0f5c4c748f7244752a1f6074cd30aa0fe131e20107)
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
    def internal_value(self) -> typing.Optional[TaskParametersLogLevel]:
        return typing.cast(typing.Optional[TaskParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersLogLevel]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aced19c0e523beb2f0dd81e401a00677c069b413090139a1f74cb9efd6346c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersMultiStatementCount",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersMultiStatementCount:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersMultiStatementCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersMultiStatementCountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersMultiStatementCountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4b0b599a14a4ac52b803303b52c348a929286944a0cea440c6374d147dca543)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersMultiStatementCountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16be429af632ea591679896dd728a7c586994093145bf8021ed27f2eb6b68adc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersMultiStatementCountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8152f2c0b5b07ed6d9bbb0061d00bcc4f464096c6028c64c502d6859b8815dca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14d9aaace5bbb4c2f899bd0c3ffaff0a359c99853fb53541288e817d551a87b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__678d9cdfb72744c933a241228f33039b3f6a4b1f6dabb566ee2e7752799f63f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersMultiStatementCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersMultiStatementCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b4e304976b3dca4e4849b11b321b20d0b5123b0406c6915dcbebc884df5934a)
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
    def internal_value(self) -> typing.Optional[TaskParametersMultiStatementCount]:
        return typing.cast(typing.Optional[TaskParametersMultiStatementCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersMultiStatementCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b87cee452ddba9ed90c200ec2dabd4ea2741e0b3633416f25b5964f19bf614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersNoorderSequenceAsDefault",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersNoorderSequenceAsDefault:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersNoorderSequenceAsDefault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersNoorderSequenceAsDefaultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersNoorderSequenceAsDefaultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b2dfa7acf382a1b7fea1a77ff5ffd5b41c20ee8b308851751ebd66cae37e0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersNoorderSequenceAsDefaultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20caacc7dd67fef85ef8c8bbaeb320f19cffecb603ed8192242d6fdf15066b0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersNoorderSequenceAsDefaultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b868a367a43456a33e2e67a0bcd1b4c0fb4d0e11fbd64294721065a773d032)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd73201d07579c465d8697c843123ab331ddd6500643df544debab7f5901c95d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f88d34d8bec689617a4cb6d15bfbe618f90e50bc408d2f09534ce2ea149bd7e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersNoorderSequenceAsDefaultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersNoorderSequenceAsDefaultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96f916243ff1cea2deebbe0af09847aa748155907959085236db5639cb5f7969)
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
    def internal_value(self) -> typing.Optional[TaskParametersNoorderSequenceAsDefault]:
        return typing.cast(typing.Optional[TaskParametersNoorderSequenceAsDefault], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersNoorderSequenceAsDefault],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b67933251d1d8ff675036e40e51b1628f6098015c39a006f9b770c041da53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersOdbcTreatDecimalAsInt",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersOdbcTreatDecimalAsInt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersOdbcTreatDecimalAsInt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersOdbcTreatDecimalAsIntList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersOdbcTreatDecimalAsIntList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98cdfc0359e792dfafab83b00ca62459ac74b3c338dc821dccd38c909f6fcb63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersOdbcTreatDecimalAsIntOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1280d8d967a7eeedfcc8cf4d10088f2b0dab9c13e71a88a0c2407fdab3533f50)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersOdbcTreatDecimalAsIntOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62df6e1f4df7ac3eac1b36bcd86a6e2b48ab98f256e67ddf9b7ab7125e4d828)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3afef9c2a9dc3da75628c9de26e115501529506515c13eba596206640dc42c47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c3a5c9ad832d2e1f7976f4ecededc7a43f6ae451e521312f3831719ac9afdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersOdbcTreatDecimalAsIntOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersOdbcTreatDecimalAsIntOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eefba97ef74ce76930deb29066d6141616df8768d8bf1cad15f86b6421a97cf6)
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
    def internal_value(self) -> typing.Optional[TaskParametersOdbcTreatDecimalAsInt]:
        return typing.cast(typing.Optional[TaskParametersOdbcTreatDecimalAsInt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersOdbcTreatDecimalAsInt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26f1b6e42f9f5d7ab1aa33b0d5dc436f144726fe865df7140b60e9a2b9d172e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TaskParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc28bd9775ed896864720c198251f765dfd88e84e431ae2c3a7887f8ee3bfe73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="abortDetachedQuery")
    def abort_detached_query(self) -> TaskParametersAbortDetachedQueryList:
        return typing.cast(TaskParametersAbortDetachedQueryList, jsii.get(self, "abortDetachedQuery"))

    @builtins.property
    @jsii.member(jsii_name="autocommit")
    def autocommit(self) -> TaskParametersAutocommitList:
        return typing.cast(TaskParametersAutocommitList, jsii.get(self, "autocommit"))

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> TaskParametersBinaryInputFormatList:
        return typing.cast(TaskParametersBinaryInputFormatList, jsii.get(self, "binaryInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> TaskParametersBinaryOutputFormatList:
        return typing.cast(TaskParametersBinaryOutputFormatList, jsii.get(self, "binaryOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> TaskParametersClientMemoryLimitList:
        return typing.cast(TaskParametersClientMemoryLimitList, jsii.get(self, "clientMemoryLimit"))

    @builtins.property
    @jsii.member(jsii_name="clientMetadataRequestUseConnectionCtx")
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> TaskParametersClientMetadataRequestUseConnectionCtxList:
        return typing.cast(TaskParametersClientMetadataRequestUseConnectionCtxList, jsii.get(self, "clientMetadataRequestUseConnectionCtx"))

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(self) -> TaskParametersClientPrefetchThreadsList:
        return typing.cast(TaskParametersClientPrefetchThreadsList, jsii.get(self, "clientPrefetchThreads"))

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(self) -> TaskParametersClientResultChunkSizeList:
        return typing.cast(TaskParametersClientResultChunkSizeList, jsii.get(self, "clientResultChunkSize"))

    @builtins.property
    @jsii.member(jsii_name="clientResultColumnCaseInsensitive")
    def client_result_column_case_insensitive(
        self,
    ) -> TaskParametersClientResultColumnCaseInsensitiveList:
        return typing.cast(TaskParametersClientResultColumnCaseInsensitiveList, jsii.get(self, "clientResultColumnCaseInsensitive"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAlive")
    def client_session_keep_alive(self) -> TaskParametersClientSessionKeepAliveList:
        return typing.cast(TaskParametersClientSessionKeepAliveList, jsii.get(self, "clientSessionKeepAlive"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> TaskParametersClientSessionKeepAliveHeartbeatFrequencyList:
        return typing.cast(TaskParametersClientSessionKeepAliveHeartbeatFrequencyList, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(
        self,
    ) -> TaskParametersClientTimestampTypeMappingList:
        return typing.cast(TaskParametersClientTimestampTypeMappingList, jsii.get(self, "clientTimestampTypeMapping"))

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> TaskParametersDateInputFormatList:
        return typing.cast(TaskParametersDateInputFormatList, jsii.get(self, "dateInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> TaskParametersDateOutputFormatList:
        return typing.cast(TaskParametersDateOutputFormatList, jsii.get(self, "dateOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="enableUnloadPhysicalTypeOptimization")
    def enable_unload_physical_type_optimization(
        self,
    ) -> TaskParametersEnableUnloadPhysicalTypeOptimizationList:
        return typing.cast(TaskParametersEnableUnloadPhysicalTypeOptimizationList, jsii.get(self, "enableUnloadPhysicalTypeOptimization"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicMerge")
    def error_on_nondeterministic_merge(
        self,
    ) -> TaskParametersErrorOnNondeterministicMergeList:
        return typing.cast(TaskParametersErrorOnNondeterministicMergeList, jsii.get(self, "errorOnNondeterministicMerge"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicUpdate")
    def error_on_nondeterministic_update(
        self,
    ) -> TaskParametersErrorOnNondeterministicUpdateList:
        return typing.cast(TaskParametersErrorOnNondeterministicUpdateList, jsii.get(self, "errorOnNondeterministicUpdate"))

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(self) -> TaskParametersGeographyOutputFormatList:
        return typing.cast(TaskParametersGeographyOutputFormatList, jsii.get(self, "geographyOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(self) -> TaskParametersGeometryOutputFormatList:
        return typing.cast(TaskParametersGeometryOutputFormatList, jsii.get(self, "geometryOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatTimestampNtzAsUtc")
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> TaskParametersJdbcTreatTimestampNtzAsUtcList:
        return typing.cast(TaskParametersJdbcTreatTimestampNtzAsUtcList, jsii.get(self, "jdbcTreatTimestampNtzAsUtc"))

    @builtins.property
    @jsii.member(jsii_name="jdbcUseSessionTimezone")
    def jdbc_use_session_timezone(self) -> TaskParametersJdbcUseSessionTimezoneList:
        return typing.cast(TaskParametersJdbcUseSessionTimezoneList, jsii.get(self, "jdbcUseSessionTimezone"))

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> TaskParametersJsonIndentList:
        return typing.cast(TaskParametersJsonIndentList, jsii.get(self, "jsonIndent"))

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> TaskParametersLockTimeoutList:
        return typing.cast(TaskParametersLockTimeoutList, jsii.get(self, "lockTimeout"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> TaskParametersLogLevelList:
        return typing.cast(TaskParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(self) -> TaskParametersMultiStatementCountList:
        return typing.cast(TaskParametersMultiStatementCountList, jsii.get(self, "multiStatementCount"))

    @builtins.property
    @jsii.member(jsii_name="noorderSequenceAsDefault")
    def noorder_sequence_as_default(self) -> TaskParametersNoorderSequenceAsDefaultList:
        return typing.cast(TaskParametersNoorderSequenceAsDefaultList, jsii.get(self, "noorderSequenceAsDefault"))

    @builtins.property
    @jsii.member(jsii_name="odbcTreatDecimalAsInt")
    def odbc_treat_decimal_as_int(self) -> TaskParametersOdbcTreatDecimalAsIntList:
        return typing.cast(TaskParametersOdbcTreatDecimalAsIntList, jsii.get(self, "odbcTreatDecimalAsInt"))

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> "TaskParametersQueryTagList":
        return typing.cast("TaskParametersQueryTagList", jsii.get(self, "queryTag"))

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCase")
    def quoted_identifiers_ignore_case(
        self,
    ) -> "TaskParametersQuotedIdentifiersIgnoreCaseList":
        return typing.cast("TaskParametersQuotedIdentifiersIgnoreCaseList", jsii.get(self, "quotedIdentifiersIgnoreCase"))

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> "TaskParametersRowsPerResultsetList":
        return typing.cast("TaskParametersRowsPerResultsetList", jsii.get(self, "rowsPerResultset"))

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(self) -> "TaskParametersS3StageVpceDnsNameList":
        return typing.cast("TaskParametersS3StageVpceDnsNameList", jsii.get(self, "s3StageVpceDnsName"))

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> "TaskParametersSearchPathList":
        return typing.cast("TaskParametersSearchPathList", jsii.get(self, "searchPath"))

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(
        self,
    ) -> "TaskParametersStatementQueuedTimeoutInSecondsList":
        return typing.cast("TaskParametersStatementQueuedTimeoutInSecondsList", jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(
        self,
    ) -> "TaskParametersStatementTimeoutInSecondsList":
        return typing.cast("TaskParametersStatementTimeoutInSecondsList", jsii.get(self, "statementTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="strictJsonOutput")
    def strict_json_output(self) -> "TaskParametersStrictJsonOutputList":
        return typing.cast("TaskParametersStrictJsonOutputList", jsii.get(self, "strictJsonOutput"))

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailures")
    def suspend_task_after_num_failures(
        self,
    ) -> "TaskParametersSuspendTaskAfterNumFailuresList":
        return typing.cast("TaskParametersSuspendTaskAfterNumFailuresList", jsii.get(self, "suspendTaskAfterNumFailures"))

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttempts")
    def task_auto_retry_attempts(self) -> "TaskParametersTaskAutoRetryAttemptsList":
        return typing.cast("TaskParametersTaskAutoRetryAttemptsList", jsii.get(self, "taskAutoRetryAttempts"))

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> "TaskParametersTimeInputFormatList":
        return typing.cast("TaskParametersTimeInputFormatList", jsii.get(self, "timeInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> "TaskParametersTimeOutputFormatList":
        return typing.cast("TaskParametersTimeOutputFormatList", jsii.get(self, "timeOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampDayIsAlways24H")
    def timestamp_day_is_always24_h(
        self,
    ) -> "TaskParametersTimestampDayIsAlways24HList":
        return typing.cast("TaskParametersTimestampDayIsAlways24HList", jsii.get(self, "timestampDayIsAlways24H"))

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(self) -> "TaskParametersTimestampInputFormatList":
        return typing.cast("TaskParametersTimestampInputFormatList", jsii.get(self, "timestampInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(
        self,
    ) -> "TaskParametersTimestampLtzOutputFormatList":
        return typing.cast("TaskParametersTimestampLtzOutputFormatList", jsii.get(self, "timestampLtzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(
        self,
    ) -> "TaskParametersTimestampNtzOutputFormatList":
        return typing.cast("TaskParametersTimestampNtzOutputFormatList", jsii.get(self, "timestampNtzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(self) -> "TaskParametersTimestampOutputFormatList":
        return typing.cast("TaskParametersTimestampOutputFormatList", jsii.get(self, "timestampOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(self) -> "TaskParametersTimestampTypeMappingList":
        return typing.cast("TaskParametersTimestampTypeMappingList", jsii.get(self, "timestampTypeMapping"))

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(self) -> "TaskParametersTimestampTzOutputFormatList":
        return typing.cast("TaskParametersTimestampTzOutputFormatList", jsii.get(self, "timestampTzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> "TaskParametersTimezoneList":
        return typing.cast("TaskParametersTimezoneList", jsii.get(self, "timezone"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "TaskParametersTraceLevelList":
        return typing.cast("TaskParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="transactionAbortOnError")
    def transaction_abort_on_error(self) -> "TaskParametersTransactionAbortOnErrorList":
        return typing.cast("TaskParametersTransactionAbortOnErrorList", jsii.get(self, "transactionAbortOnError"))

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(
        self,
    ) -> "TaskParametersTransactionDefaultIsolationLevelList":
        return typing.cast("TaskParametersTransactionDefaultIsolationLevelList", jsii.get(self, "transactionDefaultIsolationLevel"))

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(self) -> "TaskParametersTwoDigitCenturyStartList":
        return typing.cast("TaskParametersTwoDigitCenturyStartList", jsii.get(self, "twoDigitCenturyStart"))

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(self) -> "TaskParametersUnsupportedDdlActionList":
        return typing.cast("TaskParametersUnsupportedDdlActionList", jsii.get(self, "unsupportedDdlAction"))

    @builtins.property
    @jsii.member(jsii_name="useCachedResult")
    def use_cached_result(self) -> "TaskParametersUseCachedResultList":
        return typing.cast("TaskParametersUseCachedResultList", jsii.get(self, "useCachedResult"))

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSize")
    def user_task_managed_initial_warehouse_size(
        self,
    ) -> "TaskParametersUserTaskManagedInitialWarehouseSizeList":
        return typing.cast("TaskParametersUserTaskManagedInitialWarehouseSizeList", jsii.get(self, "userTaskManagedInitialWarehouseSize"))

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSeconds")
    def user_task_minimum_trigger_interval_in_seconds(
        self,
    ) -> "TaskParametersUserTaskMinimumTriggerIntervalInSecondsList":
        return typing.cast("TaskParametersUserTaskMinimumTriggerIntervalInSecondsList", jsii.get(self, "userTaskMinimumTriggerIntervalInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMs")
    def user_task_timeout_ms(self) -> "TaskParametersUserTaskTimeoutMsList":
        return typing.cast("TaskParametersUserTaskTimeoutMsList", jsii.get(self, "userTaskTimeoutMs"))

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> "TaskParametersWeekOfYearPolicyList":
        return typing.cast("TaskParametersWeekOfYearPolicyList", jsii.get(self, "weekOfYearPolicy"))

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> "TaskParametersWeekStartList":
        return typing.cast("TaskParametersWeekStartList", jsii.get(self, "weekStart"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TaskParameters]:
        return typing.cast(typing.Optional[TaskParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f798241430ed58dadfc2429b3520a59dae2af9d7682dec174174ab7de0e5d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersQueryTag",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersQueryTag:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersQueryTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersQueryTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersQueryTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65a85c7549f8b1fa916c05a59392a5d545fa2480e5c3e053ae8a85e4487e35d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersQueryTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4de21e0a1fc204085d2b9ccec9501c348b8cb2c93747ebb56012553fca06b3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersQueryTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f2e50f7b39b3a52b6c22994059e57916f2db96ce0285e61185cd82ebeaeb7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e0f226c0f84ebaa3d9e7c9ad676fc2d8628538535ffbd26be3e184b07a1f97b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02a8c7eee5f9ec6ffbc3bd4e9e0dd61e1d441348e822afcaba52cda66b638d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersQueryTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersQueryTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecd461d76e002e1f4e229f2457a2b8319d5fb5d4601ada6ddb98e77c6e7b3d75)
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
    def internal_value(self) -> typing.Optional[TaskParametersQueryTag]:
        return typing.cast(typing.Optional[TaskParametersQueryTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersQueryTag]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259141e16c1e8348d3a6179f70b75ce3cde0cb903207cd34c82c09cee0d6054f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersQuotedIdentifiersIgnoreCase",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersQuotedIdentifiersIgnoreCase:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersQuotedIdentifiersIgnoreCase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersQuotedIdentifiersIgnoreCaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersQuotedIdentifiersIgnoreCaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dbadd8d1fa8a7783eee80e3c31415410bb135d8233b640016d42d3acae4aa3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersQuotedIdentifiersIgnoreCaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1122b57befcc9202df39bcd1be7bbe2bd5d0e048ea1f1ef62cda38396ef3f00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersQuotedIdentifiersIgnoreCaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd77693ba13243bcc417840a26fc8f393da70bccbc156438603ced5cd7704eec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d918a549bfdfab5909643d73aea338d742873e5512460f7f7800023235a49e85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07e3eeb82934a488fa15f55d493d4aba7f4397a5444971f05b78aa700187fdd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersQuotedIdentifiersIgnoreCaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersQuotedIdentifiersIgnoreCaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b70345402db76c2964e79e437e0fb4509d3505fc322c6a41d5c9c0e7eab622f2)
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
    ) -> typing.Optional[TaskParametersQuotedIdentifiersIgnoreCase]:
        return typing.cast(typing.Optional[TaskParametersQuotedIdentifiersIgnoreCase], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersQuotedIdentifiersIgnoreCase],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c28b0cf8e5ac32afc2a6aad14d835b163c448c0f4f01b385c510ac7b84d5f9e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersRowsPerResultset",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersRowsPerResultset:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersRowsPerResultset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersRowsPerResultsetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersRowsPerResultsetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66c6dfb97bb1619a8c29ec5a17b42b4971096550feade40cd05f17b8d92ce630)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersRowsPerResultsetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c53ab5bd43f4c13b7afe56f7bf5ddb2986593e56639d9d2efaf48eafaea79e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersRowsPerResultsetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e024dc3e676ee30bff339040d6e2771ac3d4bc4492cda0e5b8f0c495848c0bc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba10f0216eb4f94a6738c189a0bb08f99738fb881a89ef9e04c28cced5270505)
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
            type_hints = typing.get_type_hints(_typecheckingstub__875d18a7ea092dbd9ddb310e5b9a0e3b931d26a700e3a9e72668f15cc3bc36f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersRowsPerResultsetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersRowsPerResultsetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2593cd5c7b0f5e7a617d31caebbc16af6ed8a1ef62e5031bae3ff2588ee20df3)
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
    def internal_value(self) -> typing.Optional[TaskParametersRowsPerResultset]:
        return typing.cast(typing.Optional[TaskParametersRowsPerResultset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersRowsPerResultset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ebf6f4b091f48b8d1dc4adc39cbaba46c25db16a56549e7fe8c945c3d84a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersS3StageVpceDnsName",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersS3StageVpceDnsName:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersS3StageVpceDnsName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersS3StageVpceDnsNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersS3StageVpceDnsNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__555bc6be6623458196498502762eb0d1f464cc305bc69ee8aa122ad5b8b1ee7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersS3StageVpceDnsNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a811d2854cba324c167af2e07ff779096a956ad58f944ed9394d995990e56524)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersS3StageVpceDnsNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3abaffa9d37d8d3867313527525818b7e577e95b3c95e88f1ca0bf223ee32a19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97eb9bbcb38dab54a4dbda905ff443a41ba5322645174f104b9f3aefff81af74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b73c82330056f4a493cec2eaad6e1d5082cd7071f0b0e4afedf6f29777186e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersS3StageVpceDnsNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersS3StageVpceDnsNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be557275bbe119c477216345a836b66ab6129d4b4f6a1173b49ee200518c5f5d)
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
    def internal_value(self) -> typing.Optional[TaskParametersS3StageVpceDnsName]:
        return typing.cast(typing.Optional[TaskParametersS3StageVpceDnsName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersS3StageVpceDnsName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8022dc02c88b1902436b8e5ffe936b858a3af1ad986dc96aa6e8f8d5fb2134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersSearchPath",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersSearchPath:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersSearchPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersSearchPathList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersSearchPathList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d92afe4ddd151e1c7af10a00a09b31ccf06a51aec00d567b4574c85da364d32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersSearchPathOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7987ba375e11e2723abef182155332468d9d9e7add2fd6115fb6a2f8fb128638)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersSearchPathOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90c0ae51390a2309bc610d173a29b5218d83a876d28c19fb11e52a0afe531a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bea4677ef0a0976b3062958f8c8a486fb441484f08c3a1110be92393c59fc82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25cb8bc0c26cfccb9d7ed2c7d1f6507fcc5276f54a42acfc904c8dfc31270861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersSearchPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersSearchPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c055da144632cc69212a5e762b08b2b6054fa1b60aabe7f91a81cd39b1c4f33d)
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
    def internal_value(self) -> typing.Optional[TaskParametersSearchPath]:
        return typing.cast(typing.Optional[TaskParametersSearchPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersSearchPath]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b04cdfbfdefbdb13ada36e51a6e4b5eb8ecade72e81f6c1f8385b1e338d264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStatementQueuedTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersStatementQueuedTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersStatementQueuedTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersStatementQueuedTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStatementQueuedTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33f74fadbafa4d6eab6c1f5a91bf65d509afd34692122354dd5e0893360e3efe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersStatementQueuedTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38af6713b14d1bc3b425e11c7c7e1fb8829df6c9d0fa83e1f2283cdfdc2a238f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersStatementQueuedTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b018cc10decf2f51e255ae42ee55a1b091a094a53d92616863a58adf977265b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f647be362f64ee2b952179ba2cc0a487a5f5ab19f550036aab93095a9eb5d50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41134057de5698093b801957372c4990f07f3b255e7e54be9c1a149ff86b9bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersStatementQueuedTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStatementQueuedTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6dbb1384ec1eb9d84dac5dcae9a7be52bbc2d64b51b9c5d529060c881c65535)
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
    ) -> typing.Optional[TaskParametersStatementQueuedTimeoutInSeconds]:
        return typing.cast(typing.Optional[TaskParametersStatementQueuedTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersStatementQueuedTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d321884796d81b04994a388e60d18cdbab0b1c05cdd91aac90afa77d1305c6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStatementTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersStatementTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersStatementTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersStatementTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStatementTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65675e4abec87bbbbb0fa8e952788e687f1785d8643a70fc4fc55cebd65afa2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersStatementTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2957e2bbdb5093ac511f36f503dc4e46e0f4f3e7f65607b1b86226a780de719d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersStatementTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efaaee39aa99a9eb954b8cd6a6d1ee89bfa861f624fd5de9106c8bb2bbd7e4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12027c28f2b56db299e004a3d3e42cc4cec81c941b9cb11a353c5189e3f92c46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df294bf189ece60ebe9cd9eb2bcc260809c22d0a25abca7de5798b95289f38ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersStatementTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStatementTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c107f07b0a50c8299be218e55849309c7e3bb6c8dac59f4dc34f2021c318178)
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
    ) -> typing.Optional[TaskParametersStatementTimeoutInSeconds]:
        return typing.cast(typing.Optional[TaskParametersStatementTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersStatementTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5c2040d449228cacb5e25279ba19ae24a7294997c7cda820608aa1121aeb79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStrictJsonOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersStrictJsonOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersStrictJsonOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersStrictJsonOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStrictJsonOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc9032c44facc1fd2778466486d1bc26f84f935987fe2f1775991ba595662a8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersStrictJsonOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253ea670a9572bda49c4583f1cdd8ae482dd871c8dfb0fcd8c3d542dd094bc76)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersStrictJsonOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbef12e23913418974e468f34ecb5a333ed90177a4a770ce96a0ae89aa34303c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f58f9c8bc2fa9067bdd129618a972c86f73fa6b37c7e6d370cee979f85683983)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fe4104f0836561fe14016936c08e2383fe0c043c6b0c88ecbdc007560a80ec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersStrictJsonOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersStrictJsonOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2184b2cd8e9a83270cd6b63086795ac2e5b63b1330bcfee635f546851471d485)
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
    def internal_value(self) -> typing.Optional[TaskParametersStrictJsonOutput]:
        return typing.cast(typing.Optional[TaskParametersStrictJsonOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersStrictJsonOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9197d957683ecd4392506a58c91a241266327a97ac906be2e94c489a2c39c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersSuspendTaskAfterNumFailures",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersSuspendTaskAfterNumFailures:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersSuspendTaskAfterNumFailures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersSuspendTaskAfterNumFailuresList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersSuspendTaskAfterNumFailuresList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b7d4aebd41bb6968f40d0bd0d31c7575c4cbd71c7ca87ddbf35c2e7e2c2b4bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersSuspendTaskAfterNumFailuresOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc87f7219b501d3e7af5597824bbdb48cfae4dd9fe264a0338f17bcf986a7c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersSuspendTaskAfterNumFailuresOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331e026be61a45d09a8f14ba90b124822638d36d863be4d8794c0662d46f45ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba24134f11f4503ac52d527c9571e969245536f6f5f51ee3b8a84f1c7e56ff0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09f234741b7056b551f3c811aa4854ff0c8fccd451747007387e4c094aede3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersSuspendTaskAfterNumFailuresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersSuspendTaskAfterNumFailuresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0296a3f98e63910c0d312fe2b036632fc3f314b2e456eab3f7dc345201316dc3)
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
    ) -> typing.Optional[TaskParametersSuspendTaskAfterNumFailures]:
        return typing.cast(typing.Optional[TaskParametersSuspendTaskAfterNumFailures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersSuspendTaskAfterNumFailures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5e508f43a826726b8bc3d31f7d3b6907afaec79f7c55da7070587c1d4653fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTaskAutoRetryAttempts",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTaskAutoRetryAttempts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTaskAutoRetryAttempts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTaskAutoRetryAttemptsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTaskAutoRetryAttemptsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58b08eb41e97d6ca282794f3ab3397b14b925d947e277002e3328c047967b1a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTaskAutoRetryAttemptsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7624fe3f204f66b3f7c0a6bfdd73bba55b4b85bb2cae195b4bdcdbb55c1f59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTaskAutoRetryAttemptsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ff12c7b5431f6848855d19d99a62e0ca51da6cc30b9d3082f3cf5b831f8f72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__599e7cc46a564ec1c3755ad24821faad7baa63330c04c77e97a67e40a3381205)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcdc4b64d7bb3075d6fddd447996101bb2f8b86e4b3f20e226d8007cf0cd297a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTaskAutoRetryAttemptsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTaskAutoRetryAttemptsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1424d660c67808ec414b9c3f06c7ddfdcfaf8dd1fcdbcd04448e5e2a89457794)
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
    def internal_value(self) -> typing.Optional[TaskParametersTaskAutoRetryAttempts]:
        return typing.cast(typing.Optional[TaskParametersTaskAutoRetryAttempts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTaskAutoRetryAttempts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac99f805d59f87ad5166b470dfee1344c165386f551557aec2e5c58463aa017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimeInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimeInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimeInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimeInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimeInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d84a8f3cdfa1e632882b6e6a329f42eef66c75da7e2714c393c8cecbab98140)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersTimeInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563aa10a9e4c69a53800d43606868ebd6320402dfce4ea6fc56c078305a548a7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimeInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ed3c1858249700e6fa0c7aae2515eb633ce37dbb4a13fdd6862e17d6cddb0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4a946e2e44002c86e5b3524ed5126b6dbaeb92d8210469466d2c6f748f17f56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ae265212541774707bead61b6c142f2a4068a08f026c792da64a1c8383fc5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimeInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimeInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a76451e3ef4a2d3a235636296ca5833baeda4417ae4f76c69811345e91316d84)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimeInputFormat]:
        return typing.cast(typing.Optional[TaskParametersTimeInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimeInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbd2968ef4ee6ba03f4f59f544eb7f712d040c4ba262679b289020acb764a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimeOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimeOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimeOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimeOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimeOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d47727d6ef9dde9a08b33412a93aeabdf8b5fa8e07ebed9af729f812cb405aff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTimeOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95041f63d9fbe8a5bc287c60ffef8d85c2586ee686c1cc4e819cede2bfc2af4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimeOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88e70e4d768e277e6e09c6798706ca5d6a2ff8026baed79b5ec74aa60822933)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c34103d7bc556091b7267e77beb6f13d984c0f95068cdfc14cc45584c3475e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e67b95a97f02a546639b4b8bf78e1288e7305c59b5faf09a8f3b4bf753e35f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimeOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimeOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7220094462bf7ba330286cda766543952fffe0507810fa9aeeda486d2cb5c48f)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimeOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersTimeOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimeOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb279292348300b4ac1aac5fcecaeebf636704866e12d387e5c807957a634a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampDayIsAlways24H",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimestampDayIsAlways24H:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimestampDayIsAlways24H(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimestampDayIsAlways24HList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampDayIsAlways24HList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3ff0d0c5fd8326e49111f6ad23571eb26395453ca961e122ba2b34312992a8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTimestampDayIsAlways24HOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9864a192d1924b5b6f2b0596f34bc60b6aa4f4756095c76b4d17ea7b488ba8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimestampDayIsAlways24HOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f03e615dac59fe2a8d3c67ebbaaefc1916f11cb0e8661e773f83e0a3338812f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c8aa4796cd6b6a4e1539de18d913d6f88541dcfee90c5e18b622d7157c8b2ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e6d8d5100f1a4bb894574e200a09d570dd3fe31de72f5dea0956c9daf77de69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimestampDayIsAlways24HOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampDayIsAlways24HOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0050d44437e04eddd00c8dfece420e7ce5b7a46ad0d8ff01b99a4a0d8c361c18)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimestampDayIsAlways24H]:
        return typing.cast(typing.Optional[TaskParametersTimestampDayIsAlways24H], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimestampDayIsAlways24H],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741114dc2c5e3bdc9c2f5ddc9b5cb2153133e64a06b4020e39b18412c961c83b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimestampInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimestampInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimestampInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d1b38e9d680a43a8de91f58dc173d27d58a94507d1a6e758c6f6ede0057ad96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTimestampInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e181639547e8eea31ca07c8be0641cbaae8ecfdd27982df9dcd39580e8e82b55)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimestampInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b524e858eba73ff26f1db046eddfd6eecb411375a4fd1326f92705c8c3f3e45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__099ec6427daa2f458f49c38ff925954d22bf8b23280d9a67149c762c3c6d8df8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff514a8e6cfd1fc2cdbfcadbfe11df9f7e32b38c9db3dfaeb2eeebaa85f8c3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimestampInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c9f54722bc4c34da5a19052cad869e2b9eb0f0b8fc25b066bd889644f027e53)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimestampInputFormat]:
        return typing.cast(typing.Optional[TaskParametersTimestampInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimestampInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c53215b2108a7bf5ba74c76be3d355229f6fa3d79489c106bf94bbd05895d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampLtzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimestampLtzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimestampLtzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimestampLtzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampLtzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c440980df93ab2d277ea636ccfa290f10567ab34a24a3a53412b9ff6165fdd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTimestampLtzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756680784b9370858e4005843777609e264f7eb36c901d0c5dfb7b47a115f617)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimestampLtzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d46284455f7632cb2da75695f66c79e1353235c2996de719e2077806ada0fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f7d069a27f8e2148d43c5122b0f6e21c5d8561ea531504f26f796a753f4978d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8bd67f9d70bf96f98890dcf895c1dbd7ef18b3b9e0d3ec8f9e938c8412069f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimestampLtzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampLtzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fde33f2f7a12d565c464fd51736e43eabd3c2aa4af003ef3c146625dae0b0611)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimestampLtzOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersTimestampLtzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimestampLtzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d331726ef1f2b12770c966d5c7fbac575f8af339500ab912238ce4a4360b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampNtzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimestampNtzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimestampNtzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimestampNtzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampNtzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a17c9c6f28a10468bf4cfc14288475caa4331f383c3b8a8ea1b67fd1207659b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTimestampNtzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7a68e1e265161c2a33f070a089a683054e35ce7e42e7f6bb96caa296a8fd46)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimestampNtzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219865d848265104d60b8de29755834177f579bae9496ac711766180627618c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__703f7ee36e765e187b7e60e132260874637994256b942e24f4f6547a95114d59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e1216677dac718ae4336f06fda7aa0a91cce8a1f3ec1dd7d5e588520c8c8bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimestampNtzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampNtzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__243c7398a50dd36de057f7b98c469b065a3338f544258fc278dbc83950c6b9c7)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimestampNtzOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersTimestampNtzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimestampNtzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d3bfc223e94be298a2fde6525abb40664fcde8a40442ec7a5aa60baf2a9790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimestampOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimestampOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimestampOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9ef5bc7b2bfb4a5e8abe97c4b5e021d6a8daf0c4178543b5c1c354351877bbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTimestampOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0208e0c50f0274903b4e9deed5fadca4d9620c8568f3baf97e9815bab163ff0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimestampOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a5e9451a37cbc8ddfd056e7dafaea3f55f1c153735eb3defcb89d09ca4757c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d700870872ca6ca9d57c1e1aa7f66b947a6bd5dc4147aac7309eb288e9cc52a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f484ad4143c3eed8c03a5045a4ccb33231b08fb82f62b6698a9cfe83e1acec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimestampOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73ad260521b66ea531d07a1fae9be3a4c06275d3fed9a9bfd463becbef83d041)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimestampOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersTimestampOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimestampOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0eda903d6b5f53bf2daabe5766f8148344290854d53d478bb4df0894d83ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampTypeMapping",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimestampTypeMapping:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimestampTypeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimestampTypeMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampTypeMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__075f58c953e951f1579921dd58eb79071238feef993da3d31c6ff891a6a37024)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTimestampTypeMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c994d02706907484e33966187cc26cbcda14cab9c355db845274b695e43a1065)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimestampTypeMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553800f13c1bffce1665d31cb57540ae06e6d66a9af08043a464981dc6d783ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bc2486a678a3c855451591c8d24b79a0d6055a3d56cfb27e1f5385e88a7f2fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b6e9f401d69c06a651786aef30e5d97155f81b60256ea82136b8b177b5c1d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimestampTypeMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampTypeMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__900304c3d624ef4ebbe2c3d4cf177856d990c2242d9f44d6c05dffa3400c1ccb)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimestampTypeMapping]:
        return typing.cast(typing.Optional[TaskParametersTimestampTypeMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimestampTypeMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77bc87b69b090e04897a3ff899269bf99e84d27e896efd154572e9a7ffac603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampTzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimestampTzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimestampTzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimestampTzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampTzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68798b482247b9659e95bb88ea2759debcb6b44b8dd39b91d5f0432b08b340ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTimestampTzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad281e7c37c4aa336f6c39a5a3a34a287228f1a10f75409155cdb7701f9c671c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimestampTzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664a7c76fc7108a3f9881c52055648a0a0503abf4d338717af190ef7b68a62f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72910fc4b530d8492aa643ce1589df63db4c04430cd2235af096a0a9f1020d4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3a9e78a88c062fdd1675de8efe7bb9347313d82f79ed06324ae097788abac52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimestampTzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimestampTzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__144f3d6558c31f0d6d940a04c7df531f35503a0740aaa0c152f69860e691a21c)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimestampTzOutputFormat]:
        return typing.cast(typing.Optional[TaskParametersTimestampTzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTimestampTzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef94d5424a0ff5e0bcbb6c83c149c68b520959bcc5c01eb51137642403ffcba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimezone",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTimezone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTimezoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimezoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1dcddd3f5874745bc455785c13f2ce8e176c76e7f8643f0973cc06dd6f1f65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersTimezoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762ea65ff13b0892d5f42d6bf2182b58f6115e6ab354ce69175906bb3a836861)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTimezoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9e7e5cdff5b7740292810e87b312fe5a9cd279837e7bad8c18c6b0ba45d518)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9b41151d368b555ff674f10a04d1cb141fa8889f24963c873b06abccfa56659)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63411ab3b0b5c1d8c9402fda7ab75d4eaed8d3a6b0facfb96828dcdf8382ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTimezoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTimezoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3716388dac8e0ae9aa0a93111b2ee10516e3bda94580f856eb85999b68df3655)
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
    def internal_value(self) -> typing.Optional[TaskParametersTimezone]:
        return typing.cast(typing.Optional[TaskParametersTimezone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersTimezone]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2d809d67a129e8b70ef3f1ca93edde790297dcf7d29feb69c6476c8f5b0aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e34df8bff311dc018564b2e16d21caf705d4bce89c2a8065f2c30c6dfe8acd7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640acc49329b8b7f0a85883f37b14e5dee5308e7ee9b047c48abd43a3e2f87cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f6c95ebb4f2e3cb13a5f0c46f2fecf3d6c4644e2c96b9a864725fa3aa02f52)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b68d720e698aab30188dc0836ac3a2895a32931128ae3f9d644505888689814)
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
            type_hints = typing.get_type_hints(_typecheckingstub__405c097b251c685d2f73589218a379978bc4ee1add609435dfaac1e9dc42ae27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b645e1d49c8f03470af99e784c132b50520a2cb74fbfeb6005f20b1ad160e7f)
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
    def internal_value(self) -> typing.Optional[TaskParametersTraceLevel]:
        return typing.cast(typing.Optional[TaskParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersTraceLevel]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d531cb89c37ebcf6fc54c41772cc3f2a147f73d70b4a751e9eab412853f10153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTransactionAbortOnError",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTransactionAbortOnError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTransactionAbortOnError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTransactionAbortOnErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTransactionAbortOnErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e8828855010daf5d327109af6b93e14a93123f64a98f79d9fce50d40c6db937)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTransactionAbortOnErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9babe2b23f6a8bba969de2763bf1625f761b2e55ae2f1684e103e5a46bb958)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTransactionAbortOnErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08ad5e25539c129e8f9c8376bef14a3d42a717f4e140c77429c4d2b90ef3e079)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c8235af58d8b6d40ea06794b773d4f4f7ba53dbcf9533aa2bee7de0ad7a9954)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e62b7c329f236b3a6ebcb634fd136ff32bcb17390d58debc9628dd5610ae379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTransactionAbortOnErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTransactionAbortOnErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5b8e4cdb1717773ba610ef6da83afeacced362f2928980d682243c7800a2624)
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
    def internal_value(self) -> typing.Optional[TaskParametersTransactionAbortOnError]:
        return typing.cast(typing.Optional[TaskParametersTransactionAbortOnError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTransactionAbortOnError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265520e24d7d725bbf2416794ca4077dcbdfdc297111c7d38baed1e918f081ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTransactionDefaultIsolationLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTransactionDefaultIsolationLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTransactionDefaultIsolationLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTransactionDefaultIsolationLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTransactionDefaultIsolationLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53e5e8d44ea4db7b1cf46d8cdb009a5cf79362ed23977e90eb260de7713f5d87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTransactionDefaultIsolationLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9538a280492a8404b64bb8deee12375f837788e9dad9b5a6b2802972f9a48ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTransactionDefaultIsolationLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5327040e69ed9ee9a879138a4d7f7e3581d4c501005acedada72f981918aeb8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bba42e7265c4747f3dda20cd1d780c998625fb0c0fa6cd296475db47b46e23e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0b6ebd9d503d742cb5a2c2a952ed960660c5c5f9ef3c9461c058f855569d871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTransactionDefaultIsolationLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTransactionDefaultIsolationLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__135093678c1dba810c9bd0fc2a37edb02334b77f4133f3f1cc49373e71efa129)
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
    ) -> typing.Optional[TaskParametersTransactionDefaultIsolationLevel]:
        return typing.cast(typing.Optional[TaskParametersTransactionDefaultIsolationLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTransactionDefaultIsolationLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c237cafae88b9a5f194281e3eb37f02700be96ffc8000d3ae2b987749312929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTwoDigitCenturyStart",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersTwoDigitCenturyStart:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersTwoDigitCenturyStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersTwoDigitCenturyStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTwoDigitCenturyStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2f38e13d915bb57e3d0048600efc0b6e4ec68a5af90585aab725cec8f6b8c59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersTwoDigitCenturyStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3b514ab2861dfb70d02de53cbb56de19d98662d00dd31f88a26144743ab262)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersTwoDigitCenturyStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11361d43dca81e5b04eeac465852dbd36b021dfd7e78eb6e854666fbc9cf90e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94f710e9b0dbd3b02dcfba18312d7044b578f7be01f43f88f542015d0a2c6384)
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
            type_hints = typing.get_type_hints(_typecheckingstub__250cb7bc985b0fd070950917e83c62c2ee502ba193263826e4b0abca79a5358f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersTwoDigitCenturyStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersTwoDigitCenturyStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87f052581ade425f9e3579a1cf299f6b5a591e037e2655def47440e39a82e7e7)
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
    def internal_value(self) -> typing.Optional[TaskParametersTwoDigitCenturyStart]:
        return typing.cast(typing.Optional[TaskParametersTwoDigitCenturyStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersTwoDigitCenturyStart],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0245c5085b4a697bc920e1e3d396820a891d07b2b20ac3754822006b919a571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUnsupportedDdlAction",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersUnsupportedDdlAction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersUnsupportedDdlAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersUnsupportedDdlActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUnsupportedDdlActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6df3017ff44b16b5ca6b56847b8d95c2f5d36b1eadc00d7bdc4c699d0351288e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersUnsupportedDdlActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0abb6275f7d1d5cdaa94bcfd75a670454dd53c94b28e9f9ff1c4b17302a9da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersUnsupportedDdlActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5821519e0ffcad8f456bac4f3d986bfb216537708b43b381875d7542f5d8f1bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95c5279fb9fcb95edadb3449ab3ebe1bd339fcb086d68c5d9630d79c93070d15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3acaa839a733ab2bd85e1d08c1d4b4039b4d9d06a9e385a4acd5619e28e02561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersUnsupportedDdlActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUnsupportedDdlActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2af037857ba211d7ff10e4b7e82e132a6b0bb697ac53407cf50d2e776bab2fce)
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
    def internal_value(self) -> typing.Optional[TaskParametersUnsupportedDdlAction]:
        return typing.cast(typing.Optional[TaskParametersUnsupportedDdlAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersUnsupportedDdlAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd06b810bf93aaa8118dff441927c250fc1a5d73f1de7f03a1da748b797ccc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUseCachedResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersUseCachedResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersUseCachedResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersUseCachedResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUseCachedResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d050a2b601ceb90a2aa4df98a608866cf49c02de787c1c9fab9b0c49edea51f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersUseCachedResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4064471f77217ffe0454ae25e8d8b5948cc5f958423f6fc30f2c8976f48937)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersUseCachedResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b265a6c36f9b6c01e13eab8d9a4d836a1cc83ef35513ce9373d44d12e8366de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f354b6b914ac4cdcfe9dd62bbebbb52395317b652045ef1f946725a610073d87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ee627d219484b46b14d6c89292015a2451ec68cab58b764c80b2a726b202b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersUseCachedResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUseCachedResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1287b6c6b51f274a31798aab1c705795058a0b6bc6ef18fdedad6ec6c30fd27)
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
    def internal_value(self) -> typing.Optional[TaskParametersUseCachedResult]:
        return typing.cast(typing.Optional[TaskParametersUseCachedResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersUseCachedResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda2e8cd610c321efc5448dd99d6c6af9d58f839b23d22ba4cba395d7c023b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskManagedInitialWarehouseSize",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersUserTaskManagedInitialWarehouseSize:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersUserTaskManagedInitialWarehouseSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersUserTaskManagedInitialWarehouseSizeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskManagedInitialWarehouseSizeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaf3621d1abff662fbfb26051f2abd4564fb5e6b814d625ba78280a7627bc44f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersUserTaskManagedInitialWarehouseSizeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4acae114616e5a914f218fefd5fe8d638d06b22367898e6b88a8fae49e385f85)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersUserTaskManagedInitialWarehouseSizeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab78e903cb5d44cc0d8b2183f616532a540a67d63b991bd5c1006a1b5f8db38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e0f93850d63f00904f7d93c7beb077772eb7f63f3532ba77626f3bcbf189e79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf3020cbd9fe119ff366a91137f7967474ceafca8a86a3a47878b732c27ac2c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersUserTaskManagedInitialWarehouseSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskManagedInitialWarehouseSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__838fecba1967612a453f4ef7a6cd62517181bf37f2ae8258750f8027586dcb05)
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
    ) -> typing.Optional[TaskParametersUserTaskManagedInitialWarehouseSize]:
        return typing.cast(typing.Optional[TaskParametersUserTaskManagedInitialWarehouseSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersUserTaskManagedInitialWarehouseSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08cc4aab54a18c180a5bdf55a84c7f45ef074b35ddef950c237762c360dbc59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskMinimumTriggerIntervalInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersUserTaskMinimumTriggerIntervalInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersUserTaskMinimumTriggerIntervalInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersUserTaskMinimumTriggerIntervalInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskMinimumTriggerIntervalInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48a7e672e19cf4566ea6cb5948574e35763b09c769c3c5c5dcac97c8b8960547)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d77a09697749a4a97cfad5e8a823e509d500ff4cb50fc35e75940e05b94f227)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b921c70858424e4e61a0e60007fe7a5b9658392a690a916d8c38e7f0e2c50d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4580b4c7db951939ed1b2d9ccb1801cee7a56322ee87cad6d882e555557b236d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4d12a85d30a473b103774c56b5b9e863045129508bd3676398c6c85ff19627a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be8930b3e3dca59f7e93d29da7cb7adb37e7eb1aeca75a2f55970ef3c2bd570e)
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
    ) -> typing.Optional[TaskParametersUserTaskMinimumTriggerIntervalInSeconds]:
        return typing.cast(typing.Optional[TaskParametersUserTaskMinimumTriggerIntervalInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersUserTaskMinimumTriggerIntervalInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ceffc56a37d0195192fbe3062ebe681f1f82625475d6fc393d4beb0be4e4a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskTimeoutMs",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersUserTaskTimeoutMs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersUserTaskTimeoutMs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersUserTaskTimeoutMsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskTimeoutMsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65deef8e7bc8c619005df00d5177c88d6da6fd66dea4bb5733df52055200232e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersUserTaskTimeoutMsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c8580b8d31ce5340129d3b109798543878365cac3be621b1188744fe3299d3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersUserTaskTimeoutMsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96116de41e2736c9aa55a56ea8d189f0037a7d3c751f459bf25d102dc90e9e57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee479c79f4d1672e1ede77c0cd7c1efc27d8aff29c52f98fafa60d8004302d74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f81ac1b9fdc75f1cba815b3395b398e5ae0194f23c80d57ba247e18caca2be2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersUserTaskTimeoutMsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersUserTaskTimeoutMsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__714344b0186203ec483a4c410063cb346e03d8cec8482f0623c6c37804a5ea46)
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
    def internal_value(self) -> typing.Optional[TaskParametersUserTaskTimeoutMs]:
        return typing.cast(typing.Optional[TaskParametersUserTaskTimeoutMs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersUserTaskTimeoutMs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bec25380ff633c52add65aa485ee62c98aae54d24556fb4007ff857168a38d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersWeekOfYearPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersWeekOfYearPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersWeekOfYearPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersWeekOfYearPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersWeekOfYearPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__802276fea21ca213cd1493e1726065776ebb30b61d906f692d73d53fe3802e8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TaskParametersWeekOfYearPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0d75bbbc91f9378103636b0ac3195ebff9c2b87ccf049b5386917e5faa8474d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersWeekOfYearPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec96826fbbeaca19bac927c80f9ae0a84b1e108766d341c82efaa12f83e291c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bd2c177aec9c889a9919f0f349fb529cd33569f1306e3d1f5d63e08cb787a8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90829dc8d441eb8b068943f51f8d2fc32e46880a14cf4772b8cf99b28a1161ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersWeekOfYearPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersWeekOfYearPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c53e88e70cefdb631e6f5d99953c94cf1e591eb44e6f3186a97345830cda21f)
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
    def internal_value(self) -> typing.Optional[TaskParametersWeekOfYearPolicy]:
        return typing.cast(typing.Optional[TaskParametersWeekOfYearPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskParametersWeekOfYearPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c789a0d6d3daca9f6ab4ba296f5410b44cd7ae89ac95237daac2f081368b20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersWeekStart",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskParametersWeekStart:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskParametersWeekStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskParametersWeekStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersWeekStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1c4865b03e4b0feed7ab4a7fb5dfd6cfc3e4cabed807aee34090165da836f21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskParametersWeekStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb52bcc8fe949f4d51d8138b2f8acd81d71b176ddb32327fd244bb9eb79bc37)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskParametersWeekStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f869b12cb49091785c3e8ffac0f6716d79fd41ebb0061ffbd7361693d2343637)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c7c4fcb0afe32116a8c664ccb3a9a9f5baf081750a81bc7bc8022e8cca24478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a60edb9b84bd046669d68afe77461bb3ac696cfffa6095d8ec1bcf9a91e933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskParametersWeekStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskParametersWeekStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9faeb76717229d9d1cf7e26cfff6b8783d750e77add90fdb0405122f0ddbb4ff)
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
    def internal_value(self) -> typing.Optional[TaskParametersWeekStart]:
        return typing.cast(typing.Optional[TaskParametersWeekStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskParametersWeekStart]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33b7de1cb92287a1bc25e22fbb273f7182cb8e72b2c04361f810bf594df2578a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskSchedule",
    jsii_struct_bases=[],
    name_mapping={"minutes": "minutes", "using_cron": "usingCron"},
)
class TaskSchedule:
    def __init__(
        self,
        *,
        minutes: typing.Optional[jsii.Number] = None,
        using_cron: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param minutes: Specifies an interval (in minutes) of wait time inserted between runs of the task. Accepts positive integers only. (conflicts with ``using_cron``) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#minutes Task#minutes}
        :param using_cron: Specifies a cron expression and time zone for periodically running the task. Supports a subset of standard cron utility syntax. (conflicts with ``minutes``) Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#using_cron Task#using_cron}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26fdd86f6131d1c9f5978fddd4ac4f3f934a0ec322df38e64f1e932a0cea784)
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument using_cron", value=using_cron, expected_type=type_hints["using_cron"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if minutes is not None:
            self._values["minutes"] = minutes
        if using_cron is not None:
            self._values["using_cron"] = using_cron

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Specifies an interval (in minutes) of wait time inserted between runs of the task.

        Accepts positive integers only. (conflicts with ``using_cron``)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#minutes Task#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def using_cron(self) -> typing.Optional[builtins.str]:
        '''Specifies a cron expression and time zone for periodically running the task.

        Supports a subset of standard cron utility syntax. (conflicts with ``minutes``)

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/task#using_cron Task#using_cron}
        '''
        result = self._values.get("using_cron")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea76911a01f30e508ea0f1a3657758ebab8b2f93a1190fc0af78d31bebc8bb35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetUsingCron")
    def reset_using_cron(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsingCron", []))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="usingCronInput")
    def using_cron_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usingCronInput"))

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5720360d1feeaf0303668e34a3098fd8c64ca0d893c1f1e35fc3fa630f35e412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usingCron")
    def using_cron(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usingCron"))

    @using_cron.setter
    def using_cron(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235f9d249174fe9af691c4256328ccce6ef623b2e0d8496ebe2117425dee801f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usingCron", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TaskSchedule]:
        return typing.cast(typing.Optional[TaskSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskSchedule]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c921879dbe22cc223b2648a95485122e1e92eddbac626502d71d5bea5fc5e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e656111545dbe9c56eadcd3bf85b829876b06d4fa4b7bd17d87f7595ba4976d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04b6ba4850ae8cb700a8c519c6730ac943fee40dcc530e19fd946557021d7fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad18050ba19f3455faf519ca5c94b2f8e1d2527cc2fc339fb350ec1990fb5efd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76b9e9864c86fdbb0360e76153e5649594bc511a5c36c53fb5cbec004f8102dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fb25368c9e1b324243bb4409919b2ae483c241cba6072a12395c32425557ac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__083e9f948a83cb8f5ad60b4794b33aa3691e6fe0c71ece5ebaa767309eac57a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowOverlappingExecution")
    def allow_overlapping_execution(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowOverlappingExecution"))

    @builtins.property
    @jsii.member(jsii_name="budget")
    def budget(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "budget"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="errorIntegration")
    def error_integration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorIntegration"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lastCommittedOn")
    def last_committed_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastCommittedOn"))

    @builtins.property
    @jsii.member(jsii_name="lastSuspendedOn")
    def last_suspended_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastSuspendedOn"))

    @builtins.property
    @jsii.member(jsii_name="lastSuspendedReason")
    def last_suspended_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastSuspendedReason"))

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
    @jsii.member(jsii_name="predecessors")
    def predecessors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "predecessors"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="taskRelations")
    def task_relations(self) -> "TaskShowOutputTaskRelationsList":
        return typing.cast("TaskShowOutputTaskRelationsList", jsii.get(self, "taskRelations"))

    @builtins.property
    @jsii.member(jsii_name="warehouse")
    def warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouse"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TaskShowOutput]:
        return typing.cast(typing.Optional[TaskShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TaskShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e26e682eb20bf553e60ccc3bc8dec759edede4272600e720314f86ffcc95de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.task.TaskShowOutputTaskRelations",
    jsii_struct_bases=[],
    name_mapping={},
)
class TaskShowOutputTaskRelations:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskShowOutputTaskRelations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TaskShowOutputTaskRelationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskShowOutputTaskRelationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f59d553c2dcf98268cda084b81eb5f693d5c53042b4bfbf0520928bec3c669ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TaskShowOutputTaskRelationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25290dc8128e1a44a8e1e7b7a5c876301a25ae237a32ddd7b41a2a86704e9c14)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TaskShowOutputTaskRelationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d489b4877187c3502033ed73eb3a8363ffe02d63c6067b792dbe2f908c3d2c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9a1dd2ca7ff24614a67799136cd6b806643c2e3cd77a63fa580677205e7a0cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7b79cf5d923d41c705aa42f6d8142d536a7816aca975870ddb3402f4bb0713c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class TaskShowOutputTaskRelationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.task.TaskShowOutputTaskRelationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d714aed54be2b18e82ebb7c95689fee6e844338a67211305085c0affa61f08a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="finalizedRootTask")
    def finalized_root_task(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finalizedRootTask"))

    @builtins.property
    @jsii.member(jsii_name="finalizer")
    def finalizer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finalizer"))

    @builtins.property
    @jsii.member(jsii_name="predecessors")
    def predecessors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "predecessors"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TaskShowOutputTaskRelations]:
        return typing.cast(typing.Optional[TaskShowOutputTaskRelations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TaskShowOutputTaskRelations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36cc5c8add9a5c66008d47f21df2b1ea3e964a1fccb197236e344e07ac659352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Task",
    "TaskConfig",
    "TaskParameters",
    "TaskParametersAbortDetachedQuery",
    "TaskParametersAbortDetachedQueryList",
    "TaskParametersAbortDetachedQueryOutputReference",
    "TaskParametersAutocommit",
    "TaskParametersAutocommitList",
    "TaskParametersAutocommitOutputReference",
    "TaskParametersBinaryInputFormat",
    "TaskParametersBinaryInputFormatList",
    "TaskParametersBinaryInputFormatOutputReference",
    "TaskParametersBinaryOutputFormat",
    "TaskParametersBinaryOutputFormatList",
    "TaskParametersBinaryOutputFormatOutputReference",
    "TaskParametersClientMemoryLimit",
    "TaskParametersClientMemoryLimitList",
    "TaskParametersClientMemoryLimitOutputReference",
    "TaskParametersClientMetadataRequestUseConnectionCtx",
    "TaskParametersClientMetadataRequestUseConnectionCtxList",
    "TaskParametersClientMetadataRequestUseConnectionCtxOutputReference",
    "TaskParametersClientPrefetchThreads",
    "TaskParametersClientPrefetchThreadsList",
    "TaskParametersClientPrefetchThreadsOutputReference",
    "TaskParametersClientResultChunkSize",
    "TaskParametersClientResultChunkSizeList",
    "TaskParametersClientResultChunkSizeOutputReference",
    "TaskParametersClientResultColumnCaseInsensitive",
    "TaskParametersClientResultColumnCaseInsensitiveList",
    "TaskParametersClientResultColumnCaseInsensitiveOutputReference",
    "TaskParametersClientSessionKeepAlive",
    "TaskParametersClientSessionKeepAliveHeartbeatFrequency",
    "TaskParametersClientSessionKeepAliveHeartbeatFrequencyList",
    "TaskParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference",
    "TaskParametersClientSessionKeepAliveList",
    "TaskParametersClientSessionKeepAliveOutputReference",
    "TaskParametersClientTimestampTypeMapping",
    "TaskParametersClientTimestampTypeMappingList",
    "TaskParametersClientTimestampTypeMappingOutputReference",
    "TaskParametersDateInputFormat",
    "TaskParametersDateInputFormatList",
    "TaskParametersDateInputFormatOutputReference",
    "TaskParametersDateOutputFormat",
    "TaskParametersDateOutputFormatList",
    "TaskParametersDateOutputFormatOutputReference",
    "TaskParametersEnableUnloadPhysicalTypeOptimization",
    "TaskParametersEnableUnloadPhysicalTypeOptimizationList",
    "TaskParametersEnableUnloadPhysicalTypeOptimizationOutputReference",
    "TaskParametersErrorOnNondeterministicMerge",
    "TaskParametersErrorOnNondeterministicMergeList",
    "TaskParametersErrorOnNondeterministicMergeOutputReference",
    "TaskParametersErrorOnNondeterministicUpdate",
    "TaskParametersErrorOnNondeterministicUpdateList",
    "TaskParametersErrorOnNondeterministicUpdateOutputReference",
    "TaskParametersGeographyOutputFormat",
    "TaskParametersGeographyOutputFormatList",
    "TaskParametersGeographyOutputFormatOutputReference",
    "TaskParametersGeometryOutputFormat",
    "TaskParametersGeometryOutputFormatList",
    "TaskParametersGeometryOutputFormatOutputReference",
    "TaskParametersJdbcTreatTimestampNtzAsUtc",
    "TaskParametersJdbcTreatTimestampNtzAsUtcList",
    "TaskParametersJdbcTreatTimestampNtzAsUtcOutputReference",
    "TaskParametersJdbcUseSessionTimezone",
    "TaskParametersJdbcUseSessionTimezoneList",
    "TaskParametersJdbcUseSessionTimezoneOutputReference",
    "TaskParametersJsonIndent",
    "TaskParametersJsonIndentList",
    "TaskParametersJsonIndentOutputReference",
    "TaskParametersList",
    "TaskParametersLockTimeout",
    "TaskParametersLockTimeoutList",
    "TaskParametersLockTimeoutOutputReference",
    "TaskParametersLogLevel",
    "TaskParametersLogLevelList",
    "TaskParametersLogLevelOutputReference",
    "TaskParametersMultiStatementCount",
    "TaskParametersMultiStatementCountList",
    "TaskParametersMultiStatementCountOutputReference",
    "TaskParametersNoorderSequenceAsDefault",
    "TaskParametersNoorderSequenceAsDefaultList",
    "TaskParametersNoorderSequenceAsDefaultOutputReference",
    "TaskParametersOdbcTreatDecimalAsInt",
    "TaskParametersOdbcTreatDecimalAsIntList",
    "TaskParametersOdbcTreatDecimalAsIntOutputReference",
    "TaskParametersOutputReference",
    "TaskParametersQueryTag",
    "TaskParametersQueryTagList",
    "TaskParametersQueryTagOutputReference",
    "TaskParametersQuotedIdentifiersIgnoreCase",
    "TaskParametersQuotedIdentifiersIgnoreCaseList",
    "TaskParametersQuotedIdentifiersIgnoreCaseOutputReference",
    "TaskParametersRowsPerResultset",
    "TaskParametersRowsPerResultsetList",
    "TaskParametersRowsPerResultsetOutputReference",
    "TaskParametersS3StageVpceDnsName",
    "TaskParametersS3StageVpceDnsNameList",
    "TaskParametersS3StageVpceDnsNameOutputReference",
    "TaskParametersSearchPath",
    "TaskParametersSearchPathList",
    "TaskParametersSearchPathOutputReference",
    "TaskParametersStatementQueuedTimeoutInSeconds",
    "TaskParametersStatementQueuedTimeoutInSecondsList",
    "TaskParametersStatementQueuedTimeoutInSecondsOutputReference",
    "TaskParametersStatementTimeoutInSeconds",
    "TaskParametersStatementTimeoutInSecondsList",
    "TaskParametersStatementTimeoutInSecondsOutputReference",
    "TaskParametersStrictJsonOutput",
    "TaskParametersStrictJsonOutputList",
    "TaskParametersStrictJsonOutputOutputReference",
    "TaskParametersSuspendTaskAfterNumFailures",
    "TaskParametersSuspendTaskAfterNumFailuresList",
    "TaskParametersSuspendTaskAfterNumFailuresOutputReference",
    "TaskParametersTaskAutoRetryAttempts",
    "TaskParametersTaskAutoRetryAttemptsList",
    "TaskParametersTaskAutoRetryAttemptsOutputReference",
    "TaskParametersTimeInputFormat",
    "TaskParametersTimeInputFormatList",
    "TaskParametersTimeInputFormatOutputReference",
    "TaskParametersTimeOutputFormat",
    "TaskParametersTimeOutputFormatList",
    "TaskParametersTimeOutputFormatOutputReference",
    "TaskParametersTimestampDayIsAlways24H",
    "TaskParametersTimestampDayIsAlways24HList",
    "TaskParametersTimestampDayIsAlways24HOutputReference",
    "TaskParametersTimestampInputFormat",
    "TaskParametersTimestampInputFormatList",
    "TaskParametersTimestampInputFormatOutputReference",
    "TaskParametersTimestampLtzOutputFormat",
    "TaskParametersTimestampLtzOutputFormatList",
    "TaskParametersTimestampLtzOutputFormatOutputReference",
    "TaskParametersTimestampNtzOutputFormat",
    "TaskParametersTimestampNtzOutputFormatList",
    "TaskParametersTimestampNtzOutputFormatOutputReference",
    "TaskParametersTimestampOutputFormat",
    "TaskParametersTimestampOutputFormatList",
    "TaskParametersTimestampOutputFormatOutputReference",
    "TaskParametersTimestampTypeMapping",
    "TaskParametersTimestampTypeMappingList",
    "TaskParametersTimestampTypeMappingOutputReference",
    "TaskParametersTimestampTzOutputFormat",
    "TaskParametersTimestampTzOutputFormatList",
    "TaskParametersTimestampTzOutputFormatOutputReference",
    "TaskParametersTimezone",
    "TaskParametersTimezoneList",
    "TaskParametersTimezoneOutputReference",
    "TaskParametersTraceLevel",
    "TaskParametersTraceLevelList",
    "TaskParametersTraceLevelOutputReference",
    "TaskParametersTransactionAbortOnError",
    "TaskParametersTransactionAbortOnErrorList",
    "TaskParametersTransactionAbortOnErrorOutputReference",
    "TaskParametersTransactionDefaultIsolationLevel",
    "TaskParametersTransactionDefaultIsolationLevelList",
    "TaskParametersTransactionDefaultIsolationLevelOutputReference",
    "TaskParametersTwoDigitCenturyStart",
    "TaskParametersTwoDigitCenturyStartList",
    "TaskParametersTwoDigitCenturyStartOutputReference",
    "TaskParametersUnsupportedDdlAction",
    "TaskParametersUnsupportedDdlActionList",
    "TaskParametersUnsupportedDdlActionOutputReference",
    "TaskParametersUseCachedResult",
    "TaskParametersUseCachedResultList",
    "TaskParametersUseCachedResultOutputReference",
    "TaskParametersUserTaskManagedInitialWarehouseSize",
    "TaskParametersUserTaskManagedInitialWarehouseSizeList",
    "TaskParametersUserTaskManagedInitialWarehouseSizeOutputReference",
    "TaskParametersUserTaskMinimumTriggerIntervalInSeconds",
    "TaskParametersUserTaskMinimumTriggerIntervalInSecondsList",
    "TaskParametersUserTaskMinimumTriggerIntervalInSecondsOutputReference",
    "TaskParametersUserTaskTimeoutMs",
    "TaskParametersUserTaskTimeoutMsList",
    "TaskParametersUserTaskTimeoutMsOutputReference",
    "TaskParametersWeekOfYearPolicy",
    "TaskParametersWeekOfYearPolicyList",
    "TaskParametersWeekOfYearPolicyOutputReference",
    "TaskParametersWeekStart",
    "TaskParametersWeekStartList",
    "TaskParametersWeekStartOutputReference",
    "TaskSchedule",
    "TaskScheduleOutputReference",
    "TaskShowOutput",
    "TaskShowOutputList",
    "TaskShowOutputOutputReference",
    "TaskShowOutputTaskRelations",
    "TaskShowOutputTaskRelationsList",
    "TaskShowOutputTaskRelationsOutputReference",
]

publication.publish()

def _typecheckingstub__c9ea4604358bdf109eaf78f231f37e685f614aef5f8076778e9130b15f8df16b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    sql_statement: builtins.str,
    started: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    after: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_overlapping_execution: typing.Optional[builtins.str] = None,
    autocommit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    binary_input_format: typing.Optional[builtins.str] = None,
    binary_output_format: typing.Optional[builtins.str] = None,
    client_memory_limit: typing.Optional[jsii.Number] = None,
    client_metadata_request_use_connection_ctx: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_prefetch_threads: typing.Optional[jsii.Number] = None,
    client_result_chunk_size: typing.Optional[jsii.Number] = None,
    client_result_column_case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_session_keep_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_session_keep_alive_heartbeat_frequency: typing.Optional[jsii.Number] = None,
    client_timestamp_type_mapping: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    config: typing.Optional[builtins.str] = None,
    date_input_format: typing.Optional[builtins.str] = None,
    date_output_format: typing.Optional[builtins.str] = None,
    enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_integration: typing.Optional[builtins.str] = None,
    error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    finalize: typing.Optional[builtins.str] = None,
    geography_output_format: typing.Optional[builtins.str] = None,
    geometry_output_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_indent: typing.Optional[jsii.Number] = None,
    lock_timeout: typing.Optional[jsii.Number] = None,
    log_level: typing.Optional[builtins.str] = None,
    multi_statement_count: typing.Optional[jsii.Number] = None,
    noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_tag: typing.Optional[builtins.str] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rows_per_resultset: typing.Optional[jsii.Number] = None,
    s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[TaskSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    search_path: typing.Optional[builtins.str] = None,
    statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
    task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
    time_input_format: typing.Optional[builtins.str] = None,
    time_output_format: typing.Optional[builtins.str] = None,
    timestamp_day_is_always24_h: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timestamp_input_format: typing.Optional[builtins.str] = None,
    timestamp_ltz_output_format: typing.Optional[builtins.str] = None,
    timestamp_ntz_output_format: typing.Optional[builtins.str] = None,
    timestamp_output_format: typing.Optional[builtins.str] = None,
    timestamp_type_mapping: typing.Optional[builtins.str] = None,
    timestamp_tz_output_format: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
    trace_level: typing.Optional[builtins.str] = None,
    transaction_abort_on_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transaction_default_isolation_level: typing.Optional[builtins.str] = None,
    two_digit_century_start: typing.Optional[jsii.Number] = None,
    unsupported_ddl_action: typing.Optional[builtins.str] = None,
    use_cached_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
    user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
    user_task_timeout_ms: typing.Optional[jsii.Number] = None,
    warehouse: typing.Optional[builtins.str] = None,
    week_of_year_policy: typing.Optional[jsii.Number] = None,
    week_start: typing.Optional[jsii.Number] = None,
    when: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4d8c59b01adbf5f8e29e6c733dbd841414111ef772ca196ca2e258f5461e7d29(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000dc1c40e67a220428cb96bf7cb09cc4f0b3f8b178495941a23748443f2b9dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4f67b7c6aaa0dff726ba8906da170893801767daeb8594a67d27e29b4a8211(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f45ea20a892361fea1f1a00ce23bf3fa2158ed4ff73473407f678b7e4d1966(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed52bd51ac39c4b02d53c556e031440abd97026a9813f0f4d71ee7da5f7566c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb3125f305c8280b29149705d01db0c20dc8e93219d3dc24ea42f2e8340677c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6221c4f6b0416e4042d00c83a22b85a3ecafe8ac94944b89106f15924fb6b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637c700d5d2b0467139b55d791050aadd034c177fad3f91bfd15085056fe1262(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2b3628ddb0842c8296d0637c79e644fb4cacacc65e2448278e75e0484e4a64(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db7243d99e12980fefad990de332880bffc74402e08c00fab52e763b84a2f09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4426fe8bd4ea007f4bf825b078e48b46ef67bef7682434b7cfb3877223fa7051(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ede84d56e4d6345bea8ec7b80845f6dae914c663e7fd56a8208cb4fe21101e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096b788c9067ad872c6182ac1120ac72584777021f5995063cd8fd3bf7bda767(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f305f4838a9b6608d2d740d284bacf14b8ca8427177adfa6cd59e3c5ea17d92(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c41cf9c392fc1149452d56c573fe7287d2eca8c4e1a3486cda39ddb8d9199f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a460ab85bdbee1b5b7d1afc2c85e737dcbf0fc049e53145eb43bcf5ac51fd64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca4e11acc7de6bd00451df8fbf84eac47525d1714900ae902cc1060fd1e02e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4663644f15e776aad0efb661ea515bf94c94a51357321a4b8454a61781655a8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f1cac5d5f949f3297141adab2d85cd48cf30efd15ee98b27acb135491cd2ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0844e07ffc28c29dd33f773b5657e1b2bcceeab2630f9209c5916db978a8c86f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198f2f6903193d6a7867ce2c2f7cfa327e45bcb384ed7d5f048bb100b388a253(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5eb20156b6371eea9d6150bb1904bc23049ba1e4170cbe9d97564bce3a4e32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a7091ea763a511d0d7d6aac91eda8352f48fe2589b2bd4970fe3d965dd677c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4576b68bcacf1e201400094ec87872eaa692bea1479646881536e16f1a28fd43(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6bd797b10149b6858ff3ecc12eb82c34e81a754d8875c454c85b378455749b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e490da0ad04f55ea72041d7a7ad70366be71fb10ec1458179fdd8d3470228b4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4951d580bd17faa92961cd864065c0d972b1263d273f9cecbbb46f26833251(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64b3bfe9c82317b45a085e9ac53577abd6c2d6c42bdfb4c9b5a38702f7a0cdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ac4d350619dd24a2df0476718884e5b07c97761bee49d3b873fc39eaa1106f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1cb3fe994d311b435fa9733c740e6910e4457cd2446b8ec938e4dee945fadb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9088a2bfd5b64fdef999d452642bac369812724888d5443e0d6a811612d20c98(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dc909823397116bcec8bf4058a0c3d831731a64c6654e469de7778f61082a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7d3f0253acb1f5642fcf01ea794f431e15e17feeb9546638fb8fb92f8ebe0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd863124f4692ee7860b1a2f8572a8bf5706309cbf4d47417627dd312bd18a87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35fdd161201488a3a65a8e3aab9a6810d45e1ad46cfb37cb179a616f85b3e1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d858bcc23f60fbf7a6a0b24fbb2c8b2dbdf262eb00106f6362ea9b9c4198ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0386968c6965db3e232384ec2c509510c8c2c9927a27b1c1b1ee48c70fd05b5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e7118930856f5db3d6bde5a565811b5df317631b0a7659cb14b9318004a10d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730207da9e10b233dc9d9524d84398699ee9ce108e3404547f68d2ddce288601(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00807a2ad95e96d76a8de34990f5922868042c1def5f3151dab6afafe4cf52eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c38ac74489a1ec15385297f1da9fb6cab68e86b4ff99d32f35fb97db4bdf60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e414d304fb0b5b56fb9ac7ec2de77f79a7b509fa1f0697c776dea0112c26c67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0382c4ecb9752bb2d404bb8295857c938035307b2c7f2aac086835abd53c2ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b278cd40c077dc3d408636838637868d09b900fc1e63409db65d40e5f8eccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2c8180e858236070f21334babaa6826e34132ad5e9ef981b98c88efd8ea3d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b77066bf27a18c21232146e79a30afa5f555f4c9c73cdd00dec8db4189eff31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5076d5b136a93294ea4e10e6fbabf3ffbea61a0341d3949102a6edd7124e1905(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd951c73ffeac27ee48f6969a8faf00a10ba7a28a77ec39a4e2e711ba15a8d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad29a4348b00843adeb8c03ba026e9b3d51c0836d9305968bd9ee4d7f94eafa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52bca2a91426ae6aa44865eb3a71e7907326767ce8f3ccec2026eebc1f4b86d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b581dcb2e7530c942a1a6ad84af489e87a2814b2c3c9f152c57e943e8b9639aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe052aea7752fcdd72fb7dd7b1d0103df9e610e8a1335817a87dbcfeab9a307a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5634334e9aa811ca6f8d622a3a5dc3741abf7a0eb417e0e9c7268262560dc45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd0903e2eeff55e572b23adfaca726d4e6d850adec915af400f8e399ea92906(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe9df6c5acb0e33d40236e196b2b34532c165d35e1090b33e2b10e2e99cb0f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e082ebbc26fba6b74675e7c9ec2209f78a6a1ed2c4c85023763284954ecac0b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9873af85c6b305a81d64bfd17f65f9c31a6cedf227ff5a94d7ddafdf2a6482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7b96a56b63f2be0a18f9a3c27842bc65fe61a1b4272dc7f17f5e328bc9fc06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a911059dd442fb2a8451d221477348274fdcef94eae305732e61bbdc31d96a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ec267cdb3bf89086e0b3b233c7a10f302e50a6bb0af429d3cfa1b9c4a6cc28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2137c00e4dbf8fb4ac0355c7fabc854bc2048550ec268ba1d418f40c811014ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7319289576ada8bc907fbc2906c172d1c7a48672a0b6e72c974c6a2af6a9e9a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb42aa5f9aff9bacd6f35feb1f06cdd0f75a8f9f838893199bd881acf7219c2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecf00a9cd7649614468d946e85905c33d4005e58a9c6e22cc5e6ec858cfdd14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4021c53075a65661455c9d1937e82d1119341d5e9c76991c0ef9a5973ff9e315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d580b67262ca576ca41c00b5da866b277ada6ad11f923c715f72ebe6407642c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd215a5b4794e793060b5f7cdaed15f6c4510f3c30f92263bf2dc02b2d7cc17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474e3cc0338e5e932ed3e8030f12840ba1aa42a2cea8d796e5ad564c4f67d77f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6add217094f96be1fdbd877c03c3acfb12531a10388192bbfa81d39cd144bd42(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6240dc59b88cc8128ed2cadcd5ef1616adff3e1f28ea512a868bf98f628315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3723ec57d593cb2af888a59c1cd076164c70c199db20322e7aa5607e02e7f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960350664d9ace313b147091fb63f8cae0d4d0389be8fd90869f821d27af750a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cca6129d7883e1890cfab97ecfe18908703485c2bb1ddb9f98ca4f633a8dfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b33c946381b3c9a032b7570564a1e2078f7d125b95b09f4d234e236ac1b576(
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
    sql_statement: builtins.str,
    started: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    after: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_overlapping_execution: typing.Optional[builtins.str] = None,
    autocommit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    binary_input_format: typing.Optional[builtins.str] = None,
    binary_output_format: typing.Optional[builtins.str] = None,
    client_memory_limit: typing.Optional[jsii.Number] = None,
    client_metadata_request_use_connection_ctx: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_prefetch_threads: typing.Optional[jsii.Number] = None,
    client_result_chunk_size: typing.Optional[jsii.Number] = None,
    client_result_column_case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_session_keep_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_session_keep_alive_heartbeat_frequency: typing.Optional[jsii.Number] = None,
    client_timestamp_type_mapping: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    config: typing.Optional[builtins.str] = None,
    date_input_format: typing.Optional[builtins.str] = None,
    date_output_format: typing.Optional[builtins.str] = None,
    enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_integration: typing.Optional[builtins.str] = None,
    error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    finalize: typing.Optional[builtins.str] = None,
    geography_output_format: typing.Optional[builtins.str] = None,
    geometry_output_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_indent: typing.Optional[jsii.Number] = None,
    lock_timeout: typing.Optional[jsii.Number] = None,
    log_level: typing.Optional[builtins.str] = None,
    multi_statement_count: typing.Optional[jsii.Number] = None,
    noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_tag: typing.Optional[builtins.str] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rows_per_resultset: typing.Optional[jsii.Number] = None,
    s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[TaskSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    search_path: typing.Optional[builtins.str] = None,
    statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
    task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
    time_input_format: typing.Optional[builtins.str] = None,
    time_output_format: typing.Optional[builtins.str] = None,
    timestamp_day_is_always24_h: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timestamp_input_format: typing.Optional[builtins.str] = None,
    timestamp_ltz_output_format: typing.Optional[builtins.str] = None,
    timestamp_ntz_output_format: typing.Optional[builtins.str] = None,
    timestamp_output_format: typing.Optional[builtins.str] = None,
    timestamp_type_mapping: typing.Optional[builtins.str] = None,
    timestamp_tz_output_format: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
    trace_level: typing.Optional[builtins.str] = None,
    transaction_abort_on_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transaction_default_isolation_level: typing.Optional[builtins.str] = None,
    two_digit_century_start: typing.Optional[jsii.Number] = None,
    unsupported_ddl_action: typing.Optional[builtins.str] = None,
    use_cached_result: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    user_task_managed_initial_warehouse_size: typing.Optional[builtins.str] = None,
    user_task_minimum_trigger_interval_in_seconds: typing.Optional[jsii.Number] = None,
    user_task_timeout_ms: typing.Optional[jsii.Number] = None,
    warehouse: typing.Optional[builtins.str] = None,
    week_of_year_policy: typing.Optional[jsii.Number] = None,
    week_start: typing.Optional[jsii.Number] = None,
    when: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b73aae876d930fd857f18e2d0bdedd651d71fd07c4606e368a04e551f713dc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9835c44ab36dc7d9b2dac3f39a662ccfc2b1c4aa0bb4b41c485b579041fde813(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40a872971f2652c809c91399a61c3a69a15e342874a9fdd6017f2b6c434f746(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1ac5e89fc2cf3a232bc41e2114865145fd9f8ce4d25a700f1bba1fa9457405(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e3c8bac0e9ec6fc98cfe6d02f2d2f86d7425c38e16146c4186efbe3b31091e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f16f43b0554e0ddc8f9c02c79247c3d760774cf982fc4e10de97ea145129d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6e3431b861831c6b090342368c246c97754beff2c969fd360145bac4305293(
    value: typing.Optional[TaskParametersAbortDetachedQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bae18e3f800aaabadbc176d8822ab63284b3d93d10669043224984b662c0c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fa5dce3862c534d03d6d4cf431d39b9e0ed0cf991b84ffd9213e2f88d87f28(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317d602b83630bdeb58be9cc0314f3c65d7e76e290497399a5a9d89925b823cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ccdf42a58d5bc497fec8bb3927a2cfc08fc851ecc39ba4e1418156d012e928(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f60107b9c838ae02da6a92e4b6aa7547711a5fc3a1f3d28d0d9034ce99d761(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa45f18596a3c7ded5511cd629fa663ddda1590251c7d9ea778f3de888b9cf4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3277c03ac9a70baeda04be60bb2a1d01a615aa83b1d59cb1f21083be52091a07(
    value: typing.Optional[TaskParametersAutocommit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb2e4e1ffe6542bc9ac4cfb666e84480a2b3af9d43ca0e40ebf45c992d365d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325b8a92290e4220702502464f8cd7f0066475e34adf5dd39409af0f20780e67(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc4aa6896663095300d91c45aad3f917cda5cd147ca69517a96cbd526b108ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47413068cfafc9ef79e611f0e695af4227c2987d701363ef5d4217cfb088a36f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bceefe509e2fe709e07958a7c4c882b69195c01da20dd124586790dae907e26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb3f30d80f4c17f59c58348fef1a795a8b9fdf6894d49a329fb3264a3330ca6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2368add5ea53b9ec9fa8ee602f84db353283827e9a49a7645315fcb2f2f91ea(
    value: typing.Optional[TaskParametersBinaryInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610fe7b1b5c2c613df7a224fad12444beb088e4ca599bc425c1d2154ed0ec964(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62af58a233e07eadf7e237d33446813ba0b45469388e69e76f3f5defe3a2104a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8180ba36fffb792d4591ccbb04e08bd42fe72598746c615be6b55841be5ee05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ff0f94fc5f322ea83824eded186c65d884cf7954de449b5454cfadcb170dc2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70223987389a978d7d27afd0053d90a159b9104d8ba721780e4bcadaf6b7b27d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3be9088a67955be8d5746c399bdff88e6dd13a4680341ea009a614d03f3305(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53dade3bb7c15c732eaeae0e1bb99c845240baf734e3ab664f45d519e97e615e(
    value: typing.Optional[TaskParametersBinaryOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836625564fc549c8fcf95639ea7c06da9a536dcfb1443f683b458afd80b4c7c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5324e1499806813c076ed46516fab84899d6852cab25e700043ab2a8b5e5dbd5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0642437bf9f5bbb2d628040684d96e869e231cf3dacbd592b68190f83887b6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacf24ba596cf009f6e293d4c6d3230f14fb6488aadbb73c4ced333f8dab24c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3a55701363519a2dc21bfbb28dac5d800f286ccdb79bb2e57c9593b83b1230(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2242bc2449b370e1c0a4b87bedfbf990cf7be425771a442df61865c2c99a5a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34b0e90db1fe54ce47170a0caf1ace878139768368797830a40d86f4ae6f322(
    value: typing.Optional[TaskParametersClientMemoryLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30052684102c32a4989c72acac5f69fb2ac90e7a1b71f6de9316830df85c7012(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc40c08c756d6b74e3efe7ec9dc14c26911b2db1de198b4483c5f52c8395a87(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ed5c28cadb0291cf8c4d07bac2b9ac3ae5162524eabc84976a28c73b3d7027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a24ec2bddba93b2f10eaa92ef723e6a926a9fe0b125fc5c1e89e5df80858b1c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ae83d023a89c5b91952e27335c44cb3b95fcfd623c12d975f82e1bf4e60e14(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed34180e0ab48409ef54f206c7017603cb81b0014b29a53a19fc41a50ebdca2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7029d02d57177bfe31d48ccc05583d4563cfc5e7182dfd011432668b9b6089(
    value: typing.Optional[TaskParametersClientMetadataRequestUseConnectionCtx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5d145c191878a9f845c5a8346d095da7c45cce65f30a9bcd3faf6bd539e673(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b66fc6fe2b7eb4ed50cf5de30a53753322adb512fff4d897f4fe190a83ee76(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381b2cd38b968643947ac27b269c0ad914dc782c756fbf6a2806942123b46d45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c08bce8ae9bfa40a9ec0224993bd88c357c46c66d31a797dfb77a16be772dd7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44631ac96ee3128d73351ae5d6fe682fe7f80095891b1e971aa97183bbaca846(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24b3944e9a0aa38160760828b91042bc0a12095fdc01e63f804db9fa2051dfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6099059751e45d55692821b44adc72c68f42fe60fa4dc2e3e61580bbc459d75a(
    value: typing.Optional[TaskParametersClientPrefetchThreads],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf61ed870be8ebbf53ec0a14158b44322fb2ae01e59343a5254b6f8f123a309(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2598331c1f41b12f2dfd8fea4df6d8256456054aa2283adb89ccc13fb9739de9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b967d7150f26aeb84f01086d8a89f4eef8822d9e9ad1a4a4969f8e033124cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaaaceb48cebb79152d6541f915f25eb6419149e96d19624be717d64c0e24c53(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62b717c931cf9b02eee450949ea464a0e08a6dba8a77ac43502e7b62e86e727(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84f82293bffd3b6e29d1d176d6f8695f102be4d963cc5a1681ff800e4356e9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437585183697a07751a74105f879e3518a0e4a5b92901d804d8672a2149df978(
    value: typing.Optional[TaskParametersClientResultChunkSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6660bb318a88147b12534e6a8f3199596e7ec2bda4850f61cb61629e2b183526(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce59af7d84f22943e604e9fa2822ed88b27ed71b573307f6f76fccb9dc58c5f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7002a515c91f14315b395eeae0ff15755ce3a44a2a3573a16b7ac62909a699e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebef6f5b410c909ba01e20d7cfcd76a979ab3a9c724f84282c208286965a0bcc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2f0545293940e5e83735ceef84fddbb05ae97521e870fa3669507d56dfedfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856db7bd94503897839b658989d73d1dad347ba8f8afe30515aec08fbe2e342b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29d5ab59a766a83b5a3761a71b4147611d83f2f4e058da8d748e9e8c7863342(
    value: typing.Optional[TaskParametersClientResultColumnCaseInsensitive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5ef0e33fa366abd5ac4bb40365d5c3d364ba82298507b34f7451efcf51dc57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc08b8df2727ee5d52f05c0a58873d03ce779b5b164c1eb40b23ff381b680f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02e6848a31faaaf204a460d3c40ee31f582317a4db616df82ff6fc121249b22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96bfc1fa4c2b4c51d6d1b7a200be03f4ea257f7f9b5c79553461e522d8cb3ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d500be8a94feb9511fc3eb38ed78bc5689b6208e2d6f711ec7b451cfa8d3aef1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f93fb817e02951b89845c3fe67a082bbc8f816dd0c5ee39b66a3eef207e03e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__550bbd467444b1d438a63a664aa10498d4a597bf35814c0fafebe3cca2b59406(
    value: typing.Optional[TaskParametersClientSessionKeepAliveHeartbeatFrequency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db656afe468fdce86b1c0877367188992f23f5a034b631c9698c1ca3656f0e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31781fb8d007b093570184055de66afa2c33565d36197454f97ff84dc4401619(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e2992061ca1143290f75d2fe6cb14b3179b8bcf562a94f98db6f58580e13fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f417797690915f72e25804e28f5716681b5688c96adbe280e6ac0a14b7a0bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c606712197fe5e54f6e8376fa1a6306628fed4ae45058d7f924422bfdf9e14(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34dd74774294e9f750483df19b66c7678b5b0f583f8ad49c4e41b24e4a59904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b7bf0665734583851f1c8c7c84839f16e387eec0f438ee20dd67dd6d44dbab(
    value: typing.Optional[TaskParametersClientSessionKeepAlive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d439b35530ab5c7caf4ca592950309ce933f86f1df661795111fd1f0f93e27b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfec196b003a9bc4fd465ce739e4a375db338b525113f81fca924349208110e0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4caa0c4c6d1bd3e06dfdcb5a33bc2a18b1bc230fd1178a2e99166986b61639d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3265fcdd7bbfa4de0ee8e26745ce5ce3c19803431ddf02393992050750f43cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b740384b5746b04783874e95792a6eb6fd75f9afe98affb5ee79874940a5b15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a88275756662a4ab51c7b73484a42191f889afa671809be2d75555a8e4a56b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fde68bf8add1ef0c5e6f720d56d760e4bc1993514c3e817269fd9a529730ae5(
    value: typing.Optional[TaskParametersClientTimestampTypeMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59635f7368a8dd21cfe8724c7505024034fa5493cd5c924147876bb96db079e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895d09a7d4bff99570ec666f15094d701cb7f866ba41200428f2a8460a0644db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84224647ffcab3ed7aa9d7b11af387a0ebc15e8c26ee396789e1d977b18d380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac109e62a2b58de7cf52a8e2c6c6d8e3c3499c30d0b8a636a65746083f002d2a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3af6d8104c3046e2a81abde1f66a0703d5a144037072bb64c7de66bfac8f028(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37582a44b56236f69fabf4e8be8f9e62eed2169db7190a9998a90b2f7937fc0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1364ff2558e20da90b1916825b0b4894c947d8ef7a668aa5388fe48cee91bfe6(
    value: typing.Optional[TaskParametersDateInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c186a60bd835fb85e0196ee37c003fc3369b636359d122502d16815c1b90bda(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9741a68a39adc6d2ed421475bb595e4ad8f97ca8d2c4d3fa07504c3dc864278(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448c719799eae775338b4af4356f044b56082f57cdf2e029fa4d130c6ed4a5f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2976bdd03d71f49dce622c06a3b370131f24e537e3658d033f948c5b30c347(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8207e982556d19d88e583049102ecdc5f918b1105fdde9345960f1daab2e24bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7191ac06455205646fb259df6d5adc7c5321cb40ff008ccf5ad8ed75db0505(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03e9dbb44510e1f0636c84e1e826269fd7553af0f44e758dd838e78a51fdb40(
    value: typing.Optional[TaskParametersDateOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ebb70ad88a3cc5b9d3a0a2f38b33f4f84e817f25f4aeeb15ebd4cedf8cfa9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefc6b0287a6b22a59d3bfa31b1456e14e3eae19a2f372c97ed239bf4c83f074(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a8367611a38d43eb682b09d0a90a08e1d1869053f7ed0309036dc298e763f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5691f04aef9e8b7973c5c3d32de7b64606838fd8c0f24773adef1c2662fd9874(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc410b98c233be28b42045c018a7b1b8edb2e143d13c4e245043840e4b6dae3c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7f7dd302b3e56798831fdd3c2952995a870858c7c98159eef3dfd75fb668fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23607c3174479f6dab808e336fc60368a0705cb8cd1cf921c12d55ebf66a6ae0(
    value: typing.Optional[TaskParametersEnableUnloadPhysicalTypeOptimization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e870dabae361a29c178c915483b85e71d163e76ec837d9c98a099837510c395(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd24910b308f2119888921c632c0f02d0824ef3a92ac2d9088293bf023882fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92024ae81ccc5d14613e31d76c0df63ce23c051d029094fcf3bdff594dbd1c5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f278e5b5698a9fc0c72246cdb2a2b01274d47e1658b4b0ab9702317c24ee0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efe069994f2d920799020ef77db4c615b52495e7fb9e702f3d9c5661505468e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed78497a0686d79ec5c4c6e5dfee9cec2e6369180d06e577f7004b7de6f07dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4b23e31b47a52b6876e60a263ce23708cd5b90b4446e9490b1767e7552e4d1(
    value: typing.Optional[TaskParametersErrorOnNondeterministicMerge],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da3a384338fea73e085f127b8d790fbc13088e557cc83066606df35e0d7e973(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307b5699e15999b8b29d1b8298ce2459fba33e4b36432e159e19f68fb1a97079(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cead59c8c110157d2cd2359aa7adc3d1417a4eaa6b8b48720ab2205caefa43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b24ab3f04c13f5513d37e9d6a41df15afa209285da185b6d4674024a3a64ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac7cb3d0cf83ce486eeee55275b1072a9b668704f35005ebd06378f01ed2e20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5158d1250437228c49682041aef384f9edba20f8ed9a01b2e96d0ee65e8ce149(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020ce17dffdbc0df461957c5bf0c2e397f35205c15bf41a3b1ac72266ec6ecee(
    value: typing.Optional[TaskParametersErrorOnNondeterministicUpdate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c6cb63905dcda889fdbdb2d921ec1317db872929cc99409fe8950a51a3e2bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e296bf94f551230278383543d1f5d350d12e841bf798210d5aa1852284dfe5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511a8097851716a61e8fbad4979bee7f30c1e4daeec9c3c985557c390232a319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443d36ac6c456bf54a1c1675391a131c5133802d24d3fa41c92c174f9c17cc29(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e190a8ab710fb238661dfddfdab9ea8d384a16f793853f30f8edca5949137a55(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6990534faa5a192a6d0e9a36a1224eb04d11b2e4897d9b359712b8d224cc4286(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75104ca1758987bebe8372d507f9d5c25c2577871a50eaad65d1e241f01699a0(
    value: typing.Optional[TaskParametersGeographyOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191ef3972bb76e492bc6cd792b4eb5bd139f5412778e7b8c2e60e9a618e57402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a89792f8aa61f41568de0ce855dc78e02f28ced766323e9ae8fe9b27e88b378(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1548bc6482d96c97f1c283b7f1ce49a4f28d49fc68ecb1fb6254115a341a83b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24fc37ea824739324f4d88f7e830a7afd96477ce2786457ea766ec8117a02806(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a7f87f9bd6b7c4e677f08955c9f763229802e3ee740d2b4a5ebd3b19d24c15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339d92b5bf783df3a4a6d7ed5ecc02474799f99fe73217fbebd3598b7ee55dff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558e1db1844d8600bc4ef112756094c09e2d0ede4fe4a431b73731676b72937e(
    value: typing.Optional[TaskParametersGeometryOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96133c47d6f3b7c30455f78e44c8dc5803805744f7e9e784059006b1eafb6269(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97310ee6a2e9815320af973c5df53e103450d34b53d4a7cd757ba1058644f09(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56abb447b23e12e0475039b118bbafb6a03022c93d23b467865f9ba6ec13c40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0e96fc3bddcc3d5845aba94896783e0dd34c0637d81b460a3a504b83d39c25(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc47922c4175cd0916d2a1818863013756db5b1489a5af858971da65b09e038(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec64a26c2f50763cfd23eca3b373fbc4d364d6719c6ff985c6b136a0b13bc097(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6588920269acb5747f61b728f79451939149cceec7b4bc33db1b5f600b3b7c6(
    value: typing.Optional[TaskParametersJdbcTreatTimestampNtzAsUtc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf73227def480b608a60293a5bf2476396736148a0b42fe037231090af20329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142c1ea92719b176be45f3d4b0f397626e42ceec1e8e4f746776e740bb0d76c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d481456244f2b175af24d2901d4bd05aff0a0cbd1715ff637a5ab3cb02f457(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3475cea6802cdd08c97b7ee9e8a49292192a737ab91145a6fa763ba2e55a9c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1cd1c020ae84c427352e5b94438343094ea679a498c92ae7df356c7bffe5d0f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b335497dbf2f9aeeee980781e5decd5d881c48ae26718d02766089587992a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f22a981a1ac2b6ca11f01bde44f3b3396a0f9e14f43b707531f138933c1187(
    value: typing.Optional[TaskParametersJdbcUseSessionTimezone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24e45df5f1de03492e86fffd66f5dee55c5034684ff22d1d574909f3e2be1ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5211b1203ce89f3c22eba8861ef5db116adae2c5658d7572fc57a2375160fc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cd8d9af1da69322d24cf4772513e2e3fd124a5de2fb061a89e2be2b00c5873(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22eb1e9e35bbfaa9ec776fb752247fa74f93dfdc62c940726dad136dc0cc9bea(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1313286a3a968ef53791e57cfb3433529b702f2c81f999a1ce41d09d0d4014d0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47177963c61f164a71d965657429b576fa4ecd212d86da33cfa3d9ce18770dcc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbc07b70fd347a0ae7bac55595130ee8ce4ff30d1d898c8e33bb502a9c3dc0d(
    value: typing.Optional[TaskParametersJsonIndent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad4d666962efa13e5719a0b8899867dc4d81a7b6270f4da5bdbe73f31e27511(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e424510baf56c0a1b3d948c982829b66917a2bc902c8e6a14fd4403145f9bb19(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10769265213fa68d98b2c1a68037c62e269821aea96f81f108eee88cc3a4a775(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e030a7460a7bd72162f4eb2acfbad9f37b4625017c4a0bc834b4183f5dc3b93(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ebecafac458d6b2425fb4b4d77dad7e89662746879f22653df778073372508(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8685a351c60ecc68fa5e7a197ef65d3807e9f11f2859a2dfe3b8b069809e0690(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2efd9f4d89a5658f17e1b0e45133d7c39bde1164619ed32e1f910a11a3496a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c830d30fecad8231f6b15a05446c102c91c3d7112f6dc2df246200c8720ab406(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a80b4afcf6e657c185e926a354b566b0f3b0bf6162bd8b8351864e4b325f3d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcf7ff796a73cd9577e4fc54248256cf9a7fc8bc5fa20d0eabad0f6350a00a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b995ed4092664a06ad7a0584a66b8e400cd67ccb0083b61b1101f73b6eea1450(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abef5311eec7e0ce6290286965666aeedd9e54185a3615c1d1056d1cbeda314c(
    value: typing.Optional[TaskParametersLockTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829eef6be32c389bde0a2266617c2fe771c0bc2f548955e944da0c84c5c28ab7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c029610a9fddb29afd2f34c9b3da34f4628e388beba10a32d3eaefb4a26af28d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd32f17a43502964abd271955af63959bc2ee219cbad0d06c6bf9bbea53490f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8267044404839c94d13619b93d9dfd55960063e4368a23229f7dab54763b435f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c0192801d039c65817a476b33476204cdc541bf6f23f82515a6a2ad404dabb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75e5c8225dd7d7cd6480f0f5c4c748f7244752a1f6074cd30aa0fe131e20107(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aced19c0e523beb2f0dd81e401a00677c069b413090139a1f74cb9efd6346c9f(
    value: typing.Optional[TaskParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b0b599a14a4ac52b803303b52c348a929286944a0cea440c6374d147dca543(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16be429af632ea591679896dd728a7c586994093145bf8021ed27f2eb6b68adc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8152f2c0b5b07ed6d9bbb0061d00bcc4f464096c6028c64c502d6859b8815dca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d9aaace5bbb4c2f899bd0c3ffaff0a359c99853fb53541288e817d551a87b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678d9cdfb72744c933a241228f33039b3f6a4b1f6dabb566ee2e7752799f63f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4e304976b3dca4e4849b11b321b20d0b5123b0406c6915dcbebc884df5934a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b87cee452ddba9ed90c200ec2dabd4ea2741e0b3633416f25b5964f19bf614(
    value: typing.Optional[TaskParametersMultiStatementCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b2dfa7acf382a1b7fea1a77ff5ffd5b41c20ee8b308851751ebd66cae37e0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20caacc7dd67fef85ef8c8bbaeb320f19cffecb603ed8192242d6fdf15066b0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b868a367a43456a33e2e67a0bcd1b4c0fb4d0e11fbd64294721065a773d032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd73201d07579c465d8697c843123ab331ddd6500643df544debab7f5901c95d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88d34d8bec689617a4cb6d15bfbe618f90e50bc408d2f09534ce2ea149bd7e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f916243ff1cea2deebbe0af09847aa748155907959085236db5639cb5f7969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b67933251d1d8ff675036e40e51b1628f6098015c39a006f9b770c041da53c(
    value: typing.Optional[TaskParametersNoorderSequenceAsDefault],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cdfc0359e792dfafab83b00ca62459ac74b3c338dc821dccd38c909f6fcb63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1280d8d967a7eeedfcc8cf4d10088f2b0dab9c13e71a88a0c2407fdab3533f50(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62df6e1f4df7ac3eac1b36bcd86a6e2b48ab98f256e67ddf9b7ab7125e4d828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afef9c2a9dc3da75628c9de26e115501529506515c13eba596206640dc42c47(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c3a5c9ad832d2e1f7976f4ecededc7a43f6ae451e521312f3831719ac9afdb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefba97ef74ce76930deb29066d6141616df8768d8bf1cad15f86b6421a97cf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26f1b6e42f9f5d7ab1aa33b0d5dc436f144726fe865df7140b60e9a2b9d172e(
    value: typing.Optional[TaskParametersOdbcTreatDecimalAsInt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc28bd9775ed896864720c198251f765dfd88e84e431ae2c3a7887f8ee3bfe73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f798241430ed58dadfc2429b3520a59dae2af9d7682dec174174ab7de0e5d5d(
    value: typing.Optional[TaskParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a85c7549f8b1fa916c05a59392a5d545fa2480e5c3e053ae8a85e4487e35d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4de21e0a1fc204085d2b9ccec9501c348b8cb2c93747ebb56012553fca06b3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f2e50f7b39b3a52b6c22994059e57916f2db96ce0285e61185cd82ebeaeb7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0f226c0f84ebaa3d9e7c9ad676fc2d8628538535ffbd26be3e184b07a1f97b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a8c7eee5f9ec6ffbc3bd4e9e0dd61e1d441348e822afcaba52cda66b638d18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd461d76e002e1f4e229f2457a2b8319d5fb5d4601ada6ddb98e77c6e7b3d75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259141e16c1e8348d3a6179f70b75ce3cde0cb903207cd34c82c09cee0d6054f(
    value: typing.Optional[TaskParametersQueryTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbadd8d1fa8a7783eee80e3c31415410bb135d8233b640016d42d3acae4aa3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1122b57befcc9202df39bcd1be7bbe2bd5d0e048ea1f1ef62cda38396ef3f00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd77693ba13243bcc417840a26fc8f393da70bccbc156438603ced5cd7704eec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d918a549bfdfab5909643d73aea338d742873e5512460f7f7800023235a49e85(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e3eeb82934a488fa15f55d493d4aba7f4397a5444971f05b78aa700187fdd9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70345402db76c2964e79e437e0fb4509d3505fc322c6a41d5c9c0e7eab622f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c28b0cf8e5ac32afc2a6aad14d835b163c448c0f4f01b385c510ac7b84d5f9e1(
    value: typing.Optional[TaskParametersQuotedIdentifiersIgnoreCase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c6dfb97bb1619a8c29ec5a17b42b4971096550feade40cd05f17b8d92ce630(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c53ab5bd43f4c13b7afe56f7bf5ddb2986593e56639d9d2efaf48eafaea79e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e024dc3e676ee30bff339040d6e2771ac3d4bc4492cda0e5b8f0c495848c0bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba10f0216eb4f94a6738c189a0bb08f99738fb881a89ef9e04c28cced5270505(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875d18a7ea092dbd9ddb310e5b9a0e3b931d26a700e3a9e72668f15cc3bc36f9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2593cd5c7b0f5e7a617d31caebbc16af6ed8a1ef62e5031bae3ff2588ee20df3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ebf6f4b091f48b8d1dc4adc39cbaba46c25db16a56549e7fe8c945c3d84a28(
    value: typing.Optional[TaskParametersRowsPerResultset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555bc6be6623458196498502762eb0d1f464cc305bc69ee8aa122ad5b8b1ee7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a811d2854cba324c167af2e07ff779096a956ad58f944ed9394d995990e56524(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abaffa9d37d8d3867313527525818b7e577e95b3c95e88f1ca0bf223ee32a19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97eb9bbcb38dab54a4dbda905ff443a41ba5322645174f104b9f3aefff81af74(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73c82330056f4a493cec2eaad6e1d5082cd7071f0b0e4afedf6f29777186e02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be557275bbe119c477216345a836b66ab6129d4b4f6a1173b49ee200518c5f5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8022dc02c88b1902436b8e5ffe936b858a3af1ad986dc96aa6e8f8d5fb2134(
    value: typing.Optional[TaskParametersS3StageVpceDnsName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d92afe4ddd151e1c7af10a00a09b31ccf06a51aec00d567b4574c85da364d32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7987ba375e11e2723abef182155332468d9d9e7add2fd6115fb6a2f8fb128638(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90c0ae51390a2309bc610d173a29b5218d83a876d28c19fb11e52a0afe531a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bea4677ef0a0976b3062958f8c8a486fb441484f08c3a1110be92393c59fc82(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25cb8bc0c26cfccb9d7ed2c7d1f6507fcc5276f54a42acfc904c8dfc31270861(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c055da144632cc69212a5e762b08b2b6054fa1b60aabe7f91a81cd39b1c4f33d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b04cdfbfdefbdb13ada36e51a6e4b5eb8ecade72e81f6c1f8385b1e338d264(
    value: typing.Optional[TaskParametersSearchPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f74fadbafa4d6eab6c1f5a91bf65d509afd34692122354dd5e0893360e3efe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38af6713b14d1bc3b425e11c7c7e1fb8829df6c9d0fa83e1f2283cdfdc2a238f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b018cc10decf2f51e255ae42ee55a1b091a094a53d92616863a58adf977265b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f647be362f64ee2b952179ba2cc0a487a5f5ab19f550036aab93095a9eb5d50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41134057de5698093b801957372c4990f07f3b255e7e54be9c1a149ff86b9bac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6dbb1384ec1eb9d84dac5dcae9a7be52bbc2d64b51b9c5d529060c881c65535(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d321884796d81b04994a388e60d18cdbab0b1c05cdd91aac90afa77d1305c6f6(
    value: typing.Optional[TaskParametersStatementQueuedTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65675e4abec87bbbbb0fa8e952788e687f1785d8643a70fc4fc55cebd65afa2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2957e2bbdb5093ac511f36f503dc4e46e0f4f3e7f65607b1b86226a780de719d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efaaee39aa99a9eb954b8cd6a6d1ee89bfa861f624fd5de9106c8bb2bbd7e4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12027c28f2b56db299e004a3d3e42cc4cec81c941b9cb11a353c5189e3f92c46(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df294bf189ece60ebe9cd9eb2bcc260809c22d0a25abca7de5798b95289f38ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c107f07b0a50c8299be218e55849309c7e3bb6c8dac59f4dc34f2021c318178(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5c2040d449228cacb5e25279ba19ae24a7294997c7cda820608aa1121aeb79(
    value: typing.Optional[TaskParametersStatementTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9032c44facc1fd2778466486d1bc26f84f935987fe2f1775991ba595662a8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253ea670a9572bda49c4583f1cdd8ae482dd871c8dfb0fcd8c3d542dd094bc76(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbef12e23913418974e468f34ecb5a333ed90177a4a770ce96a0ae89aa34303c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58f9c8bc2fa9067bdd129618a972c86f73fa6b37c7e6d370cee979f85683983(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe4104f0836561fe14016936c08e2383fe0c043c6b0c88ecbdc007560a80ec2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2184b2cd8e9a83270cd6b63086795ac2e5b63b1330bcfee635f546851471d485(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9197d957683ecd4392506a58c91a241266327a97ac906be2e94c489a2c39c28(
    value: typing.Optional[TaskParametersStrictJsonOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7d4aebd41bb6968f40d0bd0d31c7575c4cbd71c7ca87ddbf35c2e7e2c2b4bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc87f7219b501d3e7af5597824bbdb48cfae4dd9fe264a0338f17bcf986a7c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331e026be61a45d09a8f14ba90b124822638d36d863be4d8794c0662d46f45ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba24134f11f4503ac52d527c9571e969245536f6f5f51ee3b8a84f1c7e56ff0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f234741b7056b551f3c811aa4854ff0c8fccd451747007387e4c094aede3fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0296a3f98e63910c0d312fe2b036632fc3f314b2e456eab3f7dc345201316dc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5e508f43a826726b8bc3d31f7d3b6907afaec79f7c55da7070587c1d4653fc(
    value: typing.Optional[TaskParametersSuspendTaskAfterNumFailures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b08eb41e97d6ca282794f3ab3397b14b925d947e277002e3328c047967b1a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7624fe3f204f66b3f7c0a6bfdd73bba55b4b85bb2cae195b4bdcdbb55c1f59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ff12c7b5431f6848855d19d99a62e0ca51da6cc30b9d3082f3cf5b831f8f72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599e7cc46a564ec1c3755ad24821faad7baa63330c04c77e97a67e40a3381205(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcdc4b64d7bb3075d6fddd447996101bb2f8b86e4b3f20e226d8007cf0cd297a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1424d660c67808ec414b9c3f06c7ddfdcfaf8dd1fcdbcd04448e5e2a89457794(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac99f805d59f87ad5166b470dfee1344c165386f551557aec2e5c58463aa017(
    value: typing.Optional[TaskParametersTaskAutoRetryAttempts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d84a8f3cdfa1e632882b6e6a329f42eef66c75da7e2714c393c8cecbab98140(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__563aa10a9e4c69a53800d43606868ebd6320402dfce4ea6fc56c078305a548a7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ed3c1858249700e6fa0c7aae2515eb633ce37dbb4a13fdd6862e17d6cddb0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a946e2e44002c86e5b3524ed5126b6dbaeb92d8210469466d2c6f748f17f56(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae265212541774707bead61b6c142f2a4068a08f026c792da64a1c8383fc5eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76451e3ef4a2d3a235636296ca5833baeda4417ae4f76c69811345e91316d84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbd2968ef4ee6ba03f4f59f544eb7f712d040c4ba262679b289020acb764a45(
    value: typing.Optional[TaskParametersTimeInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47727d6ef9dde9a08b33412a93aeabdf8b5fa8e07ebed9af729f812cb405aff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95041f63d9fbe8a5bc287c60ffef8d85c2586ee686c1cc4e819cede2bfc2af4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88e70e4d768e277e6e09c6798706ca5d6a2ff8026baed79b5ec74aa60822933(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c34103d7bc556091b7267e77beb6f13d984c0f95068cdfc14cc45584c3475e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e67b95a97f02a546639b4b8bf78e1288e7305c59b5faf09a8f3b4bf753e35f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7220094462bf7ba330286cda766543952fffe0507810fa9aeeda486d2cb5c48f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb279292348300b4ac1aac5fcecaeebf636704866e12d387e5c807957a634a3(
    value: typing.Optional[TaskParametersTimeOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ff0d0c5fd8326e49111f6ad23571eb26395453ca961e122ba2b34312992a8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9864a192d1924b5b6f2b0596f34bc60b6aa4f4756095c76b4d17ea7b488ba8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f03e615dac59fe2a8d3c67ebbaaefc1916f11cb0e8661e773f83e0a3338812f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8aa4796cd6b6a4e1539de18d913d6f88541dcfee90c5e18b622d7157c8b2ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6d8d5100f1a4bb894574e200a09d570dd3fe31de72f5dea0956c9daf77de69(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0050d44437e04eddd00c8dfece420e7ce5b7a46ad0d8ff01b99a4a0d8c361c18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741114dc2c5e3bdc9c2f5ddc9b5cb2153133e64a06b4020e39b18412c961c83b(
    value: typing.Optional[TaskParametersTimestampDayIsAlways24H],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d1b38e9d680a43a8de91f58dc173d27d58a94507d1a6e758c6f6ede0057ad96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e181639547e8eea31ca07c8be0641cbaae8ecfdd27982df9dcd39580e8e82b55(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b524e858eba73ff26f1db046eddfd6eecb411375a4fd1326f92705c8c3f3e45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099ec6427daa2f458f49c38ff925954d22bf8b23280d9a67149c762c3c6d8df8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff514a8e6cfd1fc2cdbfcadbfe11df9f7e32b38c9db3dfaeb2eeebaa85f8c3e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9f54722bc4c34da5a19052cad869e2b9eb0f0b8fc25b066bd889644f027e53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c53215b2108a7bf5ba74c76be3d355229f6fa3d79489c106bf94bbd05895d8(
    value: typing.Optional[TaskParametersTimestampInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c440980df93ab2d277ea636ccfa290f10567ab34a24a3a53412b9ff6165fdd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756680784b9370858e4005843777609e264f7eb36c901d0c5dfb7b47a115f617(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d46284455f7632cb2da75695f66c79e1353235c2996de719e2077806ada0fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7d069a27f8e2148d43c5122b0f6e21c5d8561ea531504f26f796a753f4978d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bd67f9d70bf96f98890dcf895c1dbd7ef18b3b9e0d3ec8f9e938c8412069f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde33f2f7a12d565c464fd51736e43eabd3c2aa4af003ef3c146625dae0b0611(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d331726ef1f2b12770c966d5c7fbac575f8af339500ab912238ce4a4360b9d(
    value: typing.Optional[TaskParametersTimestampLtzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17c9c6f28a10468bf4cfc14288475caa4331f383c3b8a8ea1b67fd1207659b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7a68e1e265161c2a33f070a089a683054e35ce7e42e7f6bb96caa296a8fd46(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219865d848265104d60b8de29755834177f579bae9496ac711766180627618c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703f7ee36e765e187b7e60e132260874637994256b942e24f4f6547a95114d59(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1216677dac718ae4336f06fda7aa0a91cce8a1f3ec1dd7d5e588520c8c8bad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243c7398a50dd36de057f7b98c469b065a3338f544258fc278dbc83950c6b9c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d3bfc223e94be298a2fde6525abb40664fcde8a40442ec7a5aa60baf2a9790(
    value: typing.Optional[TaskParametersTimestampNtzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ef5bc7b2bfb4a5e8abe97c4b5e021d6a8daf0c4178543b5c1c354351877bbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0208e0c50f0274903b4e9deed5fadca4d9620c8568f3baf97e9815bab163ff0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a5e9451a37cbc8ddfd056e7dafaea3f55f1c153735eb3defcb89d09ca4757c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d700870872ca6ca9d57c1e1aa7f66b947a6bd5dc4147aac7309eb288e9cc52a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f484ad4143c3eed8c03a5045a4ccb33231b08fb82f62b6698a9cfe83e1acec7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ad260521b66ea531d07a1fae9be3a4c06275d3fed9a9bfd463becbef83d041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0eda903d6b5f53bf2daabe5766f8148344290854d53d478bb4df0894d83ca9(
    value: typing.Optional[TaskParametersTimestampOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075f58c953e951f1579921dd58eb79071238feef993da3d31c6ff891a6a37024(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c994d02706907484e33966187cc26cbcda14cab9c355db845274b695e43a1065(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553800f13c1bffce1665d31cb57540ae06e6d66a9af08043a464981dc6d783ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc2486a678a3c855451591c8d24b79a0d6055a3d56cfb27e1f5385e88a7f2fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6e9f401d69c06a651786aef30e5d97155f81b60256ea82136b8b177b5c1d26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900304c3d624ef4ebbe2c3d4cf177856d990c2242d9f44d6c05dffa3400c1ccb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77bc87b69b090e04897a3ff899269bf99e84d27e896efd154572e9a7ffac603(
    value: typing.Optional[TaskParametersTimestampTypeMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68798b482247b9659e95bb88ea2759debcb6b44b8dd39b91d5f0432b08b340ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad281e7c37c4aa336f6c39a5a3a34a287228f1a10f75409155cdb7701f9c671c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664a7c76fc7108a3f9881c52055648a0a0503abf4d338717af190ef7b68a62f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72910fc4b530d8492aa643ce1589df63db4c04430cd2235af096a0a9f1020d4b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a9e78a88c062fdd1675de8efe7bb9347313d82f79ed06324ae097788abac52(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144f3d6558c31f0d6d940a04c7df531f35503a0740aaa0c152f69860e691a21c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef94d5424a0ff5e0bcbb6c83c149c68b520959bcc5c01eb51137642403ffcba(
    value: typing.Optional[TaskParametersTimestampTzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1dcddd3f5874745bc455785c13f2ce8e176c76e7f8643f0973cc06dd6f1f65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762ea65ff13b0892d5f42d6bf2182b58f6115e6ab354ce69175906bb3a836861(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9e7e5cdff5b7740292810e87b312fe5a9cd279837e7bad8c18c6b0ba45d518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b41151d368b555ff674f10a04d1cb141fa8889f24963c873b06abccfa56659(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63411ab3b0b5c1d8c9402fda7ab75d4eaed8d3a6b0facfb96828dcdf8382ffe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3716388dac8e0ae9aa0a93111b2ee10516e3bda94580f856eb85999b68df3655(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2d809d67a129e8b70ef3f1ca93edde790297dcf7d29feb69c6476c8f5b0aa1(
    value: typing.Optional[TaskParametersTimezone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34df8bff311dc018564b2e16d21caf705d4bce89c2a8065f2c30c6dfe8acd7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640acc49329b8b7f0a85883f37b14e5dee5308e7ee9b047c48abd43a3e2f87cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f6c95ebb4f2e3cb13a5f0c46f2fecf3d6c4644e2c96b9a864725fa3aa02f52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b68d720e698aab30188dc0836ac3a2895a32931128ae3f9d644505888689814(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405c097b251c685d2f73589218a379978bc4ee1add609435dfaac1e9dc42ae27(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b645e1d49c8f03470af99e784c132b50520a2cb74fbfeb6005f20b1ad160e7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d531cb89c37ebcf6fc54c41772cc3f2a147f73d70b4a751e9eab412853f10153(
    value: typing.Optional[TaskParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8828855010daf5d327109af6b93e14a93123f64a98f79d9fce50d40c6db937(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9babe2b23f6a8bba969de2763bf1625f761b2e55ae2f1684e103e5a46bb958(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ad5e25539c129e8f9c8376bef14a3d42a717f4e140c77429c4d2b90ef3e079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8235af58d8b6d40ea06794b773d4f4f7ba53dbcf9533aa2bee7de0ad7a9954(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e62b7c329f236b3a6ebcb634fd136ff32bcb17390d58debc9628dd5610ae379(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b8e4cdb1717773ba610ef6da83afeacced362f2928980d682243c7800a2624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265520e24d7d725bbf2416794ca4077dcbdfdc297111c7d38baed1e918f081ca(
    value: typing.Optional[TaskParametersTransactionAbortOnError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e5e8d44ea4db7b1cf46d8cdb009a5cf79362ed23977e90eb260de7713f5d87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9538a280492a8404b64bb8deee12375f837788e9dad9b5a6b2802972f9a48ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5327040e69ed9ee9a879138a4d7f7e3581d4c501005acedada72f981918aeb8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba42e7265c4747f3dda20cd1d780c998625fb0c0fa6cd296475db47b46e23e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b6ebd9d503d742cb5a2c2a952ed960660c5c5f9ef3c9461c058f855569d871(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135093678c1dba810c9bd0fc2a37edb02334b77f4133f3f1cc49373e71efa129(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c237cafae88b9a5f194281e3eb37f02700be96ffc8000d3ae2b987749312929(
    value: typing.Optional[TaskParametersTransactionDefaultIsolationLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f38e13d915bb57e3d0048600efc0b6e4ec68a5af90585aab725cec8f6b8c59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3b514ab2861dfb70d02de53cbb56de19d98662d00dd31f88a26144743ab262(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11361d43dca81e5b04eeac465852dbd36b021dfd7e78eb6e854666fbc9cf90e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f710e9b0dbd3b02dcfba18312d7044b578f7be01f43f88f542015d0a2c6384(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250cb7bc985b0fd070950917e83c62c2ee502ba193263826e4b0abca79a5358f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f052581ade425f9e3579a1cf299f6b5a591e037e2655def47440e39a82e7e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0245c5085b4a697bc920e1e3d396820a891d07b2b20ac3754822006b919a571(
    value: typing.Optional[TaskParametersTwoDigitCenturyStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df3017ff44b16b5ca6b56847b8d95c2f5d36b1eadc00d7bdc4c699d0351288e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0abb6275f7d1d5cdaa94bcfd75a670454dd53c94b28e9f9ff1c4b17302a9da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5821519e0ffcad8f456bac4f3d986bfb216537708b43b381875d7542f5d8f1bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c5279fb9fcb95edadb3449ab3ebe1bd339fcb086d68c5d9630d79c93070d15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3acaa839a733ab2bd85e1d08c1d4b4039b4d9d06a9e385a4acd5619e28e02561(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af037857ba211d7ff10e4b7e82e132a6b0bb697ac53407cf50d2e776bab2fce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd06b810bf93aaa8118dff441927c250fc1a5d73f1de7f03a1da748b797ccc5(
    value: typing.Optional[TaskParametersUnsupportedDdlAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d050a2b601ceb90a2aa4df98a608866cf49c02de787c1c9fab9b0c49edea51f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4064471f77217ffe0454ae25e8d8b5948cc5f958423f6fc30f2c8976f48937(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b265a6c36f9b6c01e13eab8d9a4d836a1cc83ef35513ce9373d44d12e8366de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f354b6b914ac4cdcfe9dd62bbebbb52395317b652045ef1f946725a610073d87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee627d219484b46b14d6c89292015a2451ec68cab58b764c80b2a726b202b35(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1287b6c6b51f274a31798aab1c705795058a0b6bc6ef18fdedad6ec6c30fd27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda2e8cd610c321efc5448dd99d6c6af9d58f839b23d22ba4cba395d7c023b46(
    value: typing.Optional[TaskParametersUseCachedResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf3621d1abff662fbfb26051f2abd4564fb5e6b814d625ba78280a7627bc44f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4acae114616e5a914f218fefd5fe8d638d06b22367898e6b88a8fae49e385f85(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab78e903cb5d44cc0d8b2183f616532a540a67d63b991bd5c1006a1b5f8db38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0f93850d63f00904f7d93c7beb077772eb7f63f3532ba77626f3bcbf189e79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3020cbd9fe119ff366a91137f7967474ceafca8a86a3a47878b732c27ac2c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838fecba1967612a453f4ef7a6cd62517181bf37f2ae8258750f8027586dcb05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08cc4aab54a18c180a5bdf55a84c7f45ef074b35ddef950c237762c360dbc59(
    value: typing.Optional[TaskParametersUserTaskManagedInitialWarehouseSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a7e672e19cf4566ea6cb5948574e35763b09c769c3c5c5dcac97c8b8960547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d77a09697749a4a97cfad5e8a823e509d500ff4cb50fc35e75940e05b94f227(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b921c70858424e4e61a0e60007fe7a5b9658392a690a916d8c38e7f0e2c50d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4580b4c7db951939ed1b2d9ccb1801cee7a56322ee87cad6d882e555557b236d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d12a85d30a473b103774c56b5b9e863045129508bd3676398c6c85ff19627a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8930b3e3dca59f7e93d29da7cb7adb37e7eb1aeca75a2f55970ef3c2bd570e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ceffc56a37d0195192fbe3062ebe681f1f82625475d6fc393d4beb0be4e4a9(
    value: typing.Optional[TaskParametersUserTaskMinimumTriggerIntervalInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65deef8e7bc8c619005df00d5177c88d6da6fd66dea4bb5733df52055200232e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c8580b8d31ce5340129d3b109798543878365cac3be621b1188744fe3299d3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96116de41e2736c9aa55a56ea8d189f0037a7d3c751f459bf25d102dc90e9e57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee479c79f4d1672e1ede77c0cd7c1efc27d8aff29c52f98fafa60d8004302d74(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81ac1b9fdc75f1cba815b3395b398e5ae0194f23c80d57ba247e18caca2be2c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714344b0186203ec483a4c410063cb346e03d8cec8482f0623c6c37804a5ea46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bec25380ff633c52add65aa485ee62c98aae54d24556fb4007ff857168a38d(
    value: typing.Optional[TaskParametersUserTaskTimeoutMs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802276fea21ca213cd1493e1726065776ebb30b61d906f692d73d53fe3802e8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d75bbbc91f9378103636b0ac3195ebff9c2b87ccf049b5386917e5faa8474d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec96826fbbeaca19bac927c80f9ae0a84b1e108766d341c82efaa12f83e291c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd2c177aec9c889a9919f0f349fb529cd33569f1306e3d1f5d63e08cb787a8a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90829dc8d441eb8b068943f51f8d2fc32e46880a14cf4772b8cf99b28a1161ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c53e88e70cefdb631e6f5d99953c94cf1e591eb44e6f3186a97345830cda21f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c789a0d6d3daca9f6ab4ba296f5410b44cd7ae89ac95237daac2f081368b20e(
    value: typing.Optional[TaskParametersWeekOfYearPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c4865b03e4b0feed7ab4a7fb5dfd6cfc3e4cabed807aee34090165da836f21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb52bcc8fe949f4d51d8138b2f8acd81d71b176ddb32327fd244bb9eb79bc37(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f869b12cb49091785c3e8ffac0f6716d79fd41ebb0061ffbd7361693d2343637(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7c4fcb0afe32116a8c664ccb3a9a9f5baf081750a81bc7bc8022e8cca24478(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a60edb9b84bd046669d68afe77461bb3ac696cfffa6095d8ec1bcf9a91e933(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9faeb76717229d9d1cf7e26cfff6b8783d750e77add90fdb0405122f0ddbb4ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b7de1cb92287a1bc25e22fbb273f7182cb8e72b2c04361f810bf594df2578a(
    value: typing.Optional[TaskParametersWeekStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26fdd86f6131d1c9f5978fddd4ac4f3f934a0ec322df38e64f1e932a0cea784(
    *,
    minutes: typing.Optional[jsii.Number] = None,
    using_cron: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea76911a01f30e508ea0f1a3657758ebab8b2f93a1190fc0af78d31bebc8bb35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5720360d1feeaf0303668e34a3098fd8c64ca0d893c1f1e35fc3fa630f35e412(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235f9d249174fe9af691c4256328ccce6ef623b2e0d8496ebe2117425dee801f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c921879dbe22cc223b2648a95485122e1e92eddbac626502d71d5bea5fc5e21(
    value: typing.Optional[TaskSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e656111545dbe9c56eadcd3bf85b829876b06d4fa4b7bd17d87f7595ba4976d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04b6ba4850ae8cb700a8c519c6730ac943fee40dcc530e19fd946557021d7fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad18050ba19f3455faf519ca5c94b2f8e1d2527cc2fc339fb350ec1990fb5efd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b9e9864c86fdbb0360e76153e5649594bc511a5c36c53fb5cbec004f8102dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb25368c9e1b324243bb4409919b2ae483c241cba6072a12395c32425557ac7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083e9f948a83cb8f5ad60b4794b33aa3691e6fe0c71ece5ebaa767309eac57a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e26e682eb20bf553e60ccc3bc8dec759edede4272600e720314f86ffcc95de(
    value: typing.Optional[TaskShowOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59d553c2dcf98268cda084b81eb5f693d5c53042b4bfbf0520928bec3c669ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25290dc8128e1a44a8e1e7b7a5c876301a25ae237a32ddd7b41a2a86704e9c14(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d489b4877187c3502033ed73eb3a8363ffe02d63c6067b792dbe2f908c3d2c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a1dd2ca7ff24614a67799136cd6b806643c2e3cd77a63fa580677205e7a0cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b79cf5d923d41c705aa42f6d8142d536a7816aca975870ddb3402f4bb0713c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d714aed54be2b18e82ebb7c95689fee6e844338a67211305085c0affa61f08a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cc5c8add9a5c66008d47f21df2b1ea3e964a1fccb197236e344e07ac659352(
    value: typing.Optional[TaskShowOutputTaskRelations],
) -> None:
    """Type checking stubs"""
    pass
