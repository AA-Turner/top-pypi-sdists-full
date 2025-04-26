r'''
# `snowflake_service_user`

Refer to the Terraform Registry for docs: [`snowflake_service_user`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user).
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


class ServiceUser(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUser",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user snowflake_service_user}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        date_input_format: typing.Optional[builtins.str] = None,
        date_output_format: typing.Optional[builtins.str] = None,
        days_to_expiry: typing.Optional[jsii.Number] = None,
        default_namespace: typing.Optional[builtins.str] = None,
        default_role: typing.Optional[builtins.str] = None,
        default_secondary_roles_option: typing.Optional[builtins.str] = None,
        default_warehouse: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        geography_output_format: typing.Optional[builtins.str] = None,
        geometry_output_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_indent: typing.Optional[jsii.Number] = None,
        lock_timeout: typing.Optional[jsii.Number] = None,
        login_name: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        mins_to_unlock: typing.Optional[jsii.Number] = None,
        multi_statement_count: typing.Optional[jsii.Number] = None,
        network_policy: typing.Optional[builtins.str] = None,
        noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_unload_to_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_tag: typing.Optional[builtins.str] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rows_per_resultset: typing.Optional[jsii.Number] = None,
        rsa_public_key: typing.Optional[builtins.str] = None,
        rsa_public_key2: typing.Optional[builtins.str] = None,
        s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
        search_path: typing.Optional[builtins.str] = None,
        simulated_data_sharing_consumer: typing.Optional[builtins.str] = None,
        statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        week_of_year_policy: typing.Optional[jsii.Number] = None,
        week_start: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user snowflake_service_user} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the user. Note that if you do not supply login_name this will be used as login_name. Check the `docs <https://docs.snowflake.net/manuals/sql-reference/sql/create-user.html#required-parameters>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#name ServiceUser#name}
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#abort_detached_query ServiceUser#abort_detached_query}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#autocommit ServiceUser#autocommit}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#binary_input_format ServiceUser#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#binary_output_format ServiceUser#binary_output_format}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_memory_limit ServiceUser#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_metadata_request_use_connection_ctx ServiceUser#client_metadata_request_use_connection_ctx}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_prefetch_threads ServiceUser#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_result_chunk_size ServiceUser#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_result_column_case_insensitive ServiceUser#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_session_keep_alive ServiceUser#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_session_keep_alive_heartbeat_frequency ServiceUser#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_timestamp_type_mapping ServiceUser#client_timestamp_type_mapping}
        :param comment: Specifies a comment for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#comment ServiceUser#comment}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#date_input_format ServiceUser#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#date_output_format ServiceUser#date_output_format}
        :param days_to_expiry: Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in. This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#days_to_expiry ServiceUser#days_to_expiry}
        :param default_namespace: Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the namespace exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_namespace ServiceUser#default_namespace}
        :param default_role: Specifies the role that is active by default for the user’s session upon login. Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_role ServiceUser#default_role}
        :param default_secondary_roles_option: Specifies the secondary roles that are active for the user’s session upon login. Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_secondary_roles_option ServiceUser#default_secondary_roles_option}
        :param default_warehouse: Specifies the virtual warehouse that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_warehouse ServiceUser#default_warehouse}
        :param disabled: Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#disabled ServiceUser#disabled}
        :param display_name: Name displayed for the user in the Snowflake web interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#display_name ServiceUser#display_name}
        :param email: Email address for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#email ServiceUser#email}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#enable_unload_physical_type_optimization ServiceUser#enable_unload_physical_type_optimization}
        :param enable_unredacted_query_syntax_error: Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error. If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#enable_unredacted_query_syntax_error ServiceUser#enable_unredacted_query_syntax_error}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#error_on_nondeterministic_merge ServiceUser#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#error_on_nondeterministic_update ServiceUser#error_on_nondeterministic_update}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#geography_output_format ServiceUser#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#geometry_output_format ServiceUser#geometry_output_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#id ServiceUser#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_treat_decimal_as_int: Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_treat_decimal_as_int ServiceUser#jdbc_treat_decimal_as_int}
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_treat_timestamp_ntz_as_utc ServiceUser#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_use_session_timezone ServiceUser#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#json_indent ServiceUser#json_indent}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#lock_timeout ServiceUser#lock_timeout}
        :param login_name: The name users use to log in. If not supplied, snowflake will use name instead. Login names are always case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#login_name ServiceUser#login_name}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#log_level ServiceUser#log_level}
        :param mins_to_unlock: Specifies the number of minutes until the temporary lock on the user login is cleared. To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#mins_to_unlock ServiceUser#mins_to_unlock}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#multi_statement_count ServiceUser#multi_statement_count}
        :param network_policy: Specifies the network policy to enforce for your account. Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#network_policy ServiceUser#network_policy}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#noorder_sequence_as_default ServiceUser#noorder_sequence_as_default}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#odbc_treat_decimal_as_int ServiceUser#odbc_treat_decimal_as_int}
        :param prevent_unload_to_internal_stages: Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#prevent_unload_to_internal_stages ServiceUser#prevent_unload_to_internal_stages}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#query_tag ServiceUser#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#quoted_identifiers_ignore_case ServiceUser#quoted_identifiers_ignore_case}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rows_per_resultset ServiceUser#rows_per_resultset}
        :param rsa_public_key: Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rsa_public_key ServiceUser#rsa_public_key}
        :param rsa_public_key2: Specifies the user’s second RSA public key; used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rsa_public_key_2 ServiceUser#rsa_public_key_2}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#s3_stage_vpce_dns_name ServiceUser#s3_stage_vpce_dns_name}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#search_path ServiceUser#search_path}
        :param simulated_data_sharing_consumer: Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views. When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#simulated_data_sharing_consumer ServiceUser#simulated_data_sharing_consumer}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#statement_queued_timeout_in_seconds ServiceUser#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#statement_timeout_in_seconds ServiceUser#statement_timeout_in_seconds}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#strict_json_output ServiceUser#strict_json_output}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#time_input_format ServiceUser#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#time_output_format ServiceUser#time_output_format}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_day_is_always_24h ServiceUser#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_input_format ServiceUser#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_ltz_output_format ServiceUser#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_ntz_output_format ServiceUser#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_output_format ServiceUser#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_type_mapping ServiceUser#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_tz_output_format ServiceUser#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timezone ServiceUser#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#trace_level ServiceUser#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#transaction_abort_on_error ServiceUser#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#transaction_default_isolation_level ServiceUser#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#two_digit_century_start ServiceUser#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#unsupported_ddl_action ServiceUser#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#use_cached_result ServiceUser#use_cached_result}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#week_of_year_policy ServiceUser#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#week_start ServiceUser#week_start}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65daeef77cfdf652d600788cd31a1a34276acf0f2fd7d88e5085c3dc97a6caa7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceUserConfig(
            name=name,
            abort_detached_query=abort_detached_query,
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
            date_input_format=date_input_format,
            date_output_format=date_output_format,
            days_to_expiry=days_to_expiry,
            default_namespace=default_namespace,
            default_role=default_role,
            default_secondary_roles_option=default_secondary_roles_option,
            default_warehouse=default_warehouse,
            disabled=disabled,
            display_name=display_name,
            email=email,
            enable_unload_physical_type_optimization=enable_unload_physical_type_optimization,
            enable_unredacted_query_syntax_error=enable_unredacted_query_syntax_error,
            error_on_nondeterministic_merge=error_on_nondeterministic_merge,
            error_on_nondeterministic_update=error_on_nondeterministic_update,
            geography_output_format=geography_output_format,
            geometry_output_format=geometry_output_format,
            id=id,
            jdbc_treat_decimal_as_int=jdbc_treat_decimal_as_int,
            jdbc_treat_timestamp_ntz_as_utc=jdbc_treat_timestamp_ntz_as_utc,
            jdbc_use_session_timezone=jdbc_use_session_timezone,
            json_indent=json_indent,
            lock_timeout=lock_timeout,
            login_name=login_name,
            log_level=log_level,
            mins_to_unlock=mins_to_unlock,
            multi_statement_count=multi_statement_count,
            network_policy=network_policy,
            noorder_sequence_as_default=noorder_sequence_as_default,
            odbc_treat_decimal_as_int=odbc_treat_decimal_as_int,
            prevent_unload_to_internal_stages=prevent_unload_to_internal_stages,
            query_tag=query_tag,
            quoted_identifiers_ignore_case=quoted_identifiers_ignore_case,
            rows_per_resultset=rows_per_resultset,
            rsa_public_key=rsa_public_key,
            rsa_public_key2=rsa_public_key2,
            s3_stage_vpce_dns_name=s3_stage_vpce_dns_name,
            search_path=search_path,
            simulated_data_sharing_consumer=simulated_data_sharing_consumer,
            statement_queued_timeout_in_seconds=statement_queued_timeout_in_seconds,
            statement_timeout_in_seconds=statement_timeout_in_seconds,
            strict_json_output=strict_json_output,
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
            week_of_year_policy=week_of_year_policy,
            week_start=week_start,
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
        '''Generates CDKTF code for importing a ServiceUser resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceUser to import.
        :param import_from_id: The id of the existing ServiceUser that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceUser to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67cd2093d2606220c1a516507a1fff537677dac25fa1af2c9dec8947a9d5e3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAbortDetachedQuery")
    def reset_abort_detached_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbortDetachedQuery", []))

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

    @jsii.member(jsii_name="resetDateInputFormat")
    def reset_date_input_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateInputFormat", []))

    @jsii.member(jsii_name="resetDateOutputFormat")
    def reset_date_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateOutputFormat", []))

    @jsii.member(jsii_name="resetDaysToExpiry")
    def reset_days_to_expiry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysToExpiry", []))

    @jsii.member(jsii_name="resetDefaultNamespace")
    def reset_default_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultNamespace", []))

    @jsii.member(jsii_name="resetDefaultRole")
    def reset_default_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultRole", []))

    @jsii.member(jsii_name="resetDefaultSecondaryRolesOption")
    def reset_default_secondary_roles_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSecondaryRolesOption", []))

    @jsii.member(jsii_name="resetDefaultWarehouse")
    def reset_default_warehouse(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultWarehouse", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetEnableUnloadPhysicalTypeOptimization")
    def reset_enable_unload_physical_type_optimization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUnloadPhysicalTypeOptimization", []))

    @jsii.member(jsii_name="resetEnableUnredactedQuerySyntaxError")
    def reset_enable_unredacted_query_syntax_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUnredactedQuerySyntaxError", []))

    @jsii.member(jsii_name="resetErrorOnNondeterministicMerge")
    def reset_error_on_nondeterministic_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOnNondeterministicMerge", []))

    @jsii.member(jsii_name="resetErrorOnNondeterministicUpdate")
    def reset_error_on_nondeterministic_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOnNondeterministicUpdate", []))

    @jsii.member(jsii_name="resetGeographyOutputFormat")
    def reset_geography_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeographyOutputFormat", []))

    @jsii.member(jsii_name="resetGeometryOutputFormat")
    def reset_geometry_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeometryOutputFormat", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJdbcTreatDecimalAsInt")
    def reset_jdbc_treat_decimal_as_int(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJdbcTreatDecimalAsInt", []))

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

    @jsii.member(jsii_name="resetLoginName")
    def reset_login_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginName", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetMinsToUnlock")
    def reset_mins_to_unlock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinsToUnlock", []))

    @jsii.member(jsii_name="resetMultiStatementCount")
    def reset_multi_statement_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiStatementCount", []))

    @jsii.member(jsii_name="resetNetworkPolicy")
    def reset_network_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPolicy", []))

    @jsii.member(jsii_name="resetNoorderSequenceAsDefault")
    def reset_noorder_sequence_as_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoorderSequenceAsDefault", []))

    @jsii.member(jsii_name="resetOdbcTreatDecimalAsInt")
    def reset_odbc_treat_decimal_as_int(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOdbcTreatDecimalAsInt", []))

    @jsii.member(jsii_name="resetPreventUnloadToInternalStages")
    def reset_prevent_unload_to_internal_stages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventUnloadToInternalStages", []))

    @jsii.member(jsii_name="resetQueryTag")
    def reset_query_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryTag", []))

    @jsii.member(jsii_name="resetQuotedIdentifiersIgnoreCase")
    def reset_quoted_identifiers_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotedIdentifiersIgnoreCase", []))

    @jsii.member(jsii_name="resetRowsPerResultset")
    def reset_rows_per_resultset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowsPerResultset", []))

    @jsii.member(jsii_name="resetRsaPublicKey")
    def reset_rsa_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaPublicKey", []))

    @jsii.member(jsii_name="resetRsaPublicKey2")
    def reset_rsa_public_key2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaPublicKey2", []))

    @jsii.member(jsii_name="resetS3StageVpceDnsName")
    def reset_s3_stage_vpce_dns_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3StageVpceDnsName", []))

    @jsii.member(jsii_name="resetSearchPath")
    def reset_search_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchPath", []))

    @jsii.member(jsii_name="resetSimulatedDataSharingConsumer")
    def reset_simulated_data_sharing_consumer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimulatedDataSharingConsumer", []))

    @jsii.member(jsii_name="resetStatementQueuedTimeoutInSeconds")
    def reset_statement_queued_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementQueuedTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetStatementTimeoutInSeconds")
    def reset_statement_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetStrictJsonOutput")
    def reset_strict_json_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictJsonOutput", []))

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

    @jsii.member(jsii_name="resetWeekOfYearPolicy")
    def reset_week_of_year_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekOfYearPolicy", []))

    @jsii.member(jsii_name="resetWeekStart")
    def reset_week_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekStart", []))

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
    def parameters(self) -> "ServiceUserParametersList":
        return typing.cast("ServiceUserParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ServiceUserShowOutputList":
        return typing.cast("ServiceUserShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="userType")
    def user_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userType"))

    @builtins.property
    @jsii.member(jsii_name="abortDetachedQueryInput")
    def abort_detached_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "abortDetachedQueryInput"))

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
    @jsii.member(jsii_name="dateInputFormatInput")
    def date_input_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateInputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormatInput")
    def date_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="daysToExpiryInput")
    def days_to_expiry_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysToExpiryInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultNamespaceInput")
    def default_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultRoleInput")
    def default_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSecondaryRolesOptionInput")
    def default_secondary_roles_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultSecondaryRolesOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultWarehouseInput")
    def default_warehouse_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultWarehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="enableUnloadPhysicalTypeOptimizationInput")
    def enable_unload_physical_type_optimization_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableUnloadPhysicalTypeOptimizationInput"))

    @builtins.property
    @jsii.member(jsii_name="enableUnredactedQuerySyntaxErrorInput")
    def enable_unredacted_query_syntax_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableUnredactedQuerySyntaxErrorInput"))

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
    @jsii.member(jsii_name="jdbcTreatDecimalAsIntInput")
    def jdbc_treat_decimal_as_int_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jdbcTreatDecimalAsIntInput"))

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
    @jsii.member(jsii_name="loginNameInput")
    def login_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="minsToUnlockInput")
    def mins_to_unlock_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minsToUnlockInput"))

    @builtins.property
    @jsii.member(jsii_name="multiStatementCountInput")
    def multi_statement_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "multiStatementCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicyInput")
    def network_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkPolicyInput"))

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
    @jsii.member(jsii_name="preventUnloadToInternalStagesInput")
    def prevent_unload_to_internal_stages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventUnloadToInternalStagesInput"))

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
    @jsii.member(jsii_name="rsaPublicKey2Input")
    def rsa_public_key2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rsaPublicKey2Input"))

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKeyInput")
    def rsa_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rsaPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsNameInput")
    def s3_stage_vpce_dns_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3StageVpceDnsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="searchPathInput")
    def search_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchPathInput"))

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumerInput")
    def simulated_data_sharing_consumer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "simulatedDataSharingConsumerInput"))

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
    @jsii.member(jsii_name="weekOfYearPolicyInput")
    def week_of_year_policy_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekOfYearPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="weekStartInput")
    def week_start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekStartInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1dac8e519f15a6f2b17153b34f38a3f5004712a7dcdf7ccc82fb3e496508ae10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "abortDetachedQuery", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__36aac519eabd09b4b7febd5f26248cdcd474c7857daf5c7469b6f72629c7b498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocommit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryInputFormat"))

    @binary_input_format.setter
    def binary_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4acfdadd8050a2db2e2b3ad82ba09aee3b2658c6522b383666f3510382392b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryOutputFormat"))

    @binary_output_format.setter
    def binary_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd3d6394e712f72d6d4088d82f68161d00f3fdeb22ec22e42debc7496d2cabd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientMemoryLimit"))

    @client_memory_limit.setter
    def client_memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861a50f4b4e10e947e8a1f5aec3bbd58cfdccc6eb51929afea39a4af5a838c96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0a19d788f9e1ca06715d7dec02c334ace454888b413a5e55bd09931470d8993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientMetadataRequestUseConnectionCtx", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientPrefetchThreads"))

    @client_prefetch_threads.setter
    def client_prefetch_threads(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77543f4b5bde3fd1d4fdac05c3a7c2b66d702129e68b7bddf0e84e900fc79566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientPrefetchThreads", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientResultChunkSize"))

    @client_result_chunk_size.setter
    def client_result_chunk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33e8b6739a4a82f4c3db8d50650d8f749bc33c53de248db90d7662990e46b53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26689387b5359fb35902f552724e6f0f4d250384bac3eb7624042b0410c5beed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cdbc542b4cf3c70d7f8562e1c1eaabef2ca175cb60eab0da0152f9b74a52d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAlive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @client_session_keep_alive_heartbeat_frequency.setter
    def client_session_keep_alive_heartbeat_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b29a5a5ff287cf552f749ad5e970e8951bb5297c1d981e01d1ec6fb0087c5c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAliveHeartbeatFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTimestampTypeMapping"))

    @client_timestamp_type_mapping.setter
    def client_timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe02bfe031dd83e5c6472d7e76ec5361912586ba01c1333c213d8f2da75bdf2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c528ddd69e179fc5d804ee7362cc056cbe8cead91efca5dab03722d56553d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateInputFormat"))

    @date_input_format.setter
    def date_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c342c0e45222505bb6e3e6177d6761658d537f7cca860acc6aa5ef524c2e7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateOutputFormat"))

    @date_output_format.setter
    def date_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb16bc86a7ee37c7769a48820078e66dd83c2bca9f8da901b7bfb73a20026c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysToExpiry")
    def days_to_expiry(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysToExpiry"))

    @days_to_expiry.setter
    def days_to_expiry(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39755037c2ccc3ffdaa374ec21548f6f5429d06c3dd5bc750f1851ffe3989802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysToExpiry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultNamespace")
    def default_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultNamespace"))

    @default_namespace.setter
    def default_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fb65485d25416264beef2e8a935e18f4b7175b65d54643a30dc5bd0cc814d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRole")
    def default_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRole"))

    @default_role.setter
    def default_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a7deb20a7236abf3fc312c8ddf0340bfee6436171e62065f15637a3e87830b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSecondaryRolesOption")
    def default_secondary_roles_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSecondaryRolesOption"))

    @default_secondary_roles_option.setter
    def default_secondary_roles_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180400e293fe7833c690e934eba2fddce26f602462b1021d8b07396c1ed69683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSecondaryRolesOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultWarehouse")
    def default_warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultWarehouse"))

    @default_warehouse.setter
    def default_warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec703367381b35c01cd78120a91fd535c23df4e8b5d905c5d448964fe64d42b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultWarehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586dc744a84e97015b403a7d2178db16c6708f93d8450f4d7442c72eba5e91a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af67a6f6e583e7111e00a4da925ea6e52539483745f629ab8c94719f455789ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0baf46f8991123801edc57a651715674b21516e4fe907817eed53a2a800d7794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ce398afdfe5fe86458e21c6c2509579353616e7ab97d9385659b2300999a86d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUnloadPhysicalTypeOptimization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableUnredactedQuerySyntaxError")
    def enable_unredacted_query_syntax_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableUnredactedQuerySyntaxError"))

    @enable_unredacted_query_syntax_error.setter
    def enable_unredacted_query_syntax_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a84bec34edd060b0f7382d5a2cf79c32d30d65362768171b8f6f94316960b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUnredactedQuerySyntaxError", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0ab4edc2f0ba1f66603236a6829e034b87087f529fc0f5bbbfc770848d9da3ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57af89b47f1126f134da19b96b05197836b83b6c6ea36090136ea6f0c0add905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOnNondeterministicUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geographyOutputFormat"))

    @geography_output_format.setter
    def geography_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0534d10d08c99535e84cced7fc710d16354fb84c8189d5d65e39ea400cb9dd68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geographyOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geometryOutputFormat"))

    @geometry_output_format.setter
    def geometry_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c05442cde566e53690c0221b5bd3eae31dc0b8e1ba6a99392d2084894f04cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geometryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75f667243161b202d2ab8d476754f1d29c4332f6fccec68b5b4291d1264b65f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatDecimalAsInt")
    def jdbc_treat_decimal_as_int(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jdbcTreatDecimalAsInt"))

    @jdbc_treat_decimal_as_int.setter
    def jdbc_treat_decimal_as_int(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dba4ac73b4fafbc65011601bd38aba6157b951f0f5b98bc0f4a24a9fccd3403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jdbcTreatDecimalAsInt", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b850fcb77171e20a0b922d0d948ee0906eb5f6b208b399b7f0f284efcc482eaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcd6fe487cc7db526ae512d1c27269dd9931a83ffbc3b890b9c170e43c840e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jdbcUseSessionTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jsonIndent"))

    @json_indent.setter
    def json_indent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0de64f43f304d1123707b6b0e1613ed8e70774fd9682e590a05775500a40ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonIndent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockTimeout"))

    @lock_timeout.setter
    def lock_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b91463c32bbb778ad0452272728987de9e365447a89ef889eab1cf23174c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginName")
    def login_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginName"))

    @login_name.setter
    def login_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb3abd30b5e56618924b3b1ed44c1d59c7f262a861fb4d2274b166ad9932b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fb7b91525507f5c7c0338921eb2d01c40f4f8a4517840ba7acb3bf6636ffe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minsToUnlock")
    def mins_to_unlock(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minsToUnlock"))

    @mins_to_unlock.setter
    def mins_to_unlock(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d29ca34b1fa53722211c7661515bed6eb284d2683a8b270a481ad40985a7b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minsToUnlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiStatementCount"))

    @multi_statement_count.setter
    def multi_statement_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c428be30b3f1d31bd701ba37961218dd7682f00731c85ae99de4da1a0f0876ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiStatementCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b02937675cafa7949530242040953b333423bb3f5c1153e4206e7f3e832eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPolicy"))

    @network_policy.setter
    def network_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7968e45de201066d2a32958e8597ad2f26fc19e7fee8be398103b8ad6a633104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkPolicy", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__37766ef83f4c6e591ad90f6e235b651518e339112d6409892be2d3418d9d29fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__053ac577b37600018ace2662f9fd10fc31cb1d9a3b5f1846168fa984ef39d9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbcTreatDecimalAsInt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventUnloadToInternalStages")
    def prevent_unload_to_internal_stages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventUnloadToInternalStages"))

    @prevent_unload_to_internal_stages.setter
    def prevent_unload_to_internal_stages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6c291b18f41fa20ce95c52d0bb37e3389a4627c955dffae8c239de08467120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventUnloadToInternalStages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryTag"))

    @query_tag.setter
    def query_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9ce21b7ae89b466c424398cd338e4954eb90f9dd441a9ea2e9ba15ae681a97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b482cc65a73d89030af8b1aa405cf0cc3490653dcbde0adf2857401073c4488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotedIdentifiersIgnoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsPerResultset"))

    @rows_per_resultset.setter
    def rows_per_resultset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48aed0e618482cad613c74e431193eb3478a41e3160aa6cf3e494a6c2068b4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsPerResultset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKey")
    def rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey"))

    @rsa_public_key.setter
    def rsa_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82346500bdfa25bfa409612cb142ad7b1952f1ac55a89647890cab9bf842a61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKey2")
    def rsa_public_key2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey2"))

    @rsa_public_key2.setter
    def rsa_public_key2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0048514bd39d20784aaea7b0592587afd51c084bb028df5d0af8134904ae09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaPublicKey2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3StageVpceDnsName"))

    @s3_stage_vpce_dns_name.setter
    def s3_stage_vpce_dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9ada3b2bc24e4e3070fcc7eb3fa36b42dc03cb6675b10016f1f263b5d4b557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3StageVpceDnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchPath"))

    @search_path.setter
    def search_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00790a949dfb300906c699b6309d48928963cd3c288ff76b995c594cb64db2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumer")
    def simulated_data_sharing_consumer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "simulatedDataSharingConsumer"))

    @simulated_data_sharing_consumer.setter
    def simulated_data_sharing_consumer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b9c48314c8999de8635ab60a0787bfc517c414b5ffd389cde78d5214429031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simulatedDataSharingConsumer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @statement_queued_timeout_in_seconds.setter
    def statement_queued_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4e5d63fe02aed04cc10ca392df19cf799efef18094ac577b1121e6d012804b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementQueuedTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementTimeoutInSeconds"))

    @statement_timeout_in_seconds.setter
    def statement_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2d5621cfacffb6d6e238bdab5953c0ba8636689f8d71f9caaa5019070bcfea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d356a215dc7d1e2de76b6aefba45176c34339a247fbaf4cea91f52649eed9f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictJsonOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeInputFormat"))

    @time_input_format.setter
    def time_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45db12f331757fbd7ee1897af5c675276d3796eaa0a4d873b7aa0b2da6f1b19d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeOutputFormat"))

    @time_output_format.setter
    def time_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf0bf493644deca36da239e1e79c651d0c1206d4c3b4a66e9aa10a522c33eab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__469d33e5168b17ee00961ea2a83054649605a3cc9317d95efb6f9a1feaf63c6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampDayIsAlways24H", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampInputFormat"))

    @timestamp_input_format.setter
    def timestamp_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096788b3aef18f01dbc364e5d16fbeeda7eb0d50e8ae1e75cce990e3fe6f7203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampLtzOutputFormat"))

    @timestamp_ltz_output_format.setter
    def timestamp_ltz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db774cbb3bc517c15912983861294055cb57c6df27fe133505734b02a62e33a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampLtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampNtzOutputFormat"))

    @timestamp_ntz_output_format.setter
    def timestamp_ntz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db293ebfde0cdb3d20bc06de2506e1ec53e46759644eea58e0d2daede830bf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampNtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampOutputFormat"))

    @timestamp_output_format.setter
    def timestamp_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c91d56c6c6ed8f084949839c95fec3f2f5a8fbc74af7180e5468efc57990c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTypeMapping"))

    @timestamp_type_mapping.setter
    def timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3c98bb18abf38cab161632f609df75b428187507f4a3eae4230bce1d252363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTzOutputFormat"))

    @timestamp_tz_output_format.setter
    def timestamp_tz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b5d2ae1677f9856b1fc7f9e5c8e2122c47c07aac495e25a1c7ec033caeb067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69a1a3bb53cf9f83d158c30ea3a5738df7f310ae5438b3d1e39cda21f3dc81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f272802876454392c3789917a0d7b80de790f6d4b5c7d38497f7f1835c38ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ba22b3615563278d12527109c3a7a0b0b1d915f8f7ff3ada80c156a2c1f73d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionAbortOnError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transactionDefaultIsolationLevel"))

    @transaction_default_isolation_level.setter
    def transaction_default_isolation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d42ba48f1b6ee654d2df3e6dae7c8d176d3a22364b2bf8e0a8de9787211d3d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionDefaultIsolationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "twoDigitCenturyStart"))

    @two_digit_century_start.setter
    def two_digit_century_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6404fee259fb14535798b3f6f3be8a4b443dbfee56373d7b58df70d426679d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twoDigitCenturyStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unsupportedDdlAction"))

    @unsupported_ddl_action.setter
    def unsupported_ddl_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455228b49444e40860a18ef6ebeefbd03afc88b95fd71706433e974da5bbc431)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5abfcffab99cad72c8d5799f33ab6c46173f2caf0cf734fc78e64043de441e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCachedResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOfYearPolicy"))

    @week_of_year_policy.setter
    def week_of_year_policy(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db21cb9c10a0e7f70c42c111f173aca866f257ae6d5a22d059d9b692e8f2849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfYearPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekStart"))

    @week_start.setter
    def week_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4c3ac6930e5a416547135ad0e234bdab4656a82d23e901cea23554eed48f81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekStart", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserConfig",
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
        "abort_detached_query": "abortDetachedQuery",
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
        "date_input_format": "dateInputFormat",
        "date_output_format": "dateOutputFormat",
        "days_to_expiry": "daysToExpiry",
        "default_namespace": "defaultNamespace",
        "default_role": "defaultRole",
        "default_secondary_roles_option": "defaultSecondaryRolesOption",
        "default_warehouse": "defaultWarehouse",
        "disabled": "disabled",
        "display_name": "displayName",
        "email": "email",
        "enable_unload_physical_type_optimization": "enableUnloadPhysicalTypeOptimization",
        "enable_unredacted_query_syntax_error": "enableUnredactedQuerySyntaxError",
        "error_on_nondeterministic_merge": "errorOnNondeterministicMerge",
        "error_on_nondeterministic_update": "errorOnNondeterministicUpdate",
        "geography_output_format": "geographyOutputFormat",
        "geometry_output_format": "geometryOutputFormat",
        "id": "id",
        "jdbc_treat_decimal_as_int": "jdbcTreatDecimalAsInt",
        "jdbc_treat_timestamp_ntz_as_utc": "jdbcTreatTimestampNtzAsUtc",
        "jdbc_use_session_timezone": "jdbcUseSessionTimezone",
        "json_indent": "jsonIndent",
        "lock_timeout": "lockTimeout",
        "login_name": "loginName",
        "log_level": "logLevel",
        "mins_to_unlock": "minsToUnlock",
        "multi_statement_count": "multiStatementCount",
        "network_policy": "networkPolicy",
        "noorder_sequence_as_default": "noorderSequenceAsDefault",
        "odbc_treat_decimal_as_int": "odbcTreatDecimalAsInt",
        "prevent_unload_to_internal_stages": "preventUnloadToInternalStages",
        "query_tag": "queryTag",
        "quoted_identifiers_ignore_case": "quotedIdentifiersIgnoreCase",
        "rows_per_resultset": "rowsPerResultset",
        "rsa_public_key": "rsaPublicKey",
        "rsa_public_key2": "rsaPublicKey2",
        "s3_stage_vpce_dns_name": "s3StageVpceDnsName",
        "search_path": "searchPath",
        "simulated_data_sharing_consumer": "simulatedDataSharingConsumer",
        "statement_queued_timeout_in_seconds": "statementQueuedTimeoutInSeconds",
        "statement_timeout_in_seconds": "statementTimeoutInSeconds",
        "strict_json_output": "strictJsonOutput",
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
        "week_of_year_policy": "weekOfYearPolicy",
        "week_start": "weekStart",
    },
)
class ServiceUserConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        date_input_format: typing.Optional[builtins.str] = None,
        date_output_format: typing.Optional[builtins.str] = None,
        days_to_expiry: typing.Optional[jsii.Number] = None,
        default_namespace: typing.Optional[builtins.str] = None,
        default_role: typing.Optional[builtins.str] = None,
        default_secondary_roles_option: typing.Optional[builtins.str] = None,
        default_warehouse: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        geography_output_format: typing.Optional[builtins.str] = None,
        geometry_output_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_indent: typing.Optional[jsii.Number] = None,
        lock_timeout: typing.Optional[jsii.Number] = None,
        login_name: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        mins_to_unlock: typing.Optional[jsii.Number] = None,
        multi_statement_count: typing.Optional[jsii.Number] = None,
        network_policy: typing.Optional[builtins.str] = None,
        noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_unload_to_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_tag: typing.Optional[builtins.str] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rows_per_resultset: typing.Optional[jsii.Number] = None,
        rsa_public_key: typing.Optional[builtins.str] = None,
        rsa_public_key2: typing.Optional[builtins.str] = None,
        s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
        search_path: typing.Optional[builtins.str] = None,
        simulated_data_sharing_consumer: typing.Optional[builtins.str] = None,
        statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        week_of_year_policy: typing.Optional[jsii.Number] = None,
        week_start: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the user. Note that if you do not supply login_name this will be used as login_name. Check the `docs <https://docs.snowflake.net/manuals/sql-reference/sql/create-user.html#required-parameters>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#name ServiceUser#name}
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#abort_detached_query ServiceUser#abort_detached_query}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#autocommit ServiceUser#autocommit}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#binary_input_format ServiceUser#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#binary_output_format ServiceUser#binary_output_format}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_memory_limit ServiceUser#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_metadata_request_use_connection_ctx ServiceUser#client_metadata_request_use_connection_ctx}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_prefetch_threads ServiceUser#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_result_chunk_size ServiceUser#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_result_column_case_insensitive ServiceUser#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_session_keep_alive ServiceUser#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_session_keep_alive_heartbeat_frequency ServiceUser#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_timestamp_type_mapping ServiceUser#client_timestamp_type_mapping}
        :param comment: Specifies a comment for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#comment ServiceUser#comment}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#date_input_format ServiceUser#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#date_output_format ServiceUser#date_output_format}
        :param days_to_expiry: Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in. This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#days_to_expiry ServiceUser#days_to_expiry}
        :param default_namespace: Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the namespace exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_namespace ServiceUser#default_namespace}
        :param default_role: Specifies the role that is active by default for the user’s session upon login. Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_role ServiceUser#default_role}
        :param default_secondary_roles_option: Specifies the secondary roles that are active for the user’s session upon login. Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_secondary_roles_option ServiceUser#default_secondary_roles_option}
        :param default_warehouse: Specifies the virtual warehouse that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_warehouse ServiceUser#default_warehouse}
        :param disabled: Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#disabled ServiceUser#disabled}
        :param display_name: Name displayed for the user in the Snowflake web interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#display_name ServiceUser#display_name}
        :param email: Email address for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#email ServiceUser#email}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#enable_unload_physical_type_optimization ServiceUser#enable_unload_physical_type_optimization}
        :param enable_unredacted_query_syntax_error: Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error. If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#enable_unredacted_query_syntax_error ServiceUser#enable_unredacted_query_syntax_error}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#error_on_nondeterministic_merge ServiceUser#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#error_on_nondeterministic_update ServiceUser#error_on_nondeterministic_update}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#geography_output_format ServiceUser#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#geometry_output_format ServiceUser#geometry_output_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#id ServiceUser#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_treat_decimal_as_int: Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_treat_decimal_as_int ServiceUser#jdbc_treat_decimal_as_int}
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_treat_timestamp_ntz_as_utc ServiceUser#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_use_session_timezone ServiceUser#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#json_indent ServiceUser#json_indent}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#lock_timeout ServiceUser#lock_timeout}
        :param login_name: The name users use to log in. If not supplied, snowflake will use name instead. Login names are always case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#login_name ServiceUser#login_name}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#log_level ServiceUser#log_level}
        :param mins_to_unlock: Specifies the number of minutes until the temporary lock on the user login is cleared. To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#mins_to_unlock ServiceUser#mins_to_unlock}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#multi_statement_count ServiceUser#multi_statement_count}
        :param network_policy: Specifies the network policy to enforce for your account. Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#network_policy ServiceUser#network_policy}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#noorder_sequence_as_default ServiceUser#noorder_sequence_as_default}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#odbc_treat_decimal_as_int ServiceUser#odbc_treat_decimal_as_int}
        :param prevent_unload_to_internal_stages: Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#prevent_unload_to_internal_stages ServiceUser#prevent_unload_to_internal_stages}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#query_tag ServiceUser#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#quoted_identifiers_ignore_case ServiceUser#quoted_identifiers_ignore_case}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rows_per_resultset ServiceUser#rows_per_resultset}
        :param rsa_public_key: Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rsa_public_key ServiceUser#rsa_public_key}
        :param rsa_public_key2: Specifies the user’s second RSA public key; used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rsa_public_key_2 ServiceUser#rsa_public_key_2}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#s3_stage_vpce_dns_name ServiceUser#s3_stage_vpce_dns_name}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#search_path ServiceUser#search_path}
        :param simulated_data_sharing_consumer: Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views. When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#simulated_data_sharing_consumer ServiceUser#simulated_data_sharing_consumer}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#statement_queued_timeout_in_seconds ServiceUser#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#statement_timeout_in_seconds ServiceUser#statement_timeout_in_seconds}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#strict_json_output ServiceUser#strict_json_output}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#time_input_format ServiceUser#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#time_output_format ServiceUser#time_output_format}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_day_is_always_24h ServiceUser#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_input_format ServiceUser#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_ltz_output_format ServiceUser#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_ntz_output_format ServiceUser#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_output_format ServiceUser#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_type_mapping ServiceUser#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_tz_output_format ServiceUser#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timezone ServiceUser#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#trace_level ServiceUser#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#transaction_abort_on_error ServiceUser#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#transaction_default_isolation_level ServiceUser#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#two_digit_century_start ServiceUser#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#unsupported_ddl_action ServiceUser#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#use_cached_result ServiceUser#use_cached_result}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#week_of_year_policy ServiceUser#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#week_start ServiceUser#week_start}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b2bc95509002ce2a86a619507d2cae7e7dcbdb03df3f7a079af7baac670bca)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument abort_detached_query", value=abort_detached_query, expected_type=type_hints["abort_detached_query"])
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
            check_type(argname="argument date_input_format", value=date_input_format, expected_type=type_hints["date_input_format"])
            check_type(argname="argument date_output_format", value=date_output_format, expected_type=type_hints["date_output_format"])
            check_type(argname="argument days_to_expiry", value=days_to_expiry, expected_type=type_hints["days_to_expiry"])
            check_type(argname="argument default_namespace", value=default_namespace, expected_type=type_hints["default_namespace"])
            check_type(argname="argument default_role", value=default_role, expected_type=type_hints["default_role"])
            check_type(argname="argument default_secondary_roles_option", value=default_secondary_roles_option, expected_type=type_hints["default_secondary_roles_option"])
            check_type(argname="argument default_warehouse", value=default_warehouse, expected_type=type_hints["default_warehouse"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument enable_unload_physical_type_optimization", value=enable_unload_physical_type_optimization, expected_type=type_hints["enable_unload_physical_type_optimization"])
            check_type(argname="argument enable_unredacted_query_syntax_error", value=enable_unredacted_query_syntax_error, expected_type=type_hints["enable_unredacted_query_syntax_error"])
            check_type(argname="argument error_on_nondeterministic_merge", value=error_on_nondeterministic_merge, expected_type=type_hints["error_on_nondeterministic_merge"])
            check_type(argname="argument error_on_nondeterministic_update", value=error_on_nondeterministic_update, expected_type=type_hints["error_on_nondeterministic_update"])
            check_type(argname="argument geography_output_format", value=geography_output_format, expected_type=type_hints["geography_output_format"])
            check_type(argname="argument geometry_output_format", value=geometry_output_format, expected_type=type_hints["geometry_output_format"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jdbc_treat_decimal_as_int", value=jdbc_treat_decimal_as_int, expected_type=type_hints["jdbc_treat_decimal_as_int"])
            check_type(argname="argument jdbc_treat_timestamp_ntz_as_utc", value=jdbc_treat_timestamp_ntz_as_utc, expected_type=type_hints["jdbc_treat_timestamp_ntz_as_utc"])
            check_type(argname="argument jdbc_use_session_timezone", value=jdbc_use_session_timezone, expected_type=type_hints["jdbc_use_session_timezone"])
            check_type(argname="argument json_indent", value=json_indent, expected_type=type_hints["json_indent"])
            check_type(argname="argument lock_timeout", value=lock_timeout, expected_type=type_hints["lock_timeout"])
            check_type(argname="argument login_name", value=login_name, expected_type=type_hints["login_name"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument mins_to_unlock", value=mins_to_unlock, expected_type=type_hints["mins_to_unlock"])
            check_type(argname="argument multi_statement_count", value=multi_statement_count, expected_type=type_hints["multi_statement_count"])
            check_type(argname="argument network_policy", value=network_policy, expected_type=type_hints["network_policy"])
            check_type(argname="argument noorder_sequence_as_default", value=noorder_sequence_as_default, expected_type=type_hints["noorder_sequence_as_default"])
            check_type(argname="argument odbc_treat_decimal_as_int", value=odbc_treat_decimal_as_int, expected_type=type_hints["odbc_treat_decimal_as_int"])
            check_type(argname="argument prevent_unload_to_internal_stages", value=prevent_unload_to_internal_stages, expected_type=type_hints["prevent_unload_to_internal_stages"])
            check_type(argname="argument query_tag", value=query_tag, expected_type=type_hints["query_tag"])
            check_type(argname="argument quoted_identifiers_ignore_case", value=quoted_identifiers_ignore_case, expected_type=type_hints["quoted_identifiers_ignore_case"])
            check_type(argname="argument rows_per_resultset", value=rows_per_resultset, expected_type=type_hints["rows_per_resultset"])
            check_type(argname="argument rsa_public_key", value=rsa_public_key, expected_type=type_hints["rsa_public_key"])
            check_type(argname="argument rsa_public_key2", value=rsa_public_key2, expected_type=type_hints["rsa_public_key2"])
            check_type(argname="argument s3_stage_vpce_dns_name", value=s3_stage_vpce_dns_name, expected_type=type_hints["s3_stage_vpce_dns_name"])
            check_type(argname="argument search_path", value=search_path, expected_type=type_hints["search_path"])
            check_type(argname="argument simulated_data_sharing_consumer", value=simulated_data_sharing_consumer, expected_type=type_hints["simulated_data_sharing_consumer"])
            check_type(argname="argument statement_queued_timeout_in_seconds", value=statement_queued_timeout_in_seconds, expected_type=type_hints["statement_queued_timeout_in_seconds"])
            check_type(argname="argument statement_timeout_in_seconds", value=statement_timeout_in_seconds, expected_type=type_hints["statement_timeout_in_seconds"])
            check_type(argname="argument strict_json_output", value=strict_json_output, expected_type=type_hints["strict_json_output"])
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
            check_type(argname="argument week_of_year_policy", value=week_of_year_policy, expected_type=type_hints["week_of_year_policy"])
            check_type(argname="argument week_start", value=week_start, expected_type=type_hints["week_start"])
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
        if abort_detached_query is not None:
            self._values["abort_detached_query"] = abort_detached_query
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
        if date_input_format is not None:
            self._values["date_input_format"] = date_input_format
        if date_output_format is not None:
            self._values["date_output_format"] = date_output_format
        if days_to_expiry is not None:
            self._values["days_to_expiry"] = days_to_expiry
        if default_namespace is not None:
            self._values["default_namespace"] = default_namespace
        if default_role is not None:
            self._values["default_role"] = default_role
        if default_secondary_roles_option is not None:
            self._values["default_secondary_roles_option"] = default_secondary_roles_option
        if default_warehouse is not None:
            self._values["default_warehouse"] = default_warehouse
        if disabled is not None:
            self._values["disabled"] = disabled
        if display_name is not None:
            self._values["display_name"] = display_name
        if email is not None:
            self._values["email"] = email
        if enable_unload_physical_type_optimization is not None:
            self._values["enable_unload_physical_type_optimization"] = enable_unload_physical_type_optimization
        if enable_unredacted_query_syntax_error is not None:
            self._values["enable_unredacted_query_syntax_error"] = enable_unredacted_query_syntax_error
        if error_on_nondeterministic_merge is not None:
            self._values["error_on_nondeterministic_merge"] = error_on_nondeterministic_merge
        if error_on_nondeterministic_update is not None:
            self._values["error_on_nondeterministic_update"] = error_on_nondeterministic_update
        if geography_output_format is not None:
            self._values["geography_output_format"] = geography_output_format
        if geometry_output_format is not None:
            self._values["geometry_output_format"] = geometry_output_format
        if id is not None:
            self._values["id"] = id
        if jdbc_treat_decimal_as_int is not None:
            self._values["jdbc_treat_decimal_as_int"] = jdbc_treat_decimal_as_int
        if jdbc_treat_timestamp_ntz_as_utc is not None:
            self._values["jdbc_treat_timestamp_ntz_as_utc"] = jdbc_treat_timestamp_ntz_as_utc
        if jdbc_use_session_timezone is not None:
            self._values["jdbc_use_session_timezone"] = jdbc_use_session_timezone
        if json_indent is not None:
            self._values["json_indent"] = json_indent
        if lock_timeout is not None:
            self._values["lock_timeout"] = lock_timeout
        if login_name is not None:
            self._values["login_name"] = login_name
        if log_level is not None:
            self._values["log_level"] = log_level
        if mins_to_unlock is not None:
            self._values["mins_to_unlock"] = mins_to_unlock
        if multi_statement_count is not None:
            self._values["multi_statement_count"] = multi_statement_count
        if network_policy is not None:
            self._values["network_policy"] = network_policy
        if noorder_sequence_as_default is not None:
            self._values["noorder_sequence_as_default"] = noorder_sequence_as_default
        if odbc_treat_decimal_as_int is not None:
            self._values["odbc_treat_decimal_as_int"] = odbc_treat_decimal_as_int
        if prevent_unload_to_internal_stages is not None:
            self._values["prevent_unload_to_internal_stages"] = prevent_unload_to_internal_stages
        if query_tag is not None:
            self._values["query_tag"] = query_tag
        if quoted_identifiers_ignore_case is not None:
            self._values["quoted_identifiers_ignore_case"] = quoted_identifiers_ignore_case
        if rows_per_resultset is not None:
            self._values["rows_per_resultset"] = rows_per_resultset
        if rsa_public_key is not None:
            self._values["rsa_public_key"] = rsa_public_key
        if rsa_public_key2 is not None:
            self._values["rsa_public_key2"] = rsa_public_key2
        if s3_stage_vpce_dns_name is not None:
            self._values["s3_stage_vpce_dns_name"] = s3_stage_vpce_dns_name
        if search_path is not None:
            self._values["search_path"] = search_path
        if simulated_data_sharing_consumer is not None:
            self._values["simulated_data_sharing_consumer"] = simulated_data_sharing_consumer
        if statement_queued_timeout_in_seconds is not None:
            self._values["statement_queued_timeout_in_seconds"] = statement_queued_timeout_in_seconds
        if statement_timeout_in_seconds is not None:
            self._values["statement_timeout_in_seconds"] = statement_timeout_in_seconds
        if strict_json_output is not None:
            self._values["strict_json_output"] = strict_json_output
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
        if week_of_year_policy is not None:
            self._values["week_of_year_policy"] = week_of_year_policy
        if week_start is not None:
            self._values["week_start"] = week_start

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
        '''Name of the user.

        Note that if you do not supply login_name this will be used as login_name. Check the `docs <https://docs.snowflake.net/manuals/sql-reference/sql/create-user.html#required-parameters>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#name ServiceUser#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def abort_detached_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#abort_detached_query ServiceUser#abort_detached_query}
        '''
        result = self._values.get("abort_detached_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def autocommit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether autocommit is enabled for the session.

        Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#autocommit ServiceUser#autocommit}
        '''
        result = self._values.get("autocommit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def binary_input_format(self) -> typing.Optional[builtins.str]:
        '''The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#binary_input_format ServiceUser#binary_input_format}
        '''
        result = self._values.get("binary_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_output_format(self) -> typing.Optional[builtins.str]:
        '''The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#binary_output_format ServiceUser#binary_output_format}
        '''
        result = self._values.get("binary_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_memory_limit(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB).

        For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_memory_limit ServiceUser#client_memory_limit}
        '''
        result = self._values.get("client_memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema.

        The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_metadata_request_use_connection_ctx ServiceUser#client_metadata_request_use_connection_ctx}
        '''
        result = self._values.get("client_metadata_request_use_connection_ctx")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_prefetch_threads(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the number of threads used by the client to pre-fetch large result sets.

        The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_prefetch_threads ServiceUser#client_prefetch_threads}
        '''
        result = self._values.get("client_prefetch_threads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_chunk_size(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB).

        The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_result_chunk_size ServiceUser#client_result_chunk_size}
        '''
        result = self._values.get("client_result_chunk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_column_case_insensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_result_column_case_insensitive ServiceUser#client_result_column_case_insensitive}
        '''
        result = self._values.get("client_result_column_case_insensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to force a user to log in again after a period of inactivity in the session.

        For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_session_keep_alive ServiceUser#client_session_keep_alive}
        '''
        result = self._values.get("client_session_keep_alive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_session_keep_alive_heartbeat_frequency ServiceUser#client_session_keep_alive_heartbeat_frequency}
        '''
        result = self._values.get("client_session_keep_alive_heartbeat_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#client_timestamp_type_mapping ServiceUser#client_timestamp_type_mapping}
        '''
        result = self._values.get("client_timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#comment ServiceUser#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#date_input_format ServiceUser#date_input_format}
        '''
        result = self._values.get("date_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#date_output_format ServiceUser#date_output_format}
        '''
        result = self._values.get("date_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_to_expiry(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in.

        This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#days_to_expiry ServiceUser#days_to_expiry}
        '''
        result = self._values.get("days_to_expiry")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_namespace(self) -> typing.Optional[builtins.str]:
        '''Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login.

        Note that the CREATE USER operation does not verify that the namespace exists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_namespace ServiceUser#default_namespace}
        '''
        result = self._values.get("default_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_role(self) -> typing.Optional[builtins.str]:
        '''Specifies the role that is active by default for the user’s session upon login.

        Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_role ServiceUser#default_role}
        '''
        result = self._values.get("default_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_secondary_roles_option(self) -> typing.Optional[builtins.str]:
        '''Specifies the secondary roles that are active for the user’s session upon login.

        Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_secondary_roles_option ServiceUser#default_secondary_roles_option}
        '''
        result = self._values.get("default_secondary_roles_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_warehouse(self) -> typing.Optional[builtins.str]:
        '''Specifies the virtual warehouse that is active by default for the user’s session upon login.

        Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#default_warehouse ServiceUser#default_warehouse}
        '''
        result = self._values.get("default_warehouse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#disabled ServiceUser#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Name displayed for the user in the Snowflake web interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#display_name ServiceUser#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email address for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#email ServiceUser#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_unload_physical_type_optimization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#enable_unload_physical_type_optimization ServiceUser#enable_unload_physical_type_optimization}
        '''
        result = self._values.get("enable_unload_physical_type_optimization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_unredacted_query_syntax_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error.

        If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#enable_unredacted_query_syntax_error ServiceUser#enable_unredacted_query_syntax_error}
        '''
        result = self._values.get("enable_unredacted_query_syntax_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#error_on_nondeterministic_merge ServiceUser#error_on_nondeterministic_merge}
        '''
        result = self._values.get("error_on_nondeterministic_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#error_on_nondeterministic_update ServiceUser#error_on_nondeterministic_update}
        '''
        result = self._values.get("error_on_nondeterministic_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def geography_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#geography_output_format ServiceUser#geography_output_format}
        '''
        result = self._values.get("geography_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geometry_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#geometry_output_format ServiceUser#geometry_output_format}
        '''
        result = self._values.get("geometry_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#id ServiceUser#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jdbc_treat_decimal_as_int(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_treat_decimal_as_int ServiceUser#jdbc_treat_decimal_as_int}
        '''
        result = self._values.get("jdbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_treat_timestamp_ntz_as_utc ServiceUser#jdbc_treat_timestamp_ntz_as_utc}
        '''
        result = self._values.get("jdbc_treat_timestamp_ntz_as_utc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_use_session_timezone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#jdbc_use_session_timezone ServiceUser#jdbc_use_session_timezone}
        '''
        result = self._values.get("jdbc_use_session_timezone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def json_indent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of blank spaces to indent each new element in JSON output in the session.

        Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#json_indent ServiceUser#json_indent}
        '''
        result = self._values.get("json_indent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lock_timeout(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement.

        For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#lock_timeout ServiceUser#lock_timeout}
        '''
        result = self._values.get("lock_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def login_name(self) -> typing.Optional[builtins.str]:
        '''The name users use to log in.

        If not supplied, snowflake will use name instead. Login names are always case-insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#login_name ServiceUser#login_name}
        '''
        result = self._values.get("login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the severity level of messages that should be ingested and made available in the active event table.

        Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#log_level ServiceUser#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mins_to_unlock(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of minutes until the temporary lock on the user login is cleared.

        To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#mins_to_unlock ServiceUser#mins_to_unlock}
        '''
        result = self._values.get("mins_to_unlock")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def multi_statement_count(self) -> typing.Optional[jsii.Number]:
        '''Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#multi_statement_count ServiceUser#multi_statement_count}
        '''
        result = self._values.get("multi_statement_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the network policy to enforce for your account.

        Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#network_policy ServiceUser#network_policy}
        '''
        result = self._values.get("network_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def noorder_sequence_as_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column.

        The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#noorder_sequence_as_default ServiceUser#noorder_sequence_as_default}
        '''
        result = self._values.get("noorder_sequence_as_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def odbc_treat_decimal_as_int(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#odbc_treat_decimal_as_int ServiceUser#odbc_treat_decimal_as_int}
        '''
        result = self._values.get("odbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_unload_to_internal_stages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO  <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#prevent_unload_to_internal_stages ServiceUser#prevent_unload_to_internal_stages}
        '''
        result = self._values.get("prevent_unload_to_internal_stages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_tag(self) -> typing.Optional[builtins.str]:
        '''Optional string that can be used to tag queries and other SQL statements executed within a session.

        The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#query_tag ServiceUser#query_tag}
        '''
        result = self._values.get("query_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters.

        By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#quoted_identifiers_ignore_case ServiceUser#quoted_identifiers_ignore_case}
        '''
        result = self._values.get("quoted_identifiers_ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rows_per_resultset(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of rows returned in a result set.

        A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rows_per_resultset ServiceUser#rows_per_resultset}
        '''
        result = self._values.get("rows_per_resultset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rsa_public_key ServiceUser#rsa_public_key}
        '''
        result = self._values.get("rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_public_key2(self) -> typing.Optional[builtins.str]:
        '''Specifies the user’s second RSA public key;

        used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#rsa_public_key_2 ServiceUser#rsa_public_key_2}
        '''
        result = self._values.get("rsa_public_key2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_stage_vpce_dns_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the DNS name of an Amazon S3 interface endpoint.

        Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#s3_stage_vpce_dns_name ServiceUser#s3_stage_vpce_dns_name}
        '''
        result = self._values.get("s3_stage_vpce_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_path(self) -> typing.Optional[builtins.str]:
        '''Specifies the path to search to resolve unqualified object names in queries.

        For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#search_path ServiceUser#search_path}
        '''
        result = self._values.get("search_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def simulated_data_sharing_consumer(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views.

        When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#simulated_data_sharing_consumer ServiceUser#simulated_data_sharing_consumer}
        '''
        result = self._values.get("simulated_data_sharing_consumer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_queued_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#statement_queued_timeout_in_seconds ServiceUser#statement_queued_timeout_in_seconds}
        '''
        result = self._values.get("statement_queued_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statement_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#statement_timeout_in_seconds ServiceUser#statement_timeout_in_seconds}
        '''
        result = self._values.get("statement_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strict_json_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#strict_json_output ServiceUser#strict_json_output}
        '''
        result = self._values.get("strict_json_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#time_input_format ServiceUser#time_input_format}
        '''
        result = self._values.get("time_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#time_output_format ServiceUser#time_output_format}
        '''
        result = self._values.get("time_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_day_is_always24_h(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_day_is_always_24h ServiceUser#timestamp_day_is_always_24h}
        '''
        result = self._values.get("timestamp_day_is_always24_h")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timestamp_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_input_format ServiceUser#timestamp_input_format}
        '''
        result = self._values.get("timestamp_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ltz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_LTZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_ltz_output_format ServiceUser#timestamp_ltz_output_format}
        '''
        result = self._values.get("timestamp_ltz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ntz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_ntz_output_format ServiceUser#timestamp_ntz_output_format}
        '''
        result = self._values.get("timestamp_ntz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_output_format ServiceUser#timestamp_output_format}
        '''
        result = self._values.get("timestamp_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_type_mapping ServiceUser#timestamp_type_mapping}
        '''
        result = self._values.get("timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_tz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_TZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timestamp_tz_output_format ServiceUser#timestamp_tz_output_format}
        '''
        result = self._values.get("timestamp_tz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone for the session.

        You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#timezone ServiceUser#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Controls how trace events are ingested into the event table.

        For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#trace_level ServiceUser#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_abort_on_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error.

        For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#transaction_abort_on_error ServiceUser#transaction_abort_on_error}
        '''
        result = self._values.get("transaction_abort_on_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transaction_default_isolation_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#transaction_default_isolation_level ServiceUser#transaction_default_isolation_level}
        '''
        result = self._values.get("transaction_default_isolation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def two_digit_century_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#two_digit_century_start ServiceUser#two_digit_century_start}
        '''
        result = self._values.get("two_digit_century_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unsupported_ddl_action(self) -> typing.Optional[builtins.str]:
        '''Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#unsupported_ddl_action ServiceUser#unsupported_ddl_action}
        '''
        result = self._values.get("unsupported_ddl_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_cached_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to reuse persisted query results, if available, when a matching query is submitted.

        For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#use_cached_result ServiceUser#use_cached_result}
        '''
        result = self._values.get("use_cached_result")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def week_of_year_policy(self) -> typing.Optional[jsii.Number]:
        '''Specifies how the weeks in a given year are computed.

        ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#week_of_year_policy ServiceUser#week_of_year_policy}
        '''
        result = self._values.get("week_of_year_policy")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the first day of the week (used by week-related date functions).

        ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/service_user#week_start ServiceUser#week_start}
        '''
        result = self._values.get("week_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersAbortDetachedQuery",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersAbortDetachedQuery:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersAbortDetachedQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersAbortDetachedQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersAbortDetachedQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a783aec0a42e90a34ee600c85fcddb713f913fdff9c3b52be0ed0120de87803)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersAbortDetachedQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c469ca83a5c2df0a906ff442d382fb41590ea4d1405ea1c7333d26df9a423bf7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersAbortDetachedQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6786c8de674174c9d196be714e6e24bec5c47623ef9e4044c74dcc6c0be18bb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__461b78280c3271b9874813ff5eb034b03ea3e3eeecd693b13df591c7b030d304)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee3ebf9bdcc6ce758b94afa6e943bda9f5225c3a1b403fbad28946020a312562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersAbortDetachedQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersAbortDetachedQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0859ef6d39d2c0c7a208499d116a1d9b4acbe9e61cc946fe9898326b4f652049)
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
    ) -> typing.Optional[ServiceUserParametersAbortDetachedQuery]:
        return typing.cast(typing.Optional[ServiceUserParametersAbortDetachedQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersAbortDetachedQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b379a3bddf7c46bb6fbf81cba29dc40fb47e1a812483fcd549a5616f2b273a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersAutocommit",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersAutocommit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersAutocommit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersAutocommitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersAutocommitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__978be8521df8d1e47e0e855ff4828f7a5150fc103257e309d075b69b54fa9a9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersAutocommitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4109c2b0a1619985723d2ec0f36a74b88d00739d9f71b02f4ea52575ba2ed6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersAutocommitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bdbee872a2906ab63784c577c275ef303674fa2641e7a5c21018d039c80af19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6243d29b8f9f0559d93f5757c1a3946ad62706501e1de402b15b61b46953449c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65b6e3d5eeefa4e4435c8d6fdfdb567fef29cec2818ac87a56220caa8f202993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersAutocommitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersAutocommitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b69481f864385e330ee93437c74e0d8c8076f456bd014e1c1a867693602ffd)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersAutocommit]:
        return typing.cast(typing.Optional[ServiceUserParametersAutocommit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersAutocommit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d935bd5b58cc0b2001ad3d6352234e68dac7d946f53a6fddb10a5ef3960227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersBinaryInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersBinaryInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersBinaryInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersBinaryInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersBinaryInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ac802069d1c5f6c88bb131300ac31173cefffc5735b91397773cf9315553a93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersBinaryInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3066bdbc52789bef13a9298c4a0c66a5590f6f2b10f4fff9d432fae13156a07d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersBinaryInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9553f957e5ee8e4cf2dab99506da637d10638b5a1a5126f541a49002f8a7edcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9191f1aba07a747f288889381e91fc6609f550b11a790604efeb3261ada419e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16633872b6878dea33cec373c91fa1a3ee91078b7659483822caeb7e5a94ec19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersBinaryInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersBinaryInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__487068bcca5f1cffd6d33ed41bd06427243e82f5c404d04a688e017ab4e18056)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersBinaryInputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersBinaryInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersBinaryInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7475a01115000a588fd1fb4faeb4956f762f18857005c9eea24550df7dd484aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersBinaryOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersBinaryOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersBinaryOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersBinaryOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersBinaryOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be961f0501d66b98e9e7999b042f576214e642ce7ae8850ae2e02255f6e6a964)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersBinaryOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460e09f6e2f37fa423b595a6e0af15c29659c74fd5103456dab9a6ab2697fef0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersBinaryOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93dddd388bc426d65a5f675de87d80d3b7336e3200535698c6654bef15281eec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b5575559d3694cb20d45ed0d5ea2c62540747503990ae7da689991913e70c19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd0d1f8135a984775d2c1815b59c5fc1dc1094e94ba8814f0969b6db84825a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersBinaryOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersBinaryOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53d70369754cf9c89db3b519da82541aea9b315fd23fe89e4a36f93d2ce2f755)
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
    ) -> typing.Optional[ServiceUserParametersBinaryOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersBinaryOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersBinaryOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1f0c11acdf6f8590a859c699aae23001076b0c35a427b0e23d567ef5faee60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientMemoryLimit",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersClientMemoryLimit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersClientMemoryLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersClientMemoryLimitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientMemoryLimitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f06f2d99266ed1484d8335dcdf766d68a235e11ce4dcc4f8317f6f34927878cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersClientMemoryLimitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5cb90e7935905a2f033fff2476704fab51592aea10480b9c9d27f440a2fc4e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersClientMemoryLimitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059a5447050e4057d64c1c93d2a7105fa7b943b403727e5bc8ee76bedbb9609b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ac1ec0d759c36b0e4f37e98149a2540062cfffaa9f299143e43d40edf47aea5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__475eeaef3cf75d6d908b51215b1c6ea6c5835b188d3ddc7ad60dc3d9261b9deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientMemoryLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientMemoryLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4bfa62babecd2303f2d4919f9f5abdd5bc7c2d3f85fc759bdc356577cc96daa)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersClientMemoryLimit]:
        return typing.cast(typing.Optional[ServiceUserParametersClientMemoryLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersClientMemoryLimit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015ab009f588279ad665f5183a20812a40c76ff48b8ffbd759f4d8179943be04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientMetadataRequestUseConnectionCtx",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersClientMetadataRequestUseConnectionCtx:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersClientMetadataRequestUseConnectionCtx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersClientMetadataRequestUseConnectionCtxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientMetadataRequestUseConnectionCtxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e60a85d8dff1d71cfb48008b773639dcca78ea22f6086f3ade85c637e11ab81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdc57b62f85fc871ed5c9da6b433b4034861c692c0aa0cd02819a83c6e15f74)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7c02e2effd9d72b27184c9f647a49b1a816beb08855ad4fab709eef17a1f6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__897a91c56614014297fff05147866ee744d640b6b2ea5051c649906812bd135a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4466151f22a4e9167d86419a586e113fd05e90dc7a636509a4cca375207a0dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07d6fa3286bf117e072d75e3e013081a7b9755a47d5a5e8e284c0f18208a0baa)
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
    ) -> typing.Optional[ServiceUserParametersClientMetadataRequestUseConnectionCtx]:
        return typing.cast(typing.Optional[ServiceUserParametersClientMetadataRequestUseConnectionCtx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersClientMetadataRequestUseConnectionCtx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7178299f6555a98ab1126c5bd796f2c8985f7fbdcf48075d8183b6537e914f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientPrefetchThreads",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersClientPrefetchThreads:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersClientPrefetchThreads(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersClientPrefetchThreadsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientPrefetchThreadsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de17ad0e24da260ab3c226304e32d46503118b7191e377b475bbaf0b6d7df06e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersClientPrefetchThreadsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07cb499d248d6fc02ca6b34e9f5a88d684d82cece5c1660ce2566bc6d84727a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersClientPrefetchThreadsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f9c29a091648e9e359de5bdb3da4f6532c9f91432e4908f7f371b8395ee11d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac4d79606d6f3b1e70d553fc3ed6bb69ddce68e6a0845132f27f8c7d56239446)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c8bc23a9aed993ab9ded3369436e3231bdae3679034beeae8e13195bbb568e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientPrefetchThreadsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientPrefetchThreadsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__021668569c8bd3a2cfc486c0aa7e4c4941d39473b91cf2c7050d527509b486e8)
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
    ) -> typing.Optional[ServiceUserParametersClientPrefetchThreads]:
        return typing.cast(typing.Optional[ServiceUserParametersClientPrefetchThreads], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersClientPrefetchThreads],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7baa60960433eba0b1c340c807136b61efdcd7e6a067257f60b5487d9d42499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientResultChunkSize",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersClientResultChunkSize:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersClientResultChunkSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersClientResultChunkSizeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientResultChunkSizeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cca3ca326b9f16cee05a26ec4391af6389a31d822f468beff61519261e9cc080)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersClientResultChunkSizeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74e1aa52e88bd8ac0572882c03813f6d856770a25879c221ffb8db2dfb20f0d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersClientResultChunkSizeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e4c5e6d5703f6c2f506fb1765ce88e86a8f06d3ec47746c273a8d6a70f9d02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8736cef9121191664a3d20cb36384265e3674d08ac166226d8fa6c36e8c316ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b963fe0b0ac52154441f551f2c595b08e39f75c4c9508b6e7fda8a60be6381a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientResultChunkSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientResultChunkSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__492dd01ceea63727bba3776de641672d417e878d150f9b80ce46fc18984bae09)
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
    ) -> typing.Optional[ServiceUserParametersClientResultChunkSize]:
        return typing.cast(typing.Optional[ServiceUserParametersClientResultChunkSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersClientResultChunkSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873042d47c5247a789b4ad3192e193ac5438c3b201d82a269fc65a77d1c4ebff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientResultColumnCaseInsensitive",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersClientResultColumnCaseInsensitive:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersClientResultColumnCaseInsensitive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersClientResultColumnCaseInsensitiveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientResultColumnCaseInsensitiveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efacf8111f8e3fb923b14890727ebd72fd6a18f3b98423580535e5278d590373)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersClientResultColumnCaseInsensitiveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb0214e7ddce51c5dd7f4cb82e5be6580ef611c351874dc1b520370dd6b5a56)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersClientResultColumnCaseInsensitiveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f26c4539a611ab6d6033502157584eefe20f543f1e56f8fc1bf13970d55fc18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__859a9d5b200b2dcb2fee2b58f7e63bd5920ee48899a490ae0abcfbc798089689)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d23cb7a548159da18af0eccc44c149314c746f0caff6ff4322720398abc3d46a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientResultColumnCaseInsensitiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientResultColumnCaseInsensitiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f807964f51aae3b0e3b22a077e96e20d8880d0cb518ea54b0088a4693a02011)
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
    ) -> typing.Optional[ServiceUserParametersClientResultColumnCaseInsensitive]:
        return typing.cast(typing.Optional[ServiceUserParametersClientResultColumnCaseInsensitive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersClientResultColumnCaseInsensitive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22b89f9c9c5af5d4557f8c7affa1c3ba63af0a46cb2767309ed4fb63f155507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientSessionKeepAlive",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersClientSessionKeepAlive:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersClientSessionKeepAlive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientSessionKeepAliveHeartbeatFrequency",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersClientSessionKeepAliveHeartbeatFrequency:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersClientSessionKeepAliveHeartbeatFrequency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f8ddda082624b8818b76e9d92661f155afe93a3735e001b5e3db84b4d5d27cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea1064aec995fa1742b8fcbbc04379a7ea01c97a485c1f6cb7558a0c715f9fb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cef09786814050519a1cde99abfc3a322c4926c7ec1e7d2a927e4254e7b284)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5115c5cfdf00db9a34e439eb9a108869aefeaf3caa2d2de770111f0117bbbf4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48f6fd248b953f878ffa79803dbd517942f18005f15389f5e84fbb5e24f1461f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1113dc76bd31adc0be2aa199a6713d9c8e9ae4350058babe56219f9ed176dacf)
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
    ) -> typing.Optional[ServiceUserParametersClientSessionKeepAliveHeartbeatFrequency]:
        return typing.cast(typing.Optional[ServiceUserParametersClientSessionKeepAliveHeartbeatFrequency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersClientSessionKeepAliveHeartbeatFrequency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996d33ae34ba672c4d9aca3661d2dfe68beb202c0a2b01994fd5074bed06dfc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientSessionKeepAliveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientSessionKeepAliveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f45c2db773e00052272364c160bc77b3ed0f979cc016a5d8a9c3da80032b3fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersClientSessionKeepAliveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eafb85c41f39feb6b69852b88d1f9b3ee77f5b4da707a791f0289c62718c53d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersClientSessionKeepAliveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46eb7cada5debf2e552b1114613e2c7452eb2e797e2598991f85993f3360f553)
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
            type_hints = typing.get_type_hints(_typecheckingstub__823382ee156edd2556c81df6b956032bcd804bcefeed97d6b283dda8d26ca91e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__071a28df653b90a2c804111919697fb28ef9dc16aed885d3d006f0ba7eb99c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientSessionKeepAliveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientSessionKeepAliveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__107aac5dc3335eb6d5227f8bec315546674323abd31c5b4c0a9b279ac03628db)
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
    ) -> typing.Optional[ServiceUserParametersClientSessionKeepAlive]:
        return typing.cast(typing.Optional[ServiceUserParametersClientSessionKeepAlive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersClientSessionKeepAlive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d352a608887e098243839c14212abbe879616bc2fc2ff4eed861bd1b2cb156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientTimestampTypeMapping",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersClientTimestampTypeMapping:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersClientTimestampTypeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersClientTimestampTypeMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientTimestampTypeMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba9924df1fa21f7849659a13f002daf38645f20db6eefa1dc8ec234947d7fabc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersClientTimestampTypeMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5551c95f091c1d09dc8a2365d7fa9af9cd9bf9066bdfa0649bdd3b4f5a5605f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersClientTimestampTypeMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a7a426b510ad21847dcf712e30cd80ac66f0307a4163caa567b2cfba26c248)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f1c3b9b152bf66656cdefa9778670891cab9a939dafefe0331cacdfb77ae3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14097184822a4ac7cedd18ae2898cb86b7e297ad4dbedd41d5c86dc4d292b08e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersClientTimestampTypeMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersClientTimestampTypeMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37e9e733f021f06e088f992afdc827ed6c4a757500ef284ffcf73c0387763157)
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
    ) -> typing.Optional[ServiceUserParametersClientTimestampTypeMapping]:
        return typing.cast(typing.Optional[ServiceUserParametersClientTimestampTypeMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersClientTimestampTypeMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6593586f33cbb1f33ab3d004ca1efd85053dec2abd3c5c8a636751df4bc2a632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersDateInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersDateInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersDateInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersDateInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersDateInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4e67fb5d2689ce304022f2d133cdea81ce676ea7a9ce1402d937f430c239406)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersDateInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552cb2574a4ed645f565849c065198aae9ee1a27a45c48574ab4d94b6a7479e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersDateInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2710b620c4bcb43889522e101f35ece7ca1e33eb1a4ed7c036d708c1a1530c87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f903485395dff983c5c7454f60b5c922d5d2b65801514689540699f121c312c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__653291e4d330b7bfd520d5418e26a471e4c38c194415bc107bf8082731c3e6a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersDateInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersDateInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb25b60a2e380159f815f06ef6f43d1f550ab22e930db07041b5b7b88075135a)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersDateInputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersDateInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersDateInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4520d9133fdf66156b262233f93a619b3a5fcc65450f563f6707d046ce50003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersDateOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersDateOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersDateOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersDateOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersDateOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4359f55743b57a19dca293cca9047cabce24c74dc836c687937fd33cb4052ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersDateOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163eaeb6638bf2973cf12cbf70326703ecf8bacab150c92b506569efd0c1c70b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersDateOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701ec46add86f60beb1cd9881c2148efdeeeafb990ca2c843c37a26204021189)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb0b6b4b352f798622d96f1a7e5499ba1f434f0da86f2e610e47ba4944e2e1b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bb3db3e7ff6f225b085796476dd5b8813a7d8447e780d8774febe6b9f63af25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersDateOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersDateOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__398c895f9d3308ad36ddff3b9e344e308b079e8afae6d3cdd0921989bf436f80)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersDateOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersDateOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersDateOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e3851433402af65324886e843ee1d8380cff4dbf61f272da3cfebc36ccd5fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersEnableUnloadPhysicalTypeOptimization",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersEnableUnloadPhysicalTypeOptimization:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersEnableUnloadPhysicalTypeOptimization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersEnableUnloadPhysicalTypeOptimizationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersEnableUnloadPhysicalTypeOptimizationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efdfd564c157b6991012ec25f44741965d667197604fc211440096a22eeadaaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462662024d76937f9567266262a246c7a3dc5212da0b27ecf947e3b295623bdd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570916356ed74a88fbc0f8f92c1079a3ac789c11a4c7fc5fd87828275c700501)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18dfaefc8152e994b0283d59da772aab70f0fe99f600b338ef600fbac9683656)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3760c4f49bb157603f16f7a4ac2493c946be52b51e08214222dcf09a6c581a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fe4789b3cae1062953ad1cebdfa12d8a9cf777a7786517ba721541748c5fe97)
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
    ) -> typing.Optional[ServiceUserParametersEnableUnloadPhysicalTypeOptimization]:
        return typing.cast(typing.Optional[ServiceUserParametersEnableUnloadPhysicalTypeOptimization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersEnableUnloadPhysicalTypeOptimization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14b7c63680dcbefe9202ebd0fc9d802963044a76143c986f35234196a60a6c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersEnableUnredactedQuerySyntaxError",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersEnableUnredactedQuerySyntaxError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersEnableUnredactedQuerySyntaxError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersEnableUnredactedQuerySyntaxErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersEnableUnredactedQuerySyntaxErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3c6132c4f8cf4d46af0cfeac6ccb0c48be7ce19c24ac41dc27ef17185307ff9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e23881ae1a34bbc71dcd22e2f541136ed94ff1e4e13d1b7bb1a5ce74501c51)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c99666b882a4ef570cdf6f842ebf952c4d777166c342e76ace6a9763beecea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c52ca2be990abfcef65d80f348a3ec48289305dcd39275e1cc5ca668192ee37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d75527b42b5041c99f46068dd60157afbff81bd7be34af68a2ef2cccd0b3405a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__353fabb9532617d2c77a436130b417c03aa4211fa1d6fb3aefbe59799604ef47)
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
    ) -> typing.Optional[ServiceUserParametersEnableUnredactedQuerySyntaxError]:
        return typing.cast(typing.Optional[ServiceUserParametersEnableUnredactedQuerySyntaxError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersEnableUnredactedQuerySyntaxError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0090c601cbb85e6e1faa4319b6ae4570e37cd69222c56317a8ed30830efbe7e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersErrorOnNondeterministicMerge",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersErrorOnNondeterministicMerge:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersErrorOnNondeterministicMerge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersErrorOnNondeterministicMergeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersErrorOnNondeterministicMergeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0bde630e40635f1e27e5cb5fcbaf6b28e2fe7e616a2aea2a5542753b2e2830f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersErrorOnNondeterministicMergeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9725d6bb4fc989779aede4127301b60d2988ebb23383d2ca4c34d65ae4b4bc85)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersErrorOnNondeterministicMergeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0efba96a44980bcce1a47a16910cfc3137bbdba1db022d27e93e8e6919857351)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c55bf231f49fd1a875d6400ae794cf63d271220edf5dc6fb72028f2fd2fc352f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a12d6db11e0617f45066b2b39d28f2a38cd70cde83762e7d0702a78b48b4671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersErrorOnNondeterministicMergeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersErrorOnNondeterministicMergeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba671ec801fd81ab57dbc069e8365d9bbcbada942a7a6be5e33d0e77643aa2ef)
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
    ) -> typing.Optional[ServiceUserParametersErrorOnNondeterministicMerge]:
        return typing.cast(typing.Optional[ServiceUserParametersErrorOnNondeterministicMerge], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersErrorOnNondeterministicMerge],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5aaf6300bee71968097375120cd47fa1f4864f2c31a355d5f8157bf2eabb5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersErrorOnNondeterministicUpdate",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersErrorOnNondeterministicUpdate:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersErrorOnNondeterministicUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersErrorOnNondeterministicUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersErrorOnNondeterministicUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ddda90864f9aa836807ebf89b4c50db432b0e815ff80aa991226237a1065153)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersErrorOnNondeterministicUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de43f8f97ceab44a7826076f43f609b6f10679f5f01c93020acfe56f9144b2bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersErrorOnNondeterministicUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a6c991715fd2abc0f977c1ebf1796bd9378ab5641abae0f10d925e64db414d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__815feb3b720aa3ecaac1d342cf8cee1021cd81354541e2770aecc3da6c7dcb73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e8329b860c26f9a78bddaeb16390971aa8ccff1720c5af94a7c97531678709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersErrorOnNondeterministicUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersErrorOnNondeterministicUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f40c192fa3af3a7af50fbb8c93c780496acd791aaedb7c437760b5a6686f052c)
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
    ) -> typing.Optional[ServiceUserParametersErrorOnNondeterministicUpdate]:
        return typing.cast(typing.Optional[ServiceUserParametersErrorOnNondeterministicUpdate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersErrorOnNondeterministicUpdate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0dcf918ca2ceeca84f1a34835cf823f20fe3053d973cbbc5a5d6cf4307d3714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersGeographyOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersGeographyOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersGeographyOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersGeographyOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersGeographyOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d34fee83c66ae5408b7de8f479a94eeb37c51443bfe262c79166eade2f825878)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersGeographyOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f3849552e0e96f348cd2948906841b17774bcb27dd7e5ef8dc524773afa6f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersGeographyOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ab21c90751f1c2e9c0c62b24771d66145039ff14824cd821575c2f905ab146)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b75edeb14da4ca63a378b6262bb00bd85cf8ec458ba73b8b5b6c5a82e9c30d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__028e91e0c45d811ceab873a7b1754cd45957f2050d014d67f44c33c303fa0d3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersGeographyOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersGeographyOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7a9ef8d8e15fe7c998910525968234df7a957c2871e5e6dc52278cb24bd2612)
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
    ) -> typing.Optional[ServiceUserParametersGeographyOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersGeographyOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersGeographyOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0ca77b7ce52f0739883c18c51f1e1752c22b60a8ca54bd3c8565dc7c8e9ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersGeometryOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersGeometryOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersGeometryOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersGeometryOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersGeometryOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6af96fdef0fb67e063ae1846df08f74b20a61c432a1836fb5df8acbdc796cd9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersGeometryOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332cc7bc855b63532fc7af7c5840fd1acb47ee3bf29957ef9dd914fdd7c86787)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersGeometryOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bca476ad62217b7345aebc5e98858f6c24a46c7ef89026e0705dce98409577b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68fb943955b538758b8ee5130f0606c6b454f25c8493e027da84483ef0ede60a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50fb7394512d97eb023a5d8ad9a1c99ce42c4b98a6cc8e3dc9487da16a805c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersGeometryOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersGeometryOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bab143c46f1bc86394a5e5dac5a0ba19861987c9879b9c8b15583762ecd02e1)
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
    ) -> typing.Optional[ServiceUserParametersGeometryOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersGeometryOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersGeometryOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8758125ba267c0368f4a9b0aa48268ac7b9f2d6eb5ae688bb95aa93b7ce65089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcTreatDecimalAsInt",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersJdbcTreatDecimalAsInt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersJdbcTreatDecimalAsInt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersJdbcTreatDecimalAsIntList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcTreatDecimalAsIntList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acbd0ebfb1b1e143307a8c7fa86ddb950e46bd0c5c0446b87d5d763b6d003f6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersJdbcTreatDecimalAsIntOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8c8eec0cc8dc79f6ef52a8156380534d6ac3695bcc819bdb0f02382b959aea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersJdbcTreatDecimalAsIntOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa0acc48643e6a02272603599b839008a48d4b72d414320e0b98eb4601f3f26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87cc8bc6ac2e6be0e06791eed281a9f532d66a75bbb7346a78631aab7a3ac831)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe2cd08afa5e2e06bb00cd06ead1c1073c8fa4924ec3b6629a722a54253f61fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersJdbcTreatDecimalAsIntOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcTreatDecimalAsIntOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c531c4b6ee9888518d80512a827c00338454bedf7fb3d2c34404345d8238da00)
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
    ) -> typing.Optional[ServiceUserParametersJdbcTreatDecimalAsInt]:
        return typing.cast(typing.Optional[ServiceUserParametersJdbcTreatDecimalAsInt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersJdbcTreatDecimalAsInt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b29e8d3cd4f9366e1cf9048de7686e06a390f72033dc7747393cddfa80393d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcTreatTimestampNtzAsUtc",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersJdbcTreatTimestampNtzAsUtc:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersJdbcTreatTimestampNtzAsUtc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersJdbcTreatTimestampNtzAsUtcList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcTreatTimestampNtzAsUtcList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9691a7eb3f49e7750ec3f0d855a36e82827c9541c3ea7230b2aa3832a3ff6ea6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4792c0950aadf63ea18feb2f5c236e17012598d885da9e9f70272474edb776d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da6395e9d24a07e974419439f6eb78839c6e2f320b68c06399c875fe9f469ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b77cb2df568bdb3a5f6b774d9651631bd91cef6810668cabb69f6aa72381499c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38d7f221323d731b0fc06bf47f81a7d8fc90469bedb1cdc24e8aad3f49d9ef05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22364a902d1bcb65edfd0cb675b3f39036c7e53deb1b6a5753cc7034566cd24b)
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
    ) -> typing.Optional[ServiceUserParametersJdbcTreatTimestampNtzAsUtc]:
        return typing.cast(typing.Optional[ServiceUserParametersJdbcTreatTimestampNtzAsUtc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersJdbcTreatTimestampNtzAsUtc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e1ef7bb60b2bb760c15c8f312537168c7d57c75d793d0b617221f294193165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcUseSessionTimezone",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersJdbcUseSessionTimezone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersJdbcUseSessionTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersJdbcUseSessionTimezoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcUseSessionTimezoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__482e89fbf6fafcd7586b5fbcfc6d01b72aa29923cdd30df6639a1be0b9ab2803)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersJdbcUseSessionTimezoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a572a0eacd0c6b721827ea67985562be98f02f81020e297ec3c3effbeacec35)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersJdbcUseSessionTimezoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2f10bb9f7639aa36b1685ca757c00812094d86d47d2fc4048f0ea677b2f77f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__186342f99a23d21261024085ef03d3d321f77aaec5fd4c8f19263be046b910f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__037c9590cb6c90d3e599f6dcdb00e466efee733a45ba1edbbd40987a64554cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersJdbcUseSessionTimezoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJdbcUseSessionTimezoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e893156679a1a7f17ae218f64b6989d4b95513b44aaee19c7269abd0e2b7749)
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
    ) -> typing.Optional[ServiceUserParametersJdbcUseSessionTimezone]:
        return typing.cast(typing.Optional[ServiceUserParametersJdbcUseSessionTimezone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersJdbcUseSessionTimezone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45ef8a95b5311fbbb9bce391c74442bce09dbe6297353d7d2bf04f4f9164d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJsonIndent",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersJsonIndent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersJsonIndent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersJsonIndentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJsonIndentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__228e35717cafe2a83997e8b7256ba9a89ae9f5213f2058d41b250bdc53820d37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersJsonIndentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61344ba55db207dfff1c280528ca58a8b56ea688edc5f9aeeaa18b34c6ccdee4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersJsonIndentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd327eb7688ebc2ca108a2472681fd8fe641ad7be1a1ae8acb0835088a349703)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e84988d7fd4b2baebac3dca09fa9a4fa4bd548cbac06ebcbba5c0c0775e7ac1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d2d5e7638b2bcc940e9961cbbb096514e0fd63295d3b3ebf354e11ab492b2d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersJsonIndentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersJsonIndentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17f3eca147e02b4e7dc710eb7c95643127e16af68b795513c207103ab9c80325)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersJsonIndent]:
        return typing.cast(typing.Optional[ServiceUserParametersJsonIndent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersJsonIndent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cabba39ba061167125e68a5e9d725b974c66a0736a4de5fb6188f5ccfa47735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d709f5f30d9d5e0b1135e77c413c79fb34550438134ee3359ac9be1c385c2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceUserParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8214ba428d83fa0a48ecbd8095e65e0df991fb0242b84b1d0aa28e04b52b21bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a224af9297cb627529143a50bb5cd84c752b3aa3126e78b98050a2b899830d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6dbe73a54f05c1b77e5a38bb656c46d4b6704f7a564c3b7c5753707e82c300f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28b0fec826b7d8adeeac10e99d79ccb1bfa62cd84e81f5bbd39153b095d5f1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersLockTimeout",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersLockTimeout:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersLockTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersLockTimeoutList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersLockTimeoutList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d4a2bbe3f672fc160234aec4a009782e285fdd4d72eb2896d52a371440b2cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersLockTimeoutOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95c6e298ab9b435ad55eb40fceb82ade5bcea12581135503c4dff4900eddb03)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersLockTimeoutOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105877f358fbb8130e6fb2515bd65cc0bf0fb7520d28e2d387e3b33b2bf04e6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffd643c0637d44dd687d0cc792e26af34679969609cf6d80a68204e18f4c3fe9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a56e873798e815d8a40974414bca1b96e0a07fc965fd81d3d04af5134dbb9f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersLockTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersLockTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed815f97ec92dc65f85622c37560a67698e2ac0d1e8af1675b17b09dc89aefff)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersLockTimeout]:
        return typing.cast(typing.Optional[ServiceUserParametersLockTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersLockTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc6111865127445b09a4fc6e499e70e86ed3c931c062bf8356cdc6e7b036d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3cdb888e9c1d43f169d18ede157eeb7e5611d7eec87892f35bd3aa5efaad546)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceUserParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1029abfa4eae0e8a5dd22569abb5df39b4d5280ed9e6677b5786c25d1a73f73c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5adc37049a748290143b61c220ee3eddcae1bef6b00001957bb514ceb6497f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2291b3490891e5b9931dcbb8fb3c33960f92d2a4cc2095b90116a007c188305)
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
            type_hints = typing.get_type_hints(_typecheckingstub__424d17076210d9ab1793c18f6d38e53bd4099dd3f595d895ad4240d4cd7759f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__630cb629185959d055ace4997e9ddaf722cc3706b0c39894f56d5b7de7329853)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersLogLevel]:
        return typing.cast(typing.Optional[ServiceUserParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersLogLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b2d4342ed1dfa5dba69f3ce781c1fcb86fb8f0564b7928df3018afa23d93d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersMultiStatementCount",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersMultiStatementCount:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersMultiStatementCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersMultiStatementCountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersMultiStatementCountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1192186428919511d75d8a06169a87fdf48d459cec20dec8ecb8dcfb66afd6ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersMultiStatementCountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855467a6e4aa2bfdc5eee527c337a060639388963da92779515e3b103669b03f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersMultiStatementCountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441464f02c643ba0c214b393dd768c5b1be2e0d4ef2059ffc79f85ece192600b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f5822596ab5c5a43d7552b66042ce2004083bb22ecff693654e24071dbd7002)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3206fd4a6d850e08d0bfe4e03754e37255bc2f24272d021ef65a848c0ae6d43f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersMultiStatementCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersMultiStatementCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b6a2ab0cffc008588a2dad136a45f04bac954c70f62fa74682e9914f628b4d1)
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
    ) -> typing.Optional[ServiceUserParametersMultiStatementCount]:
        return typing.cast(typing.Optional[ServiceUserParametersMultiStatementCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersMultiStatementCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29b8976dd3078e8c402aed8fcb98f357e6e79d677da95688783a0229e7526c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersNetworkPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersNetworkPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersNetworkPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersNetworkPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersNetworkPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c45bbd3ccab6714677510a254760f536d3d2b2035d337f120f8c9a01b02f8dfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersNetworkPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95de8c38f3df9376f3901aaabcb3a073c9e000f221dde08216c25e35aa35fde)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersNetworkPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2789b72b46410f6ae071b6f20b6480f8cc4f8797288fe8c7c61f3b1fc7136ed1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e4efb7f893e5623cbce4157be0a6e6513cc97cac05f6f2de65fc18caa331b9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e337c572b214e0fe5523e69a3edb494adf92fce289431d5ada69ada2806419b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersNetworkPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersNetworkPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a336bd72f779714c0ebd9a9427acbc5b965e858dfcc5ea64fa51b5af6a2ea95e)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersNetworkPolicy]:
        return typing.cast(typing.Optional[ServiceUserParametersNetworkPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersNetworkPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ed9c2937c814c28cafd7d772fed2bd525ee89e9d81b1d77a2d7bd416762b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersNoorderSequenceAsDefault",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersNoorderSequenceAsDefault:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersNoorderSequenceAsDefault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersNoorderSequenceAsDefaultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersNoorderSequenceAsDefaultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__960c9bac9f8c5332b2231aad2379599b594800bad5af9af98e43e0712cb8d5d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersNoorderSequenceAsDefaultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a610f9d34b0ba13c66b1e69f482b69442494568a817d9306985f0572fc5c44)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersNoorderSequenceAsDefaultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588f822162878548aae1bbd4a039be6aa2d1adb91e9258e9548482d3edc9e6dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be7e40edee321b88b427850c7c52804c33766728e73446d4fdc305f08d55baa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b188970b8fe5859018d26e2d9895c061f69c1ef6ee27fc0434a2c47dc760a33b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersNoorderSequenceAsDefaultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersNoorderSequenceAsDefaultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__992c0ed72ad2c1f8bc7751370e73b59c45f6ca80dc6672837384d93df8594fdf)
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
    ) -> typing.Optional[ServiceUserParametersNoorderSequenceAsDefault]:
        return typing.cast(typing.Optional[ServiceUserParametersNoorderSequenceAsDefault], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersNoorderSequenceAsDefault],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e414f41ead74efe6d5c8a8dd9a3d80424dab6741558662622c8b061712ff3ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersOdbcTreatDecimalAsInt",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersOdbcTreatDecimalAsInt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersOdbcTreatDecimalAsInt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersOdbcTreatDecimalAsIntList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersOdbcTreatDecimalAsIntList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a41285ac977a24590662d2b29f51e88c5c549db921bad825df300a277d82e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersOdbcTreatDecimalAsIntOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cb73e1fd6585eee17a4171e385fb3f0c5d4ce72975f0ac00f31926ed4d9a9ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersOdbcTreatDecimalAsIntOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfde877e3671d6a1fcb962a3b7890665d296cc59273c2b58b33c2eb72e944864)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4d02b2a1f0495635b1842bf69684b9c2d4f6af3aa2470ca95fc701ead3f1200)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c590f7d525f2a5a977a74af52368cde632a0ab61b7676d028eb53ef7e5ced76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersOdbcTreatDecimalAsIntOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersOdbcTreatDecimalAsIntOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1c1a2b82828065fc9b180a563db3823f460c43e9ef25a0233ebb206286a2e02)
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
    ) -> typing.Optional[ServiceUserParametersOdbcTreatDecimalAsInt]:
        return typing.cast(typing.Optional[ServiceUserParametersOdbcTreatDecimalAsInt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersOdbcTreatDecimalAsInt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57ec6af373624b1d5bf8f03a29baa4be36f04de02e813a6978949e01b82e765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__186378c31f754ab32ca8e0680b8bc0ec96601fe50f766318e0667f1744fb1e4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="abortDetachedQuery")
    def abort_detached_query(self) -> ServiceUserParametersAbortDetachedQueryList:
        return typing.cast(ServiceUserParametersAbortDetachedQueryList, jsii.get(self, "abortDetachedQuery"))

    @builtins.property
    @jsii.member(jsii_name="autocommit")
    def autocommit(self) -> ServiceUserParametersAutocommitList:
        return typing.cast(ServiceUserParametersAutocommitList, jsii.get(self, "autocommit"))

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> ServiceUserParametersBinaryInputFormatList:
        return typing.cast(ServiceUserParametersBinaryInputFormatList, jsii.get(self, "binaryInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> ServiceUserParametersBinaryOutputFormatList:
        return typing.cast(ServiceUserParametersBinaryOutputFormatList, jsii.get(self, "binaryOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> ServiceUserParametersClientMemoryLimitList:
        return typing.cast(ServiceUserParametersClientMemoryLimitList, jsii.get(self, "clientMemoryLimit"))

    @builtins.property
    @jsii.member(jsii_name="clientMetadataRequestUseConnectionCtx")
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> ServiceUserParametersClientMetadataRequestUseConnectionCtxList:
        return typing.cast(ServiceUserParametersClientMetadataRequestUseConnectionCtxList, jsii.get(self, "clientMetadataRequestUseConnectionCtx"))

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(self) -> ServiceUserParametersClientPrefetchThreadsList:
        return typing.cast(ServiceUserParametersClientPrefetchThreadsList, jsii.get(self, "clientPrefetchThreads"))

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(
        self,
    ) -> ServiceUserParametersClientResultChunkSizeList:
        return typing.cast(ServiceUserParametersClientResultChunkSizeList, jsii.get(self, "clientResultChunkSize"))

    @builtins.property
    @jsii.member(jsii_name="clientResultColumnCaseInsensitive")
    def client_result_column_case_insensitive(
        self,
    ) -> ServiceUserParametersClientResultColumnCaseInsensitiveList:
        return typing.cast(ServiceUserParametersClientResultColumnCaseInsensitiveList, jsii.get(self, "clientResultColumnCaseInsensitive"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAlive")
    def client_session_keep_alive(
        self,
    ) -> ServiceUserParametersClientSessionKeepAliveList:
        return typing.cast(ServiceUserParametersClientSessionKeepAliveList, jsii.get(self, "clientSessionKeepAlive"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList:
        return typing.cast(ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(
        self,
    ) -> ServiceUserParametersClientTimestampTypeMappingList:
        return typing.cast(ServiceUserParametersClientTimestampTypeMappingList, jsii.get(self, "clientTimestampTypeMapping"))

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> ServiceUserParametersDateInputFormatList:
        return typing.cast(ServiceUserParametersDateInputFormatList, jsii.get(self, "dateInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> ServiceUserParametersDateOutputFormatList:
        return typing.cast(ServiceUserParametersDateOutputFormatList, jsii.get(self, "dateOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="enableUnloadPhysicalTypeOptimization")
    def enable_unload_physical_type_optimization(
        self,
    ) -> ServiceUserParametersEnableUnloadPhysicalTypeOptimizationList:
        return typing.cast(ServiceUserParametersEnableUnloadPhysicalTypeOptimizationList, jsii.get(self, "enableUnloadPhysicalTypeOptimization"))

    @builtins.property
    @jsii.member(jsii_name="enableUnredactedQuerySyntaxError")
    def enable_unredacted_query_syntax_error(
        self,
    ) -> ServiceUserParametersEnableUnredactedQuerySyntaxErrorList:
        return typing.cast(ServiceUserParametersEnableUnredactedQuerySyntaxErrorList, jsii.get(self, "enableUnredactedQuerySyntaxError"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicMerge")
    def error_on_nondeterministic_merge(
        self,
    ) -> ServiceUserParametersErrorOnNondeterministicMergeList:
        return typing.cast(ServiceUserParametersErrorOnNondeterministicMergeList, jsii.get(self, "errorOnNondeterministicMerge"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicUpdate")
    def error_on_nondeterministic_update(
        self,
    ) -> ServiceUserParametersErrorOnNondeterministicUpdateList:
        return typing.cast(ServiceUserParametersErrorOnNondeterministicUpdateList, jsii.get(self, "errorOnNondeterministicUpdate"))

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(self) -> ServiceUserParametersGeographyOutputFormatList:
        return typing.cast(ServiceUserParametersGeographyOutputFormatList, jsii.get(self, "geographyOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(self) -> ServiceUserParametersGeometryOutputFormatList:
        return typing.cast(ServiceUserParametersGeometryOutputFormatList, jsii.get(self, "geometryOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatDecimalAsInt")
    def jdbc_treat_decimal_as_int(
        self,
    ) -> ServiceUserParametersJdbcTreatDecimalAsIntList:
        return typing.cast(ServiceUserParametersJdbcTreatDecimalAsIntList, jsii.get(self, "jdbcTreatDecimalAsInt"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatTimestampNtzAsUtc")
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> ServiceUserParametersJdbcTreatTimestampNtzAsUtcList:
        return typing.cast(ServiceUserParametersJdbcTreatTimestampNtzAsUtcList, jsii.get(self, "jdbcTreatTimestampNtzAsUtc"))

    @builtins.property
    @jsii.member(jsii_name="jdbcUseSessionTimezone")
    def jdbc_use_session_timezone(
        self,
    ) -> ServiceUserParametersJdbcUseSessionTimezoneList:
        return typing.cast(ServiceUserParametersJdbcUseSessionTimezoneList, jsii.get(self, "jdbcUseSessionTimezone"))

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> ServiceUserParametersJsonIndentList:
        return typing.cast(ServiceUserParametersJsonIndentList, jsii.get(self, "jsonIndent"))

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> ServiceUserParametersLockTimeoutList:
        return typing.cast(ServiceUserParametersLockTimeoutList, jsii.get(self, "lockTimeout"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> ServiceUserParametersLogLevelList:
        return typing.cast(ServiceUserParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(self) -> ServiceUserParametersMultiStatementCountList:
        return typing.cast(ServiceUserParametersMultiStatementCountList, jsii.get(self, "multiStatementCount"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> ServiceUserParametersNetworkPolicyList:
        return typing.cast(ServiceUserParametersNetworkPolicyList, jsii.get(self, "networkPolicy"))

    @builtins.property
    @jsii.member(jsii_name="noorderSequenceAsDefault")
    def noorder_sequence_as_default(
        self,
    ) -> ServiceUserParametersNoorderSequenceAsDefaultList:
        return typing.cast(ServiceUserParametersNoorderSequenceAsDefaultList, jsii.get(self, "noorderSequenceAsDefault"))

    @builtins.property
    @jsii.member(jsii_name="odbcTreatDecimalAsInt")
    def odbc_treat_decimal_as_int(
        self,
    ) -> ServiceUserParametersOdbcTreatDecimalAsIntList:
        return typing.cast(ServiceUserParametersOdbcTreatDecimalAsIntList, jsii.get(self, "odbcTreatDecimalAsInt"))

    @builtins.property
    @jsii.member(jsii_name="preventUnloadToInternalStages")
    def prevent_unload_to_internal_stages(
        self,
    ) -> "ServiceUserParametersPreventUnloadToInternalStagesList":
        return typing.cast("ServiceUserParametersPreventUnloadToInternalStagesList", jsii.get(self, "preventUnloadToInternalStages"))

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> "ServiceUserParametersQueryTagList":
        return typing.cast("ServiceUserParametersQueryTagList", jsii.get(self, "queryTag"))

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCase")
    def quoted_identifiers_ignore_case(
        self,
    ) -> "ServiceUserParametersQuotedIdentifiersIgnoreCaseList":
        return typing.cast("ServiceUserParametersQuotedIdentifiersIgnoreCaseList", jsii.get(self, "quotedIdentifiersIgnoreCase"))

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> "ServiceUserParametersRowsPerResultsetList":
        return typing.cast("ServiceUserParametersRowsPerResultsetList", jsii.get(self, "rowsPerResultset"))

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(self) -> "ServiceUserParametersS3StageVpceDnsNameList":
        return typing.cast("ServiceUserParametersS3StageVpceDnsNameList", jsii.get(self, "s3StageVpceDnsName"))

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> "ServiceUserParametersSearchPathList":
        return typing.cast("ServiceUserParametersSearchPathList", jsii.get(self, "searchPath"))

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumer")
    def simulated_data_sharing_consumer(
        self,
    ) -> "ServiceUserParametersSimulatedDataSharingConsumerList":
        return typing.cast("ServiceUserParametersSimulatedDataSharingConsumerList", jsii.get(self, "simulatedDataSharingConsumer"))

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(
        self,
    ) -> "ServiceUserParametersStatementQueuedTimeoutInSecondsList":
        return typing.cast("ServiceUserParametersStatementQueuedTimeoutInSecondsList", jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(
        self,
    ) -> "ServiceUserParametersStatementTimeoutInSecondsList":
        return typing.cast("ServiceUserParametersStatementTimeoutInSecondsList", jsii.get(self, "statementTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="strictJsonOutput")
    def strict_json_output(self) -> "ServiceUserParametersStrictJsonOutputList":
        return typing.cast("ServiceUserParametersStrictJsonOutputList", jsii.get(self, "strictJsonOutput"))

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> "ServiceUserParametersTimeInputFormatList":
        return typing.cast("ServiceUserParametersTimeInputFormatList", jsii.get(self, "timeInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> "ServiceUserParametersTimeOutputFormatList":
        return typing.cast("ServiceUserParametersTimeOutputFormatList", jsii.get(self, "timeOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampDayIsAlways24H")
    def timestamp_day_is_always24_h(
        self,
    ) -> "ServiceUserParametersTimestampDayIsAlways24HList":
        return typing.cast("ServiceUserParametersTimestampDayIsAlways24HList", jsii.get(self, "timestampDayIsAlways24H"))

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(self) -> "ServiceUserParametersTimestampInputFormatList":
        return typing.cast("ServiceUserParametersTimestampInputFormatList", jsii.get(self, "timestampInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(
        self,
    ) -> "ServiceUserParametersTimestampLtzOutputFormatList":
        return typing.cast("ServiceUserParametersTimestampLtzOutputFormatList", jsii.get(self, "timestampLtzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(
        self,
    ) -> "ServiceUserParametersTimestampNtzOutputFormatList":
        return typing.cast("ServiceUserParametersTimestampNtzOutputFormatList", jsii.get(self, "timestampNtzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(
        self,
    ) -> "ServiceUserParametersTimestampOutputFormatList":
        return typing.cast("ServiceUserParametersTimestampOutputFormatList", jsii.get(self, "timestampOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(self) -> "ServiceUserParametersTimestampTypeMappingList":
        return typing.cast("ServiceUserParametersTimestampTypeMappingList", jsii.get(self, "timestampTypeMapping"))

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(
        self,
    ) -> "ServiceUserParametersTimestampTzOutputFormatList":
        return typing.cast("ServiceUserParametersTimestampTzOutputFormatList", jsii.get(self, "timestampTzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> "ServiceUserParametersTimezoneList":
        return typing.cast("ServiceUserParametersTimezoneList", jsii.get(self, "timezone"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "ServiceUserParametersTraceLevelList":
        return typing.cast("ServiceUserParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="transactionAbortOnError")
    def transaction_abort_on_error(
        self,
    ) -> "ServiceUserParametersTransactionAbortOnErrorList":
        return typing.cast("ServiceUserParametersTransactionAbortOnErrorList", jsii.get(self, "transactionAbortOnError"))

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(
        self,
    ) -> "ServiceUserParametersTransactionDefaultIsolationLevelList":
        return typing.cast("ServiceUserParametersTransactionDefaultIsolationLevelList", jsii.get(self, "transactionDefaultIsolationLevel"))

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(
        self,
    ) -> "ServiceUserParametersTwoDigitCenturyStartList":
        return typing.cast("ServiceUserParametersTwoDigitCenturyStartList", jsii.get(self, "twoDigitCenturyStart"))

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(self) -> "ServiceUserParametersUnsupportedDdlActionList":
        return typing.cast("ServiceUserParametersUnsupportedDdlActionList", jsii.get(self, "unsupportedDdlAction"))

    @builtins.property
    @jsii.member(jsii_name="useCachedResult")
    def use_cached_result(self) -> "ServiceUserParametersUseCachedResultList":
        return typing.cast("ServiceUserParametersUseCachedResultList", jsii.get(self, "useCachedResult"))

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> "ServiceUserParametersWeekOfYearPolicyList":
        return typing.cast("ServiceUserParametersWeekOfYearPolicyList", jsii.get(self, "weekOfYearPolicy"))

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> "ServiceUserParametersWeekStartList":
        return typing.cast("ServiceUserParametersWeekStartList", jsii.get(self, "weekStart"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceUserParameters]:
        return typing.cast(typing.Optional[ServiceUserParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceUserParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddbcf177e566220c7439925eab3af5d57550e4c3826feb005670089c2599eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersPreventUnloadToInternalStages",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersPreventUnloadToInternalStages:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersPreventUnloadToInternalStages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersPreventUnloadToInternalStagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersPreventUnloadToInternalStagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa3b060f4e8c713982f050d75ccce32c143a04f24690bbe0b09897d75b947ad9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersPreventUnloadToInternalStagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e59cff2722abf775c13bc475772c6eb52b5903341ca89762cacc43899c556c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersPreventUnloadToInternalStagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d120448fef62a554ea19b5d3b56289bc5da153979cd7142c6308b692a8537ba6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fca8f564f3866d07822e61aaac10081448efd3a9f8eef94b3096d956b2f6bffd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9351d39fa82a7c0ea2b087750390b76db8bfcf78bc4ea5d0a59ef81d07913a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersPreventUnloadToInternalStagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersPreventUnloadToInternalStagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__577effacfb94548e3f2139ce1910e58c4a653e6180cfba7ce009738d9d834ec0)
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
    ) -> typing.Optional[ServiceUserParametersPreventUnloadToInternalStages]:
        return typing.cast(typing.Optional[ServiceUserParametersPreventUnloadToInternalStages], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersPreventUnloadToInternalStages],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8001eedd03f73be4691f7acd33c02be557a2a90cfbebd51d460d185c25217965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersQueryTag",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersQueryTag:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersQueryTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersQueryTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersQueryTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b210069dc5264942291cf2bd3fc9524cf7f2fb6aec044d0cac997331e0d4a6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceUserParametersQueryTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0fda6da73407d822622ace79c08e47adf5ef8ba95e8f946cedd56a5a8a87e86)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersQueryTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1060a88004a065a30283b20e2041fa26f5eb626e9a08f150b298054a20b2a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbab72bb5dba2f5f24fb1596b1d8b2975052b9fb6d030b0fc9a9ba89ce1e4e87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5098acc0bb6816a4a53835ced7dfd07dc7b907fdf07aa105f386e9cdc2c22763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersQueryTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersQueryTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ec34273344c2b30bd6b2dcdd6175884ec9e3fd7f87ade7ed3a2e630b1f8fb60)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersQueryTag]:
        return typing.cast(typing.Optional[ServiceUserParametersQueryTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersQueryTag],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ce78e687b220fd5441d53bf34e58a6495d6dc2a886a24024538abca462e792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersQuotedIdentifiersIgnoreCase",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersQuotedIdentifiersIgnoreCase:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersQuotedIdentifiersIgnoreCase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersQuotedIdentifiersIgnoreCaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersQuotedIdentifiersIgnoreCaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af4d960d9e15c0461a94f0e755ac400bb530bcd03519f098d1442614f3e95be9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d0628eb6cb92c32b7c992e97215cdededa8cc290fc584febf803067012cf60)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2148194eb61a4e4f28287c05923a090f590e7fa402f6eef8aeae6e4a72f3e8ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3650b43bdf6f3a501b9236f5e50cecf4ef7460ae972add998c78c30cad6a67f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19b0a283ec3c11487aaf4f0d7088d14d1a1972055967e73b9d49f2688284c853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc21a72d69dd328a7c4887307f5301643449e86e9ae4eca9c6c5c11e8e5662c0)
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
    ) -> typing.Optional[ServiceUserParametersQuotedIdentifiersIgnoreCase]:
        return typing.cast(typing.Optional[ServiceUserParametersQuotedIdentifiersIgnoreCase], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersQuotedIdentifiersIgnoreCase],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b1ffd14fc45f85e296568baadb21dee65411cb1b6d7738f0a5f444eaec17a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersRowsPerResultset",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersRowsPerResultset:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersRowsPerResultset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersRowsPerResultsetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersRowsPerResultsetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97f5ebfababad053bb8040fb6e92ef0552d815c6648b07c24efdb2d1ba14e70b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersRowsPerResultsetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2205c35d988af3790079725f0f44bc3091896b0a3af3a472019c19b069af0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersRowsPerResultsetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d407e021e91290b1c8ad9967137af39c8ee88b641b90238a931dbe03f8752bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19237fd3e2b51ef36817ab17b041a78716fdecb22fd0461cea3bd13ae6606d7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41b864500f12deebb9aef4a8fc2dbe853de30e8de507d8976c5b1edb88ade96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersRowsPerResultsetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersRowsPerResultsetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__284f3115c51c50da081bfa87b05a9b231dca9d2c6ec5dd37723ceb46c303448e)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersRowsPerResultset]:
        return typing.cast(typing.Optional[ServiceUserParametersRowsPerResultset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersRowsPerResultset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e88dcc26a84c89d435e842fcf131ac72c438cf956892c0cc832982e9b0bc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersS3StageVpceDnsName",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersS3StageVpceDnsName:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersS3StageVpceDnsName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersS3StageVpceDnsNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersS3StageVpceDnsNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbd3e3f0812fe2f3eb2b41e55fbd1503d227faddbadad4c48f3a1f812c4d94ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersS3StageVpceDnsNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1215793f18e54d8ba0ccabfef7646be94e58301bd3764d30294615d277d9a6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersS3StageVpceDnsNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd92d48383cee3aababb7a200f364e55517fc32eff4cec9fccc8b7e27e830ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a44227fe85c19a2e5c4633fd366612af9fef1d87e3e4cdbe60fba78600558a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1d7e78cdf517dc2d77905a42167cba5d24bfd5188a4a0de484cfd45bc207989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersS3StageVpceDnsNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersS3StageVpceDnsNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab1bdb7edd6382de477ea97af9b9c99facfad88c7fd7feb22fced3448fe5756)
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
    ) -> typing.Optional[ServiceUserParametersS3StageVpceDnsName]:
        return typing.cast(typing.Optional[ServiceUserParametersS3StageVpceDnsName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersS3StageVpceDnsName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd8718b4ef8578b2e01e15609e41e5d78faa8b703977e5a31413cf4aa722ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersSearchPath",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersSearchPath:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersSearchPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersSearchPathList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersSearchPathList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b48cc7b7970ecc70ba925fa376eeb887000f4089586b54971d17ec1204d1f27a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersSearchPathOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67a95a03c3c9c7337de34d350cb4e78adb2ee465bb8fd9a5b0d6a5cdd26cbf6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersSearchPathOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158caf3e6aa6a4ee349af49b6c35112ff24c3df9e138e8c2ba23705306c2b687)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed5f7fa044a202e9cec3d51c58d5cc470c94f4ba181db9aa9654fb094cf81a0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db21b36844be7374c115d7480e75db10a6bcbf6ab3676410d10616d50ef2e941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersSearchPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersSearchPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de756d425e52f5ccdfd615886edbb6046a54a6b8049b1f99d546a5d8643aff0)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersSearchPath]:
        return typing.cast(typing.Optional[ServiceUserParametersSearchPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersSearchPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1339f090fd1f3dc3a2a2d811a77ed90d40d5cd2ae6fa56b898de77e051bdffc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersSimulatedDataSharingConsumer",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersSimulatedDataSharingConsumer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersSimulatedDataSharingConsumer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersSimulatedDataSharingConsumerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersSimulatedDataSharingConsumerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2404830596b04998df9d857e3ae10ada40ab0ed75366f114bc929bf8d95008f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersSimulatedDataSharingConsumerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bbb4bb3c366ea90318133630aaa4ee9dea8179ecf926bc07bc6ce22f46704c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersSimulatedDataSharingConsumerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4c8148835e52b23cd429e3aff146532c372f087b62d50c76e3513a0d730bd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30957679e1e393954f6e047340121a1014c2b4dd5bcfb29c5b54fec4a858d38c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07744cdbdb75c7ddde4385ad218a94b97ff2c98517379d6f403d2bc4ba6a0089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersSimulatedDataSharingConsumerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersSimulatedDataSharingConsumerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d4ef9692c8a805b3d8bf4c8b171f459436b27cf83888dd31d72ebac0bb80ef)
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
    ) -> typing.Optional[ServiceUserParametersSimulatedDataSharingConsumer]:
        return typing.cast(typing.Optional[ServiceUserParametersSimulatedDataSharingConsumer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersSimulatedDataSharingConsumer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb3336b2c54bf0c6bd56cf4a36471e640c5682ec6cbdcb4060a5ceb396466ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStatementQueuedTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersStatementQueuedTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersStatementQueuedTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersStatementQueuedTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStatementQueuedTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1940b2d5ca547e5cfd276e119c54f8f57248276e6bc5d7521949673f6068a994)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824ae1d8787036e63a0b79b22470b05db0de074515f9aeb2d47832b210258bef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1496d3995fc09d59fee2af5d8e9b019888ddb9e3cf6574ede47d8638e765c8c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c4d9cd3f829b33c62737493928d3f825bfebe098253c3090f54a262be49eb31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02eee590ec844de0a9f829fde394bbf07a493e1db30040c041132a91d3c5bdda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad915e961552ff9df6ed15b1abc5010a558c5906d2a6497e66345db6deb21af0)
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
    ) -> typing.Optional[ServiceUserParametersStatementQueuedTimeoutInSeconds]:
        return typing.cast(typing.Optional[ServiceUserParametersStatementQueuedTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersStatementQueuedTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c8842bb0863c1ff452e169dbd77658192ad57eeb70791198c472b5568cb12f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStatementTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersStatementTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersStatementTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersStatementTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStatementTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf58861d8ec3ed57ee88255e0d2d576812185b6e6f5cbd74edbfe363f33fb946)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersStatementTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec4300f548803495eb9045716a6822a1ff3d52c4f15b0de1857074501e482ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersStatementTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7046f8244460b7f6df031f877261f7d038ddc4d96fea976a1f24ba434387d46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__513c4a23a26b4696a5a39adbecde170d4a5b38c8f3207da79eabdaa0b3cf5934)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7f611ad742014c19ec1d42f7a14427f4045dd1484cee5b4de6a2d676ac9dc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersStatementTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStatementTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d6a9cd23dac4d1e10bbda552c4b69bd9ba623c23b8a49f1e2b626a6c90a707c)
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
    ) -> typing.Optional[ServiceUserParametersStatementTimeoutInSeconds]:
        return typing.cast(typing.Optional[ServiceUserParametersStatementTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersStatementTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ac4e07fa5fee171d6c456dfae043369a726ea69e0d789fdb39fa213b3e6d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStrictJsonOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersStrictJsonOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersStrictJsonOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersStrictJsonOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStrictJsonOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de3e0419aec664efbf6cec39099bf1aed0a40d48327689916b039959a84113dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersStrictJsonOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c0d1dd312c8cccb18ea13e419d3413252068b52682a7881639c20a16e6f1134)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersStrictJsonOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ec652d25a7d8e9da103dfaaebdd098dd5381c91c92684507d20d97e77e900b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89db7a9b8646d6f8c1e4331e2bec37821728a6eec617d3279447a5224c8949a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2ebf59b4cc15a85248e90543761157967c5d6733b6c8e2668226d8ba2e75613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersStrictJsonOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersStrictJsonOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__885d824726f1aaed47f0e34a1b65522a18539dca0fba7a4c67b7224eae325e4e)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersStrictJsonOutput]:
        return typing.cast(typing.Optional[ServiceUserParametersStrictJsonOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersStrictJsonOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45509088d9900f05624179de75a0b857d8b842e128b121e82e2f8aac099149d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimeInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimeInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimeInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimeInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimeInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7a738f72d49c2a19b7f66c4d7ccf7fdd15058daf6991baa916bff9fb8d59c11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimeInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086a9e00b19cb1980a950184ac9d2fa4bb282fd6581ef2214db0c5a7e375da05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimeInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825a3174a3b20507cf35ff119b54f599c88b3f73427118b36cb85ee55a955ef2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c088ed9b9b1a3742978290e48f29cef869f61ce1738fa209a5c974f6bb26e232)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb25373788192e583a10519480cc869d2a45211b070e3ab257b42ceeadc70238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimeInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimeInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3540bbc60ac23c065bbfade5f17ebd5077c92ec0c8ee2034fccf19cb515b369)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersTimeInputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersTimeInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimeInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b49b35c42ae7de3cd645e22bb639f9e0050cb72d3e181b50d697b7a5ee953ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimeOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimeOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimeOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimeOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimeOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b69d10456cd2a71e2ea6d0148da46ab465b43f6ffcce6d80cddaacb0035a1b62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimeOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5f968be61dc9138c2309da36511889f64dde703080c9e8b1f6712d0253e0d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimeOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d047c9c03e0db1a1144cd71b82dc50149554768d6aaf7dba4aed80b3b7664560)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c51f484df773ce6c7709ad8818be5f7470c9fa6eb3d5d6b86e05fe33026a093)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d10d9105733636dde28bdc3842214162be05c04f0a411160fcbecbef17ced30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimeOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimeOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4744d468bb00d34b59bf75e605a5798741b03a0b5fb2757eec38b4a02254d150)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersTimeOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersTimeOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimeOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ac1b433010f637f9e689c24423de3a3aea9ecf75731add38d70f74888586e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampDayIsAlways24H",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimestampDayIsAlways24H:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimestampDayIsAlways24H(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimestampDayIsAlways24HList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampDayIsAlways24HList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1eeeb82853d14f11cb826ce9281e4bd9216d8a9a65e00bbd925fbb75a5f517f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimestampDayIsAlways24HOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19299ea5819a7d1aeb8884bdd123a9505ad802fc3bd2e6c0c4c7d62323b80c33)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimestampDayIsAlways24HOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b58d3c1734e11d34105c61122ee5245911e7319c8384374f6595c52ec827e74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96c82788091ddd38a7311954840bba8779276e814ef4815ef4c337477a69183)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1771fb004bcbefc74e615050126e0545c7dce909a222af54e7f67cfdfd585a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimestampDayIsAlways24HOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampDayIsAlways24HOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__236d88f8505b8943577286b1467da0125be21225f983ee52615e6c20680adb8a)
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
    ) -> typing.Optional[ServiceUserParametersTimestampDayIsAlways24H]:
        return typing.cast(typing.Optional[ServiceUserParametersTimestampDayIsAlways24H], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimestampDayIsAlways24H],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9dc9ab291c2cf3d2fd64a6f7bfa27f40c5f37dbec1c30c906a3850c6c3844f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimestampInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimestampInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimestampInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc0db0371f786a2cd0ddc55bbbfc96ee91522d49a4843837a659469efd781c6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimestampInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d622bccdcdcbe9fabf507dda75069d445e7380186768219902f9a192a4f6c3ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimestampInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252bdcf4ba10f513da4ee0c69db19f5a9b26963c2b648a060ee704d16d0c9bbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c547c16975aee52daf2a98502313ba658c9ee5faa8de22cea553e34abf1f38f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53b4a41a6b8a4e885da3f9a53e2341cb48f0f7f3abead4e19e1129ac24b9300f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimestampInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb8649d493eaaf21d710638bcb07640088da060363501117a8197d2379b9c52a)
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
    ) -> typing.Optional[ServiceUserParametersTimestampInputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersTimestampInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimestampInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cd9bea40fbf5b2fcb615b56496fe41c49178784398c3096309522e2c815e18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampLtzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimestampLtzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimestampLtzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimestampLtzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampLtzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65815a775da4203c7688a1503dad5bd4877b2193fd61c6e9ab39d65153bbd100)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimestampLtzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f599fae9426f57a38d2ca8322138267c1ae41bafb6f5af787e7009bf0d4a18)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimestampLtzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265ef48cdd3d6f6b41bae5ed48500f96314ab5ad9c5be93fada6f810feb84975)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae3c9d0bee012dfa117c570e9d81d2f94b33b6a1b1850dd6bba9451eb7af58e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c27187f07137ca9d7376ed6f79006d6c8fbfaa8d48b946c82f00e42ca8c14465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimestampLtzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampLtzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f077d5d5fff295fc7f1d4e6b38ade0eeff41e3e3f0e89935378620658bfffcfe)
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
    ) -> typing.Optional[ServiceUserParametersTimestampLtzOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersTimestampLtzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimestampLtzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0f9b82d9b6150dd834ed1403ac9059dc1016e365a1d11d3da44ccab6a07926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampNtzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimestampNtzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimestampNtzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimestampNtzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampNtzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35aa03960fbdb792d118cf22cace2b55cfcf6bfdeeaf97390a0b615aacc9f89f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimestampNtzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd5d12b3b7cf52a4dd5063439e86346db21c2581738d0835a782722e569b59d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimestampNtzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb3251c234fe20d098cb61f8a28ffe56749472b58356559f1b6b9d4d03c128e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e14fe92ebaab27b5821aa2140d14fffa7697fdf4d58cba601a8094551f1bb843)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cacfefb1585f43cde9cd5f1a0dcdcf90ecda63d3819791c8f8c9ff649ec66fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimestampNtzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampNtzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab1ee72fb623a1093b727675c581c18dc7c7a6b88495fee7d19349cae193695a)
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
    ) -> typing.Optional[ServiceUserParametersTimestampNtzOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersTimestampNtzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimestampNtzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a325fc6a8f425060794ee323668bd24182aa89f285ac1a2381e60f844d1dcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimestampOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimestampOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimestampOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a46688921f26543f08fafd4333f014c554c769b75bfeb5ee00067d8b59c534c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimestampOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059bfea9267e4263143cff692d9997655a9441637a207898abe13f6af258462c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimestampOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4050920a86ab1fee17a9683df4f4bc4eafa7caaee79026e39abff80f82448e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a8b65edc19f06837cf05bff659835c752ecc3e68fcc753b476231edec8f5c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47afc9b2cc025540d43436d704af2a1287a7b27ed6bbdc5f1ec7cc8ffca54ba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimestampOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28b483a13b4e852aa510991f380464c9ee023891985188c398372f436a613e9a)
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
    ) -> typing.Optional[ServiceUserParametersTimestampOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersTimestampOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimestampOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d77016e3654a787b61f70e5ed014aba6a15c5952169d8726e95860b5427bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampTypeMapping",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimestampTypeMapping:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimestampTypeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimestampTypeMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampTypeMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cac8724a5e8fba517019023d28b93f76775ab3cfd4ed3e2dd3fff3dcb15a51fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimestampTypeMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855ac7492ea841a6a6b63b5a17378cc1432d72ba78bb544ab6879c489fb77790)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimestampTypeMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053e1527e27595597c51755389758927e4a664e486c8f0c4052ba80ef9779bca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67bf54ddc812860433247675a90a4074c78beafbf3d7388426945fc3b544a9c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ec3339d7c25d3b904e9d35164b6adec37f4ab914a524c46558162a6eaf25998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimestampTypeMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampTypeMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88e16a9b105feb2a76ba1b8c5b28bd4d97cae1d80c39d9a00be3209ced10e09e)
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
    ) -> typing.Optional[ServiceUserParametersTimestampTypeMapping]:
        return typing.cast(typing.Optional[ServiceUserParametersTimestampTypeMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimestampTypeMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af98b7e336c2cffe392e296dfc684d0fd2d0eb555dbd5e998de5eb3fad92eec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampTzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimestampTzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimestampTzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimestampTzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampTzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90c80556e32d27b99086e0578908a8324ca6200e0cbbbccad0b74c4da2792a52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTimestampTzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d988e06aa17cdd8cd925d6c0a9161b20ff9b38a074740ce58886de09d6f45bbb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimestampTzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac52345f6a695be9c7df90fd798a87855cb17dbdf606ff85d74063bde223f7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__873e306d96639b04f9383ca15f4cd991a41a8a730dcf95dfdabfbd232de6bbe4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20bd7a15844c9a1f1ddcff4bb5af46d441b4030adc2af8159ad74c4396d26e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimestampTzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimestampTzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d286a3566ae87b0c6bbb87433167bb824d950aff1ce40b8b6c9fd1692c4bc13)
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
    ) -> typing.Optional[ServiceUserParametersTimestampTzOutputFormat]:
        return typing.cast(typing.Optional[ServiceUserParametersTimestampTzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimestampTzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0d5e2240f86c7f261cdd45b4c2461ee067fd82f711cbce2dbb9c4bc5bb3779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimezone",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTimezone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTimezoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimezoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__593088917a8aab14b1ccc8ff8d23440d70f92a847a32234b2be014b8f456eb14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceUserParametersTimezoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ee1e87f40345eea6ace7d3a172ee9ce3b85078d3be9633032c4ff4b2c09c857)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTimezoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fc1f7d42b665b09bd10b336b9de8f0f6e4681c628049bbe319192d50b4bc39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f220d0ca504d208bc2c28f533399b064df1f96a4247bca5583ca6656653e3be9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cea133b544073ff47a3d75f1d09300d9ee805186830431c075604590956a3d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTimezoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTimezoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b9900b45501f7e9c0898f5a039135a3ede779ef552e44aa9f15ca92396cf976)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersTimezone]:
        return typing.cast(typing.Optional[ServiceUserParametersTimezone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTimezone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef73bec62243f91f826a6f32f423c186e23856c4eb0d3f72c66eb76e034f034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70631ee9dfa7a4356fdf7fbd1e8df02a5d1d8d720873a437b1f5638babaadd37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1345018221e3d2daf10ecd328b614b1f7fc75f4cb9f3d18ca51e27f2de9c4bd9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be60113e9bb98667678ff4f2a5fb78bc7c02969fe7d0d40e225e3976263df30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c6f0770df44037a5bde6d80a32f59814e3d17483aca2beeb0d2eae68c737bcd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__513132649ec345a03b20d38442fb2f9ba7a2b856cfb8f296f2abcdb6d6d6264e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cd2659fffed96b88d37fcd070fba5ff28039d3a275248f2c86ff84fa29099eb)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersTraceLevel]:
        return typing.cast(typing.Optional[ServiceUserParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d69d6dd98227751193bc30ae28ee079bb372d5739b64abf84ed28841aebf03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTransactionAbortOnError",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTransactionAbortOnError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTransactionAbortOnError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTransactionAbortOnErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTransactionAbortOnErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f603a93a316f2a8d939dac83fe5cc4d1ee82f77b4c91800800e143b5e68285)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTransactionAbortOnErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478808bec73f97aa7369f881c79410cec11c75c4dfae24d8745d8b07b6d2ca91)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTransactionAbortOnErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b447809743f5d1fe85b2b2c8ee8c1995f58850ffee548aa87706c480f350b8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2efcc187e7573b015688fe490f1bdcada561b27fb7a613a0105ecad5fbb7d5ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79c6825e0519116596c28ff731860805a77bdf2fc47c8e9fa2f7c1b58d918f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTransactionAbortOnErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTransactionAbortOnErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86b72d60ddb333d9fa1c481cf5cbde0d7d6e62189fa59af38f04a7daf294c3f2)
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
    ) -> typing.Optional[ServiceUserParametersTransactionAbortOnError]:
        return typing.cast(typing.Optional[ServiceUserParametersTransactionAbortOnError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTransactionAbortOnError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd7e7fd4bfe8dd7ef6c97bba6fa9b40c01c9a8bbfd70852c898c9ac1e8b5b32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTransactionDefaultIsolationLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTransactionDefaultIsolationLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTransactionDefaultIsolationLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTransactionDefaultIsolationLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTransactionDefaultIsolationLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6c7b6157177ee6babfc8a3326c78db19c4e1b50963ad5dfb1d5edaf437a2c33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTransactionDefaultIsolationLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd779a6176dc335b737cddbd326a59401e5d0a43b143e5207023ba85ae1b21a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTransactionDefaultIsolationLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4af106baa0f7c0d1ac3e1df8640bd5f19facdce637e92efc008aaed5546edbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9f53f8d49d0cce89f9e665bbdf080557af8a70825267a51cd9e9bac7a5dc6f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9d40fe7c87f78d3b8beda87005225109be3fcfd316d9e29e402d875fa723cbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTransactionDefaultIsolationLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTransactionDefaultIsolationLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56c85f7ae1ee5629dcae43aeb01aa0be68b0dbfa6bd0f38a787e64594ad7a4d0)
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
    ) -> typing.Optional[ServiceUserParametersTransactionDefaultIsolationLevel]:
        return typing.cast(typing.Optional[ServiceUserParametersTransactionDefaultIsolationLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTransactionDefaultIsolationLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8c94b3278f12b018dd549a96740d6fb7a7c8cb8efdd53ba7dadeb4ac1c4ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTwoDigitCenturyStart",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersTwoDigitCenturyStart:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersTwoDigitCenturyStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersTwoDigitCenturyStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTwoDigitCenturyStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b44e4f48ec97132bf9c5fe602c6cc37141cf0e84ec3560cbdeb151a2d99dc98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersTwoDigitCenturyStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa010002191c27a30cd63c0821a87e044a84f1a94abc8d2816736cb2482a62c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersTwoDigitCenturyStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59232fedc9bc20c908261acafb5b1577548c9362ac6668c19975d19102102922)
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
            type_hints = typing.get_type_hints(_typecheckingstub__906c2117e9bd59114635111b712a2f840791a2f62c7299a8a8198c9ad0c43f7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b3e63d85dd762c073e24c3bfa584f684674d002324faaf8b77c4f7f91447680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersTwoDigitCenturyStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersTwoDigitCenturyStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfcbcc0c0ecb74b8adf45d7e4b281a26066fd950d0fea76030d76c4687cb4d6e)
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
    ) -> typing.Optional[ServiceUserParametersTwoDigitCenturyStart]:
        return typing.cast(typing.Optional[ServiceUserParametersTwoDigitCenturyStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersTwoDigitCenturyStart],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2130d86709252cca63c6f3f5999804bc1964cf5a7a93161158c4963823e613c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersUnsupportedDdlAction",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersUnsupportedDdlAction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersUnsupportedDdlAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersUnsupportedDdlActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersUnsupportedDdlActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d44628afcadd0c65794ae545e08dda1ae4a769292b79aed00aa4794cd96b2b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersUnsupportedDdlActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff32e79ebe79a1015518d190aca12e783666b6b4cb03fb0a3d7b7a269ec1e818)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersUnsupportedDdlActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9e74d35585ac72fcbe7d444d68eabbb766b609a4dff4a9c1d25e186012a4c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f90340d618de64b5e9e08b3265553c64fa52e3aa679c7f58abdeaa16e1571069)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a08464f82844358a4bea3e8fc13c87793395a29ec1aa960b72711cbf6894bbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersUnsupportedDdlActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersUnsupportedDdlActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de55d0f52619c08111821752ebcedf7bffb8875139f6dc89ba14d2b6af589a7)
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
    ) -> typing.Optional[ServiceUserParametersUnsupportedDdlAction]:
        return typing.cast(typing.Optional[ServiceUserParametersUnsupportedDdlAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersUnsupportedDdlAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ce0f389fa3e8bb472dd9813bf128c9ae5ca17d7a7ccf8ce51e6bde7439e427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersUseCachedResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersUseCachedResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersUseCachedResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersUseCachedResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersUseCachedResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__768fbfc5bd988558ad7ecbba6838381a68d4705f3f165b591529dba13cbd753f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersUseCachedResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd06b186e5e874c9b0bc28fdb3ca3568549948f741b05b5d5a6d7951e84399df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersUseCachedResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f430d8b933cf816fd67a60fcad808c2787859cd1d4a2374618c38f1ad7a8c1ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebfaf8e1356a03c9179676731730b90fe3bcd9226df73d2844821b2848ba2e80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c0031b4b39a2f06b3179385a48c26f51f377a06417dc80ec856c2b4ffbfbd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersUseCachedResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersUseCachedResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f134636c721baeb9b2dfc86b6e46c84a0e60e3809b1e9b594c3cc26f103cb290)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersUseCachedResult]:
        return typing.cast(typing.Optional[ServiceUserParametersUseCachedResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersUseCachedResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655c9e8709b5cb9d30801c091746754d7b274ea11020208c29baf3053cb10bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersWeekOfYearPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersWeekOfYearPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersWeekOfYearPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersWeekOfYearPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersWeekOfYearPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b101235b7455cc882f7e3dbeddff342c9a00709182ebd232b7c51922fcffddc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersWeekOfYearPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e6201da6e316921769b6651870af315ac2f655f7b5b9d2fed11e911e4b588d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersWeekOfYearPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7c24a5c07263f4fa16582f037e9a7a3d38424383f9ca51618101784493944a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16dcf7b4ad0b386aa2940b0d841351efc1b54fe6df2cd0a764a63dc8c55f263c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a70b8418c92d0e7abb436009ba63bb6fa981c89bea015f3302660dfa57469bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersWeekOfYearPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersWeekOfYearPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e4c240da218007dce9106baf8b7e5b53dee7c9ef3d42b5dd9309c1b5c427ff9)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersWeekOfYearPolicy]:
        return typing.cast(typing.Optional[ServiceUserParametersWeekOfYearPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersWeekOfYearPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0d7f2a0135ab45a4a51eefcbbbfdf1c06efd00c9e713390cb614ed17b245c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersWeekStart",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserParametersWeekStart:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserParametersWeekStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserParametersWeekStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersWeekStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c83b4a7a6f4329104b9d0acf1dfe9374ab1413a009b7b1ab2f1797a786983c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceUserParametersWeekStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e198c4c69b1aed615687add77b9002a8f76a7d5a14dc3a1040e1e10d55430f9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserParametersWeekStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4989b814a9e37d7675ac8f01bf01df21472fb4d97e932cbe336e8f22ea22d36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a12d26d115ed9c58e0d0dc815ba62b186b56737f6c7043ab225325f8e32be8e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__261f91ad3a390ae4decc9061dd68f1723ce6eb4b97685af116a0e13b1dcd0681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserParametersWeekStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserParametersWeekStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28b982e96c7b450443340419e6f813770d242375848e0b0fd7d41567616e4be9)
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
    def internal_value(self) -> typing.Optional[ServiceUserParametersWeekStart]:
        return typing.cast(typing.Optional[ServiceUserParametersWeekStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceUserParametersWeekStart],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99af3486c07229ad1f31ae3541b632a0b26bb39909393a8c7b95ced5d50355d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceUserShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUserShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUserShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__259c0e188b08d688677bee30ad2c903485f6d69532739bb3cfae23ac1973cd59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceUserShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d65df2451e779599fb746b2763df9cc0fff5b812f2e2642ed8bebbfec3eba0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceUserShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d85c5d5b3aaee9cb6dbab158656cc5057c7fd90b27959e4cd9a931b8bf900b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4773de7c6cde1590cc7029d6ed8446a317a3dd6ac547af1d487a9175df6e1a90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b534a3d3d256ee23ee822a754c05fae09f517e1332bbacd2bc70637f85beba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceUserShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.serviceUser.ServiceUserShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__354d7ef3cd88596125d9a4b35c0ab6c3731b3c5c95e388a93187fecc4570b323)
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
    @jsii.member(jsii_name="daysToExpiry")
    def days_to_expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "daysToExpiry"))

    @builtins.property
    @jsii.member(jsii_name="defaultNamespace")
    def default_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultNamespace"))

    @builtins.property
    @jsii.member(jsii_name="defaultRole")
    def default_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRole"))

    @builtins.property
    @jsii.member(jsii_name="defaultSecondaryRoles")
    def default_secondary_roles(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSecondaryRoles"))

    @builtins.property
    @jsii.member(jsii_name="defaultWarehouse")
    def default_warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultWarehouse"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "disabled"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="expiresAtTime")
    def expires_at_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresAtTime"))

    @builtins.property
    @jsii.member(jsii_name="extAuthnDuo")
    def ext_authn_duo(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "extAuthnDuo"))

    @builtins.property
    @jsii.member(jsii_name="extAuthnUid")
    def ext_authn_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extAuthnUid"))

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @builtins.property
    @jsii.member(jsii_name="hasMfa")
    def has_mfa(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasMfa"))

    @builtins.property
    @jsii.member(jsii_name="hasPassword")
    def has_password(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasPassword"))

    @builtins.property
    @jsii.member(jsii_name="hasRsaPublicKey")
    def has_rsa_public_key(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasRsaPublicKey"))

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @builtins.property
    @jsii.member(jsii_name="lastSuccessLogin")
    def last_success_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastSuccessLogin"))

    @builtins.property
    @jsii.member(jsii_name="lockedUntilTime")
    def locked_until_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockedUntilTime"))

    @builtins.property
    @jsii.member(jsii_name="loginName")
    def login_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginName"))

    @builtins.property
    @jsii.member(jsii_name="minsToBypassMfa")
    def mins_to_bypass_mfa(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minsToBypassMfa"))

    @builtins.property
    @jsii.member(jsii_name="minsToUnlock")
    def mins_to_unlock(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minsToUnlock"))

    @builtins.property
    @jsii.member(jsii_name="mustChangePassword")
    def must_change_password(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mustChangePassword"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeLock")
    def snowflake_lock(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "snowflakeLock"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceUserShowOutput]:
        return typing.cast(typing.Optional[ServiceUserShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceUserShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e9a28162e0a85abc7ff75d5cd0a06c50e40af0a750ae7531714c7747d845f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServiceUser",
    "ServiceUserConfig",
    "ServiceUserParameters",
    "ServiceUserParametersAbortDetachedQuery",
    "ServiceUserParametersAbortDetachedQueryList",
    "ServiceUserParametersAbortDetachedQueryOutputReference",
    "ServiceUserParametersAutocommit",
    "ServiceUserParametersAutocommitList",
    "ServiceUserParametersAutocommitOutputReference",
    "ServiceUserParametersBinaryInputFormat",
    "ServiceUserParametersBinaryInputFormatList",
    "ServiceUserParametersBinaryInputFormatOutputReference",
    "ServiceUserParametersBinaryOutputFormat",
    "ServiceUserParametersBinaryOutputFormatList",
    "ServiceUserParametersBinaryOutputFormatOutputReference",
    "ServiceUserParametersClientMemoryLimit",
    "ServiceUserParametersClientMemoryLimitList",
    "ServiceUserParametersClientMemoryLimitOutputReference",
    "ServiceUserParametersClientMetadataRequestUseConnectionCtx",
    "ServiceUserParametersClientMetadataRequestUseConnectionCtxList",
    "ServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference",
    "ServiceUserParametersClientPrefetchThreads",
    "ServiceUserParametersClientPrefetchThreadsList",
    "ServiceUserParametersClientPrefetchThreadsOutputReference",
    "ServiceUserParametersClientResultChunkSize",
    "ServiceUserParametersClientResultChunkSizeList",
    "ServiceUserParametersClientResultChunkSizeOutputReference",
    "ServiceUserParametersClientResultColumnCaseInsensitive",
    "ServiceUserParametersClientResultColumnCaseInsensitiveList",
    "ServiceUserParametersClientResultColumnCaseInsensitiveOutputReference",
    "ServiceUserParametersClientSessionKeepAlive",
    "ServiceUserParametersClientSessionKeepAliveHeartbeatFrequency",
    "ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList",
    "ServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference",
    "ServiceUserParametersClientSessionKeepAliveList",
    "ServiceUserParametersClientSessionKeepAliveOutputReference",
    "ServiceUserParametersClientTimestampTypeMapping",
    "ServiceUserParametersClientTimestampTypeMappingList",
    "ServiceUserParametersClientTimestampTypeMappingOutputReference",
    "ServiceUserParametersDateInputFormat",
    "ServiceUserParametersDateInputFormatList",
    "ServiceUserParametersDateInputFormatOutputReference",
    "ServiceUserParametersDateOutputFormat",
    "ServiceUserParametersDateOutputFormatList",
    "ServiceUserParametersDateOutputFormatOutputReference",
    "ServiceUserParametersEnableUnloadPhysicalTypeOptimization",
    "ServiceUserParametersEnableUnloadPhysicalTypeOptimizationList",
    "ServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference",
    "ServiceUserParametersEnableUnredactedQuerySyntaxError",
    "ServiceUserParametersEnableUnredactedQuerySyntaxErrorList",
    "ServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference",
    "ServiceUserParametersErrorOnNondeterministicMerge",
    "ServiceUserParametersErrorOnNondeterministicMergeList",
    "ServiceUserParametersErrorOnNondeterministicMergeOutputReference",
    "ServiceUserParametersErrorOnNondeterministicUpdate",
    "ServiceUserParametersErrorOnNondeterministicUpdateList",
    "ServiceUserParametersErrorOnNondeterministicUpdateOutputReference",
    "ServiceUserParametersGeographyOutputFormat",
    "ServiceUserParametersGeographyOutputFormatList",
    "ServiceUserParametersGeographyOutputFormatOutputReference",
    "ServiceUserParametersGeometryOutputFormat",
    "ServiceUserParametersGeometryOutputFormatList",
    "ServiceUserParametersGeometryOutputFormatOutputReference",
    "ServiceUserParametersJdbcTreatDecimalAsInt",
    "ServiceUserParametersJdbcTreatDecimalAsIntList",
    "ServiceUserParametersJdbcTreatDecimalAsIntOutputReference",
    "ServiceUserParametersJdbcTreatTimestampNtzAsUtc",
    "ServiceUserParametersJdbcTreatTimestampNtzAsUtcList",
    "ServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference",
    "ServiceUserParametersJdbcUseSessionTimezone",
    "ServiceUserParametersJdbcUseSessionTimezoneList",
    "ServiceUserParametersJdbcUseSessionTimezoneOutputReference",
    "ServiceUserParametersJsonIndent",
    "ServiceUserParametersJsonIndentList",
    "ServiceUserParametersJsonIndentOutputReference",
    "ServiceUserParametersList",
    "ServiceUserParametersLockTimeout",
    "ServiceUserParametersLockTimeoutList",
    "ServiceUserParametersLockTimeoutOutputReference",
    "ServiceUserParametersLogLevel",
    "ServiceUserParametersLogLevelList",
    "ServiceUserParametersLogLevelOutputReference",
    "ServiceUserParametersMultiStatementCount",
    "ServiceUserParametersMultiStatementCountList",
    "ServiceUserParametersMultiStatementCountOutputReference",
    "ServiceUserParametersNetworkPolicy",
    "ServiceUserParametersNetworkPolicyList",
    "ServiceUserParametersNetworkPolicyOutputReference",
    "ServiceUserParametersNoorderSequenceAsDefault",
    "ServiceUserParametersNoorderSequenceAsDefaultList",
    "ServiceUserParametersNoorderSequenceAsDefaultOutputReference",
    "ServiceUserParametersOdbcTreatDecimalAsInt",
    "ServiceUserParametersOdbcTreatDecimalAsIntList",
    "ServiceUserParametersOdbcTreatDecimalAsIntOutputReference",
    "ServiceUserParametersOutputReference",
    "ServiceUserParametersPreventUnloadToInternalStages",
    "ServiceUserParametersPreventUnloadToInternalStagesList",
    "ServiceUserParametersPreventUnloadToInternalStagesOutputReference",
    "ServiceUserParametersQueryTag",
    "ServiceUserParametersQueryTagList",
    "ServiceUserParametersQueryTagOutputReference",
    "ServiceUserParametersQuotedIdentifiersIgnoreCase",
    "ServiceUserParametersQuotedIdentifiersIgnoreCaseList",
    "ServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference",
    "ServiceUserParametersRowsPerResultset",
    "ServiceUserParametersRowsPerResultsetList",
    "ServiceUserParametersRowsPerResultsetOutputReference",
    "ServiceUserParametersS3StageVpceDnsName",
    "ServiceUserParametersS3StageVpceDnsNameList",
    "ServiceUserParametersS3StageVpceDnsNameOutputReference",
    "ServiceUserParametersSearchPath",
    "ServiceUserParametersSearchPathList",
    "ServiceUserParametersSearchPathOutputReference",
    "ServiceUserParametersSimulatedDataSharingConsumer",
    "ServiceUserParametersSimulatedDataSharingConsumerList",
    "ServiceUserParametersSimulatedDataSharingConsumerOutputReference",
    "ServiceUserParametersStatementQueuedTimeoutInSeconds",
    "ServiceUserParametersStatementQueuedTimeoutInSecondsList",
    "ServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference",
    "ServiceUserParametersStatementTimeoutInSeconds",
    "ServiceUserParametersStatementTimeoutInSecondsList",
    "ServiceUserParametersStatementTimeoutInSecondsOutputReference",
    "ServiceUserParametersStrictJsonOutput",
    "ServiceUserParametersStrictJsonOutputList",
    "ServiceUserParametersStrictJsonOutputOutputReference",
    "ServiceUserParametersTimeInputFormat",
    "ServiceUserParametersTimeInputFormatList",
    "ServiceUserParametersTimeInputFormatOutputReference",
    "ServiceUserParametersTimeOutputFormat",
    "ServiceUserParametersTimeOutputFormatList",
    "ServiceUserParametersTimeOutputFormatOutputReference",
    "ServiceUserParametersTimestampDayIsAlways24H",
    "ServiceUserParametersTimestampDayIsAlways24HList",
    "ServiceUserParametersTimestampDayIsAlways24HOutputReference",
    "ServiceUserParametersTimestampInputFormat",
    "ServiceUserParametersTimestampInputFormatList",
    "ServiceUserParametersTimestampInputFormatOutputReference",
    "ServiceUserParametersTimestampLtzOutputFormat",
    "ServiceUserParametersTimestampLtzOutputFormatList",
    "ServiceUserParametersTimestampLtzOutputFormatOutputReference",
    "ServiceUserParametersTimestampNtzOutputFormat",
    "ServiceUserParametersTimestampNtzOutputFormatList",
    "ServiceUserParametersTimestampNtzOutputFormatOutputReference",
    "ServiceUserParametersTimestampOutputFormat",
    "ServiceUserParametersTimestampOutputFormatList",
    "ServiceUserParametersTimestampOutputFormatOutputReference",
    "ServiceUserParametersTimestampTypeMapping",
    "ServiceUserParametersTimestampTypeMappingList",
    "ServiceUserParametersTimestampTypeMappingOutputReference",
    "ServiceUserParametersTimestampTzOutputFormat",
    "ServiceUserParametersTimestampTzOutputFormatList",
    "ServiceUserParametersTimestampTzOutputFormatOutputReference",
    "ServiceUserParametersTimezone",
    "ServiceUserParametersTimezoneList",
    "ServiceUserParametersTimezoneOutputReference",
    "ServiceUserParametersTraceLevel",
    "ServiceUserParametersTraceLevelList",
    "ServiceUserParametersTraceLevelOutputReference",
    "ServiceUserParametersTransactionAbortOnError",
    "ServiceUserParametersTransactionAbortOnErrorList",
    "ServiceUserParametersTransactionAbortOnErrorOutputReference",
    "ServiceUserParametersTransactionDefaultIsolationLevel",
    "ServiceUserParametersTransactionDefaultIsolationLevelList",
    "ServiceUserParametersTransactionDefaultIsolationLevelOutputReference",
    "ServiceUserParametersTwoDigitCenturyStart",
    "ServiceUserParametersTwoDigitCenturyStartList",
    "ServiceUserParametersTwoDigitCenturyStartOutputReference",
    "ServiceUserParametersUnsupportedDdlAction",
    "ServiceUserParametersUnsupportedDdlActionList",
    "ServiceUserParametersUnsupportedDdlActionOutputReference",
    "ServiceUserParametersUseCachedResult",
    "ServiceUserParametersUseCachedResultList",
    "ServiceUserParametersUseCachedResultOutputReference",
    "ServiceUserParametersWeekOfYearPolicy",
    "ServiceUserParametersWeekOfYearPolicyList",
    "ServiceUserParametersWeekOfYearPolicyOutputReference",
    "ServiceUserParametersWeekStart",
    "ServiceUserParametersWeekStartList",
    "ServiceUserParametersWeekStartOutputReference",
    "ServiceUserShowOutput",
    "ServiceUserShowOutputList",
    "ServiceUserShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__65daeef77cfdf652d600788cd31a1a34276acf0f2fd7d88e5085c3dc97a6caa7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
    date_input_format: typing.Optional[builtins.str] = None,
    date_output_format: typing.Optional[builtins.str] = None,
    days_to_expiry: typing.Optional[jsii.Number] = None,
    default_namespace: typing.Optional[builtins.str] = None,
    default_role: typing.Optional[builtins.str] = None,
    default_secondary_roles_option: typing.Optional[builtins.str] = None,
    default_warehouse: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    geography_output_format: typing.Optional[builtins.str] = None,
    geometry_output_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_indent: typing.Optional[jsii.Number] = None,
    lock_timeout: typing.Optional[jsii.Number] = None,
    login_name: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    mins_to_unlock: typing.Optional[jsii.Number] = None,
    multi_statement_count: typing.Optional[jsii.Number] = None,
    network_policy: typing.Optional[builtins.str] = None,
    noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_unload_to_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_tag: typing.Optional[builtins.str] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rows_per_resultset: typing.Optional[jsii.Number] = None,
    rsa_public_key: typing.Optional[builtins.str] = None,
    rsa_public_key2: typing.Optional[builtins.str] = None,
    s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
    search_path: typing.Optional[builtins.str] = None,
    simulated_data_sharing_consumer: typing.Optional[builtins.str] = None,
    statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
    week_of_year_policy: typing.Optional[jsii.Number] = None,
    week_start: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__c67cd2093d2606220c1a516507a1fff537677dac25fa1af2c9dec8947a9d5e3c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dac8e519f15a6f2b17153b34f38a3f5004712a7dcdf7ccc82fb3e496508ae10(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36aac519eabd09b4b7febd5f26248cdcd474c7857daf5c7469b6f72629c7b498(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4acfdadd8050a2db2e2b3ad82ba09aee3b2658c6522b383666f3510382392b44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd3d6394e712f72d6d4088d82f68161d00f3fdeb22ec22e42debc7496d2cabd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861a50f4b4e10e947e8a1f5aec3bbd58cfdccc6eb51929afea39a4af5a838c96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a19d788f9e1ca06715d7dec02c334ace454888b413a5e55bd09931470d8993(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77543f4b5bde3fd1d4fdac05c3a7c2b66d702129e68b7bddf0e84e900fc79566(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33e8b6739a4a82f4c3db8d50650d8f749bc33c53de248db90d7662990e46b53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26689387b5359fb35902f552724e6f0f4d250384bac3eb7624042b0410c5beed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdbc542b4cf3c70d7f8562e1c1eaabef2ca175cb60eab0da0152f9b74a52d42(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b29a5a5ff287cf552f749ad5e970e8951bb5297c1d981e01d1ec6fb0087c5c58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe02bfe031dd83e5c6472d7e76ec5361912586ba01c1333c213d8f2da75bdf2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c528ddd69e179fc5d804ee7362cc056cbe8cead91efca5dab03722d56553d46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c342c0e45222505bb6e3e6177d6761658d537f7cca860acc6aa5ef524c2e7ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb16bc86a7ee37c7769a48820078e66dd83c2bca9f8da901b7bfb73a20026c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39755037c2ccc3ffdaa374ec21548f6f5429d06c3dd5bc750f1851ffe3989802(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fb65485d25416264beef2e8a935e18f4b7175b65d54643a30dc5bd0cc814d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a7deb20a7236abf3fc312c8ddf0340bfee6436171e62065f15637a3e87830b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180400e293fe7833c690e934eba2fddce26f602462b1021d8b07396c1ed69683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec703367381b35c01cd78120a91fd535c23df4e8b5d905c5d448964fe64d42b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586dc744a84e97015b403a7d2178db16c6708f93d8450f4d7442c72eba5e91a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af67a6f6e583e7111e00a4da925ea6e52539483745f629ab8c94719f455789ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baf46f8991123801edc57a651715674b21516e4fe907817eed53a2a800d7794(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce398afdfe5fe86458e21c6c2509579353616e7ab97d9385659b2300999a86d3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a84bec34edd060b0f7382d5a2cf79c32d30d65362768171b8f6f94316960b69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab4edc2f0ba1f66603236a6829e034b87087f529fc0f5bbbfc770848d9da3ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57af89b47f1126f134da19b96b05197836b83b6c6ea36090136ea6f0c0add905(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0534d10d08c99535e84cced7fc710d16354fb84c8189d5d65e39ea400cb9dd68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c05442cde566e53690c0221b5bd3eae31dc0b8e1ba6a99392d2084894f04cea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75f667243161b202d2ab8d476754f1d29c4332f6fccec68b5b4291d1264b65f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dba4ac73b4fafbc65011601bd38aba6157b951f0f5b98bc0f4a24a9fccd3403(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b850fcb77171e20a0b922d0d948ee0906eb5f6b208b399b7f0f284efcc482eaa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd6fe487cc7db526ae512d1c27269dd9931a83ffbc3b890b9c170e43c840e25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0de64f43f304d1123707b6b0e1613ed8e70774fd9682e590a05775500a40ff4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b91463c32bbb778ad0452272728987de9e365447a89ef889eab1cf23174c05(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb3abd30b5e56618924b3b1ed44c1d59c7f262a861fb4d2274b166ad9932b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fb7b91525507f5c7c0338921eb2d01c40f4f8a4517840ba7acb3bf6636ffe0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d29ca34b1fa53722211c7661515bed6eb284d2683a8b270a481ad40985a7b1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c428be30b3f1d31bd701ba37961218dd7682f00731c85ae99de4da1a0f0876ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b02937675cafa7949530242040953b333423bb3f5c1153e4206e7f3e832eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7968e45de201066d2a32958e8597ad2f26fc19e7fee8be398103b8ad6a633104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37766ef83f4c6e591ad90f6e235b651518e339112d6409892be2d3418d9d29fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053ac577b37600018ace2662f9fd10fc31cb1d9a3b5f1846168fa984ef39d9d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6c291b18f41fa20ce95c52d0bb37e3389a4627c955dffae8c239de08467120(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9ce21b7ae89b466c424398cd338e4954eb90f9dd441a9ea2e9ba15ae681a97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b482cc65a73d89030af8b1aa405cf0cc3490653dcbde0adf2857401073c4488(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48aed0e618482cad613c74e431193eb3478a41e3160aa6cf3e494a6c2068b4f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82346500bdfa25bfa409612cb142ad7b1952f1ac55a89647890cab9bf842a61f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0048514bd39d20784aaea7b0592587afd51c084bb028df5d0af8134904ae09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9ada3b2bc24e4e3070fcc7eb3fa36b42dc03cb6675b10016f1f263b5d4b557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00790a949dfb300906c699b6309d48928963cd3c288ff76b995c594cb64db2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b9c48314c8999de8635ab60a0787bfc517c414b5ffd389cde78d5214429031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4e5d63fe02aed04cc10ca392df19cf799efef18094ac577b1121e6d012804b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2d5621cfacffb6d6e238bdab5953c0ba8636689f8d71f9caaa5019070bcfea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d356a215dc7d1e2de76b6aefba45176c34339a247fbaf4cea91f52649eed9f89(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45db12f331757fbd7ee1897af5c675276d3796eaa0a4d873b7aa0b2da6f1b19d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf0bf493644deca36da239e1e79c651d0c1206d4c3b4a66e9aa10a522c33eab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469d33e5168b17ee00961ea2a83054649605a3cc9317d95efb6f9a1feaf63c6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096788b3aef18f01dbc364e5d16fbeeda7eb0d50e8ae1e75cce990e3fe6f7203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db774cbb3bc517c15912983861294055cb57c6df27fe133505734b02a62e33a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db293ebfde0cdb3d20bc06de2506e1ec53e46759644eea58e0d2daede830bf92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c91d56c6c6ed8f084949839c95fec3f2f5a8fbc74af7180e5468efc57990c09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3c98bb18abf38cab161632f609df75b428187507f4a3eae4230bce1d252363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b5d2ae1677f9856b1fc7f9e5c8e2122c47c07aac495e25a1c7ec033caeb067(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69a1a3bb53cf9f83d158c30ea3a5738df7f310ae5438b3d1e39cda21f3dc81e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f272802876454392c3789917a0d7b80de790f6d4b5c7d38497f7f1835c38ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba22b3615563278d12527109c3a7a0b0b1d915f8f7ff3ada80c156a2c1f73d8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d42ba48f1b6ee654d2df3e6dae7c8d176d3a22364b2bf8e0a8de9787211d3d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6404fee259fb14535798b3f6f3be8a4b443dbfee56373d7b58df70d426679d61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455228b49444e40860a18ef6ebeefbd03afc88b95fd71706433e974da5bbc431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abfcffab99cad72c8d5799f33ab6c46173f2caf0cf734fc78e64043de441e75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db21cb9c10a0e7f70c42c111f173aca866f257ae6d5a22d059d9b692e8f2849(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4c3ac6930e5a416547135ad0e234bdab4656a82d23e901cea23554eed48f81(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b2bc95509002ce2a86a619507d2cae7e7dcbdb03df3f7a079af7baac670bca(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
    date_input_format: typing.Optional[builtins.str] = None,
    date_output_format: typing.Optional[builtins.str] = None,
    days_to_expiry: typing.Optional[jsii.Number] = None,
    default_namespace: typing.Optional[builtins.str] = None,
    default_role: typing.Optional[builtins.str] = None,
    default_secondary_roles_option: typing.Optional[builtins.str] = None,
    default_warehouse: typing.Optional[builtins.str] = None,
    disabled: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    geography_output_format: typing.Optional[builtins.str] = None,
    geometry_output_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_indent: typing.Optional[jsii.Number] = None,
    lock_timeout: typing.Optional[jsii.Number] = None,
    login_name: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    mins_to_unlock: typing.Optional[jsii.Number] = None,
    multi_statement_count: typing.Optional[jsii.Number] = None,
    network_policy: typing.Optional[builtins.str] = None,
    noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_unload_to_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_tag: typing.Optional[builtins.str] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rows_per_resultset: typing.Optional[jsii.Number] = None,
    rsa_public_key: typing.Optional[builtins.str] = None,
    rsa_public_key2: typing.Optional[builtins.str] = None,
    s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
    search_path: typing.Optional[builtins.str] = None,
    simulated_data_sharing_consumer: typing.Optional[builtins.str] = None,
    statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
    week_of_year_policy: typing.Optional[jsii.Number] = None,
    week_start: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a783aec0a42e90a34ee600c85fcddb713f913fdff9c3b52be0ed0120de87803(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c469ca83a5c2df0a906ff442d382fb41590ea4d1405ea1c7333d26df9a423bf7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6786c8de674174c9d196be714e6e24bec5c47623ef9e4044c74dcc6c0be18bb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461b78280c3271b9874813ff5eb034b03ea3e3eeecd693b13df591c7b030d304(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3ebf9bdcc6ce758b94afa6e943bda9f5225c3a1b403fbad28946020a312562(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0859ef6d39d2c0c7a208499d116a1d9b4acbe9e61cc946fe9898326b4f652049(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b379a3bddf7c46bb6fbf81cba29dc40fb47e1a812483fcd549a5616f2b273a02(
    value: typing.Optional[ServiceUserParametersAbortDetachedQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978be8521df8d1e47e0e855ff4828f7a5150fc103257e309d075b69b54fa9a9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4109c2b0a1619985723d2ec0f36a74b88d00739d9f71b02f4ea52575ba2ed6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bdbee872a2906ab63784c577c275ef303674fa2641e7a5c21018d039c80af19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6243d29b8f9f0559d93f5757c1a3946ad62706501e1de402b15b61b46953449c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b6e3d5eeefa4e4435c8d6fdfdb567fef29cec2818ac87a56220caa8f202993(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b69481f864385e330ee93437c74e0d8c8076f456bd014e1c1a867693602ffd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d935bd5b58cc0b2001ad3d6352234e68dac7d946f53a6fddb10a5ef3960227(
    value: typing.Optional[ServiceUserParametersAutocommit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac802069d1c5f6c88bb131300ac31173cefffc5735b91397773cf9315553a93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3066bdbc52789bef13a9298c4a0c66a5590f6f2b10f4fff9d432fae13156a07d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9553f957e5ee8e4cf2dab99506da637d10638b5a1a5126f541a49002f8a7edcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9191f1aba07a747f288889381e91fc6609f550b11a790604efeb3261ada419e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16633872b6878dea33cec373c91fa1a3ee91078b7659483822caeb7e5a94ec19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487068bcca5f1cffd6d33ed41bd06427243e82f5c404d04a688e017ab4e18056(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7475a01115000a588fd1fb4faeb4956f762f18857005c9eea24550df7dd484aa(
    value: typing.Optional[ServiceUserParametersBinaryInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be961f0501d66b98e9e7999b042f576214e642ce7ae8850ae2e02255f6e6a964(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460e09f6e2f37fa423b595a6e0af15c29659c74fd5103456dab9a6ab2697fef0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dddd388bc426d65a5f675de87d80d3b7336e3200535698c6654bef15281eec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5575559d3694cb20d45ed0d5ea2c62540747503990ae7da689991913e70c19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0d1f8135a984775d2c1815b59c5fc1dc1094e94ba8814f0969b6db84825a89(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d70369754cf9c89db3b519da82541aea9b315fd23fe89e4a36f93d2ce2f755(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1f0c11acdf6f8590a859c699aae23001076b0c35a427b0e23d567ef5faee60(
    value: typing.Optional[ServiceUserParametersBinaryOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06f2d99266ed1484d8335dcdf766d68a235e11ce4dcc4f8317f6f34927878cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5cb90e7935905a2f033fff2476704fab51592aea10480b9c9d27f440a2fc4e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059a5447050e4057d64c1c93d2a7105fa7b943b403727e5bc8ee76bedbb9609b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac1ec0d759c36b0e4f37e98149a2540062cfffaa9f299143e43d40edf47aea5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475eeaef3cf75d6d908b51215b1c6ea6c5835b188d3ddc7ad60dc3d9261b9deb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bfa62babecd2303f2d4919f9f5abdd5bc7c2d3f85fc759bdc356577cc96daa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015ab009f588279ad665f5183a20812a40c76ff48b8ffbd759f4d8179943be04(
    value: typing.Optional[ServiceUserParametersClientMemoryLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e60a85d8dff1d71cfb48008b773639dcca78ea22f6086f3ade85c637e11ab81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdc57b62f85fc871ed5c9da6b433b4034861c692c0aa0cd02819a83c6e15f74(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7c02e2effd9d72b27184c9f647a49b1a816beb08855ad4fab709eef17a1f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897a91c56614014297fff05147866ee744d640b6b2ea5051c649906812bd135a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4466151f22a4e9167d86419a586e113fd05e90dc7a636509a4cca375207a0dbc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d6fa3286bf117e072d75e3e013081a7b9755a47d5a5e8e284c0f18208a0baa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7178299f6555a98ab1126c5bd796f2c8985f7fbdcf48075d8183b6537e914f(
    value: typing.Optional[ServiceUserParametersClientMetadataRequestUseConnectionCtx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de17ad0e24da260ab3c226304e32d46503118b7191e377b475bbaf0b6d7df06e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07cb499d248d6fc02ca6b34e9f5a88d684d82cece5c1660ce2566bc6d84727a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f9c29a091648e9e359de5bdb3da4f6532c9f91432e4908f7f371b8395ee11d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4d79606d6f3b1e70d553fc3ed6bb69ddce68e6a0845132f27f8c7d56239446(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8bc23a9aed993ab9ded3369436e3231bdae3679034beeae8e13195bbb568e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021668569c8bd3a2cfc486c0aa7e4c4941d39473b91cf2c7050d527509b486e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7baa60960433eba0b1c340c807136b61efdcd7e6a067257f60b5487d9d42499(
    value: typing.Optional[ServiceUserParametersClientPrefetchThreads],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca3ca326b9f16cee05a26ec4391af6389a31d822f468beff61519261e9cc080(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74e1aa52e88bd8ac0572882c03813f6d856770a25879c221ffb8db2dfb20f0d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e4c5e6d5703f6c2f506fb1765ce88e86a8f06d3ec47746c273a8d6a70f9d02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8736cef9121191664a3d20cb36384265e3674d08ac166226d8fa6c36e8c316ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b963fe0b0ac52154441f551f2c595b08e39f75c4c9508b6e7fda8a60be6381a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492dd01ceea63727bba3776de641672d417e878d150f9b80ce46fc18984bae09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873042d47c5247a789b4ad3192e193ac5438c3b201d82a269fc65a77d1c4ebff(
    value: typing.Optional[ServiceUserParametersClientResultChunkSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efacf8111f8e3fb923b14890727ebd72fd6a18f3b98423580535e5278d590373(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb0214e7ddce51c5dd7f4cb82e5be6580ef611c351874dc1b520370dd6b5a56(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f26c4539a611ab6d6033502157584eefe20f543f1e56f8fc1bf13970d55fc18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859a9d5b200b2dcb2fee2b58f7e63bd5920ee48899a490ae0abcfbc798089689(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23cb7a548159da18af0eccc44c149314c746f0caff6ff4322720398abc3d46a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f807964f51aae3b0e3b22a077e96e20d8880d0cb518ea54b0088a4693a02011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22b89f9c9c5af5d4557f8c7affa1c3ba63af0a46cb2767309ed4fb63f155507(
    value: typing.Optional[ServiceUserParametersClientResultColumnCaseInsensitive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8ddda082624b8818b76e9d92661f155afe93a3735e001b5e3db84b4d5d27cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea1064aec995fa1742b8fcbbc04379a7ea01c97a485c1f6cb7558a0c715f9fb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cef09786814050519a1cde99abfc3a322c4926c7ec1e7d2a927e4254e7b284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5115c5cfdf00db9a34e439eb9a108869aefeaf3caa2d2de770111f0117bbbf4d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f6fd248b953f878ffa79803dbd517942f18005f15389f5e84fbb5e24f1461f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1113dc76bd31adc0be2aa199a6713d9c8e9ae4350058babe56219f9ed176dacf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996d33ae34ba672c4d9aca3661d2dfe68beb202c0a2b01994fd5074bed06dfc7(
    value: typing.Optional[ServiceUserParametersClientSessionKeepAliveHeartbeatFrequency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f45c2db773e00052272364c160bc77b3ed0f979cc016a5d8a9c3da80032b3fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eafb85c41f39feb6b69852b88d1f9b3ee77f5b4da707a791f0289c62718c53d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46eb7cada5debf2e552b1114613e2c7452eb2e797e2598991f85993f3360f553(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823382ee156edd2556c81df6b956032bcd804bcefeed97d6b283dda8d26ca91e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071a28df653b90a2c804111919697fb28ef9dc16aed885d3d006f0ba7eb99c50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107aac5dc3335eb6d5227f8bec315546674323abd31c5b4c0a9b279ac03628db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d352a608887e098243839c14212abbe879616bc2fc2ff4eed861bd1b2cb156(
    value: typing.Optional[ServiceUserParametersClientSessionKeepAlive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9924df1fa21f7849659a13f002daf38645f20db6eefa1dc8ec234947d7fabc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5551c95f091c1d09dc8a2365d7fa9af9cd9bf9066bdfa0649bdd3b4f5a5605f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a7a426b510ad21847dcf712e30cd80ac66f0307a4163caa567b2cfba26c248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f1c3b9b152bf66656cdefa9778670891cab9a939dafefe0331cacdfb77ae3b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14097184822a4ac7cedd18ae2898cb86b7e297ad4dbedd41d5c86dc4d292b08e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e9e733f021f06e088f992afdc827ed6c4a757500ef284ffcf73c0387763157(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6593586f33cbb1f33ab3d004ca1efd85053dec2abd3c5c8a636751df4bc2a632(
    value: typing.Optional[ServiceUserParametersClientTimestampTypeMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e67fb5d2689ce304022f2d133cdea81ce676ea7a9ce1402d937f430c239406(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552cb2574a4ed645f565849c065198aae9ee1a27a45c48574ab4d94b6a7479e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2710b620c4bcb43889522e101f35ece7ca1e33eb1a4ed7c036d708c1a1530c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f903485395dff983c5c7454f60b5c922d5d2b65801514689540699f121c312c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653291e4d330b7bfd520d5418e26a471e4c38c194415bc107bf8082731c3e6a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb25b60a2e380159f815f06ef6f43d1f550ab22e930db07041b5b7b88075135a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4520d9133fdf66156b262233f93a619b3a5fcc65450f563f6707d046ce50003(
    value: typing.Optional[ServiceUserParametersDateInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4359f55743b57a19dca293cca9047cabce24c74dc836c687937fd33cb4052ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163eaeb6638bf2973cf12cbf70326703ecf8bacab150c92b506569efd0c1c70b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701ec46add86f60beb1cd9881c2148efdeeeafb990ca2c843c37a26204021189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0b6b4b352f798622d96f1a7e5499ba1f434f0da86f2e610e47ba4944e2e1b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb3db3e7ff6f225b085796476dd5b8813a7d8447e780d8774febe6b9f63af25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398c895f9d3308ad36ddff3b9e344e308b079e8afae6d3cdd0921989bf436f80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e3851433402af65324886e843ee1d8380cff4dbf61f272da3cfebc36ccd5fd(
    value: typing.Optional[ServiceUserParametersDateOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdfd564c157b6991012ec25f44741965d667197604fc211440096a22eeadaaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462662024d76937f9567266262a246c7a3dc5212da0b27ecf947e3b295623bdd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570916356ed74a88fbc0f8f92c1079a3ac789c11a4c7fc5fd87828275c700501(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dfaefc8152e994b0283d59da772aab70f0fe99f600b338ef600fbac9683656(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3760c4f49bb157603f16f7a4ac2493c946be52b51e08214222dcf09a6c581a62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe4789b3cae1062953ad1cebdfa12d8a9cf777a7786517ba721541748c5fe97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14b7c63680dcbefe9202ebd0fc9d802963044a76143c986f35234196a60a6c3(
    value: typing.Optional[ServiceUserParametersEnableUnloadPhysicalTypeOptimization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c6132c4f8cf4d46af0cfeac6ccb0c48be7ce19c24ac41dc27ef17185307ff9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e23881ae1a34bbc71dcd22e2f541136ed94ff1e4e13d1b7bb1a5ce74501c51(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c99666b882a4ef570cdf6f842ebf952c4d777166c342e76ace6a9763beecea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c52ca2be990abfcef65d80f348a3ec48289305dcd39275e1cc5ca668192ee37(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75527b42b5041c99f46068dd60157afbff81bd7be34af68a2ef2cccd0b3405a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353fabb9532617d2c77a436130b417c03aa4211fa1d6fb3aefbe59799604ef47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0090c601cbb85e6e1faa4319b6ae4570e37cd69222c56317a8ed30830efbe7e0(
    value: typing.Optional[ServiceUserParametersEnableUnredactedQuerySyntaxError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bde630e40635f1e27e5cb5fcbaf6b28e2fe7e616a2aea2a5542753b2e2830f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9725d6bb4fc989779aede4127301b60d2988ebb23383d2ca4c34d65ae4b4bc85(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efba96a44980bcce1a47a16910cfc3137bbdba1db022d27e93e8e6919857351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55bf231f49fd1a875d6400ae794cf63d271220edf5dc6fb72028f2fd2fc352f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a12d6db11e0617f45066b2b39d28f2a38cd70cde83762e7d0702a78b48b4671(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba671ec801fd81ab57dbc069e8365d9bbcbada942a7a6be5e33d0e77643aa2ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5aaf6300bee71968097375120cd47fa1f4864f2c31a355d5f8157bf2eabb5a(
    value: typing.Optional[ServiceUserParametersErrorOnNondeterministicMerge],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddda90864f9aa836807ebf89b4c50db432b0e815ff80aa991226237a1065153(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de43f8f97ceab44a7826076f43f609b6f10679f5f01c93020acfe56f9144b2bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a6c991715fd2abc0f977c1ebf1796bd9378ab5641abae0f10d925e64db414d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815feb3b720aa3ecaac1d342cf8cee1021cd81354541e2770aecc3da6c7dcb73(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e8329b860c26f9a78bddaeb16390971aa8ccff1720c5af94a7c97531678709(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40c192fa3af3a7af50fbb8c93c780496acd791aaedb7c437760b5a6686f052c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0dcf918ca2ceeca84f1a34835cf823f20fe3053d973cbbc5a5d6cf4307d3714(
    value: typing.Optional[ServiceUserParametersErrorOnNondeterministicUpdate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34fee83c66ae5408b7de8f479a94eeb37c51443bfe262c79166eade2f825878(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f3849552e0e96f348cd2948906841b17774bcb27dd7e5ef8dc524773afa6f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ab21c90751f1c2e9c0c62b24771d66145039ff14824cd821575c2f905ab146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b75edeb14da4ca63a378b6262bb00bd85cf8ec458ba73b8b5b6c5a82e9c30d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028e91e0c45d811ceab873a7b1754cd45957f2050d014d67f44c33c303fa0d3c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a9ef8d8e15fe7c998910525968234df7a957c2871e5e6dc52278cb24bd2612(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0ca77b7ce52f0739883c18c51f1e1752c22b60a8ca54bd3c8565dc7c8e9ea1(
    value: typing.Optional[ServiceUserParametersGeographyOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af96fdef0fb67e063ae1846df08f74b20a61c432a1836fb5df8acbdc796cd9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332cc7bc855b63532fc7af7c5840fd1acb47ee3bf29957ef9dd914fdd7c86787(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bca476ad62217b7345aebc5e98858f6c24a46c7ef89026e0705dce98409577b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68fb943955b538758b8ee5130f0606c6b454f25c8493e027da84483ef0ede60a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fb7394512d97eb023a5d8ad9a1c99ce42c4b98a6cc8e3dc9487da16a805c50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bab143c46f1bc86394a5e5dac5a0ba19861987c9879b9c8b15583762ecd02e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8758125ba267c0368f4a9b0aa48268ac7b9f2d6eb5ae688bb95aa93b7ce65089(
    value: typing.Optional[ServiceUserParametersGeometryOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acbd0ebfb1b1e143307a8c7fa86ddb950e46bd0c5c0446b87d5d763b6d003f6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8c8eec0cc8dc79f6ef52a8156380534d6ac3695bcc819bdb0f02382b959aea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa0acc48643e6a02272603599b839008a48d4b72d414320e0b98eb4601f3f26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cc8bc6ac2e6be0e06791eed281a9f532d66a75bbb7346a78631aab7a3ac831(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2cd08afa5e2e06bb00cd06ead1c1073c8fa4924ec3b6629a722a54253f61fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c531c4b6ee9888518d80512a827c00338454bedf7fb3d2c34404345d8238da00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b29e8d3cd4f9366e1cf9048de7686e06a390f72033dc7747393cddfa80393d(
    value: typing.Optional[ServiceUserParametersJdbcTreatDecimalAsInt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9691a7eb3f49e7750ec3f0d855a36e82827c9541c3ea7230b2aa3832a3ff6ea6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4792c0950aadf63ea18feb2f5c236e17012598d885da9e9f70272474edb776d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da6395e9d24a07e974419439f6eb78839c6e2f320b68c06399c875fe9f469ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77cb2df568bdb3a5f6b774d9651631bd91cef6810668cabb69f6aa72381499c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d7f221323d731b0fc06bf47f81a7d8fc90469bedb1cdc24e8aad3f49d9ef05(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22364a902d1bcb65edfd0cb675b3f39036c7e53deb1b6a5753cc7034566cd24b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e1ef7bb60b2bb760c15c8f312537168c7d57c75d793d0b617221f294193165(
    value: typing.Optional[ServiceUserParametersJdbcTreatTimestampNtzAsUtc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482e89fbf6fafcd7586b5fbcfc6d01b72aa29923cdd30df6639a1be0b9ab2803(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a572a0eacd0c6b721827ea67985562be98f02f81020e297ec3c3effbeacec35(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2f10bb9f7639aa36b1685ca757c00812094d86d47d2fc4048f0ea677b2f77f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186342f99a23d21261024085ef03d3d321f77aaec5fd4c8f19263be046b910f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037c9590cb6c90d3e599f6dcdb00e466efee733a45ba1edbbd40987a64554cf7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e893156679a1a7f17ae218f64b6989d4b95513b44aaee19c7269abd0e2b7749(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45ef8a95b5311fbbb9bce391c74442bce09dbe6297353d7d2bf04f4f9164d53(
    value: typing.Optional[ServiceUserParametersJdbcUseSessionTimezone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228e35717cafe2a83997e8b7256ba9a89ae9f5213f2058d41b250bdc53820d37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61344ba55db207dfff1c280528ca58a8b56ea688edc5f9aeeaa18b34c6ccdee4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd327eb7688ebc2ca108a2472681fd8fe641ad7be1a1ae8acb0835088a349703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e84988d7fd4b2baebac3dca09fa9a4fa4bd548cbac06ebcbba5c0c0775e7ac1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2d5e7638b2bcc940e9961cbbb096514e0fd63295d3b3ebf354e11ab492b2d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f3eca147e02b4e7dc710eb7c95643127e16af68b795513c207103ab9c80325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cabba39ba061167125e68a5e9d725b974c66a0736a4de5fb6188f5ccfa47735(
    value: typing.Optional[ServiceUserParametersJsonIndent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d709f5f30d9d5e0b1135e77c413c79fb34550438134ee3359ac9be1c385c2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8214ba428d83fa0a48ecbd8095e65e0df991fb0242b84b1d0aa28e04b52b21bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a224af9297cb627529143a50bb5cd84c752b3aa3126e78b98050a2b899830d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6dbe73a54f05c1b77e5a38bb656c46d4b6704f7a564c3b7c5753707e82c300f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b0fec826b7d8adeeac10e99d79ccb1bfa62cd84e81f5bbd39153b095d5f1dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d4a2bbe3f672fc160234aec4a009782e285fdd4d72eb2896d52a371440b2cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95c6e298ab9b435ad55eb40fceb82ade5bcea12581135503c4dff4900eddb03(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105877f358fbb8130e6fb2515bd65cc0bf0fb7520d28e2d387e3b33b2bf04e6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd643c0637d44dd687d0cc792e26af34679969609cf6d80a68204e18f4c3fe9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56e873798e815d8a40974414bca1b96e0a07fc965fd81d3d04af5134dbb9f24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed815f97ec92dc65f85622c37560a67698e2ac0d1e8af1675b17b09dc89aefff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc6111865127445b09a4fc6e499e70e86ed3c931c062bf8356cdc6e7b036d29(
    value: typing.Optional[ServiceUserParametersLockTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cdb888e9c1d43f169d18ede157eeb7e5611d7eec87892f35bd3aa5efaad546(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1029abfa4eae0e8a5dd22569abb5df39b4d5280ed9e6677b5786c25d1a73f73c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5adc37049a748290143b61c220ee3eddcae1bef6b00001957bb514ceb6497f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2291b3490891e5b9931dcbb8fb3c33960f92d2a4cc2095b90116a007c188305(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424d17076210d9ab1793c18f6d38e53bd4099dd3f595d895ad4240d4cd7759f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630cb629185959d055ace4997e9ddaf722cc3706b0c39894f56d5b7de7329853(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b2d4342ed1dfa5dba69f3ce781c1fcb86fb8f0564b7928df3018afa23d93d2(
    value: typing.Optional[ServiceUserParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1192186428919511d75d8a06169a87fdf48d459cec20dec8ecb8dcfb66afd6ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855467a6e4aa2bfdc5eee527c337a060639388963da92779515e3b103669b03f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441464f02c643ba0c214b393dd768c5b1be2e0d4ef2059ffc79f85ece192600b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5822596ab5c5a43d7552b66042ce2004083bb22ecff693654e24071dbd7002(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3206fd4a6d850e08d0bfe4e03754e37255bc2f24272d021ef65a848c0ae6d43f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6a2ab0cffc008588a2dad136a45f04bac954c70f62fa74682e9914f628b4d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29b8976dd3078e8c402aed8fcb98f357e6e79d677da95688783a0229e7526c0(
    value: typing.Optional[ServiceUserParametersMultiStatementCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45bbd3ccab6714677510a254760f536d3d2b2035d337f120f8c9a01b02f8dfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95de8c38f3df9376f3901aaabcb3a073c9e000f221dde08216c25e35aa35fde(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2789b72b46410f6ae071b6f20b6480f8cc4f8797288fe8c7c61f3b1fc7136ed1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4efb7f893e5623cbce4157be0a6e6513cc97cac05f6f2de65fc18caa331b9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e337c572b214e0fe5523e69a3edb494adf92fce289431d5ada69ada2806419b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a336bd72f779714c0ebd9a9427acbc5b965e858dfcc5ea64fa51b5af6a2ea95e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ed9c2937c814c28cafd7d772fed2bd525ee89e9d81b1d77a2d7bd416762b73(
    value: typing.Optional[ServiceUserParametersNetworkPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960c9bac9f8c5332b2231aad2379599b594800bad5af9af98e43e0712cb8d5d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a610f9d34b0ba13c66b1e69f482b69442494568a817d9306985f0572fc5c44(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588f822162878548aae1bbd4a039be6aa2d1adb91e9258e9548482d3edc9e6dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7e40edee321b88b427850c7c52804c33766728e73446d4fdc305f08d55baa9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b188970b8fe5859018d26e2d9895c061f69c1ef6ee27fc0434a2c47dc760a33b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992c0ed72ad2c1f8bc7751370e73b59c45f6ca80dc6672837384d93df8594fdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e414f41ead74efe6d5c8a8dd9a3d80424dab6741558662622c8b061712ff3ac1(
    value: typing.Optional[ServiceUserParametersNoorderSequenceAsDefault],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a41285ac977a24590662d2b29f51e88c5c549db921bad825df300a277d82e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb73e1fd6585eee17a4171e385fb3f0c5d4ce72975f0ac00f31926ed4d9a9ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfde877e3671d6a1fcb962a3b7890665d296cc59273c2b58b33c2eb72e944864(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d02b2a1f0495635b1842bf69684b9c2d4f6af3aa2470ca95fc701ead3f1200(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c590f7d525f2a5a977a74af52368cde632a0ab61b7676d028eb53ef7e5ced76(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c1a2b82828065fc9b180a563db3823f460c43e9ef25a0233ebb206286a2e02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57ec6af373624b1d5bf8f03a29baa4be36f04de02e813a6978949e01b82e765(
    value: typing.Optional[ServiceUserParametersOdbcTreatDecimalAsInt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186378c31f754ab32ca8e0680b8bc0ec96601fe50f766318e0667f1744fb1e4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddbcf177e566220c7439925eab3af5d57550e4c3826feb005670089c2599eb8(
    value: typing.Optional[ServiceUserParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3b060f4e8c713982f050d75ccce32c143a04f24690bbe0b09897d75b947ad9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e59cff2722abf775c13bc475772c6eb52b5903341ca89762cacc43899c556c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d120448fef62a554ea19b5d3b56289bc5da153979cd7142c6308b692a8537ba6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca8f564f3866d07822e61aaac10081448efd3a9f8eef94b3096d956b2f6bffd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9351d39fa82a7c0ea2b087750390b76db8bfcf78bc4ea5d0a59ef81d07913a1c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577effacfb94548e3f2139ce1910e58c4a653e6180cfba7ce009738d9d834ec0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8001eedd03f73be4691f7acd33c02be557a2a90cfbebd51d460d185c25217965(
    value: typing.Optional[ServiceUserParametersPreventUnloadToInternalStages],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b210069dc5264942291cf2bd3fc9524cf7f2fb6aec044d0cac997331e0d4a6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fda6da73407d822622ace79c08e47adf5ef8ba95e8f946cedd56a5a8a87e86(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1060a88004a065a30283b20e2041fa26f5eb626e9a08f150b298054a20b2a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbab72bb5dba2f5f24fb1596b1d8b2975052b9fb6d030b0fc9a9ba89ce1e4e87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5098acc0bb6816a4a53835ced7dfd07dc7b907fdf07aa105f386e9cdc2c22763(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec34273344c2b30bd6b2dcdd6175884ec9e3fd7f87ade7ed3a2e630b1f8fb60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ce78e687b220fd5441d53bf34e58a6495d6dc2a886a24024538abca462e792(
    value: typing.Optional[ServiceUserParametersQueryTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4d960d9e15c0461a94f0e755ac400bb530bcd03519f098d1442614f3e95be9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d0628eb6cb92c32b7c992e97215cdededa8cc290fc584febf803067012cf60(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2148194eb61a4e4f28287c05923a090f590e7fa402f6eef8aeae6e4a72f3e8ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3650b43bdf6f3a501b9236f5e50cecf4ef7460ae972add998c78c30cad6a67f1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b0a283ec3c11487aaf4f0d7088d14d1a1972055967e73b9d49f2688284c853(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc21a72d69dd328a7c4887307f5301643449e86e9ae4eca9c6c5c11e8e5662c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b1ffd14fc45f85e296568baadb21dee65411cb1b6d7738f0a5f444eaec17a2(
    value: typing.Optional[ServiceUserParametersQuotedIdentifiersIgnoreCase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f5ebfababad053bb8040fb6e92ef0552d815c6648b07c24efdb2d1ba14e70b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2205c35d988af3790079725f0f44bc3091896b0a3af3a472019c19b069af0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d407e021e91290b1c8ad9967137af39c8ee88b641b90238a931dbe03f8752bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19237fd3e2b51ef36817ab17b041a78716fdecb22fd0461cea3bd13ae6606d7f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b864500f12deebb9aef4a8fc2dbe853de30e8de507d8976c5b1edb88ade96a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284f3115c51c50da081bfa87b05a9b231dca9d2c6ec5dd37723ceb46c303448e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e88dcc26a84c89d435e842fcf131ac72c438cf956892c0cc832982e9b0bc6a(
    value: typing.Optional[ServiceUserParametersRowsPerResultset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd3e3f0812fe2f3eb2b41e55fbd1503d227faddbadad4c48f3a1f812c4d94ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1215793f18e54d8ba0ccabfef7646be94e58301bd3764d30294615d277d9a6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd92d48383cee3aababb7a200f364e55517fc32eff4cec9fccc8b7e27e830ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a44227fe85c19a2e5c4633fd366612af9fef1d87e3e4cdbe60fba78600558a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d7e78cdf517dc2d77905a42167cba5d24bfd5188a4a0de484cfd45bc207989(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab1bdb7edd6382de477ea97af9b9c99facfad88c7fd7feb22fced3448fe5756(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd8718b4ef8578b2e01e15609e41e5d78faa8b703977e5a31413cf4aa722ebb(
    value: typing.Optional[ServiceUserParametersS3StageVpceDnsName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48cc7b7970ecc70ba925fa376eeb887000f4089586b54971d17ec1204d1f27a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67a95a03c3c9c7337de34d350cb4e78adb2ee465bb8fd9a5b0d6a5cdd26cbf6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158caf3e6aa6a4ee349af49b6c35112ff24c3df9e138e8c2ba23705306c2b687(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5f7fa044a202e9cec3d51c58d5cc470c94f4ba181db9aa9654fb094cf81a0f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db21b36844be7374c115d7480e75db10a6bcbf6ab3676410d10616d50ef2e941(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de756d425e52f5ccdfd615886edbb6046a54a6b8049b1f99d546a5d8643aff0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1339f090fd1f3dc3a2a2d811a77ed90d40d5cd2ae6fa56b898de77e051bdffc2(
    value: typing.Optional[ServiceUserParametersSearchPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2404830596b04998df9d857e3ae10ada40ab0ed75366f114bc929bf8d95008f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bbb4bb3c366ea90318133630aaa4ee9dea8179ecf926bc07bc6ce22f46704c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4c8148835e52b23cd429e3aff146532c372f087b62d50c76e3513a0d730bd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30957679e1e393954f6e047340121a1014c2b4dd5bcfb29c5b54fec4a858d38c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07744cdbdb75c7ddde4385ad218a94b97ff2c98517379d6f403d2bc4ba6a0089(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d4ef9692c8a805b3d8bf4c8b171f459436b27cf83888dd31d72ebac0bb80ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb3336b2c54bf0c6bd56cf4a36471e640c5682ec6cbdcb4060a5ceb396466ae(
    value: typing.Optional[ServiceUserParametersSimulatedDataSharingConsumer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1940b2d5ca547e5cfd276e119c54f8f57248276e6bc5d7521949673f6068a994(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824ae1d8787036e63a0b79b22470b05db0de074515f9aeb2d47832b210258bef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1496d3995fc09d59fee2af5d8e9b019888ddb9e3cf6574ede47d8638e765c8c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4d9cd3f829b33c62737493928d3f825bfebe098253c3090f54a262be49eb31(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02eee590ec844de0a9f829fde394bbf07a493e1db30040c041132a91d3c5bdda(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad915e961552ff9df6ed15b1abc5010a558c5906d2a6497e66345db6deb21af0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c8842bb0863c1ff452e169dbd77658192ad57eeb70791198c472b5568cb12f(
    value: typing.Optional[ServiceUserParametersStatementQueuedTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf58861d8ec3ed57ee88255e0d2d576812185b6e6f5cbd74edbfe363f33fb946(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec4300f548803495eb9045716a6822a1ff3d52c4f15b0de1857074501e482ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7046f8244460b7f6df031f877261f7d038ddc4d96fea976a1f24ba434387d46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513c4a23a26b4696a5a39adbecde170d4a5b38c8f3207da79eabdaa0b3cf5934(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f611ad742014c19ec1d42f7a14427f4045dd1484cee5b4de6a2d676ac9dc0d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6a9cd23dac4d1e10bbda552c4b69bd9ba623c23b8a49f1e2b626a6c90a707c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ac4e07fa5fee171d6c456dfae043369a726ea69e0d789fdb39fa213b3e6d19(
    value: typing.Optional[ServiceUserParametersStatementTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3e0419aec664efbf6cec39099bf1aed0a40d48327689916b039959a84113dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0d1dd312c8cccb18ea13e419d3413252068b52682a7881639c20a16e6f1134(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ec652d25a7d8e9da103dfaaebdd098dd5381c91c92684507d20d97e77e900b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89db7a9b8646d6f8c1e4331e2bec37821728a6eec617d3279447a5224c8949a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ebf59b4cc15a85248e90543761157967c5d6733b6c8e2668226d8ba2e75613(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885d824726f1aaed47f0e34a1b65522a18539dca0fba7a4c67b7224eae325e4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45509088d9900f05624179de75a0b857d8b842e128b121e82e2f8aac099149d(
    value: typing.Optional[ServiceUserParametersStrictJsonOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a738f72d49c2a19b7f66c4d7ccf7fdd15058daf6991baa916bff9fb8d59c11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086a9e00b19cb1980a950184ac9d2fa4bb282fd6581ef2214db0c5a7e375da05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825a3174a3b20507cf35ff119b54f599c88b3f73427118b36cb85ee55a955ef2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c088ed9b9b1a3742978290e48f29cef869f61ce1738fa209a5c974f6bb26e232(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb25373788192e583a10519480cc869d2a45211b070e3ab257b42ceeadc70238(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3540bbc60ac23c065bbfade5f17ebd5077c92ec0c8ee2034fccf19cb515b369(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b49b35c42ae7de3cd645e22bb639f9e0050cb72d3e181b50d697b7a5ee953ad(
    value: typing.Optional[ServiceUserParametersTimeInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69d10456cd2a71e2ea6d0148da46ab465b43f6ffcce6d80cddaacb0035a1b62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5f968be61dc9138c2309da36511889f64dde703080c9e8b1f6712d0253e0d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d047c9c03e0db1a1144cd71b82dc50149554768d6aaf7dba4aed80b3b7664560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c51f484df773ce6c7709ad8818be5f7470c9fa6eb3d5d6b86e05fe33026a093(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d10d9105733636dde28bdc3842214162be05c04f0a411160fcbecbef17ced30(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4744d468bb00d34b59bf75e605a5798741b03a0b5fb2757eec38b4a02254d150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ac1b433010f637f9e689c24423de3a3aea9ecf75731add38d70f74888586e9(
    value: typing.Optional[ServiceUserParametersTimeOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eeeb82853d14f11cb826ce9281e4bd9216d8a9a65e00bbd925fbb75a5f517f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19299ea5819a7d1aeb8884bdd123a9505ad802fc3bd2e6c0c4c7d62323b80c33(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b58d3c1734e11d34105c61122ee5245911e7319c8384374f6595c52ec827e74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96c82788091ddd38a7311954840bba8779276e814ef4815ef4c337477a69183(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1771fb004bcbefc74e615050126e0545c7dce909a222af54e7f67cfdfd585a6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236d88f8505b8943577286b1467da0125be21225f983ee52615e6c20680adb8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9dc9ab291c2cf3d2fd64a6f7bfa27f40c5f37dbec1c30c906a3850c6c3844f0(
    value: typing.Optional[ServiceUserParametersTimestampDayIsAlways24H],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0db0371f786a2cd0ddc55bbbfc96ee91522d49a4843837a659469efd781c6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d622bccdcdcbe9fabf507dda75069d445e7380186768219902f9a192a4f6c3ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252bdcf4ba10f513da4ee0c69db19f5a9b26963c2b648a060ee704d16d0c9bbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c547c16975aee52daf2a98502313ba658c9ee5faa8de22cea553e34abf1f38f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b4a41a6b8a4e885da3f9a53e2341cb48f0f7f3abead4e19e1129ac24b9300f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8649d493eaaf21d710638bcb07640088da060363501117a8197d2379b9c52a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cd9bea40fbf5b2fcb615b56496fe41c49178784398c3096309522e2c815e18(
    value: typing.Optional[ServiceUserParametersTimestampInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65815a775da4203c7688a1503dad5bd4877b2193fd61c6e9ab39d65153bbd100(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f599fae9426f57a38d2ca8322138267c1ae41bafb6f5af787e7009bf0d4a18(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265ef48cdd3d6f6b41bae5ed48500f96314ab5ad9c5be93fada6f810feb84975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3c9d0bee012dfa117c570e9d81d2f94b33b6a1b1850dd6bba9451eb7af58e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27187f07137ca9d7376ed6f79006d6c8fbfaa8d48b946c82f00e42ca8c14465(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f077d5d5fff295fc7f1d4e6b38ade0eeff41e3e3f0e89935378620658bfffcfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0f9b82d9b6150dd834ed1403ac9059dc1016e365a1d11d3da44ccab6a07926(
    value: typing.Optional[ServiceUserParametersTimestampLtzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35aa03960fbdb792d118cf22cace2b55cfcf6bfdeeaf97390a0b615aacc9f89f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd5d12b3b7cf52a4dd5063439e86346db21c2581738d0835a782722e569b59d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb3251c234fe20d098cb61f8a28ffe56749472b58356559f1b6b9d4d03c128e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14fe92ebaab27b5821aa2140d14fffa7697fdf4d58cba601a8094551f1bb843(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacfefb1585f43cde9cd5f1a0dcdcf90ecda63d3819791c8f8c9ff649ec66fdf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1ee72fb623a1093b727675c581c18dc7c7a6b88495fee7d19349cae193695a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a325fc6a8f425060794ee323668bd24182aa89f285ac1a2381e60f844d1dcf(
    value: typing.Optional[ServiceUserParametersTimestampNtzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46688921f26543f08fafd4333f014c554c769b75bfeb5ee00067d8b59c534c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059bfea9267e4263143cff692d9997655a9441637a207898abe13f6af258462c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4050920a86ab1fee17a9683df4f4bc4eafa7caaee79026e39abff80f82448e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a8b65edc19f06837cf05bff659835c752ecc3e68fcc753b476231edec8f5c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47afc9b2cc025540d43436d704af2a1287a7b27ed6bbdc5f1ec7cc8ffca54ba6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b483a13b4e852aa510991f380464c9ee023891985188c398372f436a613e9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d77016e3654a787b61f70e5ed014aba6a15c5952169d8726e95860b5427bd9(
    value: typing.Optional[ServiceUserParametersTimestampOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac8724a5e8fba517019023d28b93f76775ab3cfd4ed3e2dd3fff3dcb15a51fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855ac7492ea841a6a6b63b5a17378cc1432d72ba78bb544ab6879c489fb77790(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053e1527e27595597c51755389758927e4a664e486c8f0c4052ba80ef9779bca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bf54ddc812860433247675a90a4074c78beafbf3d7388426945fc3b544a9c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec3339d7c25d3b904e9d35164b6adec37f4ab914a524c46558162a6eaf25998(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e16a9b105feb2a76ba1b8c5b28bd4d97cae1d80c39d9a00be3209ced10e09e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af98b7e336c2cffe392e296dfc684d0fd2d0eb555dbd5e998de5eb3fad92eec2(
    value: typing.Optional[ServiceUserParametersTimestampTypeMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c80556e32d27b99086e0578908a8324ca6200e0cbbbccad0b74c4da2792a52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d988e06aa17cdd8cd925d6c0a9161b20ff9b38a074740ce58886de09d6f45bbb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac52345f6a695be9c7df90fd798a87855cb17dbdf606ff85d74063bde223f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873e306d96639b04f9383ca15f4cd991a41a8a730dcf95dfdabfbd232de6bbe4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bd7a15844c9a1f1ddcff4bb5af46d441b4030adc2af8159ad74c4396d26e48(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d286a3566ae87b0c6bbb87433167bb824d950aff1ce40b8b6c9fd1692c4bc13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0d5e2240f86c7f261cdd45b4c2461ee067fd82f711cbce2dbb9c4bc5bb3779(
    value: typing.Optional[ServiceUserParametersTimestampTzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593088917a8aab14b1ccc8ff8d23440d70f92a847a32234b2be014b8f456eb14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee1e87f40345eea6ace7d3a172ee9ce3b85078d3be9633032c4ff4b2c09c857(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fc1f7d42b665b09bd10b336b9de8f0f6e4681c628049bbe319192d50b4bc39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f220d0ca504d208bc2c28f533399b064df1f96a4247bca5583ca6656653e3be9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea133b544073ff47a3d75f1d09300d9ee805186830431c075604590956a3d5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9900b45501f7e9c0898f5a039135a3ede779ef552e44aa9f15ca92396cf976(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef73bec62243f91f826a6f32f423c186e23856c4eb0d3f72c66eb76e034f034(
    value: typing.Optional[ServiceUserParametersTimezone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70631ee9dfa7a4356fdf7fbd1e8df02a5d1d8d720873a437b1f5638babaadd37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1345018221e3d2daf10ecd328b614b1f7fc75f4cb9f3d18ca51e27f2de9c4bd9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be60113e9bb98667678ff4f2a5fb78bc7c02969fe7d0d40e225e3976263df30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6f0770df44037a5bde6d80a32f59814e3d17483aca2beeb0d2eae68c737bcd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513132649ec345a03b20d38442fb2f9ba7a2b856cfb8f296f2abcdb6d6d6264e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd2659fffed96b88d37fcd070fba5ff28039d3a275248f2c86ff84fa29099eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d69d6dd98227751193bc30ae28ee079bb372d5739b64abf84ed28841aebf03(
    value: typing.Optional[ServiceUserParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f603a93a316f2a8d939dac83fe5cc4d1ee82f77b4c91800800e143b5e68285(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478808bec73f97aa7369f881c79410cec11c75c4dfae24d8745d8b07b6d2ca91(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b447809743f5d1fe85b2b2c8ee8c1995f58850ffee548aa87706c480f350b8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2efcc187e7573b015688fe490f1bdcada561b27fb7a613a0105ecad5fbb7d5ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c6825e0519116596c28ff731860805a77bdf2fc47c8e9fa2f7c1b58d918f88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b72d60ddb333d9fa1c481cf5cbde0d7d6e62189fa59af38f04a7daf294c3f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd7e7fd4bfe8dd7ef6c97bba6fa9b40c01c9a8bbfd70852c898c9ac1e8b5b32(
    value: typing.Optional[ServiceUserParametersTransactionAbortOnError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c7b6157177ee6babfc8a3326c78db19c4e1b50963ad5dfb1d5edaf437a2c33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd779a6176dc335b737cddbd326a59401e5d0a43b143e5207023ba85ae1b21a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4af106baa0f7c0d1ac3e1df8640bd5f19facdce637e92efc008aaed5546edbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f53f8d49d0cce89f9e665bbdf080557af8a70825267a51cd9e9bac7a5dc6f6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d40fe7c87f78d3b8beda87005225109be3fcfd316d9e29e402d875fa723cbe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c85f7ae1ee5629dcae43aeb01aa0be68b0dbfa6bd0f38a787e64594ad7a4d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8c94b3278f12b018dd549a96740d6fb7a7c8cb8efdd53ba7dadeb4ac1c4ea4(
    value: typing.Optional[ServiceUserParametersTransactionDefaultIsolationLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b44e4f48ec97132bf9c5fe602c6cc37141cf0e84ec3560cbdeb151a2d99dc98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa010002191c27a30cd63c0821a87e044a84f1a94abc8d2816736cb2482a62c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59232fedc9bc20c908261acafb5b1577548c9362ac6668c19975d19102102922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906c2117e9bd59114635111b712a2f840791a2f62c7299a8a8198c9ad0c43f7e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3e63d85dd762c073e24c3bfa584f684674d002324faaf8b77c4f7f91447680(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfcbcc0c0ecb74b8adf45d7e4b281a26066fd950d0fea76030d76c4687cb4d6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2130d86709252cca63c6f3f5999804bc1964cf5a7a93161158c4963823e613c(
    value: typing.Optional[ServiceUserParametersTwoDigitCenturyStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d44628afcadd0c65794ae545e08dda1ae4a769292b79aed00aa4794cd96b2b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff32e79ebe79a1015518d190aca12e783666b6b4cb03fb0a3d7b7a269ec1e818(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9e74d35585ac72fcbe7d444d68eabbb766b609a4dff4a9c1d25e186012a4c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90340d618de64b5e9e08b3265553c64fa52e3aa679c7f58abdeaa16e1571069(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a08464f82844358a4bea3e8fc13c87793395a29ec1aa960b72711cbf6894bbc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de55d0f52619c08111821752ebcedf7bffb8875139f6dc89ba14d2b6af589a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ce0f389fa3e8bb472dd9813bf128c9ae5ca17d7a7ccf8ce51e6bde7439e427(
    value: typing.Optional[ServiceUserParametersUnsupportedDdlAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768fbfc5bd988558ad7ecbba6838381a68d4705f3f165b591529dba13cbd753f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd06b186e5e874c9b0bc28fdb3ca3568549948f741b05b5d5a6d7951e84399df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f430d8b933cf816fd67a60fcad808c2787859cd1d4a2374618c38f1ad7a8c1ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfaf8e1356a03c9179676731730b90fe3bcd9226df73d2844821b2848ba2e80(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c0031b4b39a2f06b3179385a48c26f51f377a06417dc80ec856c2b4ffbfbd9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f134636c721baeb9b2dfc86b6e46c84a0e60e3809b1e9b594c3cc26f103cb290(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655c9e8709b5cb9d30801c091746754d7b274ea11020208c29baf3053cb10bb9(
    value: typing.Optional[ServiceUserParametersUseCachedResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b101235b7455cc882f7e3dbeddff342c9a00709182ebd232b7c51922fcffddc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e6201da6e316921769b6651870af315ac2f655f7b5b9d2fed11e911e4b588d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7c24a5c07263f4fa16582f037e9a7a3d38424383f9ca51618101784493944a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16dcf7b4ad0b386aa2940b0d841351efc1b54fe6df2cd0a764a63dc8c55f263c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70b8418c92d0e7abb436009ba63bb6fa981c89bea015f3302660dfa57469bc6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4c240da218007dce9106baf8b7e5b53dee7c9ef3d42b5dd9309c1b5c427ff9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0d7f2a0135ab45a4a51eefcbbbfdf1c06efd00c9e713390cb614ed17b245c2(
    value: typing.Optional[ServiceUserParametersWeekOfYearPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c83b4a7a6f4329104b9d0acf1dfe9374ab1413a009b7b1ab2f1797a786983c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e198c4c69b1aed615687add77b9002a8f76a7d5a14dc3a1040e1e10d55430f9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4989b814a9e37d7675ac8f01bf01df21472fb4d97e932cbe336e8f22ea22d36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12d26d115ed9c58e0d0dc815ba62b186b56737f6c7043ab225325f8e32be8e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261f91ad3a390ae4decc9061dd68f1723ce6eb4b97685af116a0e13b1dcd0681(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b982e96c7b450443340419e6f813770d242375848e0b0fd7d41567616e4be9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99af3486c07229ad1f31ae3541b632a0b26bb39909393a8c7b95ced5d50355d(
    value: typing.Optional[ServiceUserParametersWeekStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259c0e188b08d688677bee30ad2c903485f6d69532739bb3cfae23ac1973cd59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d65df2451e779599fb746b2763df9cc0fff5b812f2e2642ed8bebbfec3eba0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d85c5d5b3aaee9cb6dbab158656cc5057c7fd90b27959e4cd9a931b8bf900b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4773de7c6cde1590cc7029d6ed8446a317a3dd6ac547af1d487a9175df6e1a90(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b534a3d3d256ee23ee822a754c05fae09f517e1332bbacd2bc70637f85beba7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354d7ef3cd88596125d9a4b35c0ab6c3731b3c5c95e388a93187fecc4570b323(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e9a28162e0a85abc7ff75d5cd0a06c50e40af0a750ae7531714c7747d845f2(
    value: typing.Optional[ServiceUserShowOutput],
) -> None:
    """Type checking stubs"""
    pass
