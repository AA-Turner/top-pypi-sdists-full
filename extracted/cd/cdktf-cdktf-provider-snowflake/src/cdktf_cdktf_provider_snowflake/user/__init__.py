r'''
# `snowflake_user`

Refer to the Terraform Registry for docs: [`snowflake_user`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user).
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


class User(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.User",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user snowflake_user}.'''

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
        disable_mfa: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        first_name: typing.Optional[builtins.str] = None,
        geography_output_format: typing.Optional[builtins.str] = None,
        geometry_output_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_indent: typing.Optional[jsii.Number] = None,
        last_name: typing.Optional[builtins.str] = None,
        lock_timeout: typing.Optional[jsii.Number] = None,
        login_name: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        middle_name: typing.Optional[builtins.str] = None,
        mins_to_bypass_mfa: typing.Optional[jsii.Number] = None,
        mins_to_unlock: typing.Optional[jsii.Number] = None,
        multi_statement_count: typing.Optional[jsii.Number] = None,
        must_change_password: typing.Optional[builtins.str] = None,
        network_policy: typing.Optional[builtins.str] = None,
        noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user snowflake_user} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the user. Note that if you do not supply login_name this will be used as login_name. Check the `docs <https://docs.snowflake.net/manuals/sql-reference/sql/create-user.html#required-parameters>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#name User#name}
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#abort_detached_query User#abort_detached_query}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#autocommit User#autocommit}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#binary_input_format User#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#binary_output_format User#binary_output_format}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_memory_limit User#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_metadata_request_use_connection_ctx User#client_metadata_request_use_connection_ctx}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_prefetch_threads User#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_result_chunk_size User#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_result_column_case_insensitive User#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_session_keep_alive User#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_session_keep_alive_heartbeat_frequency User#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_timestamp_type_mapping User#client_timestamp_type_mapping}
        :param comment: Specifies a comment for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#comment User#comment}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#date_input_format User#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#date_output_format User#date_output_format}
        :param days_to_expiry: Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in. This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#days_to_expiry User#days_to_expiry}
        :param default_namespace: Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the namespace exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_namespace User#default_namespace}
        :param default_role: Specifies the role that is active by default for the user’s session upon login. Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_role User#default_role}
        :param default_secondary_roles_option: Specifies the secondary roles that are active for the user’s session upon login. Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_secondary_roles_option User#default_secondary_roles_option}
        :param default_warehouse: Specifies the virtual warehouse that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_warehouse User#default_warehouse}
        :param disabled: Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#disabled User#disabled}
        :param disable_mfa: Allows enabling or disabling `multi-factor authentication <https://docs.snowflake.com/en/user-guide/security-mfa>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#disable_mfa User#disable_mfa}
        :param display_name: Name displayed for the user in the Snowflake web interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#display_name User#display_name}
        :param email: Email address for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#email User#email}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#enable_unload_physical_type_optimization User#enable_unload_physical_type_optimization}
        :param enable_unredacted_query_syntax_error: Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error. If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#enable_unredacted_query_syntax_error User#enable_unredacted_query_syntax_error}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#error_on_nondeterministic_merge User#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#error_on_nondeterministic_update User#error_on_nondeterministic_update}
        :param first_name: First name of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#first_name User#first_name}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#geography_output_format User#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#geometry_output_format User#geometry_output_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#id User#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_treat_decimal_as_int: Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_treat_decimal_as_int User#jdbc_treat_decimal_as_int}
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_treat_timestamp_ntz_as_utc User#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_use_session_timezone User#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#json_indent User#json_indent}
        :param last_name: Last name of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#last_name User#last_name}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#lock_timeout User#lock_timeout}
        :param login_name: The name users use to log in. If not supplied, snowflake will use name instead. Login names are always case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#login_name User#login_name}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#log_level User#log_level}
        :param middle_name: Middle name of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#middle_name User#middle_name}
        :param mins_to_bypass_mfa: Specifies the number of minutes to temporarily bypass MFA for the user. This property can be used to allow a MFA-enrolled user to temporarily bypass MFA during login in the event that their MFA device is not available. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#mins_to_bypass_mfa User#mins_to_bypass_mfa}
        :param mins_to_unlock: Specifies the number of minutes until the temporary lock on the user login is cleared. To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#mins_to_unlock User#mins_to_unlock}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#multi_statement_count User#multi_statement_count}
        :param must_change_password: Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#must_change_password User#must_change_password}
        :param network_policy: Specifies the network policy to enforce for your account. Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#network_policy User#network_policy}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#noorder_sequence_as_default User#noorder_sequence_as_default}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#odbc_treat_decimal_as_int User#odbc_treat_decimal_as_int}
        :param password: Password for the user. **WARNING:** this will put the password in the terraform state file. Use carefully. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#password User#password}
        :param prevent_unload_to_internal_stages: Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#prevent_unload_to_internal_stages User#prevent_unload_to_internal_stages}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#query_tag User#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#quoted_identifiers_ignore_case User#quoted_identifiers_ignore_case}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rows_per_resultset User#rows_per_resultset}
        :param rsa_public_key: Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rsa_public_key User#rsa_public_key}
        :param rsa_public_key2: Specifies the user’s second RSA public key; used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rsa_public_key_2 User#rsa_public_key_2}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#s3_stage_vpce_dns_name User#s3_stage_vpce_dns_name}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#search_path User#search_path}
        :param simulated_data_sharing_consumer: Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views. When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#simulated_data_sharing_consumer User#simulated_data_sharing_consumer}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#statement_queued_timeout_in_seconds User#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#statement_timeout_in_seconds User#statement_timeout_in_seconds}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#strict_json_output User#strict_json_output}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#time_input_format User#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#time_output_format User#time_output_format}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_day_is_always_24h User#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_input_format User#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_ltz_output_format User#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_ntz_output_format User#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_output_format User#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_type_mapping User#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_tz_output_format User#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timezone User#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#trace_level User#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#transaction_abort_on_error User#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#transaction_default_isolation_level User#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#two_digit_century_start User#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#unsupported_ddl_action User#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#use_cached_result User#use_cached_result}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#week_of_year_policy User#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#week_start User#week_start}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84baddd02b2eb7d700b468bb97ddf9f5a11245bd45b1f2245c8755de57d049b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = UserConfig(
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
            disable_mfa=disable_mfa,
            display_name=display_name,
            email=email,
            enable_unload_physical_type_optimization=enable_unload_physical_type_optimization,
            enable_unredacted_query_syntax_error=enable_unredacted_query_syntax_error,
            error_on_nondeterministic_merge=error_on_nondeterministic_merge,
            error_on_nondeterministic_update=error_on_nondeterministic_update,
            first_name=first_name,
            geography_output_format=geography_output_format,
            geometry_output_format=geometry_output_format,
            id=id,
            jdbc_treat_decimal_as_int=jdbc_treat_decimal_as_int,
            jdbc_treat_timestamp_ntz_as_utc=jdbc_treat_timestamp_ntz_as_utc,
            jdbc_use_session_timezone=jdbc_use_session_timezone,
            json_indent=json_indent,
            last_name=last_name,
            lock_timeout=lock_timeout,
            login_name=login_name,
            log_level=log_level,
            middle_name=middle_name,
            mins_to_bypass_mfa=mins_to_bypass_mfa,
            mins_to_unlock=mins_to_unlock,
            multi_statement_count=multi_statement_count,
            must_change_password=must_change_password,
            network_policy=network_policy,
            noorder_sequence_as_default=noorder_sequence_as_default,
            odbc_treat_decimal_as_int=odbc_treat_decimal_as_int,
            password=password,
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
        '''Generates CDKTF code for importing a User resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the User to import.
        :param import_from_id: The id of the existing User that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the User to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72414f2a9320dd73073a9cfd82d56b9f7c834226827c1ef0171ee81418205d13)
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

    @jsii.member(jsii_name="resetDisableMfa")
    def reset_disable_mfa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableMfa", []))

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

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

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

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetLockTimeout")
    def reset_lock_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockTimeout", []))

    @jsii.member(jsii_name="resetLoginName")
    def reset_login_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginName", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetMiddleName")
    def reset_middle_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMiddleName", []))

    @jsii.member(jsii_name="resetMinsToBypassMfa")
    def reset_mins_to_bypass_mfa(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinsToBypassMfa", []))

    @jsii.member(jsii_name="resetMinsToUnlock")
    def reset_mins_to_unlock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinsToUnlock", []))

    @jsii.member(jsii_name="resetMultiStatementCount")
    def reset_multi_statement_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiStatementCount", []))

    @jsii.member(jsii_name="resetMustChangePassword")
    def reset_must_change_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMustChangePassword", []))

    @jsii.member(jsii_name="resetNetworkPolicy")
    def reset_network_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPolicy", []))

    @jsii.member(jsii_name="resetNoorderSequenceAsDefault")
    def reset_noorder_sequence_as_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoorderSequenceAsDefault", []))

    @jsii.member(jsii_name="resetOdbcTreatDecimalAsInt")
    def reset_odbc_treat_decimal_as_int(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOdbcTreatDecimalAsInt", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

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
    def parameters(self) -> "UserParametersList":
        return typing.cast("UserParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "UserShowOutputList":
        return typing.cast("UserShowOutputList", jsii.get(self, "showOutput"))

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
    @jsii.member(jsii_name="disableMfaInput")
    def disable_mfa_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "disableMfaInput"))

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
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

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
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

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
    @jsii.member(jsii_name="middleNameInput")
    def middle_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "middleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="minsToBypassMfaInput")
    def mins_to_bypass_mfa_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minsToBypassMfaInput"))

    @builtins.property
    @jsii.member(jsii_name="minsToUnlockInput")
    def mins_to_unlock_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minsToUnlockInput"))

    @builtins.property
    @jsii.member(jsii_name="multiStatementCountInput")
    def multi_statement_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "multiStatementCountInput"))

    @builtins.property
    @jsii.member(jsii_name="mustChangePasswordInput")
    def must_change_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mustChangePasswordInput"))

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
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__87e93bcdfd7b6764bed293b518e1b59b457368e3031f9a4fcf6aad93d27aa9b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65b409c8cf1ef79bfe2887a07d40ff37f47e3247c1719418f27863c997d9a650)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocommit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryInputFormat"))

    @binary_input_format.setter
    def binary_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c2abb9ede0c9b116746fafd63d3ee29566e180c76174e5725996045ea855e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryOutputFormat"))

    @binary_output_format.setter
    def binary_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086cbee761d1c461401a16b8b7ed80bb0a0b005606fa0426fbf232d8308ef03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientMemoryLimit"))

    @client_memory_limit.setter
    def client_memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e1715d4c53187c8531495d659de6bc119a9eda44360241c422e0964fae6da8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__479948a83f40ef0c892306e8c7ca74953d928ae43159770d729115ce3124225a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientMetadataRequestUseConnectionCtx", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientPrefetchThreads"))

    @client_prefetch_threads.setter
    def client_prefetch_threads(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07b15f09a62981f06066edca6ae58b59feaf96b0e938d81ce7b794a8c9133b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientPrefetchThreads", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientResultChunkSize"))

    @client_result_chunk_size.setter
    def client_result_chunk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b19e5c01b4a9791a0909c5aa2d998ab035a0004f4cc186dbe5f47f6c674a851)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b96f72bb9d3fecb1d12a370dbe04632b7296d1f2bee4c07821dc41301bbf6707)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30d4d7dc88c807e5c229aff25cd49613277f4cdf1afde0e1e322c0ea9b43c0ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAlive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @client_session_keep_alive_heartbeat_frequency.setter
    def client_session_keep_alive_heartbeat_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc45e18f70bffff86eed3c524bcedef5b6cc83da9b2009ab7ddc190d74ee228f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAliveHeartbeatFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTimestampTypeMapping"))

    @client_timestamp_type_mapping.setter
    def client_timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c3c4d66ff299eebe64eb9a243cec518d6fdd41e0998df9682e8241ab9ee931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c70d58a7dde72cf09c0145b794bb011cb77822b7c8d91de012cabddf0dc2f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateInputFormat"))

    @date_input_format.setter
    def date_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9536e78e0f65927976b89fd4d9eab104128d2be82cfbbb2fa23289ec65b236ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateOutputFormat"))

    @date_output_format.setter
    def date_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa118058c43d6bee6d11493315874792e30a8f7ed093203560650f33f0807a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysToExpiry")
    def days_to_expiry(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysToExpiry"))

    @days_to_expiry.setter
    def days_to_expiry(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4964372dbabf6810058499c379ac2f27ce63e96e383d95769f2090d2b6a8df62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysToExpiry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultNamespace")
    def default_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultNamespace"))

    @default_namespace.setter
    def default_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214a9ff205ee25636ec25f2fd215554275c9a32ac3378657ae75588682eed3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRole")
    def default_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRole"))

    @default_role.setter
    def default_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e767c3f4ed95e67d76786727e22e4670c693d1487eb2d8932b27be46669dd0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSecondaryRolesOption")
    def default_secondary_roles_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSecondaryRolesOption"))

    @default_secondary_roles_option.setter
    def default_secondary_roles_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37893dda19f1104c6b4021d41c3b72df1de285c29864ec03c9e6846c6dcdaf13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSecondaryRolesOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultWarehouse")
    def default_warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultWarehouse"))

    @default_warehouse.setter
    def default_warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f64251ded505f4cefd6d4d5a15536f93689a9c0ad81a5cdc2f1af931991f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultWarehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a755af3704f43753f2f278203f460cef46dcfaf3983e2953def6f033c7ec4c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableMfa")
    def disable_mfa(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disableMfa"))

    @disable_mfa.setter
    def disable_mfa(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e66f39f7cd562a553aa56ca25ebf629538e16c125550f5a570f3589ca008b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableMfa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b1a168967696bb92a92bf73717f80fa6aac4e483681eb8903630ad5a692161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3322d98011bab95439fe965e9f7921436ff80ae4534133e91799adc6d07a6903)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9383d8667c41020f11eb3eb8626a616f22ef62af000af450e17c66c47cbdc794)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f12677c5d41250e7176255d9e749098efae5c86a6ecb7f2f6c83a80227bc53f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__219020d01b499f4330de8601c7ed119d8c2b4d6de1af719ae62d17c4443f850b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__938e04c75af4ffb0e4cf3fc7c80861cb52f9ef74a8d7f425d6e5d85c48f33f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOnNondeterministicUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80b44a9d175599c1710c1ea47900e135b503a5f2a7b488e134a8149de564bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geographyOutputFormat"))

    @geography_output_format.setter
    def geography_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2c3a057fffb837f25650ce9914dac8c527cec1a77e6fff9878732f8f196545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geographyOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geometryOutputFormat"))

    @geometry_output_format.setter
    def geometry_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df1ce84483883a596f0d5b98ad8bff649dd26e4e5475ba7c1965d286f7089748)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geometryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee534fe04b85b73ab500205e9b2d0a244d624b079ae8eb269c0d80ae790dd1e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d10c40fbefd0fe09d300857685f44b95866b8952499d21bd18441a560ac2c726)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e857edc0e28f48da29720d4621b25ce6842a60bba690a2a5b524ba783aa197f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31deba4ea185aba9b475a4ac1dc5e0c1c1411e21040cda56cde1b2367bb9754f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jdbcUseSessionTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jsonIndent"))

    @json_indent.setter
    def json_indent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7cac65ac6bb6af35d68bf14970c3eb521db7997fede20bb7f1aa5dd1dbf7b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonIndent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0530543bda1184a7d929f8715889576a41c54bd5c8644b766fe2fc19dd25a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockTimeout"))

    @lock_timeout.setter
    def lock_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf526e77d8d1d92e07add7743c0fac525871f7c8376d82883254e72e0770972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginName")
    def login_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginName"))

    @login_name.setter
    def login_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd62b8766f563c8bbaaf20c2117ac094fe19bf602c1dc6abca677209db98a0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79dc1b87fa3f79c7cef34753b325791fe9a47f571936afb2c9a51293dd7b131f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="middleName")
    def middle_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "middleName"))

    @middle_name.setter
    def middle_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59b0ac0a85ab3df7b3b8fd6e69f65ea1c802431a7e9e2a4e532acda3be01de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "middleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minsToBypassMfa")
    def mins_to_bypass_mfa(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minsToBypassMfa"))

    @mins_to_bypass_mfa.setter
    def mins_to_bypass_mfa(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e33c28257d95ebd907f3b53e617be06076819ca7558e136b9dd223774f65133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minsToBypassMfa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minsToUnlock")
    def mins_to_unlock(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minsToUnlock"))

    @mins_to_unlock.setter
    def mins_to_unlock(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9beaf0b44f6c5ce45dad2add5e2c31ff4dceb768c62e2e6cfdfaf1dd1c15d9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minsToUnlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiStatementCount"))

    @multi_statement_count.setter
    def multi_statement_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79b7a596e67fbc1a570f37a8489e5d53f918bef1cc5bab1482a0d61c158eff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiStatementCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mustChangePassword")
    def must_change_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mustChangePassword"))

    @must_change_password.setter
    def must_change_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e87ca7689a8a9fc7bd76f1cc4572091cc8d1cd7db878cb8216171610932cb84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mustChangePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554b40f61c913aa67692d8d1364c59a569973014f8481649a24b270d88673a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPolicy"))

    @network_policy.setter
    def network_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090e61befe8290bb6bf73b79e730e2b8c0a66b55eafb0f4ed24f33c3106eb356)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57b69396f8e1f503615167d3823c57ea6c73fbe15273735305281b519bd521f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a34be85b5291e5c01b195774d5dede0f9ee294127b7f1b460f9f4b9a0d889739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbcTreatDecimalAsInt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c384735f0ac2a22cda9e91e8ccb6aef7e481039f3eff75233e4d931bd764d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__9d7b1cc04ba6d6692b4fb584cea69e4ab098a295c2283d54f344fc6e54accd04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventUnloadToInternalStages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryTag"))

    @query_tag.setter
    def query_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429994498fc2cdb2ec04e4b9680c7c2fcffe045c382a1743c4dc29f33010ba09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9a19865b06d8aa66297dcbe886f68e80396ea9a837b6aa349e941b596faa9c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotedIdentifiersIgnoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsPerResultset"))

    @rows_per_resultset.setter
    def rows_per_resultset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d25ca72e1d09b7aedcd27ea3b3fd930995583de3c6a6eb17e40a446bdbd73c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsPerResultset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKey")
    def rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey"))

    @rsa_public_key.setter
    def rsa_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfab7a98ff160c89e43e23358130c93fe0eacfcf22f37020938d9cdef3270d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKey2")
    def rsa_public_key2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey2"))

    @rsa_public_key2.setter
    def rsa_public_key2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e609e3a1336017dda59d661522b3f1323545c41e3aa80da6eb0016a37a52ffa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaPublicKey2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3StageVpceDnsName"))

    @s3_stage_vpce_dns_name.setter
    def s3_stage_vpce_dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae4e3b8a59e80d6cd786e25db7da41e2d297c7b0d456a3f828660463dc27deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3StageVpceDnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchPath"))

    @search_path.setter
    def search_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3591ec5992e5b085017cc066c9fe6193de0687e04f12064fabb717726448e418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumer")
    def simulated_data_sharing_consumer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "simulatedDataSharingConsumer"))

    @simulated_data_sharing_consumer.setter
    def simulated_data_sharing_consumer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2108cddc6f5a5ab163d764333c8f7c98c3aef7a9e3cc5c637be7529c883ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simulatedDataSharingConsumer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @statement_queued_timeout_in_seconds.setter
    def statement_queued_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be7dfc1020122daa87c78a32c2efdec4b014b4d811301cd9377a8dc746687af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementQueuedTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementTimeoutInSeconds"))

    @statement_timeout_in_seconds.setter
    def statement_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab662307baf8c5706aeaf4814b28713894fba4f03d5df46d166f07f61494c5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__292160608f24a88f04a78d99e74e6a09d44eee680b4e0bae46079d882b1caeb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictJsonOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeInputFormat"))

    @time_input_format.setter
    def time_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ec30799fe5df04d5db586e883e5b3a3bc83b6e256317347b611f06847f66fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeOutputFormat"))

    @time_output_format.setter
    def time_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281b5175554bb9f9fdb7ebd67da89a5a00304a5d57cb0e849ca889fca86a4a96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd91e8375139d63bbc4f0c650b01f28bd6fecfa59ae8dc2ecde3b15610cf584b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampDayIsAlways24H", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampInputFormat"))

    @timestamp_input_format.setter
    def timestamp_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac92d40ec65e0809cf9a2d482bffe850aee9b0fbb823cede5834b2e186b3fcb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampLtzOutputFormat"))

    @timestamp_ltz_output_format.setter
    def timestamp_ltz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ccdff2b5ef78bce87bbb1e8ffdbb289ca9bbbef6406dcb599489cadaffb7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampLtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampNtzOutputFormat"))

    @timestamp_ntz_output_format.setter
    def timestamp_ntz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1f610ccb5502b6464232cc06016d47c112df845f1f087a205c7fd0fe56f502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampNtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampOutputFormat"))

    @timestamp_output_format.setter
    def timestamp_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c452d4e99094f3b56bb0f754ee14a9381f38edfcf8d19cbb155d95d6ad06c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTypeMapping"))

    @timestamp_type_mapping.setter
    def timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac174786a644bafb77b31edb37bd1e112a7c90cb30f5b5cf2147d4b859b1be1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTzOutputFormat"))

    @timestamp_tz_output_format.setter
    def timestamp_tz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa77c824c491a1b95ffa4e4081661baa9863156d9e18d24f221c8baefe47764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f25e1803a2ad12535a256ebf369aa5162859202d6a9715ae9a4f6c3aac2607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6738f77bc3e92bcae3520ce2801219e20adc327c158397ba3684c75c3f3aac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87f05ea993560925ccb02c6028d2d534f8bee6651180a6b15a50740aff0846ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionAbortOnError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transactionDefaultIsolationLevel"))

    @transaction_default_isolation_level.setter
    def transaction_default_isolation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195de03975ac421559756af4c830411f10d6373802a227718a3299104db03e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionDefaultIsolationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "twoDigitCenturyStart"))

    @two_digit_century_start.setter
    def two_digit_century_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a56e345db8f2fa469e659cb59fc2bc3bf6d40f61ed47bb35fcc51e296526ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twoDigitCenturyStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unsupportedDdlAction"))

    @unsupported_ddl_action.setter
    def unsupported_ddl_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f8dadfbf8755e3cad2f48fd83e79dafcf981ded31fe28eb4bf9865edb6a57c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7519e9d1fe61f2a83dbb0cf8939ce666427ecdef9cb96f2db5f51fe04c0aa88c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCachedResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOfYearPolicy"))

    @week_of_year_policy.setter
    def week_of_year_policy(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15c6e81d54612118f6389e78a34e9a4d8d5abce77b5b153a1eb4d4288f322b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfYearPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekStart"))

    @week_start.setter
    def week_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89a4032f1919968789a33a97a5aa202bed13b59202c07a27464e8aae8ff7966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekStart", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserConfig",
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
        "disable_mfa": "disableMfa",
        "display_name": "displayName",
        "email": "email",
        "enable_unload_physical_type_optimization": "enableUnloadPhysicalTypeOptimization",
        "enable_unredacted_query_syntax_error": "enableUnredactedQuerySyntaxError",
        "error_on_nondeterministic_merge": "errorOnNondeterministicMerge",
        "error_on_nondeterministic_update": "errorOnNondeterministicUpdate",
        "first_name": "firstName",
        "geography_output_format": "geographyOutputFormat",
        "geometry_output_format": "geometryOutputFormat",
        "id": "id",
        "jdbc_treat_decimal_as_int": "jdbcTreatDecimalAsInt",
        "jdbc_treat_timestamp_ntz_as_utc": "jdbcTreatTimestampNtzAsUtc",
        "jdbc_use_session_timezone": "jdbcUseSessionTimezone",
        "json_indent": "jsonIndent",
        "last_name": "lastName",
        "lock_timeout": "lockTimeout",
        "login_name": "loginName",
        "log_level": "logLevel",
        "middle_name": "middleName",
        "mins_to_bypass_mfa": "minsToBypassMfa",
        "mins_to_unlock": "minsToUnlock",
        "multi_statement_count": "multiStatementCount",
        "must_change_password": "mustChangePassword",
        "network_policy": "networkPolicy",
        "noorder_sequence_as_default": "noorderSequenceAsDefault",
        "odbc_treat_decimal_as_int": "odbcTreatDecimalAsInt",
        "password": "password",
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
class UserConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disable_mfa: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        first_name: typing.Optional[builtins.str] = None,
        geography_output_format: typing.Optional[builtins.str] = None,
        geometry_output_format: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_indent: typing.Optional[jsii.Number] = None,
        last_name: typing.Optional[builtins.str] = None,
        lock_timeout: typing.Optional[jsii.Number] = None,
        login_name: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        middle_name: typing.Optional[builtins.str] = None,
        mins_to_bypass_mfa: typing.Optional[jsii.Number] = None,
        mins_to_unlock: typing.Optional[jsii.Number] = None,
        multi_statement_count: typing.Optional[jsii.Number] = None,
        must_change_password: typing.Optional[builtins.str] = None,
        network_policy: typing.Optional[builtins.str] = None,
        noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
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
        :param name: Name of the user. Note that if you do not supply login_name this will be used as login_name. Check the `docs <https://docs.snowflake.net/manuals/sql-reference/sql/create-user.html#required-parameters>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#name User#name}
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#abort_detached_query User#abort_detached_query}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#autocommit User#autocommit}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#binary_input_format User#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#binary_output_format User#binary_output_format}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_memory_limit User#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_metadata_request_use_connection_ctx User#client_metadata_request_use_connection_ctx}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_prefetch_threads User#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_result_chunk_size User#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_result_column_case_insensitive User#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_session_keep_alive User#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_session_keep_alive_heartbeat_frequency User#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_timestamp_type_mapping User#client_timestamp_type_mapping}
        :param comment: Specifies a comment for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#comment User#comment}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#date_input_format User#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#date_output_format User#date_output_format}
        :param days_to_expiry: Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in. This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#days_to_expiry User#days_to_expiry}
        :param default_namespace: Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the namespace exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_namespace User#default_namespace}
        :param default_role: Specifies the role that is active by default for the user’s session upon login. Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_role User#default_role}
        :param default_secondary_roles_option: Specifies the secondary roles that are active for the user’s session upon login. Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_secondary_roles_option User#default_secondary_roles_option}
        :param default_warehouse: Specifies the virtual warehouse that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_warehouse User#default_warehouse}
        :param disabled: Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#disabled User#disabled}
        :param disable_mfa: Allows enabling or disabling `multi-factor authentication <https://docs.snowflake.com/en/user-guide/security-mfa>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#disable_mfa User#disable_mfa}
        :param display_name: Name displayed for the user in the Snowflake web interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#display_name User#display_name}
        :param email: Email address for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#email User#email}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#enable_unload_physical_type_optimization User#enable_unload_physical_type_optimization}
        :param enable_unredacted_query_syntax_error: Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error. If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#enable_unredacted_query_syntax_error User#enable_unredacted_query_syntax_error}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#error_on_nondeterministic_merge User#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#error_on_nondeterministic_update User#error_on_nondeterministic_update}
        :param first_name: First name of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#first_name User#first_name}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#geography_output_format User#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#geometry_output_format User#geometry_output_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#id User#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_treat_decimal_as_int: Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_treat_decimal_as_int User#jdbc_treat_decimal_as_int}
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_treat_timestamp_ntz_as_utc User#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_use_session_timezone User#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#json_indent User#json_indent}
        :param last_name: Last name of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#last_name User#last_name}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#lock_timeout User#lock_timeout}
        :param login_name: The name users use to log in. If not supplied, snowflake will use name instead. Login names are always case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#login_name User#login_name}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#log_level User#log_level}
        :param middle_name: Middle name of the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#middle_name User#middle_name}
        :param mins_to_bypass_mfa: Specifies the number of minutes to temporarily bypass MFA for the user. This property can be used to allow a MFA-enrolled user to temporarily bypass MFA during login in the event that their MFA device is not available. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#mins_to_bypass_mfa User#mins_to_bypass_mfa}
        :param mins_to_unlock: Specifies the number of minutes until the temporary lock on the user login is cleared. To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#mins_to_unlock User#mins_to_unlock}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#multi_statement_count User#multi_statement_count}
        :param must_change_password: Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#must_change_password User#must_change_password}
        :param network_policy: Specifies the network policy to enforce for your account. Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#network_policy User#network_policy}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#noorder_sequence_as_default User#noorder_sequence_as_default}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#odbc_treat_decimal_as_int User#odbc_treat_decimal_as_int}
        :param password: Password for the user. **WARNING:** this will put the password in the terraform state file. Use carefully. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#password User#password}
        :param prevent_unload_to_internal_stages: Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#prevent_unload_to_internal_stages User#prevent_unload_to_internal_stages}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#query_tag User#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#quoted_identifiers_ignore_case User#quoted_identifiers_ignore_case}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rows_per_resultset User#rows_per_resultset}
        :param rsa_public_key: Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rsa_public_key User#rsa_public_key}
        :param rsa_public_key2: Specifies the user’s second RSA public key; used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rsa_public_key_2 User#rsa_public_key_2}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#s3_stage_vpce_dns_name User#s3_stage_vpce_dns_name}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#search_path User#search_path}
        :param simulated_data_sharing_consumer: Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views. When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#simulated_data_sharing_consumer User#simulated_data_sharing_consumer}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#statement_queued_timeout_in_seconds User#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#statement_timeout_in_seconds User#statement_timeout_in_seconds}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#strict_json_output User#strict_json_output}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#time_input_format User#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#time_output_format User#time_output_format}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_day_is_always_24h User#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_input_format User#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_ltz_output_format User#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_ntz_output_format User#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_output_format User#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_type_mapping User#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_tz_output_format User#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timezone User#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#trace_level User#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#transaction_abort_on_error User#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#transaction_default_isolation_level User#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#two_digit_century_start User#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#unsupported_ddl_action User#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#use_cached_result User#use_cached_result}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#week_of_year_policy User#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#week_start User#week_start}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bcd50566d7e5a0f6a888a622822b1bb2e90816ef4e28ff46370e9a97874f2c)
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
            check_type(argname="argument disable_mfa", value=disable_mfa, expected_type=type_hints["disable_mfa"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument enable_unload_physical_type_optimization", value=enable_unload_physical_type_optimization, expected_type=type_hints["enable_unload_physical_type_optimization"])
            check_type(argname="argument enable_unredacted_query_syntax_error", value=enable_unredacted_query_syntax_error, expected_type=type_hints["enable_unredacted_query_syntax_error"])
            check_type(argname="argument error_on_nondeterministic_merge", value=error_on_nondeterministic_merge, expected_type=type_hints["error_on_nondeterministic_merge"])
            check_type(argname="argument error_on_nondeterministic_update", value=error_on_nondeterministic_update, expected_type=type_hints["error_on_nondeterministic_update"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument geography_output_format", value=geography_output_format, expected_type=type_hints["geography_output_format"])
            check_type(argname="argument geometry_output_format", value=geometry_output_format, expected_type=type_hints["geometry_output_format"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jdbc_treat_decimal_as_int", value=jdbc_treat_decimal_as_int, expected_type=type_hints["jdbc_treat_decimal_as_int"])
            check_type(argname="argument jdbc_treat_timestamp_ntz_as_utc", value=jdbc_treat_timestamp_ntz_as_utc, expected_type=type_hints["jdbc_treat_timestamp_ntz_as_utc"])
            check_type(argname="argument jdbc_use_session_timezone", value=jdbc_use_session_timezone, expected_type=type_hints["jdbc_use_session_timezone"])
            check_type(argname="argument json_indent", value=json_indent, expected_type=type_hints["json_indent"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument lock_timeout", value=lock_timeout, expected_type=type_hints["lock_timeout"])
            check_type(argname="argument login_name", value=login_name, expected_type=type_hints["login_name"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument middle_name", value=middle_name, expected_type=type_hints["middle_name"])
            check_type(argname="argument mins_to_bypass_mfa", value=mins_to_bypass_mfa, expected_type=type_hints["mins_to_bypass_mfa"])
            check_type(argname="argument mins_to_unlock", value=mins_to_unlock, expected_type=type_hints["mins_to_unlock"])
            check_type(argname="argument multi_statement_count", value=multi_statement_count, expected_type=type_hints["multi_statement_count"])
            check_type(argname="argument must_change_password", value=must_change_password, expected_type=type_hints["must_change_password"])
            check_type(argname="argument network_policy", value=network_policy, expected_type=type_hints["network_policy"])
            check_type(argname="argument noorder_sequence_as_default", value=noorder_sequence_as_default, expected_type=type_hints["noorder_sequence_as_default"])
            check_type(argname="argument odbc_treat_decimal_as_int", value=odbc_treat_decimal_as_int, expected_type=type_hints["odbc_treat_decimal_as_int"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
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
        if disable_mfa is not None:
            self._values["disable_mfa"] = disable_mfa
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
        if first_name is not None:
            self._values["first_name"] = first_name
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
        if last_name is not None:
            self._values["last_name"] = last_name
        if lock_timeout is not None:
            self._values["lock_timeout"] = lock_timeout
        if login_name is not None:
            self._values["login_name"] = login_name
        if log_level is not None:
            self._values["log_level"] = log_level
        if middle_name is not None:
            self._values["middle_name"] = middle_name
        if mins_to_bypass_mfa is not None:
            self._values["mins_to_bypass_mfa"] = mins_to_bypass_mfa
        if mins_to_unlock is not None:
            self._values["mins_to_unlock"] = mins_to_unlock
        if multi_statement_count is not None:
            self._values["multi_statement_count"] = multi_statement_count
        if must_change_password is not None:
            self._values["must_change_password"] = must_change_password
        if network_policy is not None:
            self._values["network_policy"] = network_policy
        if noorder_sequence_as_default is not None:
            self._values["noorder_sequence_as_default"] = noorder_sequence_as_default
        if odbc_treat_decimal_as_int is not None:
            self._values["odbc_treat_decimal_as_int"] = odbc_treat_decimal_as_int
        if password is not None:
            self._values["password"] = password
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#name User#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def abort_detached_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#abort_detached_query User#abort_detached_query}
        '''
        result = self._values.get("abort_detached_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def autocommit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether autocommit is enabled for the session.

        Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#autocommit User#autocommit}
        '''
        result = self._values.get("autocommit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def binary_input_format(self) -> typing.Optional[builtins.str]:
        '''The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#binary_input_format User#binary_input_format}
        '''
        result = self._values.get("binary_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_output_format(self) -> typing.Optional[builtins.str]:
        '''The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#binary_output_format User#binary_output_format}
        '''
        result = self._values.get("binary_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_memory_limit(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB).

        For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_memory_limit User#client_memory_limit}
        '''
        result = self._values.get("client_memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema.

        The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_metadata_request_use_connection_ctx User#client_metadata_request_use_connection_ctx}
        '''
        result = self._values.get("client_metadata_request_use_connection_ctx")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_prefetch_threads(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the number of threads used by the client to pre-fetch large result sets.

        The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_prefetch_threads User#client_prefetch_threads}
        '''
        result = self._values.get("client_prefetch_threads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_chunk_size(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB).

        The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_result_chunk_size User#client_result_chunk_size}
        '''
        result = self._values.get("client_result_chunk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_column_case_insensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_result_column_case_insensitive User#client_result_column_case_insensitive}
        '''
        result = self._values.get("client_result_column_case_insensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to force a user to log in again after a period of inactivity in the session.

        For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_session_keep_alive User#client_session_keep_alive}
        '''
        result = self._values.get("client_session_keep_alive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_session_keep_alive_heartbeat_frequency User#client_session_keep_alive_heartbeat_frequency}
        '''
        result = self._values.get("client_session_keep_alive_heartbeat_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#client_timestamp_type_mapping User#client_timestamp_type_mapping}
        '''
        result = self._values.get("client_timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#comment User#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#date_input_format User#date_input_format}
        '''
        result = self._values.get("date_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#date_output_format User#date_output_format}
        '''
        result = self._values.get("date_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_to_expiry(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in.

        This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#days_to_expiry User#days_to_expiry}
        '''
        result = self._values.get("days_to_expiry")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_namespace(self) -> typing.Optional[builtins.str]:
        '''Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login.

        Note that the CREATE USER operation does not verify that the namespace exists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_namespace User#default_namespace}
        '''
        result = self._values.get("default_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_role(self) -> typing.Optional[builtins.str]:
        '''Specifies the role that is active by default for the user’s session upon login.

        Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_role User#default_role}
        '''
        result = self._values.get("default_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_secondary_roles_option(self) -> typing.Optional[builtins.str]:
        '''Specifies the secondary roles that are active for the user’s session upon login.

        Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_secondary_roles_option User#default_secondary_roles_option}
        '''
        result = self._values.get("default_secondary_roles_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_warehouse(self) -> typing.Optional[builtins.str]:
        '''Specifies the virtual warehouse that is active by default for the user’s session upon login.

        Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#default_warehouse User#default_warehouse}
        '''
        result = self._values.get("default_warehouse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#disabled User#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_mfa(self) -> typing.Optional[builtins.str]:
        '''Allows enabling or disabling `multi-factor authentication <https://docs.snowflake.com/en/user-guide/security-mfa>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#disable_mfa User#disable_mfa}
        '''
        result = self._values.get("disable_mfa")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Name displayed for the user in the Snowflake web interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#display_name User#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email address for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#email User#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_unload_physical_type_optimization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#enable_unload_physical_type_optimization User#enable_unload_physical_type_optimization}
        '''
        result = self._values.get("enable_unload_physical_type_optimization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_unredacted_query_syntax_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error.

        If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#enable_unredacted_query_syntax_error User#enable_unredacted_query_syntax_error}
        '''
        result = self._values.get("enable_unredacted_query_syntax_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#error_on_nondeterministic_merge User#error_on_nondeterministic_merge}
        '''
        result = self._values.get("error_on_nondeterministic_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#error_on_nondeterministic_update User#error_on_nondeterministic_update}
        '''
        result = self._values.get("error_on_nondeterministic_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''First name of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#first_name User#first_name}
        '''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geography_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#geography_output_format User#geography_output_format}
        '''
        result = self._values.get("geography_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geometry_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#geometry_output_format User#geometry_output_format}
        '''
        result = self._values.get("geometry_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#id User#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_treat_decimal_as_int User#jdbc_treat_decimal_as_int}
        '''
        result = self._values.get("jdbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_treat_timestamp_ntz_as_utc User#jdbc_treat_timestamp_ntz_as_utc}
        '''
        result = self._values.get("jdbc_treat_timestamp_ntz_as_utc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_use_session_timezone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#jdbc_use_session_timezone User#jdbc_use_session_timezone}
        '''
        result = self._values.get("jdbc_use_session_timezone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def json_indent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of blank spaces to indent each new element in JSON output in the session.

        Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#json_indent User#json_indent}
        '''
        result = self._values.get("json_indent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Last name of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#last_name User#last_name}
        '''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_timeout(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement.

        For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#lock_timeout User#lock_timeout}
        '''
        result = self._values.get("lock_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def login_name(self) -> typing.Optional[builtins.str]:
        '''The name users use to log in.

        If not supplied, snowflake will use name instead. Login names are always case-insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#login_name User#login_name}
        '''
        result = self._values.get("login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the severity level of messages that should be ingested and made available in the active event table.

        Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#log_level User#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def middle_name(self) -> typing.Optional[builtins.str]:
        '''Middle name of the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#middle_name User#middle_name}
        '''
        result = self._values.get("middle_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mins_to_bypass_mfa(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of minutes to temporarily bypass MFA for the user.

        This property can be used to allow a MFA-enrolled user to temporarily bypass MFA during login in the event that their MFA device is not available. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#mins_to_bypass_mfa User#mins_to_bypass_mfa}
        '''
        result = self._values.get("mins_to_bypass_mfa")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mins_to_unlock(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of minutes until the temporary lock on the user login is cleared.

        To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#mins_to_unlock User#mins_to_unlock}
        '''
        result = self._values.get("mins_to_unlock")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def multi_statement_count(self) -> typing.Optional[jsii.Number]:
        '''Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#multi_statement_count User#multi_statement_count}
        '''
        result = self._values.get("multi_statement_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def must_change_password(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#must_change_password User#must_change_password}
        '''
        result = self._values.get("must_change_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the network policy to enforce for your account.

        Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#network_policy User#network_policy}
        '''
        result = self._values.get("network_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def noorder_sequence_as_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column.

        The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#noorder_sequence_as_default User#noorder_sequence_as_default}
        '''
        result = self._values.get("noorder_sequence_as_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def odbc_treat_decimal_as_int(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#odbc_treat_decimal_as_int User#odbc_treat_decimal_as_int}
        '''
        result = self._values.get("odbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the user.

        **WARNING:** this will put the password in the terraform state file. Use carefully. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#password User#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prevent_unload_to_internal_stages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO  <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#prevent_unload_to_internal_stages User#prevent_unload_to_internal_stages}
        '''
        result = self._values.get("prevent_unload_to_internal_stages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_tag(self) -> typing.Optional[builtins.str]:
        '''Optional string that can be used to tag queries and other SQL statements executed within a session.

        The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#query_tag User#query_tag}
        '''
        result = self._values.get("query_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters.

        By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#quoted_identifiers_ignore_case User#quoted_identifiers_ignore_case}
        '''
        result = self._values.get("quoted_identifiers_ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rows_per_resultset(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of rows returned in a result set.

        A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rows_per_resultset User#rows_per_resultset}
        '''
        result = self._values.get("rows_per_resultset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rsa_public_key User#rsa_public_key}
        '''
        result = self._values.get("rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_public_key2(self) -> typing.Optional[builtins.str]:
        '''Specifies the user’s second RSA public key;

        used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#rsa_public_key_2 User#rsa_public_key_2}
        '''
        result = self._values.get("rsa_public_key2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_stage_vpce_dns_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the DNS name of an Amazon S3 interface endpoint.

        Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#s3_stage_vpce_dns_name User#s3_stage_vpce_dns_name}
        '''
        result = self._values.get("s3_stage_vpce_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_path(self) -> typing.Optional[builtins.str]:
        '''Specifies the path to search to resolve unqualified object names in queries.

        For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#search_path User#search_path}
        '''
        result = self._values.get("search_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def simulated_data_sharing_consumer(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views.

        When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#simulated_data_sharing_consumer User#simulated_data_sharing_consumer}
        '''
        result = self._values.get("simulated_data_sharing_consumer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_queued_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#statement_queued_timeout_in_seconds User#statement_queued_timeout_in_seconds}
        '''
        result = self._values.get("statement_queued_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statement_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#statement_timeout_in_seconds User#statement_timeout_in_seconds}
        '''
        result = self._values.get("statement_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strict_json_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#strict_json_output User#strict_json_output}
        '''
        result = self._values.get("strict_json_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#time_input_format User#time_input_format}
        '''
        result = self._values.get("time_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#time_output_format User#time_output_format}
        '''
        result = self._values.get("time_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_day_is_always24_h(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_day_is_always_24h User#timestamp_day_is_always_24h}
        '''
        result = self._values.get("timestamp_day_is_always24_h")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timestamp_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_input_format User#timestamp_input_format}
        '''
        result = self._values.get("timestamp_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ltz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_LTZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_ltz_output_format User#timestamp_ltz_output_format}
        '''
        result = self._values.get("timestamp_ltz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ntz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_ntz_output_format User#timestamp_ntz_output_format}
        '''
        result = self._values.get("timestamp_ntz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_output_format User#timestamp_output_format}
        '''
        result = self._values.get("timestamp_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_type_mapping User#timestamp_type_mapping}
        '''
        result = self._values.get("timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_tz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_TZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timestamp_tz_output_format User#timestamp_tz_output_format}
        '''
        result = self._values.get("timestamp_tz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone for the session.

        You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#timezone User#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Controls how trace events are ingested into the event table.

        For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#trace_level User#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_abort_on_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error.

        For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#transaction_abort_on_error User#transaction_abort_on_error}
        '''
        result = self._values.get("transaction_abort_on_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transaction_default_isolation_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#transaction_default_isolation_level User#transaction_default_isolation_level}
        '''
        result = self._values.get("transaction_default_isolation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def two_digit_century_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#two_digit_century_start User#two_digit_century_start}
        '''
        result = self._values.get("two_digit_century_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unsupported_ddl_action(self) -> typing.Optional[builtins.str]:
        '''Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#unsupported_ddl_action User#unsupported_ddl_action}
        '''
        result = self._values.get("unsupported_ddl_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_cached_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to reuse persisted query results, if available, when a matching query is submitted.

        For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#use_cached_result User#use_cached_result}
        '''
        result = self._values.get("use_cached_result")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def week_of_year_policy(self) -> typing.Optional[jsii.Number]:
        '''Specifies how the weeks in a given year are computed.

        ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#week_of_year_policy User#week_of_year_policy}
        '''
        result = self._values.get("week_of_year_policy")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the first day of the week (used by week-related date functions).

        ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/user#week_start User#week_start}
        '''
        result = self._values.get("week_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersAbortDetachedQuery",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersAbortDetachedQuery:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersAbortDetachedQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersAbortDetachedQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersAbortDetachedQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77bcd7e947fa6d5c9d46acfd73e5ac52f4a18338bc08925729a7cf5daae4cde5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersAbortDetachedQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08fb0915bdd84f1d9f706053dd06b24eb66e8ac59eabbc75cac92cf75557f63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersAbortDetachedQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d30464b811d5602b33e397cad646f23dce30bf5b02d85ae3f63a12bfefdbc9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f68b4d7f3a11594a1235f7f45520f4fa298bf7749bd44c2b163977a05855265)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16b7589af69276346b071334bf6aa749c9748bc296ada7345070d4fbc3723637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersAbortDetachedQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersAbortDetachedQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a6820bc97c9ce7e91b7f096136d03160004acc8529ca6a5acbfae877211cc53)
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
    def internal_value(self) -> typing.Optional[UserParametersAbortDetachedQuery]:
        return typing.cast(typing.Optional[UserParametersAbortDetachedQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersAbortDetachedQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228c227a1b244fe603e777d34831f36f9d078a84decb0dcef93f709ca6017271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersAutocommit",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersAutocommit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersAutocommit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersAutocommitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersAutocommitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8b98a2cbf8d94d8dc321587cd39046454c8dd032d536bc934451378b21e15b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersAutocommitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2528402a209a67fbcc1597c316660a54e4ca8d0b491bbd9c7df58099ffc66b87)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersAutocommitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1eafe17b0def28d8a0fc8860f505c042eaf6973437cc8f546549ba01ee9bdf6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6f3ec2d76271d05bc2226497fc68d74b4cffcad37041436e672d7a037b60757)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9ec1db1bb47aaa2967b98f9ec54a477d5131695721c2a436bf4e4cf93b41a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersAutocommitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersAutocommitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9699bd6055cca785b5b35a04c637450e6e3ec8c4e0054f7f8c11e5a62727f52)
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
    def internal_value(self) -> typing.Optional[UserParametersAutocommit]:
        return typing.cast(typing.Optional[UserParametersAutocommit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersAutocommit]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb727962005ea32d3b490acbe9bd871de4e962fbeba47f3fda386975da56328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersBinaryInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersBinaryInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersBinaryInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersBinaryInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersBinaryInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbfdabe91952fc706148e8e63c96404085c807f86c29212fa70a9e53bee35789)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersBinaryInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5718953dd8297ed21add4b52a3a5a925165d3010c2313c5875bbdf75819b3d12)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersBinaryInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f57e5e25306d0fc84edfb2917a88fa53688bbcf0963c87450c00bfa8ad490b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01cfec7a5aef50b1395294b6aea0eed8bdecac4239a350de9b974ac95b2a5c5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__734a466eb0432e9976c3d238d13d088aab8fec5bf4c335e16bcfe09c1646f43c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersBinaryInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersBinaryInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__808a00848b371b50e1c954103ecd773adb367566d5e805d2a2cef9b32b8bf48a)
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
    def internal_value(self) -> typing.Optional[UserParametersBinaryInputFormat]:
        return typing.cast(typing.Optional[UserParametersBinaryInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersBinaryInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3d4d1b3bc3e53b812b5841950c6eebc8f97793e0f9f5224710f92f5ac0d780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersBinaryOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersBinaryOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersBinaryOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersBinaryOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersBinaryOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb3a288bfbca62314c94ce7ecebae7d792a3770980f423dc8f44ea6e2ae38eb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersBinaryOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abd41865c5d5e5dad855f1ede02b9dd433177b3ca916809725b50d8d84a3d6b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersBinaryOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d250f385c2de5e8840cb9c00c8ec46e513f2d19ebae7c6eebdcd1b7baffcc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f85ff0e12a6a010421f6a384eab97952b67b847376b43742e417e2f7d075b4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ac87e158c06b4d3c1100411aa952cace1fdc242a68ca5b09ba0c425cfd142d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersBinaryOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersBinaryOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd3e05a1b85b6341583838971949ccdabc14d7f91649269905c95cc6dfc08b03)
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
    def internal_value(self) -> typing.Optional[UserParametersBinaryOutputFormat]:
        return typing.cast(typing.Optional[UserParametersBinaryOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersBinaryOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30da9808e8b71cf4c4174ffe3dfe0f1b12e2223a1d8e7c06204e5b3635ad38f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientMemoryLimit",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersClientMemoryLimit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersClientMemoryLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersClientMemoryLimitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientMemoryLimitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__014740eb2d4860eed241d4afc4fc8e03345594d242393f01d805a3ee071636b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersClientMemoryLimitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef9794e77c8cea9c1167986e5f687f30bbb4049fe3bbd8da9dcb57642329c36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersClientMemoryLimitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c862737204049b678f182f467655002407c460d7b220533f41f83dfe24a153)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca320da31a5cb2b595f0d375809523c1599d70d83396fc0eafd0f22204223325)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f69fb4e090dc2ca2f336b416b1317cfe29b3879f116d449e338835bf925f4ad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersClientMemoryLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientMemoryLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fb9b2e5d4c2c02f7602feb31277ea3d7a080fa1bfc3f0f9ababb95a0c9f92ef)
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
    def internal_value(self) -> typing.Optional[UserParametersClientMemoryLimit]:
        return typing.cast(typing.Optional[UserParametersClientMemoryLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersClientMemoryLimit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f313953cb08c610126b6f94393bd7404f318b502669f9ce2e28673b699233337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientMetadataRequestUseConnectionCtx",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersClientMetadataRequestUseConnectionCtx:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersClientMetadataRequestUseConnectionCtx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersClientMetadataRequestUseConnectionCtxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientMetadataRequestUseConnectionCtxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed4fe1074eba3baa286638a17cc2cb312268295e9cbde434adf669691efed797)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersClientMetadataRequestUseConnectionCtxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040c916e686150937cddafc2b1a80fa9b2f06c18f6cd88957a2839d0d713edfa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersClientMetadataRequestUseConnectionCtxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78da5be11496a839b1e68b054585578abe209e5025dd61b92e49c2f261e6f2ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60b1a2851643e4db4a2cb5962115f4f98175538de50fc190944319e8328cadde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ab5161a6d9bdf401b6fcde1533815fbdf25cc6ed4503accce767ed323f3ced6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersClientMetadataRequestUseConnectionCtxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientMetadataRequestUseConnectionCtxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2da1277818d0077cc35ee7c3bd3058088ff422d0787473b3cfcdcce7db8897a)
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
    ) -> typing.Optional[UserParametersClientMetadataRequestUseConnectionCtx]:
        return typing.cast(typing.Optional[UserParametersClientMetadataRequestUseConnectionCtx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersClientMetadataRequestUseConnectionCtx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542aebd2588d6d6bcd84a2a7ab78633e57421bf32718d7af7f1b73a0a2713a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientPrefetchThreads",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersClientPrefetchThreads:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersClientPrefetchThreads(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersClientPrefetchThreadsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientPrefetchThreadsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9937efa9ac7d6ed0b8cd7bc691b3e88d564b4d94687422d712d38af6ecb74c8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersClientPrefetchThreadsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b0d902498f59d27cbef19790753a7c31576194f6fecbda8682f94a1c4ddb62)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersClientPrefetchThreadsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfacd3d8e4f3b0e3c97a6cee135c2f89fc9bfce6d02a05d4c4115323685f1a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fad1c935e120fea37614a6d8b2004c363bce158defbcf3b8d387d817eed73fb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da90f1a9252a8541b1d652a4875a2dfae8f2ca27f8f9f4741e2b2ca365773e9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersClientPrefetchThreadsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientPrefetchThreadsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d244ce07b62ec3d83a51c587b251e26d3131bdab07083cf546373b5ea009178e)
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
    def internal_value(self) -> typing.Optional[UserParametersClientPrefetchThreads]:
        return typing.cast(typing.Optional[UserParametersClientPrefetchThreads], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersClientPrefetchThreads],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2443b03787f50b319729c1d5d24a03761559c4c1a85f4dc55ee7632f97b2d44b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientResultChunkSize",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersClientResultChunkSize:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersClientResultChunkSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersClientResultChunkSizeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientResultChunkSizeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__634ccc504b165098dc1f246fba69815a336c7d4afb1d9375466c7d29a9037976)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersClientResultChunkSizeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c20d58a22ae4df3b6d108d9af7ac6497417504c73d69583ef7e55caf862edc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersClientResultChunkSizeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74ff34467e0f67d80fbf2ad4b09c195ba7c9b5218ceabaa513bafefd37d44e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c97575c5e889cfa6c44df1248550e0a1785ebd89fc789a8a40d27049473e50f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ab48b0fc21b2d29fd0c815ab2284a29c217473e8c7705d58429d62c88daedca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersClientResultChunkSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientResultChunkSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d16da9e3af91dac3d2d6a022ec14f366b0f0538c36a3feb8eef3540e44f4c4a2)
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
    def internal_value(self) -> typing.Optional[UserParametersClientResultChunkSize]:
        return typing.cast(typing.Optional[UserParametersClientResultChunkSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersClientResultChunkSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f9185c106275ede01a08ab89449f88ea7b120ff7ffa08c52c65b2c5baae496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientResultColumnCaseInsensitive",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersClientResultColumnCaseInsensitive:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersClientResultColumnCaseInsensitive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersClientResultColumnCaseInsensitiveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientResultColumnCaseInsensitiveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f0a8f51a5134d53e694f0e962f573bdd7896374c4aa429bcec3abef817797b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersClientResultColumnCaseInsensitiveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3585de0526e6d9573f36df819ba65b8326509a659ceba6368166d5b21c5c75)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersClientResultColumnCaseInsensitiveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e5bec052d7546fc6e7a63593cbe7fc7af78b00a49b85cf52d0cec0ed013661)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c4f1dbba931582d2cc1fc76a16e4148498c586a65260c4a00b42edef53d6aa3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32d41e390819f0ef5d4ad0ab31fd4b2bb71f605a71f7437ebfe96a5f862ad43f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersClientResultColumnCaseInsensitiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientResultColumnCaseInsensitiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1a2af70b42f303e335aec48161a38930cb311bf7e044fbf5058df6ea4830470)
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
    ) -> typing.Optional[UserParametersClientResultColumnCaseInsensitive]:
        return typing.cast(typing.Optional[UserParametersClientResultColumnCaseInsensitive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersClientResultColumnCaseInsensitive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7475ff3230b42f208799f1ecae876500c52ce230b37dfd95d51e0cbc2d3e7d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientSessionKeepAlive",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersClientSessionKeepAlive:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersClientSessionKeepAlive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientSessionKeepAliveHeartbeatFrequency",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersClientSessionKeepAliveHeartbeatFrequency:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersClientSessionKeepAliveHeartbeatFrequency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersClientSessionKeepAliveHeartbeatFrequencyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientSessionKeepAliveHeartbeatFrequencyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44946529a30126a6d4d27c2d8e7f7e525c300a828dfcff9364320cb7b7993ce0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c712f69fa2561e2d1fe2bbc5f52981168faa41a5ab448e75e50624b5f354566b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85639ebd04434dcf270aa4a81049bf1daa321718bd4b25e80ebc80c23207343a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a0e84fea1976d99ce4398dd38496e5ba8b3a10fb2dbdb6347b37ae33e8a2ad0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1af57e7d3c4e954f2929394528285fb97e0ba415cd3877591231236d8f61c973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__868fb13f3b3b2d7046236e990e78db35892b94b2fe92d821fa80c8283d4786b5)
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
    ) -> typing.Optional[UserParametersClientSessionKeepAliveHeartbeatFrequency]:
        return typing.cast(typing.Optional[UserParametersClientSessionKeepAliveHeartbeatFrequency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersClientSessionKeepAliveHeartbeatFrequency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5175a1f681a889ed6dd2e0481e10f6ccf96830bbf88d1c603254b1dc80ac6727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class UserParametersClientSessionKeepAliveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientSessionKeepAliveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93c0e3e9e432900e1ea7af791dda897e68797198bc289f6a49e077007c89dc01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersClientSessionKeepAliveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b70404af3b81ef8c1ba894dd8b6b7412f737c20ab615314fc46b62ef8970fd9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersClientSessionKeepAliveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800edbe41fd71aaab89341b80d4fe2882c6fde021657c74ec4e560870b374a8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b37de4d6ccdad65fc9fd7e86280c97cd48b63e89cf86c521219fa9b3209d5f0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a9053627998d7a7fa11884d12bc89e9e2220c8fc78625cfc6445e51c8d556ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersClientSessionKeepAliveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientSessionKeepAliveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79cb6916c75c000d3376c756de22258412ea1285e18cae29cd15b97d06ce62d7)
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
    def internal_value(self) -> typing.Optional[UserParametersClientSessionKeepAlive]:
        return typing.cast(typing.Optional[UserParametersClientSessionKeepAlive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersClientSessionKeepAlive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07a4f151c3bb2535e47927bef2ee987503f4254f10c085e82415f42dd28f8a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientTimestampTypeMapping",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersClientTimestampTypeMapping:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersClientTimestampTypeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersClientTimestampTypeMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientTimestampTypeMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca2d53b9ac81b42090b597e6904de1abb942ab7e1b0c19e94dbcb6e0d3b53d96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersClientTimestampTypeMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f29f9acb71111dd2b7acad7154c610c75cbc02ef1229e329e239d06ac0b86cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersClientTimestampTypeMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d298261722b9b576b4c32e4b31769c8e1e8b4e842b3fd31827504a4f0a1c4ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f24bcaa6e9b223e65087e64e64af64dce4d1ff10d62b453a8085f0b0a1f23754)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36a1bac09282c406921f376e30222d0c9385dfe8d8eecd79f101ef68aab2bc1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersClientTimestampTypeMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersClientTimestampTypeMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0616b9eef651c7972516c65d6fb350033a5fef3eb32519ecb056769339e3cd30)
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
    ) -> typing.Optional[UserParametersClientTimestampTypeMapping]:
        return typing.cast(typing.Optional[UserParametersClientTimestampTypeMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersClientTimestampTypeMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6209de93240e09e23997fd2df9908b8b94b1a7222ea05a88977c7e118ac7b52e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersDateInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersDateInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersDateInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersDateInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersDateInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fbd740d102371d44fdc79e634b4ec9aff77c3dc8e698dbe38a30d70a0d8e128)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersDateInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c7cca5bdbef6efecdc7e31d04eb57e0f5bb699b0720975b88546de17d4c611)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersDateInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad24f1ee6a74d413b39109534fdc82798d66b1d44d5a332488afc1b10eece46d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbfb7ebdc5393acf307a71a18fc5e41b5770378e09752d978f31d48701351735)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e7916b052e9f3bc09558bfa9f8a21bbbbd518f5bd93d091e4cde1d8729bddbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersDateInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersDateInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6fb2254784e0a2341558368796c5f31a8aafebe3228bb086984e687ebb4bf89)
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
    def internal_value(self) -> typing.Optional[UserParametersDateInputFormat]:
        return typing.cast(typing.Optional[UserParametersDateInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersDateInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec665e6fa2fd9b9d76306a9859d5f95507009dd8e5a000fd15de805c9d9cfbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersDateOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersDateOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersDateOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersDateOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersDateOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7121e892342930d78401ca18de0379c0374cba71b995c7c2bf7180b8481a030f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersDateOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3063179f5f494a3247df833b0aa7e2a8d3834c5a9b4bc69e8faa6b6df204cb3c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersDateOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c5cffc26b817bb4881f41e3295fd3c771bc28ca810292f7a6bea80f5bb0e70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__854d3e389182a269e02483189b2f31e5ede611ddefaed29fcdd18ec6c5eb9ad5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aef9d0566c2f8da1f65cd347e8d9c4af48deb9c9b84bf36388ecaabf42fb37f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersDateOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersDateOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b99167ea9c819b1f1d498108a0990e60109c61058a99d9ea54c795793f68e941)
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
    def internal_value(self) -> typing.Optional[UserParametersDateOutputFormat]:
        return typing.cast(typing.Optional[UserParametersDateOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersDateOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b5c41b198e2f3dda7c71c12ce94174bac31cdfa3a58f4b6e5d43c3f1abc41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersEnableUnloadPhysicalTypeOptimization",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersEnableUnloadPhysicalTypeOptimization:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersEnableUnloadPhysicalTypeOptimization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersEnableUnloadPhysicalTypeOptimizationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersEnableUnloadPhysicalTypeOptimizationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50ef0d9ef0b7c8a71fe56190aa85cdba285509dddb045175c58ec09378431f2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersEnableUnloadPhysicalTypeOptimizationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618bbe3d633411bfdf03a0abafbace3c8f2691963cb5b08e88934bdc33a4c5f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersEnableUnloadPhysicalTypeOptimizationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea9e64422ace8eb9c6d3a32b5bba84ca655d53dc900ae8d4e327c7257a87276a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebd94a6bb4d6086f6eaf231a3deb137a76ca323b625f364002bef4ced04183d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25826720738045cd34f4d77c5d08000eff47f802d3d83d69f4aa2228d2ae3bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersEnableUnloadPhysicalTypeOptimizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersEnableUnloadPhysicalTypeOptimizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ed2ec4089fbf5e26b5f0dc9a031ab3e5619bab34bb2de5fa16d1b8f23818a84)
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
    ) -> typing.Optional[UserParametersEnableUnloadPhysicalTypeOptimization]:
        return typing.cast(typing.Optional[UserParametersEnableUnloadPhysicalTypeOptimization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersEnableUnloadPhysicalTypeOptimization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968c8699b74c515e5e60f4b8018f5dd0df58fa1edb784e9839018e991c498ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersEnableUnredactedQuerySyntaxError",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersEnableUnredactedQuerySyntaxError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersEnableUnredactedQuerySyntaxError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersEnableUnredactedQuerySyntaxErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersEnableUnredactedQuerySyntaxErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ba213e9d487f4839c03b64c9be0ef8b15159419b0e02a409d16a5d4a6259fa6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersEnableUnredactedQuerySyntaxErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b839f3acc6a19703888a3fea906146f1bd2ffdf817257a75912aea7522825d33)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersEnableUnredactedQuerySyntaxErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876fca32c7a73d739e48574d7dc4ab077f6267ae3ad75d9d5b9190aeb04e049f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a090e973a1b37d426ad5907b46d4c2c198ab83e070b05b9fb73f65d9334a80f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3db1bdd089d04c80e9a4853e8267ff1a5294ac5e4ec73ee523701e5c91deed3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersEnableUnredactedQuerySyntaxErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersEnableUnredactedQuerySyntaxErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25ff220bc657fc5eed93cf122f059ecafb9db9582aba81ce3e4a21f688e7f897)
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
    ) -> typing.Optional[UserParametersEnableUnredactedQuerySyntaxError]:
        return typing.cast(typing.Optional[UserParametersEnableUnredactedQuerySyntaxError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersEnableUnredactedQuerySyntaxError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228e5b337d5e5672efd333a043e53f34abd8e7998748f1ac50174b86e81b2dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersErrorOnNondeterministicMerge",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersErrorOnNondeterministicMerge:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersErrorOnNondeterministicMerge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersErrorOnNondeterministicMergeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersErrorOnNondeterministicMergeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e42be6f99db431c36aeac594a74367b64fea764a4dfe66debfe1f489c1c09ae1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersErrorOnNondeterministicMergeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243ddd00988591c037bd8e2e83bcd854ff8cc4e941c025668c0546666e3770d3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersErrorOnNondeterministicMergeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ceac47fd4ee639005ae5a6a6f3f57541ea2b823b2cfc3ed69994aa2faaacf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d5c35f0a5e85778cb0d614293e04e908826d00bc86d18a92bc8699ae5f0fe96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cd4808ed00477c7791bddc3d809e868e88c6351d7050080a173065b353a9501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersErrorOnNondeterministicMergeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersErrorOnNondeterministicMergeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6722e72576c1db8f9d91dde7307bbcb90ab35ae3dbb53fdfcb265afc55187a6e)
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
    ) -> typing.Optional[UserParametersErrorOnNondeterministicMerge]:
        return typing.cast(typing.Optional[UserParametersErrorOnNondeterministicMerge], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersErrorOnNondeterministicMerge],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18cb20211eb3fd9868c5cbaef5b2196a871f4ac770c56d9132b4b79fae27d076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersErrorOnNondeterministicUpdate",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersErrorOnNondeterministicUpdate:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersErrorOnNondeterministicUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersErrorOnNondeterministicUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersErrorOnNondeterministicUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4188e522f5cb80b19bcbdb6e263ac692cd6995a4953ed7d07780fa258e4b67a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersErrorOnNondeterministicUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b2bf4a1d14b9561d641719f652a62ea32303ef62300f9cc113a6af64d11383)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersErrorOnNondeterministicUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0c1feee19b63ad80a8bccd718c6004bdac187a08be3c890a38d979dec3db01f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__512aeb4f9ed5e61bcd50b2a8ea545717707913768deac30523e58c9c43c0679a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7943f07d42dbf1c2eba0739cf89763536d74dbe4d853d231158e1c2c193951e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersErrorOnNondeterministicUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersErrorOnNondeterministicUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1e0d88990bc03a48fbcae5acb1fbb18f17c1d0e19719a7abd7c56aea11b032)
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
    ) -> typing.Optional[UserParametersErrorOnNondeterministicUpdate]:
        return typing.cast(typing.Optional[UserParametersErrorOnNondeterministicUpdate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersErrorOnNondeterministicUpdate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c43c79b3f39a058560ef80255e4ff85c5059f7abe87b5c8647a99f014bb546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersGeographyOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersGeographyOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersGeographyOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersGeographyOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersGeographyOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6df93cd2810944c3dbfd8262a64b2564663f68d55a32f231b788dd5ad7451355)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersGeographyOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62aede7a941a579e1765ea21c4cbe5a3e8ad45a96faa40f3b2f7d0539449fff3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersGeographyOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1bf7da977465c324c3654493b38cb9a1985bafb5323ff56ae2bfe96a8438ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62ecd665ffe5f75f47daebf2358152eec4be8d70afac3fc0b100cdb7db4705c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc2d9583820e7ec9a7eed4216896614632429953989b7fe2d8810c223fb1f60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersGeographyOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersGeographyOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9456b542fbe21b6f551f4be6fc325d96996becdf7b169c63a29e0f1445835aee)
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
    def internal_value(self) -> typing.Optional[UserParametersGeographyOutputFormat]:
        return typing.cast(typing.Optional[UserParametersGeographyOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersGeographyOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6630899d06467b356adaf5e4adda8b103ab7576cc6ed5ba01a9f4e83060e384b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersGeometryOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersGeometryOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersGeometryOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersGeometryOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersGeometryOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__827b1c16ca58fc02ef7204ccaa74e385243416273c0a9a17c8859e017c564f05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersGeometryOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c706303dae6b92b7348e43fd3cf19fef5df0a3c2920079e12c820a8ff29862)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersGeometryOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc382880531deeb6e1ed36cf8c9549b5143afc5838985c47361133036bfd7c9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24edebeafbe56eeb5e6aa4eeee06ba975ece19a12b8f13cfba6ef11a789710c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbad5bf27000dbce9c67585901645c2b9f9bbf3218f4a4ddae2549235c3d3bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersGeometryOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersGeometryOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__198a971e27834cb46055e5a68b2d9a3c51586256c0ef6242b028e02260a215ad)
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
    def internal_value(self) -> typing.Optional[UserParametersGeometryOutputFormat]:
        return typing.cast(typing.Optional[UserParametersGeometryOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersGeometryOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca49dee7a53a4ada441dd7badc8b75b0824ccb968d620d3616a450cd7b66de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcTreatDecimalAsInt",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersJdbcTreatDecimalAsInt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersJdbcTreatDecimalAsInt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersJdbcTreatDecimalAsIntList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcTreatDecimalAsIntList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9c04a9c8767f6f9da9963b6dd63b3f14a73b5e3af100f930ea21ae9575a42ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersJdbcTreatDecimalAsIntOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c550c52203c06cacef302a4660f1e86c0df84dc8d28cbee7a0a55324499284f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersJdbcTreatDecimalAsIntOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a125acd4ffb98eb541a512be2a0b29427f77bb9e009288fa5f01eb8625ff1e68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63e830395911d58d3df4149a2c2f6e9a19867113fb0a0bb8ce5975a76ef0cb4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ab5aebafaabe75c502f6ffac09dfb249f806a87e02fd6fd44c8ca8bf7be6fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersJdbcTreatDecimalAsIntOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcTreatDecimalAsIntOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8c438cef45c20daef0b85abbfed9cf61af4eb7e369065f74fc12c052a9d2be7)
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
    def internal_value(self) -> typing.Optional[UserParametersJdbcTreatDecimalAsInt]:
        return typing.cast(typing.Optional[UserParametersJdbcTreatDecimalAsInt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersJdbcTreatDecimalAsInt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28be02fdb32ccdff80a6630eb47a348a541ccbccf0aa6394046532d618b517c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcTreatTimestampNtzAsUtc",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersJdbcTreatTimestampNtzAsUtc:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersJdbcTreatTimestampNtzAsUtc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersJdbcTreatTimestampNtzAsUtcList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcTreatTimestampNtzAsUtcList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b63151fcc05d6e5bb1ce098542bcc97e490ad07747c81191bf369027809361c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersJdbcTreatTimestampNtzAsUtcOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4241bab5614fdb6f9084fac2742c1d4d3e7508f7c82f1c64f55373778f9857c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersJdbcTreatTimestampNtzAsUtcOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5010dd54e9313cbda16dc32ee923d09139c56c0a2c4a19dff671762a9e0a566f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdd9022f367709b39fb77a43568389d37582a4c6b369e72cfb459902d025f6dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__177590f791ff513cdbd39b062946dc2b822568be49f4df6f1775a33640120e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersJdbcTreatTimestampNtzAsUtcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcTreatTimestampNtzAsUtcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1cf1c87bd4ef3df6e916a1c776872d56416fdb9cd8f34382042946b4ce44a11)
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
    ) -> typing.Optional[UserParametersJdbcTreatTimestampNtzAsUtc]:
        return typing.cast(typing.Optional[UserParametersJdbcTreatTimestampNtzAsUtc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersJdbcTreatTimestampNtzAsUtc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd12e4443704e2f214ea11c5570a3f511ae037f373e1b7fcf50650ff652f233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcUseSessionTimezone",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersJdbcUseSessionTimezone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersJdbcUseSessionTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersJdbcUseSessionTimezoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcUseSessionTimezoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ce54c66da2dbdd14f02ef524ea4a39e1ce965613f881e51de0eab9c8f5301d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersJdbcUseSessionTimezoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e5e6acba2792b229321b898b8133aac726b18982a009c6b342f37a0ad47d32)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersJdbcUseSessionTimezoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf1bedd952ddecc477a90554f39b178f7558153e5e1977ee0717bd67d62d9f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__638531ed6e86d8bdd1543a01c07393b1817702e3c81e967e2573ecbf31d1b239)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61a2e7084a3da9a2ab54fcbefd8de055ffd3d7b831f94ccb20938861fffb299d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersJdbcUseSessionTimezoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJdbcUseSessionTimezoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbc951e36249e9ad1a590801c6b0327c0803a93ac6313c78c44e6ebd217be0b)
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
    def internal_value(self) -> typing.Optional[UserParametersJdbcUseSessionTimezone]:
        return typing.cast(typing.Optional[UserParametersJdbcUseSessionTimezone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersJdbcUseSessionTimezone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee88c438fd67865947af20427a8bfbda2ee21bfea2aecc0d54db7181ea104a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJsonIndent",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersJsonIndent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersJsonIndent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersJsonIndentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJsonIndentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c6f43886548a69f5dcdbad5df37b43ed629ee44fac25ab1b521146433278e3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersJsonIndentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf030616e4778b59a21d012b6c3fbe9cfa98a49c9e9db579f0ff76d0501e00b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersJsonIndentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72912e7d80670d046e2f68ed9307a73a2418dcfb7d810a18398ea153f82a871a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__854e1ee0750a7dd75c9199f3ba8c8698416af1dca9f87e5bfeb30c76cd50b693)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c59b2aa93387048cd2a2e5c79513e9c5b18259ba1ba2bb51c1fe961b583af2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersJsonIndentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersJsonIndentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4e146b396c19d71fdc5f2c7757a4857fbdbcce6be49f6991fa5f4ab5181fe51)
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
    def internal_value(self) -> typing.Optional[UserParametersJsonIndent]:
        return typing.cast(typing.Optional[UserParametersJsonIndent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersJsonIndent]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203efd1c43bc5c825c6a044c8082baf708f79a97c019823bac54f1b27127c498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class UserParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fc44de93966e6aee2efc4baa284c9fdf541e723000e96f0086cca0c3b1602e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c07b70d985481464796d42cc7f9ff8db0422cb19831bc3aba134388ddc9d9c4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f5395c5f87e500512fa4df7ca30bf42df60b2b0a01616d66d30b1d114aded0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdff4cec53d0b0970b71e29b248bab568280766d63932d951ac8b8efe900ce3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff4e49277ba0f07f0c4f8b7687cfb77ac82d378bcfd53cda1434c19cc6310e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersLockTimeout",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersLockTimeout:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersLockTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersLockTimeoutList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersLockTimeoutList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20fa63433cce260b6d7838b333ea09732ee2fa669297c7b16a00d472f4b95402)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersLockTimeoutOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43ef71feb218d8b6b4a4a34c6544325069b315330957ffdc07d538e3dc4be20)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersLockTimeoutOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b120883f46953baee13cff036ab72d35df17f1f32538dbfed46c73b7e6aec3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f9e11c17863aceaf1202702a4976f3c6ae1a158644a833ab3cdc146e1ac7fa3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d53ca30516485f15950f7ef9957181f100bc504c199e920dda86e559338107ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersLockTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersLockTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b33632b2b0e0cce81aecf1ab47dc72c888b563ea0c1ead810abf611c9b4c140)
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
    def internal_value(self) -> typing.Optional[UserParametersLockTimeout]:
        return typing.cast(typing.Optional[UserParametersLockTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersLockTimeout]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cea2794e598d25fbb6157869f73e6467b6c259d76b2d868178e896c0b39f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afdeee444028d68073cbf8357405c79f34681058cb435a06eeab096e219b7731)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d57322e4c9c21cc143a02ece47c41b4d61f7f6d5cc808341e439c23c4d9f9a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9623cf9f79a53f79412e97f5fe400c7a9de5c4ef93c9da3d77f3c0f3eb14a0d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__192d27a7e6e7c0fce8a29c1dbff6670d4b5604d68ad0367cdc9ddb92086e4dff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62de3eeb59c6297c19bc8cda643116d55f9fe4dcddb5971cf41d434b701429ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81fb089be79eaee03855612e8240d20560487cb66be81a9a0275dd55d7cab652)
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
    def internal_value(self) -> typing.Optional[UserParametersLogLevel]:
        return typing.cast(typing.Optional[UserParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersLogLevel]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69000731273ea0b06120d6fcaa3a19b4ff600ac186dd137bf8398e389e50c542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersMultiStatementCount",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersMultiStatementCount:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersMultiStatementCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersMultiStatementCountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersMultiStatementCountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c42734bac70b4972255a22f8dfd6a4600559ac7a539135211b31ba07de90fe5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersMultiStatementCountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310ee66bd231dd7ea8cf6a990df07ad006f7c936f4edb56ccb10ab6a7be12a73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersMultiStatementCountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af9e9b3967574bc7035273bee3d71a6ce20acc1d57db44795243283447061bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__878a480b8ef0b5934f3aa0eedced7649055540f4ea016b1f2849f86a1e78dfb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf8b029c4369e98b3b279fc8e0b18ba2ae6843dbb632c104e00a79cdc4b13f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersMultiStatementCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersMultiStatementCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c19853bc9cfc71373f03e446ff11964c01479b3ae777495b9cd78171eb8d776)
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
    def internal_value(self) -> typing.Optional[UserParametersMultiStatementCount]:
        return typing.cast(typing.Optional[UserParametersMultiStatementCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersMultiStatementCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a765e54a3b13b11f24e88dab153522f2fa788752837d01758ff9660f043e85f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersNetworkPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersNetworkPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersNetworkPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersNetworkPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersNetworkPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcd779b5dbadae0a783bbeecfead6dcaf4fbd3e71970a8a367bb55c4f46e07e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersNetworkPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a47f31c3445f7fdd5cfc3c8e8bf21a1525b108b204c61beff7bf01ebb2c9ee2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersNetworkPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4abe6c434ac43707ad705432a209a5694f1050ca100d724d69f38fc873db9d7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e213358cab89b1bdfc8d0c53d033d308e32021e5d45c7eb8122ac25c32f15b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b71ef10de7fa0e09025e3e51aa6c916969e196169dd8f17398b43027fd8f9e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersNetworkPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersNetworkPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42478bdddbb767b3622c563505b4332fc3e0224c60e4d3871845a151bee13db2)
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
    def internal_value(self) -> typing.Optional[UserParametersNetworkPolicy]:
        return typing.cast(typing.Optional[UserParametersNetworkPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersNetworkPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c391c85f20d2ae8bc589ddeda510f9538eedf4470983e7cbf66907d3571bcc31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersNoorderSequenceAsDefault",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersNoorderSequenceAsDefault:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersNoorderSequenceAsDefault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersNoorderSequenceAsDefaultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersNoorderSequenceAsDefaultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61c6136f73d74872a1f5b26b164f3c04424552c253be8b3fab6aa5ddc7aca282)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersNoorderSequenceAsDefaultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1127cd64575f97d94fca50ce59dfd65d5cf0be32e3bd27b2c50fa186df5de1c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersNoorderSequenceAsDefaultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c1e70cfcb664d12a184f457b39ae6b9bcc92126a9c967d0cd08b9555adf994)
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
            type_hints = typing.get_type_hints(_typecheckingstub__933b89476b8e0aa522740a0aadc0dfe44ebedbc3a07a6928e357451c5821cda0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06e7a1be8b2a56ce1736d7174de8116fbec56e1babb15bc46605a8152a515194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersNoorderSequenceAsDefaultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersNoorderSequenceAsDefaultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd1e3e90fd34386d927602d44feceb9794d82f64b15fb297a1a01f2af44da72c)
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
    def internal_value(self) -> typing.Optional[UserParametersNoorderSequenceAsDefault]:
        return typing.cast(typing.Optional[UserParametersNoorderSequenceAsDefault], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersNoorderSequenceAsDefault],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dba96d3b0d1b95b6cec42a058a90d1b5247102b743112873f5bcd25a14bf937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersOdbcTreatDecimalAsInt",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersOdbcTreatDecimalAsInt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersOdbcTreatDecimalAsInt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersOdbcTreatDecimalAsIntList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersOdbcTreatDecimalAsIntList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a07a7ceed183bbabe457bb26dcabfe50a2e7dcd4695100ae688a20cbe80e87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersOdbcTreatDecimalAsIntOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9163fd09b8160d09149cead8ad0fc5f68435c65d8a35f060d425ad1562087cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersOdbcTreatDecimalAsIntOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58a8f68758598f30ea4de5f55710f1d7c41a2a5f0f4644ee4af00ddca6be403)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f41237e35a3aed7e53365381417fd2af94804572c6bb872dc47b351a4f4ff60c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1913d16a8adc1f6d6cbb94b61cd3df6a1ebcca15bad565aea428c0f287d90922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersOdbcTreatDecimalAsIntOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersOdbcTreatDecimalAsIntOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__091665dfe9ca437f4c387aa22a6c8a0fd8df74d784bb7aec5a88c3dae6c860e0)
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
    def internal_value(self) -> typing.Optional[UserParametersOdbcTreatDecimalAsInt]:
        return typing.cast(typing.Optional[UserParametersOdbcTreatDecimalAsInt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersOdbcTreatDecimalAsInt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e795151e3323ca8bb6271ced5027f111a359aa78baae8008293e2a3b0ec6f7e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class UserParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ae5533879c2a6a1b0578cd47c8b317399b7dc007fe89e4691cc7b83569dd57f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="abortDetachedQuery")
    def abort_detached_query(self) -> UserParametersAbortDetachedQueryList:
        return typing.cast(UserParametersAbortDetachedQueryList, jsii.get(self, "abortDetachedQuery"))

    @builtins.property
    @jsii.member(jsii_name="autocommit")
    def autocommit(self) -> UserParametersAutocommitList:
        return typing.cast(UserParametersAutocommitList, jsii.get(self, "autocommit"))

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> UserParametersBinaryInputFormatList:
        return typing.cast(UserParametersBinaryInputFormatList, jsii.get(self, "binaryInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> UserParametersBinaryOutputFormatList:
        return typing.cast(UserParametersBinaryOutputFormatList, jsii.get(self, "binaryOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> UserParametersClientMemoryLimitList:
        return typing.cast(UserParametersClientMemoryLimitList, jsii.get(self, "clientMemoryLimit"))

    @builtins.property
    @jsii.member(jsii_name="clientMetadataRequestUseConnectionCtx")
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> UserParametersClientMetadataRequestUseConnectionCtxList:
        return typing.cast(UserParametersClientMetadataRequestUseConnectionCtxList, jsii.get(self, "clientMetadataRequestUseConnectionCtx"))

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(self) -> UserParametersClientPrefetchThreadsList:
        return typing.cast(UserParametersClientPrefetchThreadsList, jsii.get(self, "clientPrefetchThreads"))

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(self) -> UserParametersClientResultChunkSizeList:
        return typing.cast(UserParametersClientResultChunkSizeList, jsii.get(self, "clientResultChunkSize"))

    @builtins.property
    @jsii.member(jsii_name="clientResultColumnCaseInsensitive")
    def client_result_column_case_insensitive(
        self,
    ) -> UserParametersClientResultColumnCaseInsensitiveList:
        return typing.cast(UserParametersClientResultColumnCaseInsensitiveList, jsii.get(self, "clientResultColumnCaseInsensitive"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAlive")
    def client_session_keep_alive(self) -> UserParametersClientSessionKeepAliveList:
        return typing.cast(UserParametersClientSessionKeepAliveList, jsii.get(self, "clientSessionKeepAlive"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> UserParametersClientSessionKeepAliveHeartbeatFrequencyList:
        return typing.cast(UserParametersClientSessionKeepAliveHeartbeatFrequencyList, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(
        self,
    ) -> UserParametersClientTimestampTypeMappingList:
        return typing.cast(UserParametersClientTimestampTypeMappingList, jsii.get(self, "clientTimestampTypeMapping"))

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> UserParametersDateInputFormatList:
        return typing.cast(UserParametersDateInputFormatList, jsii.get(self, "dateInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> UserParametersDateOutputFormatList:
        return typing.cast(UserParametersDateOutputFormatList, jsii.get(self, "dateOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="enableUnloadPhysicalTypeOptimization")
    def enable_unload_physical_type_optimization(
        self,
    ) -> UserParametersEnableUnloadPhysicalTypeOptimizationList:
        return typing.cast(UserParametersEnableUnloadPhysicalTypeOptimizationList, jsii.get(self, "enableUnloadPhysicalTypeOptimization"))

    @builtins.property
    @jsii.member(jsii_name="enableUnredactedQuerySyntaxError")
    def enable_unredacted_query_syntax_error(
        self,
    ) -> UserParametersEnableUnredactedQuerySyntaxErrorList:
        return typing.cast(UserParametersEnableUnredactedQuerySyntaxErrorList, jsii.get(self, "enableUnredactedQuerySyntaxError"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicMerge")
    def error_on_nondeterministic_merge(
        self,
    ) -> UserParametersErrorOnNondeterministicMergeList:
        return typing.cast(UserParametersErrorOnNondeterministicMergeList, jsii.get(self, "errorOnNondeterministicMerge"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicUpdate")
    def error_on_nondeterministic_update(
        self,
    ) -> UserParametersErrorOnNondeterministicUpdateList:
        return typing.cast(UserParametersErrorOnNondeterministicUpdateList, jsii.get(self, "errorOnNondeterministicUpdate"))

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(self) -> UserParametersGeographyOutputFormatList:
        return typing.cast(UserParametersGeographyOutputFormatList, jsii.get(self, "geographyOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(self) -> UserParametersGeometryOutputFormatList:
        return typing.cast(UserParametersGeometryOutputFormatList, jsii.get(self, "geometryOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatDecimalAsInt")
    def jdbc_treat_decimal_as_int(self) -> UserParametersJdbcTreatDecimalAsIntList:
        return typing.cast(UserParametersJdbcTreatDecimalAsIntList, jsii.get(self, "jdbcTreatDecimalAsInt"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatTimestampNtzAsUtc")
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> UserParametersJdbcTreatTimestampNtzAsUtcList:
        return typing.cast(UserParametersJdbcTreatTimestampNtzAsUtcList, jsii.get(self, "jdbcTreatTimestampNtzAsUtc"))

    @builtins.property
    @jsii.member(jsii_name="jdbcUseSessionTimezone")
    def jdbc_use_session_timezone(self) -> UserParametersJdbcUseSessionTimezoneList:
        return typing.cast(UserParametersJdbcUseSessionTimezoneList, jsii.get(self, "jdbcUseSessionTimezone"))

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> UserParametersJsonIndentList:
        return typing.cast(UserParametersJsonIndentList, jsii.get(self, "jsonIndent"))

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> UserParametersLockTimeoutList:
        return typing.cast(UserParametersLockTimeoutList, jsii.get(self, "lockTimeout"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> UserParametersLogLevelList:
        return typing.cast(UserParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(self) -> UserParametersMultiStatementCountList:
        return typing.cast(UserParametersMultiStatementCountList, jsii.get(self, "multiStatementCount"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> UserParametersNetworkPolicyList:
        return typing.cast(UserParametersNetworkPolicyList, jsii.get(self, "networkPolicy"))

    @builtins.property
    @jsii.member(jsii_name="noorderSequenceAsDefault")
    def noorder_sequence_as_default(self) -> UserParametersNoorderSequenceAsDefaultList:
        return typing.cast(UserParametersNoorderSequenceAsDefaultList, jsii.get(self, "noorderSequenceAsDefault"))

    @builtins.property
    @jsii.member(jsii_name="odbcTreatDecimalAsInt")
    def odbc_treat_decimal_as_int(self) -> UserParametersOdbcTreatDecimalAsIntList:
        return typing.cast(UserParametersOdbcTreatDecimalAsIntList, jsii.get(self, "odbcTreatDecimalAsInt"))

    @builtins.property
    @jsii.member(jsii_name="preventUnloadToInternalStages")
    def prevent_unload_to_internal_stages(
        self,
    ) -> "UserParametersPreventUnloadToInternalStagesList":
        return typing.cast("UserParametersPreventUnloadToInternalStagesList", jsii.get(self, "preventUnloadToInternalStages"))

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> "UserParametersQueryTagList":
        return typing.cast("UserParametersQueryTagList", jsii.get(self, "queryTag"))

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCase")
    def quoted_identifiers_ignore_case(
        self,
    ) -> "UserParametersQuotedIdentifiersIgnoreCaseList":
        return typing.cast("UserParametersQuotedIdentifiersIgnoreCaseList", jsii.get(self, "quotedIdentifiersIgnoreCase"))

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> "UserParametersRowsPerResultsetList":
        return typing.cast("UserParametersRowsPerResultsetList", jsii.get(self, "rowsPerResultset"))

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(self) -> "UserParametersS3StageVpceDnsNameList":
        return typing.cast("UserParametersS3StageVpceDnsNameList", jsii.get(self, "s3StageVpceDnsName"))

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> "UserParametersSearchPathList":
        return typing.cast("UserParametersSearchPathList", jsii.get(self, "searchPath"))

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumer")
    def simulated_data_sharing_consumer(
        self,
    ) -> "UserParametersSimulatedDataSharingConsumerList":
        return typing.cast("UserParametersSimulatedDataSharingConsumerList", jsii.get(self, "simulatedDataSharingConsumer"))

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(
        self,
    ) -> "UserParametersStatementQueuedTimeoutInSecondsList":
        return typing.cast("UserParametersStatementQueuedTimeoutInSecondsList", jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(
        self,
    ) -> "UserParametersStatementTimeoutInSecondsList":
        return typing.cast("UserParametersStatementTimeoutInSecondsList", jsii.get(self, "statementTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="strictJsonOutput")
    def strict_json_output(self) -> "UserParametersStrictJsonOutputList":
        return typing.cast("UserParametersStrictJsonOutputList", jsii.get(self, "strictJsonOutput"))

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> "UserParametersTimeInputFormatList":
        return typing.cast("UserParametersTimeInputFormatList", jsii.get(self, "timeInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> "UserParametersTimeOutputFormatList":
        return typing.cast("UserParametersTimeOutputFormatList", jsii.get(self, "timeOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampDayIsAlways24H")
    def timestamp_day_is_always24_h(
        self,
    ) -> "UserParametersTimestampDayIsAlways24HList":
        return typing.cast("UserParametersTimestampDayIsAlways24HList", jsii.get(self, "timestampDayIsAlways24H"))

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(self) -> "UserParametersTimestampInputFormatList":
        return typing.cast("UserParametersTimestampInputFormatList", jsii.get(self, "timestampInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(
        self,
    ) -> "UserParametersTimestampLtzOutputFormatList":
        return typing.cast("UserParametersTimestampLtzOutputFormatList", jsii.get(self, "timestampLtzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(
        self,
    ) -> "UserParametersTimestampNtzOutputFormatList":
        return typing.cast("UserParametersTimestampNtzOutputFormatList", jsii.get(self, "timestampNtzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(self) -> "UserParametersTimestampOutputFormatList":
        return typing.cast("UserParametersTimestampOutputFormatList", jsii.get(self, "timestampOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(self) -> "UserParametersTimestampTypeMappingList":
        return typing.cast("UserParametersTimestampTypeMappingList", jsii.get(self, "timestampTypeMapping"))

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(self) -> "UserParametersTimestampTzOutputFormatList":
        return typing.cast("UserParametersTimestampTzOutputFormatList", jsii.get(self, "timestampTzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> "UserParametersTimezoneList":
        return typing.cast("UserParametersTimezoneList", jsii.get(self, "timezone"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "UserParametersTraceLevelList":
        return typing.cast("UserParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="transactionAbortOnError")
    def transaction_abort_on_error(self) -> "UserParametersTransactionAbortOnErrorList":
        return typing.cast("UserParametersTransactionAbortOnErrorList", jsii.get(self, "transactionAbortOnError"))

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(
        self,
    ) -> "UserParametersTransactionDefaultIsolationLevelList":
        return typing.cast("UserParametersTransactionDefaultIsolationLevelList", jsii.get(self, "transactionDefaultIsolationLevel"))

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(self) -> "UserParametersTwoDigitCenturyStartList":
        return typing.cast("UserParametersTwoDigitCenturyStartList", jsii.get(self, "twoDigitCenturyStart"))

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(self) -> "UserParametersUnsupportedDdlActionList":
        return typing.cast("UserParametersUnsupportedDdlActionList", jsii.get(self, "unsupportedDdlAction"))

    @builtins.property
    @jsii.member(jsii_name="useCachedResult")
    def use_cached_result(self) -> "UserParametersUseCachedResultList":
        return typing.cast("UserParametersUseCachedResultList", jsii.get(self, "useCachedResult"))

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> "UserParametersWeekOfYearPolicyList":
        return typing.cast("UserParametersWeekOfYearPolicyList", jsii.get(self, "weekOfYearPolicy"))

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> "UserParametersWeekStartList":
        return typing.cast("UserParametersWeekStartList", jsii.get(self, "weekStart"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[UserParameters]:
        return typing.cast(typing.Optional[UserParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261fb652a7200b854387f52d2e4ad90b5d9855878ca22a2d08446e7785c29e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersPreventUnloadToInternalStages",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersPreventUnloadToInternalStages:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersPreventUnloadToInternalStages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersPreventUnloadToInternalStagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersPreventUnloadToInternalStagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cb3c3c43ae7d941baa269dcedf8aeab373f9c2f1d2a75c5fc7656b0e1a72f1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersPreventUnloadToInternalStagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018b7551f2bb4e5d14a309087b2bf546b367f6d42b40377970eed30f11476516)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersPreventUnloadToInternalStagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f71733c466a3df53094b4244f63cebc172f9ae5bfde2b4b1ffb747031ffd1fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b68d63c80b5200f85a8f5f0eaa1bd2a34e42a925801105b1de69d95103e1fbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a4ec488898942d6b1c1f2e56812787dca9e4c69c64006eddcbf544e06478d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersPreventUnloadToInternalStagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersPreventUnloadToInternalStagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bb4e8b390e6d2d6178a536eef8f426f3608071d4bd276773eec2db6e427ae6f)
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
    ) -> typing.Optional[UserParametersPreventUnloadToInternalStages]:
        return typing.cast(typing.Optional[UserParametersPreventUnloadToInternalStages], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersPreventUnloadToInternalStages],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d67208c1e7eb65aa0af4d715454edea47102c45299d5cdf0917255ba071de29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersQueryTag",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersQueryTag:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersQueryTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersQueryTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersQueryTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9120dfd2379f6ed7ed003537afba6d339499e6718bcea2e19049c7b66f96ea82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersQueryTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7a581bcfe8eba700e9684ee67e4e22f7837cf177483f2b7968953bf79887fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersQueryTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9521a1bbdd89453b6a9dea4517893277fcb5fceae40ed90132ab362bb8f23aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__818596e14438803dee345ce2279b9dabd4a1a52b5131f60770dab54710cc1a7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__528775edf680e535f1f612c576bed94efda0b378231963f31168b526770c53f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersQueryTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersQueryTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c4aeeac37315ce3599bd41a4b108ecd452f2587d0b2bec1f20388074706fba9)
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
    def internal_value(self) -> typing.Optional[UserParametersQueryTag]:
        return typing.cast(typing.Optional[UserParametersQueryTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersQueryTag]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393331a2eb85a4b1281b5f41521a77663bb418300f4f7967e8bf11dd84a94bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersQuotedIdentifiersIgnoreCase",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersQuotedIdentifiersIgnoreCase:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersQuotedIdentifiersIgnoreCase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersQuotedIdentifiersIgnoreCaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersQuotedIdentifiersIgnoreCaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04213fa0eeab529508eb3dedf6b9fc9121572feb6226f1d7ebf01026d4356801)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersQuotedIdentifiersIgnoreCaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268ed42e925b7acab8042c82fed52d8e20b35b836b46691ffc263dd729b9fc7d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersQuotedIdentifiersIgnoreCaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93b7e7bbb9c0e4779a7d6cebbef27a635623699d5bf2151698affbc9da83f78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a92055ce3b2073260d586d23a974427e5e0d68ffab14c5cf1772d8734df31895)
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
            type_hints = typing.get_type_hints(_typecheckingstub__529b0e9dce8b976fc867bbdf3161a00d050c3f42ce5e0dc1958576e4d71f54da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersQuotedIdentifiersIgnoreCaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersQuotedIdentifiersIgnoreCaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45e05a5c0fc50b17cbc5bc20f83ecf38c2d8850ac4ac36f21cdee9408999be50)
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
    ) -> typing.Optional[UserParametersQuotedIdentifiersIgnoreCase]:
        return typing.cast(typing.Optional[UserParametersQuotedIdentifiersIgnoreCase], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersQuotedIdentifiersIgnoreCase],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96f951661ba9b0033e9a2505ac5ed27ce52f8f2f20781e6a38306fe3daea178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersRowsPerResultset",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersRowsPerResultset:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersRowsPerResultset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersRowsPerResultsetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersRowsPerResultsetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__968162573b4b1d2cf57b777264933fb165242b1e28dbf7bebe3a866d308ad1dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersRowsPerResultsetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d3ca2817795c967d6e4305c85ecaa186d3137c6843115dd4e79ede18b4e30c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersRowsPerResultsetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4028359aabff2c2e83e8d3a879ca85d8c2a2599d436f05af5ffda0c8fa2c50db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcbea1bcbb9e1123e9eae6faf8677a49f4be372f57c1b3186decab793d1dd566)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c7119dd959e4721634c6242786439fb827db644585760db89e10497ee589310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersRowsPerResultsetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersRowsPerResultsetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71ff1f692c9a1f6dfc384754579b84c3312af9cb95b2193fc3e097166c07d539)
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
    def internal_value(self) -> typing.Optional[UserParametersRowsPerResultset]:
        return typing.cast(typing.Optional[UserParametersRowsPerResultset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersRowsPerResultset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e551fe1360916a12ffd56bd70540f08b00929f0209685b6008b9d2192558a476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersS3StageVpceDnsName",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersS3StageVpceDnsName:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersS3StageVpceDnsName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersS3StageVpceDnsNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersS3StageVpceDnsNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f37ea95eb76b0c72c030bbf126179b1c9569980661680d58755f1b105048f33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersS3StageVpceDnsNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9176d5c2a9d1848b90057170ed2ab149eaf0cb6f7ef517a05c0ad0837f5518c5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersS3StageVpceDnsNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3a2d196d84771ca215085a0ec9ff4a20377e2ad6af4b08e42389333a1860e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c56f3961aa8f03fc6dd8841b3d5aab0b08b7ffd9affa01925a97e86bbf8853b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfa1370bb9e2ad8a499c3a1281a5bdeef45dfc0e66336ee19e195f3a4ee4a9c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersS3StageVpceDnsNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersS3StageVpceDnsNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6d0707b2b8d9e38c41e1fae01758b23e7453f148f44491e6ee19e9d81e81c55)
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
    def internal_value(self) -> typing.Optional[UserParametersS3StageVpceDnsName]:
        return typing.cast(typing.Optional[UserParametersS3StageVpceDnsName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersS3StageVpceDnsName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cccb31e7cffd6d62a4fe3000988786afe5cc16a86ccf65bf9722dc17bc5438a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersSearchPath",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersSearchPath:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersSearchPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersSearchPathList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersSearchPathList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3a5f5629648682179b46f0335712e4c22517a363e30427576523eaa9ca4dba8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersSearchPathOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8eb288d9f36b909277dac2968222fefc3df1545b4fb2b176c60c35c6e1cf35c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersSearchPathOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19e46b01797df4bbbe5f71eb872e9bc63a7b149ec460b716088fc858ec0025d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a55bf9ff6cfee6a7a9ef07866e19efd4c84c1e6341444ddbda8a08421055fb45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96444e572e3994315d8d6fa38e017655f08995227753885743ab93199ebf2243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersSearchPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersSearchPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f245de31e57c533ec399994f9e7c977ec6c850c38332ab9523ff97f765af0587)
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
    def internal_value(self) -> typing.Optional[UserParametersSearchPath]:
        return typing.cast(typing.Optional[UserParametersSearchPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersSearchPath]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__124857773a89bba1a7b5789fa43bb7dd1314a4178213e01d103d67f418dc3710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersSimulatedDataSharingConsumer",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersSimulatedDataSharingConsumer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersSimulatedDataSharingConsumer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersSimulatedDataSharingConsumerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersSimulatedDataSharingConsumerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02400147603bd2049225e754a86bc052e2f51b72d3bd96b16b12da86b40b93c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersSimulatedDataSharingConsumerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbe85d0ae333f6e1a56a22bf00d97a5df445f15c3c646e694c804c9226a241b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersSimulatedDataSharingConsumerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1e8fa8002b4c93dcdaa5d77dda6f86ebb9600b48c0d3db3ef64c0980c86e41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__381a0c3a3d6edd3d6742cd7f802b3682af10aa954c4658fb6c39ad6e261dee13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ce0b1289dbc6f3944ab05e6264772ee4a0ba40dcc88effb35004495866a58ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersSimulatedDataSharingConsumerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersSimulatedDataSharingConsumerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ce3018c9ec09b503a1fac8e3570b2426fc764708c2ecabc73ba31824f1aadaf)
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
    ) -> typing.Optional[UserParametersSimulatedDataSharingConsumer]:
        return typing.cast(typing.Optional[UserParametersSimulatedDataSharingConsumer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersSimulatedDataSharingConsumer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0438d11df748f48b72537096259aad8282294e54c91aa476033d1792baa2ac80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStatementQueuedTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersStatementQueuedTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersStatementQueuedTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersStatementQueuedTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStatementQueuedTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__792ca85508a3aff48948a84535f418bce32e978b0014ea4868b78941b5514b4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersStatementQueuedTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4ed6496c0bb67b115d0e3fa7700ee47dfb4ca7e2f8dd4389b4c80f7299eb0e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersStatementQueuedTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc6c455cd5d3d4a97c532b6bdc004bc9d9bd861c5865a6c0c9f48950f75ff19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e516843545fb27f1418e94d2fd1e3dc70f4b34e1e49554c0619dbc7b426ce1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7022cc4fe14c939d145eac0e81bf0f1187586cb5011076b017abae4fcbe52edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersStatementQueuedTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStatementQueuedTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6de74165a23cdc4b1d2690b402e853f956baadfddd7221fa29da2abff1301dd5)
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
    ) -> typing.Optional[UserParametersStatementQueuedTimeoutInSeconds]:
        return typing.cast(typing.Optional[UserParametersStatementQueuedTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersStatementQueuedTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d376f09df94245927e53cd01f47731199e14823a409e6524ddf0328555c9090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStatementTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersStatementTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersStatementTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersStatementTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStatementTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1570061015faf48707208f2726a2eb4a56521ba0eab0c92a78ea5a7c097434f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersStatementTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fcf829ae93125bcac6fbe9c1fc9a1218e162a79ad54ffe913d3867bebdd96c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersStatementTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185cd36ab394201523e080d64b8461ee99c06cd514a63007e3ca459ac9544580)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74efaaeb10dd49a3f678b869593c011691e41c9d00817315af44b7dc5302aed3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c964325ff76427766b19dc0a5d0ee7bf9d49bcd13cb9cf2d3c6926d3fbc9aa49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersStatementTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStatementTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8547673412418ba87c18f077a1db58172133108f1126684c1abadf9d7deacc6d)
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
    ) -> typing.Optional[UserParametersStatementTimeoutInSeconds]:
        return typing.cast(typing.Optional[UserParametersStatementTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersStatementTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87e41653948f22ff8a1ab124a17afb330bd9b53b11aefdd52bb9280ffef4f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStrictJsonOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersStrictJsonOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersStrictJsonOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersStrictJsonOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStrictJsonOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15c5b2b65059b48a430431c82bddb000432c1e959242206d73240b85fecc1801)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersStrictJsonOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40aa941c4beb46b90a1b8e8c5c0629b73c189884a7632371282a919f2f36b241)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersStrictJsonOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9400ab9235ed6ae82cedf4e8c7302ee23504335a492e828e6fbab656c935ad8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__583838fbdab100ac167244622b4b13223df17e27fc3a814dfbc682ad9d64c493)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a31ecfe88dd1c4324f7809a60fc1d4a6d2382ebf61adf9aae4d39a63fcb84da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersStrictJsonOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersStrictJsonOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a14fc595352ea5a27c0f2b04c67b2adf9455cab3417426624d37945e1974295b)
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
    def internal_value(self) -> typing.Optional[UserParametersStrictJsonOutput]:
        return typing.cast(typing.Optional[UserParametersStrictJsonOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersStrictJsonOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7906cf058ff39c6a885783538251dee055e1afd0544e8e43abb20e8b68f0a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimeInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimeInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimeInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimeInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimeInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae04dd13155bf861e0a6be066b5d7faf0395741567dcbd43507c6e6d212615ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersTimeInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3577ac1540d39a2b50f56547c1f40b24478fa11b730f7885c7f153cf1b2f35e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimeInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed688932978e8302275550ed1c0f2522ffbfbc97b1a2fe862f27e21de9860f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__804905f1b40b35a85bdf3348c08741235d3e8a14b00935513dc88402af2a2a82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b17e0c61ddd41af9614e9eeb2b1fe67f1611e4e5968644839f17eafe6bf4d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimeInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimeInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__064a9ab7cbf23cc3431d572f7698f1fead54b57363d0a706e4109e9500eb7d68)
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
    def internal_value(self) -> typing.Optional[UserParametersTimeInputFormat]:
        return typing.cast(typing.Optional[UserParametersTimeInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimeInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4c8ad67bcb38e2b52b2bc9e1721cb8bdc2994e61bedb0e39a508a53c808f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimeOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimeOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimeOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimeOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimeOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a933064c1368864be77b140c9b2e5039b96f7f6316175cb74385b90dbdb5cc7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTimeOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9ccc1979550f9dc1c4e956c076d345e236c43bbc66b84aab44ba0a7250e04c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimeOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5646ec0a2b3ed48aba0628315d8aee2cd347c7384826ad6b05067f3ed4a6684f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3468394680744f38d4c6a2aae11dc8fe9faaf035d38891b14a8b64d81286a687)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0778a6ebb88f79ba6c3020c616de4c9f0be48f6beb287ae92ebc4b53c377c2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimeOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimeOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9df03b1be48f2c784a31108d7879caaca4ae32c1a7a731b35806c790bf57740b)
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
    def internal_value(self) -> typing.Optional[UserParametersTimeOutputFormat]:
        return typing.cast(typing.Optional[UserParametersTimeOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimeOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738f457f4afd545f623d246308eb22410c57fece686468478fa224eeaf58edb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampDayIsAlways24H",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimestampDayIsAlways24H:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimestampDayIsAlways24H(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimestampDayIsAlways24HList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampDayIsAlways24HList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f169eae7e66f3df15e1e3e66aac98157d4832aec8a106d8460b3498cb82368d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTimestampDayIsAlways24HOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5998ce4765c246943fe3442332265a6af915289af2525e2877a69a705fc98a5e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimestampDayIsAlways24HOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016cd0b86800703890e2ecc188d3e5b05818e6214e258938ade58a6788a73034)
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
            type_hints = typing.get_type_hints(_typecheckingstub__101099c30fc9a6e15edcd84c482aa0d83f45519122872c3d3b87ee7e4ef02a25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95a984621216583340552f4cd9ed9ea6fc71c3f767640324a9e894cbe5ac9db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimestampDayIsAlways24HOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampDayIsAlways24HOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e061e4b5473e05b866087e5eff533840175ac171eb8d3d838d76bc77550455ea)
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
    def internal_value(self) -> typing.Optional[UserParametersTimestampDayIsAlways24H]:
        return typing.cast(typing.Optional[UserParametersTimestampDayIsAlways24H], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimestampDayIsAlways24H],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717ef67b4a0dac7493b15be66dbca0a23bbfa0d11915d04e54e3f98a595400e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimestampInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimestampInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimestampInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1693568474ec6551709b67b34c00df6991eea3b6838c62930869e23a5f5bc35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTimestampInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c8ed7b8eedb568c967d1526fb666824d6c081ae06c1d07adcad6d3ca4ed9e7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimestampInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215819e98f3028deab408a3b2945681d4e4fd6abe186d07894fa65f6d940afa3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73d37463bf75ce84801802226be6966469dc9a1ba28922d5856dfef195fedce3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54cde81827d686c70504530aab3d3ae93a1109d305bc047ba3e6fdedd9304d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimestampInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a089184ab607215bd04ab3d6ea40c6d630d88809eb09ebb50e0f7b2e02911fa)
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
    def internal_value(self) -> typing.Optional[UserParametersTimestampInputFormat]:
        return typing.cast(typing.Optional[UserParametersTimestampInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimestampInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716d20dbd9f6ca6f82f4acb8793c2022f4fc304bda0a8720cd2805edc2b92114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampLtzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimestampLtzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimestampLtzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimestampLtzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampLtzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b1b0bcb722c57338d17e3650470e518b3ad2402f464f6ca9da448012496efc2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTimestampLtzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5506ee2a6de6217d9a2f16601c6ffdaf69f405bfc9f8b5d4f7757f9aa8c242)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimestampLtzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcc4dbf06831818c590734a531f6234d31020e9de96c41a91949cc1a58424d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8cd5bdb0eb7ac8dd95508e74b38b178f88a2b2438a886ed550de41b36305776)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a25c7f20b480d300ad53bfb4409812553bdf4a04d1c88bb997f1bb5f108fa01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimestampLtzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampLtzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3f48a00aacf6e165cab642c3efca2f1143211cb91b2951fff23aff3056ea059)
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
    def internal_value(self) -> typing.Optional[UserParametersTimestampLtzOutputFormat]:
        return typing.cast(typing.Optional[UserParametersTimestampLtzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimestampLtzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e6355969f6bda481434587ca937b8f9a8573d0b987d0e2ffa6ac42bec4c60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampNtzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimestampNtzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimestampNtzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimestampNtzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampNtzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26b2e964f719e7bc77d887a7b453c33a0e6af02be5c5b137c9b10e04237108ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTimestampNtzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d50544f9369490d0dd2681c849d086aa9e525f4abe35b00d4f94482ecdc7a17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimestampNtzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced24ae34e46f5ac2e27e0e7068d67663b210b532c633e289277094d174c0b95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0dfb03f4da2a6ef3a9b752e2fc93c75343a86d1338fcea0cdfc7d7f5bba3e93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd3364f77374b2b32b4c46a56fd7e4cf2f831d89fe055158ad3e03bc8452917c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimestampNtzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampNtzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10a8c5fb93649722ff7c2d75b921ba388aeea9208272d17ede96efe93a5f1d95)
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
    def internal_value(self) -> typing.Optional[UserParametersTimestampNtzOutputFormat]:
        return typing.cast(typing.Optional[UserParametersTimestampNtzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimestampNtzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdca95a27e3821d516926abcb67920dd41f12cdcdd9850faabe527197f33bcd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimestampOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimestampOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimestampOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5491d7eb536507594b01c93a26292bb24e52eb2bdc897fb6343909bacea14f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTimestampOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26db9d4459bde59f8456c545a5847462664ac354b6054c1e6fef6b85cf86d678)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimestampOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d389eda024c8ef90890830aae72972eae5d8edfdec5ab40bbebcebc06e0d6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dba773a9b2fe7238f3103935cf9eda8015f317dadd993835044b73e58b5e43f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb6a680307145e65c7ce09110a572fdc00b7296d3effdf2d965a7d26de6117b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimestampOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ec6954a73e856b9535c9286788c6769b5ebae4a3165f72da13da6dd29743218)
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
    def internal_value(self) -> typing.Optional[UserParametersTimestampOutputFormat]:
        return typing.cast(typing.Optional[UserParametersTimestampOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimestampOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc906878fe4542f0640c51330dbcc18bf57010a88695dcdcba26cac249cdcc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampTypeMapping",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimestampTypeMapping:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimestampTypeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimestampTypeMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampTypeMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0004f8dc9b08712ef5e5edad43a165cb0695e24884cce5ec02deeb189cb1b8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTimestampTypeMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23cba309384b1138adb69c96d4471fd801d2059c3c299680fdca22ccb42bdbc0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimestampTypeMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8882f92300f21825568b2bbcef84afc082a8c010436f399a46de89fbce773a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eb5fd4c546fde6a2f0eaecf9cb85f3bed951c6b9c39a2b5d2a14a24bc20d1e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__135c97c56f81c2ed43364c16f961c3248b2c3aa2d4009e9d2416300654a1891c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimestampTypeMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampTypeMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b90814e2ebf4536c4fb29787e90195655f24ee6e538457e0407f70789e99c3ed)
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
    def internal_value(self) -> typing.Optional[UserParametersTimestampTypeMapping]:
        return typing.cast(typing.Optional[UserParametersTimestampTypeMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimestampTypeMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32089263342acf7b01210af1095665bb959635f094f94c2f064bb4b006884efa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampTzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimestampTzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimestampTzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimestampTzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampTzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a51901286659556558763517d23b47e0f49b2a0df6becff0f3c1ea631627ce53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTimestampTzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578ce33f9efb109b36484cc8ee129ac591f2cf585b4a222ffb2baf630eb955c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimestampTzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1b76ec0f7bcff3c3dda274bba4b77897cbe4c4f27955e5e0e9fd8601ae6cee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf297114b5f0e58a288cc112fa6419d1a0e2c701ccd2ee93c142570c539d698e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c55503b375d844d3b42eaf30151a657e92cff40bcf613cb26bbb030112bbe268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimestampTzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimestampTzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f0e5445d07508a7be7ae9aef6bb0b2bbce667500d3e0e7762f246fc155dd91d)
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
    def internal_value(self) -> typing.Optional[UserParametersTimestampTzOutputFormat]:
        return typing.cast(typing.Optional[UserParametersTimestampTzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTimestampTzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d6d1041edae8b7826d30dd631cfead1dd7958af9e8fbe71710da4f33a2c293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimezone",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTimezone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTimezoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimezoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__806a37a9f9d12256625e195e0ee0fd0f40de8f954d72baa9343b8a4fca4d572c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersTimezoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a28981162e1d575d26d52cccad277f946edf7e6ed26945810b6214c9794c1f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTimezoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d391730f4d154e84aef7d6ed63640ab8c55f0cd699b052229cc1ceb29ad6dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd40bc00b5a2781b53e52b8d2334483efdd1a2b7b10306a789f5cf5781aede30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd99ed3c67f563b028667470033b70ddc404eaec8aa58830b712640945f0f3ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTimezoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTimezoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01be5d2920049d5efd9058362c0643c1ef34233fccd087bd957e210ef1cab653)
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
    def internal_value(self) -> typing.Optional[UserParametersTimezone]:
        return typing.cast(typing.Optional[UserParametersTimezone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersTimezone]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea562036da29045b7caa97398e638f65c56ff3a32bf5d29250dba3b01c1b012c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bdda2d5ab02da898525a58afaf27cea0cdc4fcbd727cabcb06e6332a91981e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd65409fd4415a78c8593c9bd67bc71bdd5f93356cdff3232759408f49795f2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396ef69ec8a6032f2f923a9db2330746d22055a3b29fdd82c7322afd486ec9e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99cb268f1bb8f5d70ca900979464dee10c6e301f67e2bd685728ebccbec31667)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd27a92935b3893b148688b31cf8009c7662316be571545adac6c685801cd7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b66ae31051e62666b47f4173654a188fcb316f8468ca8640261a960442375e25)
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
    def internal_value(self) -> typing.Optional[UserParametersTraceLevel]:
        return typing.cast(typing.Optional[UserParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersTraceLevel]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df640224cefd813fef6b5cff6770311a727ea3062df2c072867e4f61130077d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTransactionAbortOnError",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTransactionAbortOnError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTransactionAbortOnError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTransactionAbortOnErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTransactionAbortOnErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2649b6b9255f07045da3890146939230617f6de8bfe73a5042041fbcea491f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTransactionAbortOnErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc74eacd8adbc9229e866003c299fe35b96bf6219609174755ab1614a51e102a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTransactionAbortOnErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c5d94328aa612f6625ad439c43fba19f2c71d593825b0aeb60304fdf08eb20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71e7cd1c118517765cac16667fa0beca83e50b0fe33396d5210d14e0c163a001)
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
            type_hints = typing.get_type_hints(_typecheckingstub__351370c3fad51d0553ce320e374e23a688e99825e155726c3f775fc1517794c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTransactionAbortOnErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTransactionAbortOnErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fbacfeb6abb0f2a1e5077959fb9b214f0d0ac1b63a4ff5b7c1b4f84ce33917b)
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
    def internal_value(self) -> typing.Optional[UserParametersTransactionAbortOnError]:
        return typing.cast(typing.Optional[UserParametersTransactionAbortOnError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTransactionAbortOnError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b041e0713924a15bd9785ad213809faa629a0e589c7365f2917e246c5d49b359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTransactionDefaultIsolationLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTransactionDefaultIsolationLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTransactionDefaultIsolationLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTransactionDefaultIsolationLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTransactionDefaultIsolationLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__673bd8e67d3652949fdda7f1725608aa1b1f221f4381bc207b0803ea2c440100)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTransactionDefaultIsolationLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e51cac7b67392fa5ab119920336ffe93ffacbd4e4f7d615df71c6be71f6cec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTransactionDefaultIsolationLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20259db11fe598f2453fbebaab19a313d3a370a0bebbce0c4af9fda909b93d6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a645d511c7061a9305531af13c62227a312da71af59824ec5b4478e33b84e24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0431cda7a7db99f4411f2b780b85e9e7f07caa30a653947c2f53bbf22d70c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTransactionDefaultIsolationLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTransactionDefaultIsolationLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bbd7902633f7dee20fc9612bae94242a274422e2ac277d19d7e7dc61fbdf1a4)
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
    ) -> typing.Optional[UserParametersTransactionDefaultIsolationLevel]:
        return typing.cast(typing.Optional[UserParametersTransactionDefaultIsolationLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTransactionDefaultIsolationLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edaca4f270ad8fb3ea7e249f4a025e7d429d54ee182560f414564954c0f9e832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTwoDigitCenturyStart",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersTwoDigitCenturyStart:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersTwoDigitCenturyStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersTwoDigitCenturyStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTwoDigitCenturyStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27f269f3b8b0068182caa8bb3b69b1c5cbae4af5ac916f9acdbefa7c7b1bea72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersTwoDigitCenturyStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75835f1623e216011b20946eb0c78ddd32111a45b7b99e9ae0025a26e9c2a5a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersTwoDigitCenturyStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1214365a59b4067786f35cf3147ab785ee47265d98cee83467027dd4e7fc6f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f25ee19c64796a08e66d876b0aa7c2318ebcf07db821705b14a7587c6844c1bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__794a0530630e7d7e13bba1cf3d4c4ca94574b351845394b0570355ceeb0a59af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersTwoDigitCenturyStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersTwoDigitCenturyStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef7ad2f9dd55207b1c05908cdbff19dcb5b6fa9b339f9f0c14226fdd66d91cdf)
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
    def internal_value(self) -> typing.Optional[UserParametersTwoDigitCenturyStart]:
        return typing.cast(typing.Optional[UserParametersTwoDigitCenturyStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersTwoDigitCenturyStart],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae16a24a001c24a97b01655521e10ae37b61656c5f72d782172bedca13f0969e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersUnsupportedDdlAction",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersUnsupportedDdlAction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersUnsupportedDdlAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersUnsupportedDdlActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersUnsupportedDdlActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d282d202ed696dbec7c6f233d93ce77e4d96cc10513fa4eee6b4e88fddc8abc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersUnsupportedDdlActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c0d6074eec82f55c40611d4065e00078eeae777cf8b9f0bd4a22e4b7a16308)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersUnsupportedDdlActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf7c11a9cbcdf8835cae53e0a0837d120feedf3a4e349a37882111f2cb164ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__caa1a7496017a868d8e466d6ad4249aab086897a244a9c0cfa2d3f945d1c6f83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__832e935af80a95bd4f50e3c80847ef8acba66cf2e8b82c9558dbdf6f80a08b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersUnsupportedDdlActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersUnsupportedDdlActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc6fafa03f45db980559ee9ced0605a7c57684b9fe762d56e080c234de7c6294)
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
    def internal_value(self) -> typing.Optional[UserParametersUnsupportedDdlAction]:
        return typing.cast(typing.Optional[UserParametersUnsupportedDdlAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersUnsupportedDdlAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cbe52a0ad56c9d332e70ae2a9972d6166c51efbd9bdeecb28fdc7d3082e1ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersUseCachedResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersUseCachedResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersUseCachedResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersUseCachedResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersUseCachedResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8520b1a13b34f1a331916421f007c39c7f242f442967dd872a97af1c8006f045)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersUseCachedResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12967a2d56e13fc00769f7ba2a691d6fc022579d9f16a7d72eaebfadd1f7764c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersUseCachedResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414c98279dcaac6d537d1af3189c73e1af4477f7471c76ed4a24164e7b3a61ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a122bd33307887e72c6fcc2d7f65da63bbaf02e29c4ebb34bec4e6bb81f2463)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e53556b62c5da6e0b11590401ac31f56abc6c6a5d16a2223c7eab3f20907f1eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersUseCachedResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersUseCachedResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d6301ccff45ceae709c62ebc1096b1cc9a9fd916b347acdefec650b0f5e1c03)
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
    def internal_value(self) -> typing.Optional[UserParametersUseCachedResult]:
        return typing.cast(typing.Optional[UserParametersUseCachedResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersUseCachedResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4031dd206e29e3026401aac901ab53853283e137d3b354189efd8a896aff8097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersWeekOfYearPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersWeekOfYearPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersWeekOfYearPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersWeekOfYearPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersWeekOfYearPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38c7d1e1dd755832225d3cf1b59306b20b54aebdc7c23f023c22f234c60067ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "UserParametersWeekOfYearPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec072a096f13a8bfd4f6e71ad9fbef8f363f1aac96c442eb202a8aec8e7fd0c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersWeekOfYearPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ac5835be809c9999f7e4d1a73deff0739700c5563c71888b59275b32ce2e86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6b50a204d40bce05054f72516ceb9423d3af7396de0af4abd9357b3979db758)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c369388a6c652b31516120dd56854ab75f52a53f7d31f87a8edbe8dc8713f814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersWeekOfYearPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersWeekOfYearPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8c04659223551e0c9837a82fe05c9967d18abaaf4b90eab4b7d8fcfba539ff0)
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
    def internal_value(self) -> typing.Optional[UserParametersWeekOfYearPolicy]:
        return typing.cast(typing.Optional[UserParametersWeekOfYearPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[UserParametersWeekOfYearPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf390ebd2309cf85ebc8181bd5701401c4f57db796d21888fafd4b3a96155254)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserParametersWeekStart",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserParametersWeekStart:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserParametersWeekStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserParametersWeekStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersWeekStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d6dc09643dfb57f28bc4d4b58d55a04ffe2c6fd89a3ec9d0b3d54ddaa9721ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserParametersWeekStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7274d83b3089e9121d6a215b9709e48d425d8f931e5f0cb1ab3e57ab4fe763)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserParametersWeekStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df033cacc293b085b4c93221a721bf59daa404dd59bf12266dd5cf263ed38b2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58491bdfc6a7efbf3d21b4eb14f41fbe9ee2a3562c9cb8fd88c0476992409fae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__909172bcef351b8421de16768e1ff26dc3430fd4ec0f4d58ff8398566e15ebd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserParametersWeekStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserParametersWeekStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04eb9dc210cd2b5ca9556fc384dba209bff87089d5778b309d3db6bf1dfc26e9)
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
    def internal_value(self) -> typing.Optional[UserParametersWeekStart]:
        return typing.cast(typing.Optional[UserParametersWeekStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserParametersWeekStart]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4389d47458703556269e202105bcb0804f36db9bafeacb452bb4b18574459740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.user.UserShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class UserShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class UserShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19c5ff046692b04d5212ced3362c15ab68585601d1632ccbdae80d512bd4fcf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "UserShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdfddfab580638872268a66fcc0a4c191b0cbe4876eb313aef4e0d11a371a2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("UserShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb83f75c4326383f5fe9734e98e5d44f792e68a8ae5904f57637f9b1a05a924b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e420039010102de85f30848cb7f6cdb7a72bde3604f5d948f62f8f45f69401e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62e7420aee03c4ee44b427605ebe0ceaf5de81f566a71667ad5bd6aae8950627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class UserShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.user.UserShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c867eade738db7501a57f8c054641ff9b1b84954ab1e530086454d0611a256)
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
    def internal_value(self) -> typing.Optional[UserShowOutput]:
        return typing.cast(typing.Optional[UserShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[UserShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c809a8cf07ab489d412093d9893bc110052e095772185ff118ac179df599a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "User",
    "UserConfig",
    "UserParameters",
    "UserParametersAbortDetachedQuery",
    "UserParametersAbortDetachedQueryList",
    "UserParametersAbortDetachedQueryOutputReference",
    "UserParametersAutocommit",
    "UserParametersAutocommitList",
    "UserParametersAutocommitOutputReference",
    "UserParametersBinaryInputFormat",
    "UserParametersBinaryInputFormatList",
    "UserParametersBinaryInputFormatOutputReference",
    "UserParametersBinaryOutputFormat",
    "UserParametersBinaryOutputFormatList",
    "UserParametersBinaryOutputFormatOutputReference",
    "UserParametersClientMemoryLimit",
    "UserParametersClientMemoryLimitList",
    "UserParametersClientMemoryLimitOutputReference",
    "UserParametersClientMetadataRequestUseConnectionCtx",
    "UserParametersClientMetadataRequestUseConnectionCtxList",
    "UserParametersClientMetadataRequestUseConnectionCtxOutputReference",
    "UserParametersClientPrefetchThreads",
    "UserParametersClientPrefetchThreadsList",
    "UserParametersClientPrefetchThreadsOutputReference",
    "UserParametersClientResultChunkSize",
    "UserParametersClientResultChunkSizeList",
    "UserParametersClientResultChunkSizeOutputReference",
    "UserParametersClientResultColumnCaseInsensitive",
    "UserParametersClientResultColumnCaseInsensitiveList",
    "UserParametersClientResultColumnCaseInsensitiveOutputReference",
    "UserParametersClientSessionKeepAlive",
    "UserParametersClientSessionKeepAliveHeartbeatFrequency",
    "UserParametersClientSessionKeepAliveHeartbeatFrequencyList",
    "UserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference",
    "UserParametersClientSessionKeepAliveList",
    "UserParametersClientSessionKeepAliveOutputReference",
    "UserParametersClientTimestampTypeMapping",
    "UserParametersClientTimestampTypeMappingList",
    "UserParametersClientTimestampTypeMappingOutputReference",
    "UserParametersDateInputFormat",
    "UserParametersDateInputFormatList",
    "UserParametersDateInputFormatOutputReference",
    "UserParametersDateOutputFormat",
    "UserParametersDateOutputFormatList",
    "UserParametersDateOutputFormatOutputReference",
    "UserParametersEnableUnloadPhysicalTypeOptimization",
    "UserParametersEnableUnloadPhysicalTypeOptimizationList",
    "UserParametersEnableUnloadPhysicalTypeOptimizationOutputReference",
    "UserParametersEnableUnredactedQuerySyntaxError",
    "UserParametersEnableUnredactedQuerySyntaxErrorList",
    "UserParametersEnableUnredactedQuerySyntaxErrorOutputReference",
    "UserParametersErrorOnNondeterministicMerge",
    "UserParametersErrorOnNondeterministicMergeList",
    "UserParametersErrorOnNondeterministicMergeOutputReference",
    "UserParametersErrorOnNondeterministicUpdate",
    "UserParametersErrorOnNondeterministicUpdateList",
    "UserParametersErrorOnNondeterministicUpdateOutputReference",
    "UserParametersGeographyOutputFormat",
    "UserParametersGeographyOutputFormatList",
    "UserParametersGeographyOutputFormatOutputReference",
    "UserParametersGeometryOutputFormat",
    "UserParametersGeometryOutputFormatList",
    "UserParametersGeometryOutputFormatOutputReference",
    "UserParametersJdbcTreatDecimalAsInt",
    "UserParametersJdbcTreatDecimalAsIntList",
    "UserParametersJdbcTreatDecimalAsIntOutputReference",
    "UserParametersJdbcTreatTimestampNtzAsUtc",
    "UserParametersJdbcTreatTimestampNtzAsUtcList",
    "UserParametersJdbcTreatTimestampNtzAsUtcOutputReference",
    "UserParametersJdbcUseSessionTimezone",
    "UserParametersJdbcUseSessionTimezoneList",
    "UserParametersJdbcUseSessionTimezoneOutputReference",
    "UserParametersJsonIndent",
    "UserParametersJsonIndentList",
    "UserParametersJsonIndentOutputReference",
    "UserParametersList",
    "UserParametersLockTimeout",
    "UserParametersLockTimeoutList",
    "UserParametersLockTimeoutOutputReference",
    "UserParametersLogLevel",
    "UserParametersLogLevelList",
    "UserParametersLogLevelOutputReference",
    "UserParametersMultiStatementCount",
    "UserParametersMultiStatementCountList",
    "UserParametersMultiStatementCountOutputReference",
    "UserParametersNetworkPolicy",
    "UserParametersNetworkPolicyList",
    "UserParametersNetworkPolicyOutputReference",
    "UserParametersNoorderSequenceAsDefault",
    "UserParametersNoorderSequenceAsDefaultList",
    "UserParametersNoorderSequenceAsDefaultOutputReference",
    "UserParametersOdbcTreatDecimalAsInt",
    "UserParametersOdbcTreatDecimalAsIntList",
    "UserParametersOdbcTreatDecimalAsIntOutputReference",
    "UserParametersOutputReference",
    "UserParametersPreventUnloadToInternalStages",
    "UserParametersPreventUnloadToInternalStagesList",
    "UserParametersPreventUnloadToInternalStagesOutputReference",
    "UserParametersQueryTag",
    "UserParametersQueryTagList",
    "UserParametersQueryTagOutputReference",
    "UserParametersQuotedIdentifiersIgnoreCase",
    "UserParametersQuotedIdentifiersIgnoreCaseList",
    "UserParametersQuotedIdentifiersIgnoreCaseOutputReference",
    "UserParametersRowsPerResultset",
    "UserParametersRowsPerResultsetList",
    "UserParametersRowsPerResultsetOutputReference",
    "UserParametersS3StageVpceDnsName",
    "UserParametersS3StageVpceDnsNameList",
    "UserParametersS3StageVpceDnsNameOutputReference",
    "UserParametersSearchPath",
    "UserParametersSearchPathList",
    "UserParametersSearchPathOutputReference",
    "UserParametersSimulatedDataSharingConsumer",
    "UserParametersSimulatedDataSharingConsumerList",
    "UserParametersSimulatedDataSharingConsumerOutputReference",
    "UserParametersStatementQueuedTimeoutInSeconds",
    "UserParametersStatementQueuedTimeoutInSecondsList",
    "UserParametersStatementQueuedTimeoutInSecondsOutputReference",
    "UserParametersStatementTimeoutInSeconds",
    "UserParametersStatementTimeoutInSecondsList",
    "UserParametersStatementTimeoutInSecondsOutputReference",
    "UserParametersStrictJsonOutput",
    "UserParametersStrictJsonOutputList",
    "UserParametersStrictJsonOutputOutputReference",
    "UserParametersTimeInputFormat",
    "UserParametersTimeInputFormatList",
    "UserParametersTimeInputFormatOutputReference",
    "UserParametersTimeOutputFormat",
    "UserParametersTimeOutputFormatList",
    "UserParametersTimeOutputFormatOutputReference",
    "UserParametersTimestampDayIsAlways24H",
    "UserParametersTimestampDayIsAlways24HList",
    "UserParametersTimestampDayIsAlways24HOutputReference",
    "UserParametersTimestampInputFormat",
    "UserParametersTimestampInputFormatList",
    "UserParametersTimestampInputFormatOutputReference",
    "UserParametersTimestampLtzOutputFormat",
    "UserParametersTimestampLtzOutputFormatList",
    "UserParametersTimestampLtzOutputFormatOutputReference",
    "UserParametersTimestampNtzOutputFormat",
    "UserParametersTimestampNtzOutputFormatList",
    "UserParametersTimestampNtzOutputFormatOutputReference",
    "UserParametersTimestampOutputFormat",
    "UserParametersTimestampOutputFormatList",
    "UserParametersTimestampOutputFormatOutputReference",
    "UserParametersTimestampTypeMapping",
    "UserParametersTimestampTypeMappingList",
    "UserParametersTimestampTypeMappingOutputReference",
    "UserParametersTimestampTzOutputFormat",
    "UserParametersTimestampTzOutputFormatList",
    "UserParametersTimestampTzOutputFormatOutputReference",
    "UserParametersTimezone",
    "UserParametersTimezoneList",
    "UserParametersTimezoneOutputReference",
    "UserParametersTraceLevel",
    "UserParametersTraceLevelList",
    "UserParametersTraceLevelOutputReference",
    "UserParametersTransactionAbortOnError",
    "UserParametersTransactionAbortOnErrorList",
    "UserParametersTransactionAbortOnErrorOutputReference",
    "UserParametersTransactionDefaultIsolationLevel",
    "UserParametersTransactionDefaultIsolationLevelList",
    "UserParametersTransactionDefaultIsolationLevelOutputReference",
    "UserParametersTwoDigitCenturyStart",
    "UserParametersTwoDigitCenturyStartList",
    "UserParametersTwoDigitCenturyStartOutputReference",
    "UserParametersUnsupportedDdlAction",
    "UserParametersUnsupportedDdlActionList",
    "UserParametersUnsupportedDdlActionOutputReference",
    "UserParametersUseCachedResult",
    "UserParametersUseCachedResultList",
    "UserParametersUseCachedResultOutputReference",
    "UserParametersWeekOfYearPolicy",
    "UserParametersWeekOfYearPolicyList",
    "UserParametersWeekOfYearPolicyOutputReference",
    "UserParametersWeekStart",
    "UserParametersWeekStartList",
    "UserParametersWeekStartOutputReference",
    "UserShowOutput",
    "UserShowOutputList",
    "UserShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__d84baddd02b2eb7d700b468bb97ddf9f5a11245bd45b1f2245c8755de57d049b(
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
    disable_mfa: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    first_name: typing.Optional[builtins.str] = None,
    geography_output_format: typing.Optional[builtins.str] = None,
    geometry_output_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_indent: typing.Optional[jsii.Number] = None,
    last_name: typing.Optional[builtins.str] = None,
    lock_timeout: typing.Optional[jsii.Number] = None,
    login_name: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mins_to_bypass_mfa: typing.Optional[jsii.Number] = None,
    mins_to_unlock: typing.Optional[jsii.Number] = None,
    multi_statement_count: typing.Optional[jsii.Number] = None,
    must_change_password: typing.Optional[builtins.str] = None,
    network_policy: typing.Optional[builtins.str] = None,
    noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__72414f2a9320dd73073a9cfd82d56b9f7c834226827c1ef0171ee81418205d13(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e93bcdfd7b6764bed293b518e1b59b457368e3031f9a4fcf6aad93d27aa9b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b409c8cf1ef79bfe2887a07d40ff37f47e3247c1719418f27863c997d9a650(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c2abb9ede0c9b116746fafd63d3ee29566e180c76174e5725996045ea855e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086cbee761d1c461401a16b8b7ed80bb0a0b005606fa0426fbf232d8308ef03d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e1715d4c53187c8531495d659de6bc119a9eda44360241c422e0964fae6da8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479948a83f40ef0c892306e8c7ca74953d928ae43159770d729115ce3124225a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b15f09a62981f06066edca6ae58b59feaf96b0e938d81ce7b794a8c9133b31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b19e5c01b4a9791a0909c5aa2d998ab035a0004f4cc186dbe5f47f6c674a851(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b96f72bb9d3fecb1d12a370dbe04632b7296d1f2bee4c07821dc41301bbf6707(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d4d7dc88c807e5c229aff25cd49613277f4cdf1afde0e1e322c0ea9b43c0ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc45e18f70bffff86eed3c524bcedef5b6cc83da9b2009ab7ddc190d74ee228f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c3c4d66ff299eebe64eb9a243cec518d6fdd41e0998df9682e8241ab9ee931(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c70d58a7dde72cf09c0145b794bb011cb77822b7c8d91de012cabddf0dc2f22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9536e78e0f65927976b89fd4d9eab104128d2be82cfbbb2fa23289ec65b236ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa118058c43d6bee6d11493315874792e30a8f7ed093203560650f33f0807a2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4964372dbabf6810058499c379ac2f27ce63e96e383d95769f2090d2b6a8df62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214a9ff205ee25636ec25f2fd215554275c9a32ac3378657ae75588682eed3f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e767c3f4ed95e67d76786727e22e4670c693d1487eb2d8932b27be46669dd0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37893dda19f1104c6b4021d41c3b72df1de285c29864ec03c9e6846c6dcdaf13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f64251ded505f4cefd6d4d5a15536f93689a9c0ad81a5cdc2f1af931991f0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a755af3704f43753f2f278203f460cef46dcfaf3983e2953def6f033c7ec4c7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e66f39f7cd562a553aa56ca25ebf629538e16c125550f5a570f3589ca008b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b1a168967696bb92a92bf73717f80fa6aac4e483681eb8903630ad5a692161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3322d98011bab95439fe965e9f7921436ff80ae4534133e91799adc6d07a6903(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9383d8667c41020f11eb3eb8626a616f22ef62af000af450e17c66c47cbdc794(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f12677c5d41250e7176255d9e749098efae5c86a6ecb7f2f6c83a80227bc53f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219020d01b499f4330de8601c7ed119d8c2b4d6de1af719ae62d17c4443f850b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938e04c75af4ffb0e4cf3fc7c80861cb52f9ef74a8d7f425d6e5d85c48f33f4f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80b44a9d175599c1710c1ea47900e135b503a5f2a7b488e134a8149de564bf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2c3a057fffb837f25650ce9914dac8c527cec1a77e6fff9878732f8f196545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1ce84483883a596f0d5b98ad8bff649dd26e4e5475ba7c1965d286f7089748(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee534fe04b85b73ab500205e9b2d0a244d624b079ae8eb269c0d80ae790dd1e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10c40fbefd0fe09d300857685f44b95866b8952499d21bd18441a560ac2c726(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e857edc0e28f48da29720d4621b25ce6842a60bba690a2a5b524ba783aa197f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31deba4ea185aba9b475a4ac1dc5e0c1c1411e21040cda56cde1b2367bb9754f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7cac65ac6bb6af35d68bf14970c3eb521db7997fede20bb7f1aa5dd1dbf7b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0530543bda1184a7d929f8715889576a41c54bd5c8644b766fe2fc19dd25a36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf526e77d8d1d92e07add7743c0fac525871f7c8376d82883254e72e0770972(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd62b8766f563c8bbaaf20c2117ac094fe19bf602c1dc6abca677209db98a0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79dc1b87fa3f79c7cef34753b325791fe9a47f571936afb2c9a51293dd7b131f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59b0ac0a85ab3df7b3b8fd6e69f65ea1c802431a7e9e2a4e532acda3be01de6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e33c28257d95ebd907f3b53e617be06076819ca7558e136b9dd223774f65133(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9beaf0b44f6c5ce45dad2add5e2c31ff4dceb768c62e2e6cfdfaf1dd1c15d9a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79b7a596e67fbc1a570f37a8489e5d53f918bef1cc5bab1482a0d61c158eff9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e87ca7689a8a9fc7bd76f1cc4572091cc8d1cd7db878cb8216171610932cb84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554b40f61c913aa67692d8d1364c59a569973014f8481649a24b270d88673a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090e61befe8290bb6bf73b79e730e2b8c0a66b55eafb0f4ed24f33c3106eb356(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b69396f8e1f503615167d3823c57ea6c73fbe15273735305281b519bd521f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34be85b5291e5c01b195774d5dede0f9ee294127b7f1b460f9f4b9a0d889739(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c384735f0ac2a22cda9e91e8ccb6aef7e481039f3eff75233e4d931bd764d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7b1cc04ba6d6692b4fb584cea69e4ab098a295c2283d54f344fc6e54accd04(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429994498fc2cdb2ec04e4b9680c7c2fcffe045c382a1743c4dc29f33010ba09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a19865b06d8aa66297dcbe886f68e80396ea9a837b6aa349e941b596faa9c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d25ca72e1d09b7aedcd27ea3b3fd930995583de3c6a6eb17e40a446bdbd73c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfab7a98ff160c89e43e23358130c93fe0eacfcf22f37020938d9cdef3270d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e609e3a1336017dda59d661522b3f1323545c41e3aa80da6eb0016a37a52ffa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae4e3b8a59e80d6cd786e25db7da41e2d297c7b0d456a3f828660463dc27deb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3591ec5992e5b085017cc066c9fe6193de0687e04f12064fabb717726448e418(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2108cddc6f5a5ab163d764333c8f7c98c3aef7a9e3cc5c637be7529c883ccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be7dfc1020122daa87c78a32c2efdec4b014b4d811301cd9377a8dc746687af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab662307baf8c5706aeaf4814b28713894fba4f03d5df46d166f07f61494c5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292160608f24a88f04a78d99e74e6a09d44eee680b4e0bae46079d882b1caeb1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ec30799fe5df04d5db586e883e5b3a3bc83b6e256317347b611f06847f66fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281b5175554bb9f9fdb7ebd67da89a5a00304a5d57cb0e849ca889fca86a4a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd91e8375139d63bbc4f0c650b01f28bd6fecfa59ae8dc2ecde3b15610cf584b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac92d40ec65e0809cf9a2d482bffe850aee9b0fbb823cede5834b2e186b3fcb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ccdff2b5ef78bce87bbb1e8ffdbb289ca9bbbef6406dcb599489cadaffb7d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1f610ccb5502b6464232cc06016d47c112df845f1f087a205c7fd0fe56f502(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c452d4e99094f3b56bb0f754ee14a9381f38edfcf8d19cbb155d95d6ad06c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac174786a644bafb77b31edb37bd1e112a7c90cb30f5b5cf2147d4b859b1be1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa77c824c491a1b95ffa4e4081661baa9863156d9e18d24f221c8baefe47764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f25e1803a2ad12535a256ebf369aa5162859202d6a9715ae9a4f6c3aac2607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6738f77bc3e92bcae3520ce2801219e20adc327c158397ba3684c75c3f3aac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f05ea993560925ccb02c6028d2d534f8bee6651180a6b15a50740aff0846ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195de03975ac421559756af4c830411f10d6373802a227718a3299104db03e8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a56e345db8f2fa469e659cb59fc2bc3bf6d40f61ed47bb35fcc51e296526ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f8dadfbf8755e3cad2f48fd83e79dafcf981ded31fe28eb4bf9865edb6a57c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7519e9d1fe61f2a83dbb0cf8939ce666427ecdef9cb96f2db5f51fe04c0aa88c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15c6e81d54612118f6389e78a34e9a4d8d5abce77b5b153a1eb4d4288f322b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89a4032f1919968789a33a97a5aa202bed13b59202c07a27464e8aae8ff7966(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bcd50566d7e5a0f6a888a622822b1bb2e90816ef4e28ff46370e9a97874f2c(
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
    disable_mfa: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    first_name: typing.Optional[builtins.str] = None,
    geography_output_format: typing.Optional[builtins.str] = None,
    geometry_output_format: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_indent: typing.Optional[jsii.Number] = None,
    last_name: typing.Optional[builtins.str] = None,
    lock_timeout: typing.Optional[jsii.Number] = None,
    login_name: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mins_to_bypass_mfa: typing.Optional[jsii.Number] = None,
    mins_to_unlock: typing.Optional[jsii.Number] = None,
    multi_statement_count: typing.Optional[jsii.Number] = None,
    must_change_password: typing.Optional[builtins.str] = None,
    network_policy: typing.Optional[builtins.str] = None,
    noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__77bcd7e947fa6d5c9d46acfd73e5ac52f4a18338bc08925729a7cf5daae4cde5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08fb0915bdd84f1d9f706053dd06b24eb66e8ac59eabbc75cac92cf75557f63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d30464b811d5602b33e397cad646f23dce30bf5b02d85ae3f63a12bfefdbc9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f68b4d7f3a11594a1235f7f45520f4fa298bf7749bd44c2b163977a05855265(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b7589af69276346b071334bf6aa749c9748bc296ada7345070d4fbc3723637(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6820bc97c9ce7e91b7f096136d03160004acc8529ca6a5acbfae877211cc53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228c227a1b244fe603e777d34831f36f9d078a84decb0dcef93f709ca6017271(
    value: typing.Optional[UserParametersAbortDetachedQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b98a2cbf8d94d8dc321587cd39046454c8dd032d536bc934451378b21e15b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2528402a209a67fbcc1597c316660a54e4ca8d0b491bbd9c7df58099ffc66b87(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1eafe17b0def28d8a0fc8860f505c042eaf6973437cc8f546549ba01ee9bdf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6f3ec2d76271d05bc2226497fc68d74b4cffcad37041436e672d7a037b60757(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ec1db1bb47aaa2967b98f9ec54a477d5131695721c2a436bf4e4cf93b41a6a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9699bd6055cca785b5b35a04c637450e6e3ec8c4e0054f7f8c11e5a62727f52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb727962005ea32d3b490acbe9bd871de4e962fbeba47f3fda386975da56328(
    value: typing.Optional[UserParametersAutocommit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfdabe91952fc706148e8e63c96404085c807f86c29212fa70a9e53bee35789(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5718953dd8297ed21add4b52a3a5a925165d3010c2313c5875bbdf75819b3d12(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f57e5e25306d0fc84edfb2917a88fa53688bbcf0963c87450c00bfa8ad490b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01cfec7a5aef50b1395294b6aea0eed8bdecac4239a350de9b974ac95b2a5c5f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734a466eb0432e9976c3d238d13d088aab8fec5bf4c335e16bcfe09c1646f43c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808a00848b371b50e1c954103ecd773adb367566d5e805d2a2cef9b32b8bf48a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3d4d1b3bc3e53b812b5841950c6eebc8f97793e0f9f5224710f92f5ac0d780(
    value: typing.Optional[UserParametersBinaryInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3a288bfbca62314c94ce7ecebae7d792a3770980f423dc8f44ea6e2ae38eb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abd41865c5d5e5dad855f1ede02b9dd433177b3ca916809725b50d8d84a3d6b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d250f385c2de5e8840cb9c00c8ec46e513f2d19ebae7c6eebdcd1b7baffcc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f85ff0e12a6a010421f6a384eab97952b67b847376b43742e417e2f7d075b4f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ac87e158c06b4d3c1100411aa952cace1fdc242a68ca5b09ba0c425cfd142d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3e05a1b85b6341583838971949ccdabc14d7f91649269905c95cc6dfc08b03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30da9808e8b71cf4c4174ffe3dfe0f1b12e2223a1d8e7c06204e5b3635ad38f1(
    value: typing.Optional[UserParametersBinaryOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014740eb2d4860eed241d4afc4fc8e03345594d242393f01d805a3ee071636b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef9794e77c8cea9c1167986e5f687f30bbb4049fe3bbd8da9dcb57642329c36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c862737204049b678f182f467655002407c460d7b220533f41f83dfe24a153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca320da31a5cb2b595f0d375809523c1599d70d83396fc0eafd0f22204223325(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69fb4e090dc2ca2f336b416b1317cfe29b3879f116d449e338835bf925f4ad3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb9b2e5d4c2c02f7602feb31277ea3d7a080fa1bfc3f0f9ababb95a0c9f92ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f313953cb08c610126b6f94393bd7404f318b502669f9ce2e28673b699233337(
    value: typing.Optional[UserParametersClientMemoryLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4fe1074eba3baa286638a17cc2cb312268295e9cbde434adf669691efed797(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040c916e686150937cddafc2b1a80fa9b2f06c18f6cd88957a2839d0d713edfa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78da5be11496a839b1e68b054585578abe209e5025dd61b92e49c2f261e6f2ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b1a2851643e4db4a2cb5962115f4f98175538de50fc190944319e8328cadde(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab5161a6d9bdf401b6fcde1533815fbdf25cc6ed4503accce767ed323f3ced6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2da1277818d0077cc35ee7c3bd3058088ff422d0787473b3cfcdcce7db8897a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542aebd2588d6d6bcd84a2a7ab78633e57421bf32718d7af7f1b73a0a2713a3b(
    value: typing.Optional[UserParametersClientMetadataRequestUseConnectionCtx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9937efa9ac7d6ed0b8cd7bc691b3e88d564b4d94687422d712d38af6ecb74c8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b0d902498f59d27cbef19790753a7c31576194f6fecbda8682f94a1c4ddb62(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfacd3d8e4f3b0e3c97a6cee135c2f89fc9bfce6d02a05d4c4115323685f1a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad1c935e120fea37614a6d8b2004c363bce158defbcf3b8d387d817eed73fb4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da90f1a9252a8541b1d652a4875a2dfae8f2ca27f8f9f4741e2b2ca365773e9b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d244ce07b62ec3d83a51c587b251e26d3131bdab07083cf546373b5ea009178e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2443b03787f50b319729c1d5d24a03761559c4c1a85f4dc55ee7632f97b2d44b(
    value: typing.Optional[UserParametersClientPrefetchThreads],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634ccc504b165098dc1f246fba69815a336c7d4afb1d9375466c7d29a9037976(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c20d58a22ae4df3b6d108d9af7ac6497417504c73d69583ef7e55caf862edc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74ff34467e0f67d80fbf2ad4b09c195ba7c9b5218ceabaa513bafefd37d44e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97575c5e889cfa6c44df1248550e0a1785ebd89fc789a8a40d27049473e50f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab48b0fc21b2d29fd0c815ab2284a29c217473e8c7705d58429d62c88daedca(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16da9e3af91dac3d2d6a022ec14f366b0f0538c36a3feb8eef3540e44f4c4a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f9185c106275ede01a08ab89449f88ea7b120ff7ffa08c52c65b2c5baae496(
    value: typing.Optional[UserParametersClientResultChunkSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0a8f51a5134d53e694f0e962f573bdd7896374c4aa429bcec3abef817797b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3585de0526e6d9573f36df819ba65b8326509a659ceba6368166d5b21c5c75(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e5bec052d7546fc6e7a63593cbe7fc7af78b00a49b85cf52d0cec0ed013661(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4f1dbba931582d2cc1fc76a16e4148498c586a65260c4a00b42edef53d6aa3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d41e390819f0ef5d4ad0ab31fd4b2bb71f605a71f7437ebfe96a5f862ad43f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a2af70b42f303e335aec48161a38930cb311bf7e044fbf5058df6ea4830470(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7475ff3230b42f208799f1ecae876500c52ce230b37dfd95d51e0cbc2d3e7d1e(
    value: typing.Optional[UserParametersClientResultColumnCaseInsensitive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44946529a30126a6d4d27c2d8e7f7e525c300a828dfcff9364320cb7b7993ce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c712f69fa2561e2d1fe2bbc5f52981168faa41a5ab448e75e50624b5f354566b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85639ebd04434dcf270aa4a81049bf1daa321718bd4b25e80ebc80c23207343a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0e84fea1976d99ce4398dd38496e5ba8b3a10fb2dbdb6347b37ae33e8a2ad0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af57e7d3c4e954f2929394528285fb97e0ba415cd3877591231236d8f61c973(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868fb13f3b3b2d7046236e990e78db35892b94b2fe92d821fa80c8283d4786b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5175a1f681a889ed6dd2e0481e10f6ccf96830bbf88d1c603254b1dc80ac6727(
    value: typing.Optional[UserParametersClientSessionKeepAliveHeartbeatFrequency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c0e3e9e432900e1ea7af791dda897e68797198bc289f6a49e077007c89dc01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b70404af3b81ef8c1ba894dd8b6b7412f737c20ab615314fc46b62ef8970fd9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800edbe41fd71aaab89341b80d4fe2882c6fde021657c74ec4e560870b374a8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37de4d6ccdad65fc9fd7e86280c97cd48b63e89cf86c521219fa9b3209d5f0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9053627998d7a7fa11884d12bc89e9e2220c8fc78625cfc6445e51c8d556ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cb6916c75c000d3376c756de22258412ea1285e18cae29cd15b97d06ce62d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07a4f151c3bb2535e47927bef2ee987503f4254f10c085e82415f42dd28f8a5(
    value: typing.Optional[UserParametersClientSessionKeepAlive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2d53b9ac81b42090b597e6904de1abb942ab7e1b0c19e94dbcb6e0d3b53d96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f29f9acb71111dd2b7acad7154c610c75cbc02ef1229e329e239d06ac0b86cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d298261722b9b576b4c32e4b31769c8e1e8b4e842b3fd31827504a4f0a1c4ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24bcaa6e9b223e65087e64e64af64dce4d1ff10d62b453a8085f0b0a1f23754(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a1bac09282c406921f376e30222d0c9385dfe8d8eecd79f101ef68aab2bc1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0616b9eef651c7972516c65d6fb350033a5fef3eb32519ecb056769339e3cd30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6209de93240e09e23997fd2df9908b8b94b1a7222ea05a88977c7e118ac7b52e(
    value: typing.Optional[UserParametersClientTimestampTypeMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fbd740d102371d44fdc79e634b4ec9aff77c3dc8e698dbe38a30d70a0d8e128(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c7cca5bdbef6efecdc7e31d04eb57e0f5bb699b0720975b88546de17d4c611(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad24f1ee6a74d413b39109534fdc82798d66b1d44d5a332488afc1b10eece46d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfb7ebdc5393acf307a71a18fc5e41b5770378e09752d978f31d48701351735(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7916b052e9f3bc09558bfa9f8a21bbbbd518f5bd93d091e4cde1d8729bddbb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6fb2254784e0a2341558368796c5f31a8aafebe3228bb086984e687ebb4bf89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec665e6fa2fd9b9d76306a9859d5f95507009dd8e5a000fd15de805c9d9cfbb9(
    value: typing.Optional[UserParametersDateInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7121e892342930d78401ca18de0379c0374cba71b995c7c2bf7180b8481a030f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3063179f5f494a3247df833b0aa7e2a8d3834c5a9b4bc69e8faa6b6df204cb3c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c5cffc26b817bb4881f41e3295fd3c771bc28ca810292f7a6bea80f5bb0e70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854d3e389182a269e02483189b2f31e5ede611ddefaed29fcdd18ec6c5eb9ad5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef9d0566c2f8da1f65cd347e8d9c4af48deb9c9b84bf36388ecaabf42fb37f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99167ea9c819b1f1d498108a0990e60109c61058a99d9ea54c795793f68e941(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b5c41b198e2f3dda7c71c12ce94174bac31cdfa3a58f4b6e5d43c3f1abc41d(
    value: typing.Optional[UserParametersDateOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ef0d9ef0b7c8a71fe56190aa85cdba285509dddb045175c58ec09378431f2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618bbe3d633411bfdf03a0abafbace3c8f2691963cb5b08e88934bdc33a4c5f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9e64422ace8eb9c6d3a32b5bba84ca655d53dc900ae8d4e327c7257a87276a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd94a6bb4d6086f6eaf231a3deb137a76ca323b625f364002bef4ced04183d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25826720738045cd34f4d77c5d08000eff47f802d3d83d69f4aa2228d2ae3bb5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed2ec4089fbf5e26b5f0dc9a031ab3e5619bab34bb2de5fa16d1b8f23818a84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968c8699b74c515e5e60f4b8018f5dd0df58fa1edb784e9839018e991c498ebd(
    value: typing.Optional[UserParametersEnableUnloadPhysicalTypeOptimization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba213e9d487f4839c03b64c9be0ef8b15159419b0e02a409d16a5d4a6259fa6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b839f3acc6a19703888a3fea906146f1bd2ffdf817257a75912aea7522825d33(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876fca32c7a73d739e48574d7dc4ab077f6267ae3ad75d9d5b9190aeb04e049f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a090e973a1b37d426ad5907b46d4c2c198ab83e070b05b9fb73f65d9334a80f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db1bdd089d04c80e9a4853e8267ff1a5294ac5e4ec73ee523701e5c91deed3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ff220bc657fc5eed93cf122f059ecafb9db9582aba81ce3e4a21f688e7f897(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228e5b337d5e5672efd333a043e53f34abd8e7998748f1ac50174b86e81b2dc5(
    value: typing.Optional[UserParametersEnableUnredactedQuerySyntaxError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42be6f99db431c36aeac594a74367b64fea764a4dfe66debfe1f489c1c09ae1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243ddd00988591c037bd8e2e83bcd854ff8cc4e941c025668c0546666e3770d3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ceac47fd4ee639005ae5a6a6f3f57541ea2b823b2cfc3ed69994aa2faaacf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d5c35f0a5e85778cb0d614293e04e908826d00bc86d18a92bc8699ae5f0fe96(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd4808ed00477c7791bddc3d809e868e88c6351d7050080a173065b353a9501(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6722e72576c1db8f9d91dde7307bbcb90ab35ae3dbb53fdfcb265afc55187a6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cb20211eb3fd9868c5cbaef5b2196a871f4ac770c56d9132b4b79fae27d076(
    value: typing.Optional[UserParametersErrorOnNondeterministicMerge],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4188e522f5cb80b19bcbdb6e263ac692cd6995a4953ed7d07780fa258e4b67a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b2bf4a1d14b9561d641719f652a62ea32303ef62300f9cc113a6af64d11383(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c1feee19b63ad80a8bccd718c6004bdac187a08be3c890a38d979dec3db01f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512aeb4f9ed5e61bcd50b2a8ea545717707913768deac30523e58c9c43c0679a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7943f07d42dbf1c2eba0739cf89763536d74dbe4d853d231158e1c2c193951e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1e0d88990bc03a48fbcae5acb1fbb18f17c1d0e19719a7abd7c56aea11b032(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c43c79b3f39a058560ef80255e4ff85c5059f7abe87b5c8647a99f014bb546(
    value: typing.Optional[UserParametersErrorOnNondeterministicUpdate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df93cd2810944c3dbfd8262a64b2564663f68d55a32f231b788dd5ad7451355(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62aede7a941a579e1765ea21c4cbe5a3e8ad45a96faa40f3b2f7d0539449fff3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1bf7da977465c324c3654493b38cb9a1985bafb5323ff56ae2bfe96a8438ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ecd665ffe5f75f47daebf2358152eec4be8d70afac3fc0b100cdb7db4705c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2d9583820e7ec9a7eed4216896614632429953989b7fe2d8810c223fb1f60d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9456b542fbe21b6f551f4be6fc325d96996becdf7b169c63a29e0f1445835aee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6630899d06467b356adaf5e4adda8b103ab7576cc6ed5ba01a9f4e83060e384b(
    value: typing.Optional[UserParametersGeographyOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827b1c16ca58fc02ef7204ccaa74e385243416273c0a9a17c8859e017c564f05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c706303dae6b92b7348e43fd3cf19fef5df0a3c2920079e12c820a8ff29862(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc382880531deeb6e1ed36cf8c9549b5143afc5838985c47361133036bfd7c9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24edebeafbe56eeb5e6aa4eeee06ba975ece19a12b8f13cfba6ef11a789710c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbad5bf27000dbce9c67585901645c2b9f9bbf3218f4a4ddae2549235c3d3bcf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198a971e27834cb46055e5a68b2d9a3c51586256c0ef6242b028e02260a215ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca49dee7a53a4ada441dd7badc8b75b0824ccb968d620d3616a450cd7b66de5(
    value: typing.Optional[UserParametersGeometryOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c04a9c8767f6f9da9963b6dd63b3f14a73b5e3af100f930ea21ae9575a42ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c550c52203c06cacef302a4660f1e86c0df84dc8d28cbee7a0a55324499284f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a125acd4ffb98eb541a512be2a0b29427f77bb9e009288fa5f01eb8625ff1e68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e830395911d58d3df4149a2c2f6e9a19867113fb0a0bb8ce5975a76ef0cb4c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab5aebafaabe75c502f6ffac09dfb249f806a87e02fd6fd44c8ca8bf7be6fb4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c438cef45c20daef0b85abbfed9cf61af4eb7e369065f74fc12c052a9d2be7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28be02fdb32ccdff80a6630eb47a348a541ccbccf0aa6394046532d618b517c(
    value: typing.Optional[UserParametersJdbcTreatDecimalAsInt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b63151fcc05d6e5bb1ce098542bcc97e490ad07747c81191bf369027809361c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4241bab5614fdb6f9084fac2742c1d4d3e7508f7c82f1c64f55373778f9857c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5010dd54e9313cbda16dc32ee923d09139c56c0a2c4a19dff671762a9e0a566f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd9022f367709b39fb77a43568389d37582a4c6b369e72cfb459902d025f6dc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177590f791ff513cdbd39b062946dc2b822568be49f4df6f1775a33640120e63(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1cf1c87bd4ef3df6e916a1c776872d56416fdb9cd8f34382042946b4ce44a11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd12e4443704e2f214ea11c5570a3f511ae037f373e1b7fcf50650ff652f233(
    value: typing.Optional[UserParametersJdbcTreatTimestampNtzAsUtc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce54c66da2dbdd14f02ef524ea4a39e1ce965613f881e51de0eab9c8f5301d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e5e6acba2792b229321b898b8133aac726b18982a009c6b342f37a0ad47d32(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf1bedd952ddecc477a90554f39b178f7558153e5e1977ee0717bd67d62d9f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638531ed6e86d8bdd1543a01c07393b1817702e3c81e967e2573ecbf31d1b239(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a2e7084a3da9a2ab54fcbefd8de055ffd3d7b831f94ccb20938861fffb299d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbc951e36249e9ad1a590801c6b0327c0803a93ac6313c78c44e6ebd217be0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee88c438fd67865947af20427a8bfbda2ee21bfea2aecc0d54db7181ea104a77(
    value: typing.Optional[UserParametersJdbcUseSessionTimezone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6f43886548a69f5dcdbad5df37b43ed629ee44fac25ab1b521146433278e3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf030616e4778b59a21d012b6c3fbe9cfa98a49c9e9db579f0ff76d0501e00b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72912e7d80670d046e2f68ed9307a73a2418dcfb7d810a18398ea153f82a871a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854e1ee0750a7dd75c9199f3ba8c8698416af1dca9f87e5bfeb30c76cd50b693(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c59b2aa93387048cd2a2e5c79513e9c5b18259ba1ba2bb51c1fe961b583af2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e146b396c19d71fdc5f2c7757a4857fbdbcce6be49f6991fa5f4ab5181fe51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203efd1c43bc5c825c6a044c8082baf708f79a97c019823bac54f1b27127c498(
    value: typing.Optional[UserParametersJsonIndent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc44de93966e6aee2efc4baa284c9fdf541e723000e96f0086cca0c3b1602e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c07b70d985481464796d42cc7f9ff8db0422cb19831bc3aba134388ddc9d9c4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f5395c5f87e500512fa4df7ca30bf42df60b2b0a01616d66d30b1d114aded0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdff4cec53d0b0970b71e29b248bab568280766d63932d951ac8b8efe900ce3b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4e49277ba0f07f0c4f8b7687cfb77ac82d378bcfd53cda1434c19cc6310e43(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fa63433cce260b6d7838b333ea09732ee2fa669297c7b16a00d472f4b95402(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43ef71feb218d8b6b4a4a34c6544325069b315330957ffdc07d538e3dc4be20(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b120883f46953baee13cff036ab72d35df17f1f32538dbfed46c73b7e6aec3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9e11c17863aceaf1202702a4976f3c6ae1a158644a833ab3cdc146e1ac7fa3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53ca30516485f15950f7ef9957181f100bc504c199e920dda86e559338107ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b33632b2b0e0cce81aecf1ab47dc72c888b563ea0c1ead810abf611c9b4c140(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cea2794e598d25fbb6157869f73e6467b6c259d76b2d868178e896c0b39f2a(
    value: typing.Optional[UserParametersLockTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdeee444028d68073cbf8357405c79f34681058cb435a06eeab096e219b7731(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d57322e4c9c21cc143a02ece47c41b4d61f7f6d5cc808341e439c23c4d9f9a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9623cf9f79a53f79412e97f5fe400c7a9de5c4ef93c9da3d77f3c0f3eb14a0d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192d27a7e6e7c0fce8a29c1dbff6670d4b5604d68ad0367cdc9ddb92086e4dff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62de3eeb59c6297c19bc8cda643116d55f9fe4dcddb5971cf41d434b701429ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fb089be79eaee03855612e8240d20560487cb66be81a9a0275dd55d7cab652(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69000731273ea0b06120d6fcaa3a19b4ff600ac186dd137bf8398e389e50c542(
    value: typing.Optional[UserParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42734bac70b4972255a22f8dfd6a4600559ac7a539135211b31ba07de90fe5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310ee66bd231dd7ea8cf6a990df07ad006f7c936f4edb56ccb10ab6a7be12a73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af9e9b3967574bc7035273bee3d71a6ce20acc1d57db44795243283447061bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878a480b8ef0b5934f3aa0eedced7649055540f4ea016b1f2849f86a1e78dfb6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8b029c4369e98b3b279fc8e0b18ba2ae6843dbb632c104e00a79cdc4b13f1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c19853bc9cfc71373f03e446ff11964c01479b3ae777495b9cd78171eb8d776(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a765e54a3b13b11f24e88dab153522f2fa788752837d01758ff9660f043e85f(
    value: typing.Optional[UserParametersMultiStatementCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd779b5dbadae0a783bbeecfead6dcaf4fbd3e71970a8a367bb55c4f46e07e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a47f31c3445f7fdd5cfc3c8e8bf21a1525b108b204c61beff7bf01ebb2c9ee2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abe6c434ac43707ad705432a209a5694f1050ca100d724d69f38fc873db9d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e213358cab89b1bdfc8d0c53d033d308e32021e5d45c7eb8122ac25c32f15b0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71ef10de7fa0e09025e3e51aa6c916969e196169dd8f17398b43027fd8f9e66(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42478bdddbb767b3622c563505b4332fc3e0224c60e4d3871845a151bee13db2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c391c85f20d2ae8bc589ddeda510f9538eedf4470983e7cbf66907d3571bcc31(
    value: typing.Optional[UserParametersNetworkPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c6136f73d74872a1f5b26b164f3c04424552c253be8b3fab6aa5ddc7aca282(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1127cd64575f97d94fca50ce59dfd65d5cf0be32e3bd27b2c50fa186df5de1c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c1e70cfcb664d12a184f457b39ae6b9bcc92126a9c967d0cd08b9555adf994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933b89476b8e0aa522740a0aadc0dfe44ebedbc3a07a6928e357451c5821cda0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e7a1be8b2a56ce1736d7174de8116fbec56e1babb15bc46605a8152a515194(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1e3e90fd34386d927602d44feceb9794d82f64b15fb297a1a01f2af44da72c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dba96d3b0d1b95b6cec42a058a90d1b5247102b743112873f5bcd25a14bf937(
    value: typing.Optional[UserParametersNoorderSequenceAsDefault],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a07a7ceed183bbabe457bb26dcabfe50a2e7dcd4695100ae688a20cbe80e87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9163fd09b8160d09149cead8ad0fc5f68435c65d8a35f060d425ad1562087cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58a8f68758598f30ea4de5f55710f1d7c41a2a5f0f4644ee4af00ddca6be403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41237e35a3aed7e53365381417fd2af94804572c6bb872dc47b351a4f4ff60c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1913d16a8adc1f6d6cbb94b61cd3df6a1ebcca15bad565aea428c0f287d90922(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091665dfe9ca437f4c387aa22a6c8a0fd8df74d784bb7aec5a88c3dae6c860e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e795151e3323ca8bb6271ced5027f111a359aa78baae8008293e2a3b0ec6f7e2(
    value: typing.Optional[UserParametersOdbcTreatDecimalAsInt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae5533879c2a6a1b0578cd47c8b317399b7dc007fe89e4691cc7b83569dd57f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261fb652a7200b854387f52d2e4ad90b5d9855878ca22a2d08446e7785c29e82(
    value: typing.Optional[UserParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb3c3c43ae7d941baa269dcedf8aeab373f9c2f1d2a75c5fc7656b0e1a72f1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018b7551f2bb4e5d14a309087b2bf546b367f6d42b40377970eed30f11476516(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f71733c466a3df53094b4244f63cebc172f9ae5bfde2b4b1ffb747031ffd1fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b68d63c80b5200f85a8f5f0eaa1bd2a34e42a925801105b1de69d95103e1fbe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4ec488898942d6b1c1f2e56812787dca9e4c69c64006eddcbf544e06478d32(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb4e8b390e6d2d6178a536eef8f426f3608071d4bd276773eec2db6e427ae6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d67208c1e7eb65aa0af4d715454edea47102c45299d5cdf0917255ba071de29(
    value: typing.Optional[UserParametersPreventUnloadToInternalStages],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9120dfd2379f6ed7ed003537afba6d339499e6718bcea2e19049c7b66f96ea82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7a581bcfe8eba700e9684ee67e4e22f7837cf177483f2b7968953bf79887fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9521a1bbdd89453b6a9dea4517893277fcb5fceae40ed90132ab362bb8f23aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818596e14438803dee345ce2279b9dabd4a1a52b5131f60770dab54710cc1a7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528775edf680e535f1f612c576bed94efda0b378231963f31168b526770c53f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4aeeac37315ce3599bd41a4b108ecd452f2587d0b2bec1f20388074706fba9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393331a2eb85a4b1281b5f41521a77663bb418300f4f7967e8bf11dd84a94bbe(
    value: typing.Optional[UserParametersQueryTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04213fa0eeab529508eb3dedf6b9fc9121572feb6226f1d7ebf01026d4356801(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268ed42e925b7acab8042c82fed52d8e20b35b836b46691ffc263dd729b9fc7d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93b7e7bbb9c0e4779a7d6cebbef27a635623699d5bf2151698affbc9da83f78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92055ce3b2073260d586d23a974427e5e0d68ffab14c5cf1772d8734df31895(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529b0e9dce8b976fc867bbdf3161a00d050c3f42ce5e0dc1958576e4d71f54da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e05a5c0fc50b17cbc5bc20f83ecf38c2d8850ac4ac36f21cdee9408999be50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96f951661ba9b0033e9a2505ac5ed27ce52f8f2f20781e6a38306fe3daea178(
    value: typing.Optional[UserParametersQuotedIdentifiersIgnoreCase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968162573b4b1d2cf57b777264933fb165242b1e28dbf7bebe3a866d308ad1dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d3ca2817795c967d6e4305c85ecaa186d3137c6843115dd4e79ede18b4e30c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4028359aabff2c2e83e8d3a879ca85d8c2a2599d436f05af5ffda0c8fa2c50db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbea1bcbb9e1123e9eae6faf8677a49f4be372f57c1b3186decab793d1dd566(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7119dd959e4721634c6242786439fb827db644585760db89e10497ee589310(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ff1f692c9a1f6dfc384754579b84c3312af9cb95b2193fc3e097166c07d539(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e551fe1360916a12ffd56bd70540f08b00929f0209685b6008b9d2192558a476(
    value: typing.Optional[UserParametersRowsPerResultset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f37ea95eb76b0c72c030bbf126179b1c9569980661680d58755f1b105048f33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9176d5c2a9d1848b90057170ed2ab149eaf0cb6f7ef517a05c0ad0837f5518c5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3a2d196d84771ca215085a0ec9ff4a20377e2ad6af4b08e42389333a1860e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56f3961aa8f03fc6dd8841b3d5aab0b08b7ffd9affa01925a97e86bbf8853b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa1370bb9e2ad8a499c3a1281a5bdeef45dfc0e66336ee19e195f3a4ee4a9c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d0707b2b8d9e38c41e1fae01758b23e7453f148f44491e6ee19e9d81e81c55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cccb31e7cffd6d62a4fe3000988786afe5cc16a86ccf65bf9722dc17bc5438a4(
    value: typing.Optional[UserParametersS3StageVpceDnsName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a5f5629648682179b46f0335712e4c22517a363e30427576523eaa9ca4dba8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8eb288d9f36b909277dac2968222fefc3df1545b4fb2b176c60c35c6e1cf35c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19e46b01797df4bbbe5f71eb872e9bc63a7b149ec460b716088fc858ec0025d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55bf9ff6cfee6a7a9ef07866e19efd4c84c1e6341444ddbda8a08421055fb45(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96444e572e3994315d8d6fa38e017655f08995227753885743ab93199ebf2243(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f245de31e57c533ec399994f9e7c977ec6c850c38332ab9523ff97f765af0587(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124857773a89bba1a7b5789fa43bb7dd1314a4178213e01d103d67f418dc3710(
    value: typing.Optional[UserParametersSearchPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02400147603bd2049225e754a86bc052e2f51b72d3bd96b16b12da86b40b93c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbe85d0ae333f6e1a56a22bf00d97a5df445f15c3c646e694c804c9226a241b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1e8fa8002b4c93dcdaa5d77dda6f86ebb9600b48c0d3db3ef64c0980c86e41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381a0c3a3d6edd3d6742cd7f802b3682af10aa954c4658fb6c39ad6e261dee13(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce0b1289dbc6f3944ab05e6264772ee4a0ba40dcc88effb35004495866a58ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce3018c9ec09b503a1fac8e3570b2426fc764708c2ecabc73ba31824f1aadaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0438d11df748f48b72537096259aad8282294e54c91aa476033d1792baa2ac80(
    value: typing.Optional[UserParametersSimulatedDataSharingConsumer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792ca85508a3aff48948a84535f418bce32e978b0014ea4868b78941b5514b4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4ed6496c0bb67b115d0e3fa7700ee47dfb4ca7e2f8dd4389b4c80f7299eb0e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc6c455cd5d3d4a97c532b6bdc004bc9d9bd861c5865a6c0c9f48950f75ff19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e516843545fb27f1418e94d2fd1e3dc70f4b34e1e49554c0619dbc7b426ce1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7022cc4fe14c939d145eac0e81bf0f1187586cb5011076b017abae4fcbe52edd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de74165a23cdc4b1d2690b402e853f956baadfddd7221fa29da2abff1301dd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d376f09df94245927e53cd01f47731199e14823a409e6524ddf0328555c9090(
    value: typing.Optional[UserParametersStatementQueuedTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1570061015faf48707208f2726a2eb4a56521ba0eab0c92a78ea5a7c097434f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcf829ae93125bcac6fbe9c1fc9a1218e162a79ad54ffe913d3867bebdd96c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185cd36ab394201523e080d64b8461ee99c06cd514a63007e3ca459ac9544580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74efaaeb10dd49a3f678b869593c011691e41c9d00817315af44b7dc5302aed3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c964325ff76427766b19dc0a5d0ee7bf9d49bcd13cb9cf2d3c6926d3fbc9aa49(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8547673412418ba87c18f077a1db58172133108f1126684c1abadf9d7deacc6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87e41653948f22ff8a1ab124a17afb330bd9b53b11aefdd52bb9280ffef4f44(
    value: typing.Optional[UserParametersStatementTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c5b2b65059b48a430431c82bddb000432c1e959242206d73240b85fecc1801(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40aa941c4beb46b90a1b8e8c5c0629b73c189884a7632371282a919f2f36b241(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9400ab9235ed6ae82cedf4e8c7302ee23504335a492e828e6fbab656c935ad8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583838fbdab100ac167244622b4b13223df17e27fc3a814dfbc682ad9d64c493(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31ecfe88dd1c4324f7809a60fc1d4a6d2382ebf61adf9aae4d39a63fcb84da4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14fc595352ea5a27c0f2b04c67b2adf9455cab3417426624d37945e1974295b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7906cf058ff39c6a885783538251dee055e1afd0544e8e43abb20e8b68f0a3d(
    value: typing.Optional[UserParametersStrictJsonOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae04dd13155bf861e0a6be066b5d7faf0395741567dcbd43507c6e6d212615ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3577ac1540d39a2b50f56547c1f40b24478fa11b730f7885c7f153cf1b2f35e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed688932978e8302275550ed1c0f2522ffbfbc97b1a2fe862f27e21de9860f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804905f1b40b35a85bdf3348c08741235d3e8a14b00935513dc88402af2a2a82(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b17e0c61ddd41af9614e9eeb2b1fe67f1611e4e5968644839f17eafe6bf4d87(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064a9ab7cbf23cc3431d572f7698f1fead54b57363d0a706e4109e9500eb7d68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4c8ad67bcb38e2b52b2bc9e1721cb8bdc2994e61bedb0e39a508a53c808f8e(
    value: typing.Optional[UserParametersTimeInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a933064c1368864be77b140c9b2e5039b96f7f6316175cb74385b90dbdb5cc7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9ccc1979550f9dc1c4e956c076d345e236c43bbc66b84aab44ba0a7250e04c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5646ec0a2b3ed48aba0628315d8aee2cd347c7384826ad6b05067f3ed4a6684f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3468394680744f38d4c6a2aae11dc8fe9faaf035d38891b14a8b64d81286a687(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0778a6ebb88f79ba6c3020c616de4c9f0be48f6beb287ae92ebc4b53c377c2a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df03b1be48f2c784a31108d7879caaca4ae32c1a7a731b35806c790bf57740b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738f457f4afd545f623d246308eb22410c57fece686468478fa224eeaf58edb7(
    value: typing.Optional[UserParametersTimeOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f169eae7e66f3df15e1e3e66aac98157d4832aec8a106d8460b3498cb82368d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5998ce4765c246943fe3442332265a6af915289af2525e2877a69a705fc98a5e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016cd0b86800703890e2ecc188d3e5b05818e6214e258938ade58a6788a73034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101099c30fc9a6e15edcd84c482aa0d83f45519122872c3d3b87ee7e4ef02a25(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a984621216583340552f4cd9ed9ea6fc71c3f767640324a9e894cbe5ac9db3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e061e4b5473e05b866087e5eff533840175ac171eb8d3d838d76bc77550455ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717ef67b4a0dac7493b15be66dbca0a23bbfa0d11915d04e54e3f98a595400e6(
    value: typing.Optional[UserParametersTimestampDayIsAlways24H],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1693568474ec6551709b67b34c00df6991eea3b6838c62930869e23a5f5bc35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c8ed7b8eedb568c967d1526fb666824d6c081ae06c1d07adcad6d3ca4ed9e7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215819e98f3028deab408a3b2945681d4e4fd6abe186d07894fa65f6d940afa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d37463bf75ce84801802226be6966469dc9a1ba28922d5856dfef195fedce3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cde81827d686c70504530aab3d3ae93a1109d305bc047ba3e6fdedd9304d45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a089184ab607215bd04ab3d6ea40c6d630d88809eb09ebb50e0f7b2e02911fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716d20dbd9f6ca6f82f4acb8793c2022f4fc304bda0a8720cd2805edc2b92114(
    value: typing.Optional[UserParametersTimestampInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1b0bcb722c57338d17e3650470e518b3ad2402f464f6ca9da448012496efc2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5506ee2a6de6217d9a2f16601c6ffdaf69f405bfc9f8b5d4f7757f9aa8c242(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcc4dbf06831818c590734a531f6234d31020e9de96c41a91949cc1a58424d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cd5bdb0eb7ac8dd95508e74b38b178f88a2b2438a886ed550de41b36305776(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a25c7f20b480d300ad53bfb4409812553bdf4a04d1c88bb997f1bb5f108fa01(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f48a00aacf6e165cab642c3efca2f1143211cb91b2951fff23aff3056ea059(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e6355969f6bda481434587ca937b8f9a8573d0b987d0e2ffa6ac42bec4c60d(
    value: typing.Optional[UserParametersTimestampLtzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b2e964f719e7bc77d887a7b453c33a0e6af02be5c5b137c9b10e04237108ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d50544f9369490d0dd2681c849d086aa9e525f4abe35b00d4f94482ecdc7a17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced24ae34e46f5ac2e27e0e7068d67663b210b532c633e289277094d174c0b95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dfb03f4da2a6ef3a9b752e2fc93c75343a86d1338fcea0cdfc7d7f5bba3e93(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3364f77374b2b32b4c46a56fd7e4cf2f831d89fe055158ad3e03bc8452917c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a8c5fb93649722ff7c2d75b921ba388aeea9208272d17ede96efe93a5f1d95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdca95a27e3821d516926abcb67920dd41f12cdcdd9850faabe527197f33bcd3(
    value: typing.Optional[UserParametersTimestampNtzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5491d7eb536507594b01c93a26292bb24e52eb2bdc897fb6343909bacea14f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26db9d4459bde59f8456c545a5847462664ac354b6054c1e6fef6b85cf86d678(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d389eda024c8ef90890830aae72972eae5d8edfdec5ab40bbebcebc06e0d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dba773a9b2fe7238f3103935cf9eda8015f317dadd993835044b73e58b5e43f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6a680307145e65c7ce09110a572fdc00b7296d3effdf2d965a7d26de6117b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec6954a73e856b9535c9286788c6769b5ebae4a3165f72da13da6dd29743218(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc906878fe4542f0640c51330dbcc18bf57010a88695dcdcba26cac249cdcc3d(
    value: typing.Optional[UserParametersTimestampOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0004f8dc9b08712ef5e5edad43a165cb0695e24884cce5ec02deeb189cb1b8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23cba309384b1138adb69c96d4471fd801d2059c3c299680fdca22ccb42bdbc0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8882f92300f21825568b2bbcef84afc082a8c010436f399a46de89fbce773a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb5fd4c546fde6a2f0eaecf9cb85f3bed951c6b9c39a2b5d2a14a24bc20d1e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135c97c56f81c2ed43364c16f961c3248b2c3aa2d4009e9d2416300654a1891c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90814e2ebf4536c4fb29787e90195655f24ee6e538457e0407f70789e99c3ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32089263342acf7b01210af1095665bb959635f094f94c2f064bb4b006884efa(
    value: typing.Optional[UserParametersTimestampTypeMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51901286659556558763517d23b47e0f49b2a0df6becff0f3c1ea631627ce53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578ce33f9efb109b36484cc8ee129ac591f2cf585b4a222ffb2baf630eb955c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1b76ec0f7bcff3c3dda274bba4b77897cbe4c4f27955e5e0e9fd8601ae6cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf297114b5f0e58a288cc112fa6419d1a0e2c701ccd2ee93c142570c539d698e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55503b375d844d3b42eaf30151a657e92cff40bcf613cb26bbb030112bbe268(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0e5445d07508a7be7ae9aef6bb0b2bbce667500d3e0e7762f246fc155dd91d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d6d1041edae8b7826d30dd631cfead1dd7958af9e8fbe71710da4f33a2c293(
    value: typing.Optional[UserParametersTimestampTzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806a37a9f9d12256625e195e0ee0fd0f40de8f954d72baa9343b8a4fca4d572c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a28981162e1d575d26d52cccad277f946edf7e6ed26945810b6214c9794c1f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d391730f4d154e84aef7d6ed63640ab8c55f0cd699b052229cc1ceb29ad6dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd40bc00b5a2781b53e52b8d2334483efdd1a2b7b10306a789f5cf5781aede30(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd99ed3c67f563b028667470033b70ddc404eaec8aa58830b712640945f0f3ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01be5d2920049d5efd9058362c0643c1ef34233fccd087bd957e210ef1cab653(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea562036da29045b7caa97398e638f65c56ff3a32bf5d29250dba3b01c1b012c(
    value: typing.Optional[UserParametersTimezone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bdda2d5ab02da898525a58afaf27cea0cdc4fcbd727cabcb06e6332a91981e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd65409fd4415a78c8593c9bd67bc71bdd5f93356cdff3232759408f49795f2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396ef69ec8a6032f2f923a9db2330746d22055a3b29fdd82c7322afd486ec9e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99cb268f1bb8f5d70ca900979464dee10c6e301f67e2bd685728ebccbec31667(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd27a92935b3893b148688b31cf8009c7662316be571545adac6c685801cd7bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66ae31051e62666b47f4173654a188fcb316f8468ca8640261a960442375e25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df640224cefd813fef6b5cff6770311a727ea3062df2c072867e4f61130077d4(
    value: typing.Optional[UserParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2649b6b9255f07045da3890146939230617f6de8bfe73a5042041fbcea491f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc74eacd8adbc9229e866003c299fe35b96bf6219609174755ab1614a51e102a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c5d94328aa612f6625ad439c43fba19f2c71d593825b0aeb60304fdf08eb20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e7cd1c118517765cac16667fa0beca83e50b0fe33396d5210d14e0c163a001(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351370c3fad51d0553ce320e374e23a688e99825e155726c3f775fc1517794c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fbacfeb6abb0f2a1e5077959fb9b214f0d0ac1b63a4ff5b7c1b4f84ce33917b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b041e0713924a15bd9785ad213809faa629a0e589c7365f2917e246c5d49b359(
    value: typing.Optional[UserParametersTransactionAbortOnError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673bd8e67d3652949fdda7f1725608aa1b1f221f4381bc207b0803ea2c440100(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e51cac7b67392fa5ab119920336ffe93ffacbd4e4f7d615df71c6be71f6cec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20259db11fe598f2453fbebaab19a313d3a370a0bebbce0c4af9fda909b93d6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a645d511c7061a9305531af13c62227a312da71af59824ec5b4478e33b84e24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0431cda7a7db99f4411f2b780b85e9e7f07caa30a653947c2f53bbf22d70c80(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbd7902633f7dee20fc9612bae94242a274422e2ac277d19d7e7dc61fbdf1a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edaca4f270ad8fb3ea7e249f4a025e7d429d54ee182560f414564954c0f9e832(
    value: typing.Optional[UserParametersTransactionDefaultIsolationLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f269f3b8b0068182caa8bb3b69b1c5cbae4af5ac916f9acdbefa7c7b1bea72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75835f1623e216011b20946eb0c78ddd32111a45b7b99e9ae0025a26e9c2a5a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1214365a59b4067786f35cf3147ab785ee47265d98cee83467027dd4e7fc6f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25ee19c64796a08e66d876b0aa7c2318ebcf07db821705b14a7587c6844c1bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794a0530630e7d7e13bba1cf3d4c4ca94574b351845394b0570355ceeb0a59af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7ad2f9dd55207b1c05908cdbff19dcb5b6fa9b339f9f0c14226fdd66d91cdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae16a24a001c24a97b01655521e10ae37b61656c5f72d782172bedca13f0969e(
    value: typing.Optional[UserParametersTwoDigitCenturyStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d282d202ed696dbec7c6f233d93ce77e4d96cc10513fa4eee6b4e88fddc8abc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c0d6074eec82f55c40611d4065e00078eeae777cf8b9f0bd4a22e4b7a16308(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf7c11a9cbcdf8835cae53e0a0837d120feedf3a4e349a37882111f2cb164ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa1a7496017a868d8e466d6ad4249aab086897a244a9c0cfa2d3f945d1c6f83(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832e935af80a95bd4f50e3c80847ef8acba66cf2e8b82c9558dbdf6f80a08b98(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6fafa03f45db980559ee9ced0605a7c57684b9fe762d56e080c234de7c6294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cbe52a0ad56c9d332e70ae2a9972d6166c51efbd9bdeecb28fdc7d3082e1ed(
    value: typing.Optional[UserParametersUnsupportedDdlAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8520b1a13b34f1a331916421f007c39c7f242f442967dd872a97af1c8006f045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12967a2d56e13fc00769f7ba2a691d6fc022579d9f16a7d72eaebfadd1f7764c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414c98279dcaac6d537d1af3189c73e1af4477f7471c76ed4a24164e7b3a61ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a122bd33307887e72c6fcc2d7f65da63bbaf02e29c4ebb34bec4e6bb81f2463(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53556b62c5da6e0b11590401ac31f56abc6c6a5d16a2223c7eab3f20907f1eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6301ccff45ceae709c62ebc1096b1cc9a9fd916b347acdefec650b0f5e1c03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4031dd206e29e3026401aac901ab53853283e137d3b354189efd8a896aff8097(
    value: typing.Optional[UserParametersUseCachedResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c7d1e1dd755832225d3cf1b59306b20b54aebdc7c23f023c22f234c60067ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec072a096f13a8bfd4f6e71ad9fbef8f363f1aac96c442eb202a8aec8e7fd0c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ac5835be809c9999f7e4d1a73deff0739700c5563c71888b59275b32ce2e86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b50a204d40bce05054f72516ceb9423d3af7396de0af4abd9357b3979db758(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c369388a6c652b31516120dd56854ab75f52a53f7d31f87a8edbe8dc8713f814(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c04659223551e0c9837a82fe05c9967d18abaaf4b90eab4b7d8fcfba539ff0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf390ebd2309cf85ebc8181bd5701401c4f57db796d21888fafd4b3a96155254(
    value: typing.Optional[UserParametersWeekOfYearPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6dc09643dfb57f28bc4d4b58d55a04ffe2c6fd89a3ec9d0b3d54ddaa9721ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7274d83b3089e9121d6a215b9709e48d425d8f931e5f0cb1ab3e57ab4fe763(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df033cacc293b085b4c93221a721bf59daa404dd59bf12266dd5cf263ed38b2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58491bdfc6a7efbf3d21b4eb14f41fbe9ee2a3562c9cb8fd88c0476992409fae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909172bcef351b8421de16768e1ff26dc3430fd4ec0f4d58ff8398566e15ebd0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04eb9dc210cd2b5ca9556fc384dba209bff87089d5778b309d3db6bf1dfc26e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4389d47458703556269e202105bcb0804f36db9bafeacb452bb4b18574459740(
    value: typing.Optional[UserParametersWeekStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c5ff046692b04d5212ced3362c15ab68585601d1632ccbdae80d512bd4fcf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdfddfab580638872268a66fcc0a4c191b0cbe4876eb313aef4e0d11a371a2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb83f75c4326383f5fe9734e98e5d44f792e68a8ae5904f57637f9b1a05a924b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e420039010102de85f30848cb7f6cdb7a72bde3604f5d948f62f8f45f69401e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e7420aee03c4ee44b427605ebe0ceaf5de81f566a71667ad5bd6aae8950627(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c867eade738db7501a57f8c054641ff9b1b84954ab1e530086454d0611a256(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c809a8cf07ab489d412093d9893bc110052e095772185ff118ac179df599a35(
    value: typing.Optional[UserShowOutput],
) -> None:
    """Type checking stubs"""
    pass
