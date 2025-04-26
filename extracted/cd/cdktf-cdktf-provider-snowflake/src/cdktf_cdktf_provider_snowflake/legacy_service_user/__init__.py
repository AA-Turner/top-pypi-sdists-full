r'''
# `snowflake_legacy_service_user`

Refer to the Terraform Registry for docs: [`snowflake_legacy_service_user`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user).
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


class LegacyServiceUser(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUser",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user snowflake_legacy_service_user}.'''

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
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user snowflake_legacy_service_user} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the user. Note that if you do not supply login_name this will be used as login_name. Check the `docs <https://docs.snowflake.net/manuals/sql-reference/sql/create-user.html#required-parameters>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#name LegacyServiceUser#name}
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#abort_detached_query LegacyServiceUser#abort_detached_query}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#autocommit LegacyServiceUser#autocommit}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#binary_input_format LegacyServiceUser#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#binary_output_format LegacyServiceUser#binary_output_format}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_memory_limit LegacyServiceUser#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_metadata_request_use_connection_ctx LegacyServiceUser#client_metadata_request_use_connection_ctx}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_prefetch_threads LegacyServiceUser#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_result_chunk_size LegacyServiceUser#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_result_column_case_insensitive LegacyServiceUser#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_session_keep_alive LegacyServiceUser#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_session_keep_alive_heartbeat_frequency LegacyServiceUser#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_timestamp_type_mapping LegacyServiceUser#client_timestamp_type_mapping}
        :param comment: Specifies a comment for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#comment LegacyServiceUser#comment}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#date_input_format LegacyServiceUser#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#date_output_format LegacyServiceUser#date_output_format}
        :param days_to_expiry: Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in. This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#days_to_expiry LegacyServiceUser#days_to_expiry}
        :param default_namespace: Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the namespace exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_namespace LegacyServiceUser#default_namespace}
        :param default_role: Specifies the role that is active by default for the user’s session upon login. Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_role LegacyServiceUser#default_role}
        :param default_secondary_roles_option: Specifies the secondary roles that are active for the user’s session upon login. Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_secondary_roles_option LegacyServiceUser#default_secondary_roles_option}
        :param default_warehouse: Specifies the virtual warehouse that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_warehouse LegacyServiceUser#default_warehouse}
        :param disabled: Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#disabled LegacyServiceUser#disabled}
        :param display_name: Name displayed for the user in the Snowflake web interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#display_name LegacyServiceUser#display_name}
        :param email: Email address for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#email LegacyServiceUser#email}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#enable_unload_physical_type_optimization LegacyServiceUser#enable_unload_physical_type_optimization}
        :param enable_unredacted_query_syntax_error: Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error. If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#enable_unredacted_query_syntax_error LegacyServiceUser#enable_unredacted_query_syntax_error}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#error_on_nondeterministic_merge LegacyServiceUser#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#error_on_nondeterministic_update LegacyServiceUser#error_on_nondeterministic_update}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#geography_output_format LegacyServiceUser#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#geometry_output_format LegacyServiceUser#geometry_output_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#id LegacyServiceUser#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_treat_decimal_as_int: Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_treat_decimal_as_int LegacyServiceUser#jdbc_treat_decimal_as_int}
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_treat_timestamp_ntz_as_utc LegacyServiceUser#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_use_session_timezone LegacyServiceUser#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#json_indent LegacyServiceUser#json_indent}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#lock_timeout LegacyServiceUser#lock_timeout}
        :param login_name: The name users use to log in. If not supplied, snowflake will use name instead. Login names are always case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#login_name LegacyServiceUser#login_name}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#log_level LegacyServiceUser#log_level}
        :param mins_to_unlock: Specifies the number of minutes until the temporary lock on the user login is cleared. To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#mins_to_unlock LegacyServiceUser#mins_to_unlock}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#multi_statement_count LegacyServiceUser#multi_statement_count}
        :param must_change_password: Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#must_change_password LegacyServiceUser#must_change_password}
        :param network_policy: Specifies the network policy to enforce for your account. Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#network_policy LegacyServiceUser#network_policy}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#noorder_sequence_as_default LegacyServiceUser#noorder_sequence_as_default}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#odbc_treat_decimal_as_int LegacyServiceUser#odbc_treat_decimal_as_int}
        :param password: Password for the user. **WARNING:** this will put the password in the terraform state file. Use carefully. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#password LegacyServiceUser#password}
        :param prevent_unload_to_internal_stages: Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#prevent_unload_to_internal_stages LegacyServiceUser#prevent_unload_to_internal_stages}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#query_tag LegacyServiceUser#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#quoted_identifiers_ignore_case LegacyServiceUser#quoted_identifiers_ignore_case}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rows_per_resultset LegacyServiceUser#rows_per_resultset}
        :param rsa_public_key: Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rsa_public_key LegacyServiceUser#rsa_public_key}
        :param rsa_public_key2: Specifies the user’s second RSA public key; used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rsa_public_key_2 LegacyServiceUser#rsa_public_key_2}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#s3_stage_vpce_dns_name LegacyServiceUser#s3_stage_vpce_dns_name}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#search_path LegacyServiceUser#search_path}
        :param simulated_data_sharing_consumer: Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views. When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#simulated_data_sharing_consumer LegacyServiceUser#simulated_data_sharing_consumer}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#statement_queued_timeout_in_seconds LegacyServiceUser#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#statement_timeout_in_seconds LegacyServiceUser#statement_timeout_in_seconds}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#strict_json_output LegacyServiceUser#strict_json_output}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#time_input_format LegacyServiceUser#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#time_output_format LegacyServiceUser#time_output_format}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_day_is_always_24h LegacyServiceUser#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_input_format LegacyServiceUser#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_ltz_output_format LegacyServiceUser#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_ntz_output_format LegacyServiceUser#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_output_format LegacyServiceUser#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_type_mapping LegacyServiceUser#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_tz_output_format LegacyServiceUser#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timezone LegacyServiceUser#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#trace_level LegacyServiceUser#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#transaction_abort_on_error LegacyServiceUser#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#transaction_default_isolation_level LegacyServiceUser#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#two_digit_century_start LegacyServiceUser#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#unsupported_ddl_action LegacyServiceUser#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#use_cached_result LegacyServiceUser#use_cached_result}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#week_of_year_policy LegacyServiceUser#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#week_start LegacyServiceUser#week_start}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69630f43fbeb2a408edfc00c0b91025ccf040b24379615b2e291ee1012259b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LegacyServiceUserConfig(
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
        '''Generates CDKTF code for importing a LegacyServiceUser resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LegacyServiceUser to import.
        :param import_from_id: The id of the existing LegacyServiceUser that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LegacyServiceUser to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7548a07c04bbe7e7b86232f4787d852ed608b98b355212ca567ca2a6852c5216)
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
    def parameters(self) -> "LegacyServiceUserParametersList":
        return typing.cast("LegacyServiceUserParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "LegacyServiceUserShowOutputList":
        return typing.cast("LegacyServiceUserShowOutputList", jsii.get(self, "showOutput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__06574f68bbb9e1ea92e32544aeb09ee3c1b213cd9f79168d63a88dbaaa395761)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceb2fe363bb4e64def429c72d63b50d4504fb6caf4b5481b8a41b0faa86862ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocommit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryInputFormat"))

    @binary_input_format.setter
    def binary_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7504488019a8a575ee6af2aaef135591bc6b4b0884697683cb7e7113eac949f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryOutputFormat"))

    @binary_output_format.setter
    def binary_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2020ae6c8337680f777cdbd9439e7c9b8d9737c0c10cc9f58d9a75b3bed3cddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientMemoryLimit"))

    @client_memory_limit.setter
    def client_memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a943167309219c9ed0b0b9f6aa886d14144da1920a9c9e7daaaa4dae355e7ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36751af9349828b7add3135a40012c8b4849edb457e0b0e90be1a11e5a15271a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientMetadataRequestUseConnectionCtx", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientPrefetchThreads"))

    @client_prefetch_threads.setter
    def client_prefetch_threads(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c68ae6ce1c83ba8d38b203309eceb7aee7f07301c6b5358c793f514a8a95851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientPrefetchThreads", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientResultChunkSize"))

    @client_result_chunk_size.setter
    def client_result_chunk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__626abe5ce03a6bec30f860294fdb3447031e0543e6f4dab22fd926064ae51925)
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
            type_hints = typing.get_type_hints(_typecheckingstub__353e201d1815d0858f4c19603d23891a43975cb27851b1a2066961a1065c0eb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af30eef3207c378127df7d81c27594247d56f6d9e29df22c7ed0041787954e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAlive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @client_session_keep_alive_heartbeat_frequency.setter
    def client_session_keep_alive_heartbeat_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653a923b6b0eff6b930375acc51629406e60c93306c6458edc4696722d1852dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAliveHeartbeatFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTimestampTypeMapping"))

    @client_timestamp_type_mapping.setter
    def client_timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__414bb2cf4abccbd1adb8f5d9119fa91066c09e83b3f5556cca92cb38fe6dad58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19840ecff5c6f2e78854e6054c8e13c00067a3a57c0d3da2baca382fead13e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateInputFormat"))

    @date_input_format.setter
    def date_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a16f744a47563ce1bcf5cff7660f05ee1c718feff667315946154cf0d9a26b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateOutputFormat"))

    @date_output_format.setter
    def date_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a901d25ad7962af9039aeff21b7fc98717a2b7b72e44751e0906d6c29790a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="daysToExpiry")
    def days_to_expiry(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "daysToExpiry"))

    @days_to_expiry.setter
    def days_to_expiry(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a11820f94118c939352b754316cef0fb25c9b2e52a05633fa979725b40c4d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysToExpiry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultNamespace")
    def default_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultNamespace"))

    @default_namespace.setter
    def default_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6722495e06006c649a61a34a99de02381722dee8a605c8330f1f248f06c0c15d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultRole")
    def default_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultRole"))

    @default_role.setter
    def default_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739bddf713d6767b347436b4143cab7c6e8a936361692160a4e918714169cfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultSecondaryRolesOption")
    def default_secondary_roles_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultSecondaryRolesOption"))

    @default_secondary_roles_option.setter
    def default_secondary_roles_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf76e58ce722a52ffe4e1e88f79923c8723b4b80531fdd1136d633428ef3baf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultSecondaryRolesOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultWarehouse")
    def default_warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultWarehouse"))

    @default_warehouse.setter
    def default_warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd61c1ae18b80098d2c613fad0bf0de5366732c855f459cf28d4c7fb9bae4f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultWarehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47eaed1b7cfb0774bc130d10871936c962cdd181e133c434960464d00fb73e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b934df9774bb30633bddc4acbb41013125a00319dc6102e29288b74b682a2fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d461224ef3ab99c820f4131a0ba879ac8a940ea2f78e189b8747fc55241a33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__456371b4e8e09b0a6f15bc6a1a6eb1ad0babecbe1f4384aeedd9f00e6757f973)
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
            type_hints = typing.get_type_hints(_typecheckingstub__870eb69d4f559eeae23693b254b2307881b92770dc9c5d6f62c3b20f32d1833e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c22bfeb7dfbd77693408cbf9c127006c3f702af0040736d98900357c93dece2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae9a384ccb413ab992a92a2e678974dcc4535f7d2b914b6c4dee8dfbce682459)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOnNondeterministicUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geographyOutputFormat"))

    @geography_output_format.setter
    def geography_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59814e740a29a81da7b17f13311410600f25dec3eedddbd6531bd90951569c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geographyOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geometryOutputFormat"))

    @geometry_output_format.setter
    def geometry_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70bd21d97088b12ee60bd43ddbc70488732278a899aef397759e2f391507fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geometryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e1bb086716b33c54adba545db912c33e2271f4069469ee9c8070a5cf31e2f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35e4391ad2c59c00fdc66f6f3b7c4b0411c004a5d1535773dd008c080db325d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fde1696e894bfb96a3583ec496f8cb494c6951788d463d9885964409bdd03b6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__712414e94f7cc1841bab26e9ea5c3f5cff4240fcca79c8c2a246241e8d627c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jdbcUseSessionTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jsonIndent"))

    @json_indent.setter
    def json_indent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9147de55c57ce8fca87aaebe4f30cf8b4776642228b6f2c1ce057834aac833a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonIndent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockTimeout"))

    @lock_timeout.setter
    def lock_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1393fcb894418e178bd244169a86a9c8f423690469ba834da884f88eea9ad81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginName")
    def login_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loginName"))

    @login_name.setter
    def login_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8557679734f29d00d791932d1458404b9d68d4997b5450efc10177546d73c9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286e24a2526006d8492309171a291ff866392b7a3295178d93fc36164706b27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minsToUnlock")
    def mins_to_unlock(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minsToUnlock"))

    @mins_to_unlock.setter
    def mins_to_unlock(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f79555f4369d160c0bfc3e54f811305e7a8a92040463dba627d0b21440ffe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minsToUnlock", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiStatementCount"))

    @multi_statement_count.setter
    def multi_statement_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b219505a893e0f25b63f7d9cb6e125af61d9e6c873ed27fb16de66aca3b052d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiStatementCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mustChangePassword")
    def must_change_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mustChangePassword"))

    @must_change_password.setter
    def must_change_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6393f28e015127f48a204ae95e08bf4a752639966b09c74ada4888a253288fca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mustChangePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__878f2363e21b478ba3a255b61e91893a62715d22f096e042e88d12e2bb5dfdc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPolicy"))

    @network_policy.setter
    def network_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a05f15a6eb7060ca6e0ea25bac286db47ca1efbbe84128272c8a52d88f9de34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27ca6ce72ed1da2c3c6accddddcf7ba5bd63be967826ee9d2b7580a106cddeb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd724a12abe89080a649738dabe448567c131d6d0685acb3dceabf945917ff39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbcTreatDecimalAsInt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c128492c797a26500b61a25d80bd965d31ad5a340799995fb640286fdc2d5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29b3e3d446350c96f9708595eca42786fb795a74fb81a35da927d26f66361efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventUnloadToInternalStages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryTag"))

    @query_tag.setter
    def query_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8b294148a01e4c82e7076aa18a445a0225b0988b019812c0ad817720cb311e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2542748f230ff5a96d5f8eed64eb069a01c171820908cffea5637e0a3d3b857b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quotedIdentifiersIgnoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsPerResultset"))

    @rows_per_resultset.setter
    def rows_per_resultset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29456820d8c039dbaba63f0d9e30288c54c8f7480732481b386f8bb446c27fb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsPerResultset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKey")
    def rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey"))

    @rsa_public_key.setter
    def rsa_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb6ac83b07ccd59e89f81c5d54876dc201c9018fbb4b1b84addb8fdbd875f869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKey2")
    def rsa_public_key2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey2"))

    @rsa_public_key2.setter
    def rsa_public_key2(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8783d1de83a0f13cff4c1158cda200c67c63a2f130846c1761f39e43e49f07a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaPublicKey2", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3StageVpceDnsName"))

    @s3_stage_vpce_dns_name.setter
    def s3_stage_vpce_dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5341249a662b0c3d4617b425e3c874ada04ead78742040ae9b59eff2c96c9241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3StageVpceDnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchPath"))

    @search_path.setter
    def search_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c31d06e473662415d466fdda395a9fd08debe2f91c37711728fcdb1d00ace3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumer")
    def simulated_data_sharing_consumer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "simulatedDataSharingConsumer"))

    @simulated_data_sharing_consumer.setter
    def simulated_data_sharing_consumer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c50f0224d75ab10c8cbbd0d9212856b79a2e73b67e216d266964cad4395c9a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simulatedDataSharingConsumer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @statement_queued_timeout_in_seconds.setter
    def statement_queued_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0f9e853567042025649e09582de602fd9fb5243d6a29151a44c4429dc74fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementQueuedTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementTimeoutInSeconds"))

    @statement_timeout_in_seconds.setter
    def statement_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b552c0267e37be0f3c7759c10c4d91b1176a3180a68fa7905d67177df435d6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97ca1c49720f351f872a6c8a48dade977bb3af0ec0c78c0d6b9a3eefcb56cfd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictJsonOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeInputFormat"))

    @time_input_format.setter
    def time_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e47cf61e2f8a8565b3def133fd6ace457e0620af22a6d87a296fe4f65418ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeOutputFormat"))

    @time_output_format.setter
    def time_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192f0febc3f9d51548a1818f3fe32c0cba4f5054c3a56c1fdd2c9a7349d8fec1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf82e8e51fcf6501e03eb14781869ca1071412f45c6c6a12991889a8c63c316f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampDayIsAlways24H", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampInputFormat"))

    @timestamp_input_format.setter
    def timestamp_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd9876bb26222908e667532399dff019cbda265fb3e5e444481d311ddb428e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampLtzOutputFormat"))

    @timestamp_ltz_output_format.setter
    def timestamp_ltz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36050674a95feb01612004170e920340cad72c5da943c088f78f38735a347169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampLtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampNtzOutputFormat"))

    @timestamp_ntz_output_format.setter
    def timestamp_ntz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4dffd2b24ec25617e3d2e25e26853b3dc04cc95fedec4f15510b137e7743629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampNtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampOutputFormat"))

    @timestamp_output_format.setter
    def timestamp_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a03f2169a897f0b88c1c7c58111213eed4983d0f74df638d76db8ef5ab10b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTypeMapping"))

    @timestamp_type_mapping.setter
    def timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97665c9eee7623cf489064fde7c29eedbf15c7bd9f9e5e9502454a639fc9934a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTzOutputFormat"))

    @timestamp_tz_output_format.setter
    def timestamp_tz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3da795d17f8c68a31ae16e7145980f88248cb487969308fd539f7571358f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99caf7e73d8838378206bbc74141bea6fba0009d3b58d387e148d32891730518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb23777b1a0f4c0ab7c0f6081d384f68e743736e66649a02d2e62485c8675460)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d01b1a4cd2e6e6e193568cb070e842861d99ad22fa44379af50fdb5c158de2a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionAbortOnError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transactionDefaultIsolationLevel"))

    @transaction_default_isolation_level.setter
    def transaction_default_isolation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3192b3007f706b31e8411127c7ebe0bdd4db2f7f505d81bca8bfc03cc4a24a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionDefaultIsolationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "twoDigitCenturyStart"))

    @two_digit_century_start.setter
    def two_digit_century_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9123eac23616f74bbc53b5af1320edbdc413bb29aba473e906dd01e4364d83de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twoDigitCenturyStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unsupportedDdlAction"))

    @unsupported_ddl_action.setter
    def unsupported_ddl_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb200aba10efb86a0b865d740cc7886719c616828e5ddd0c0fb009ec8ce25a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f1997e6a92de47354105c80522c69bdd586228e6d5b2e03e7d627ba423e1993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCachedResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOfYearPolicy"))

    @week_of_year_policy.setter
    def week_of_year_policy(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46128413dcbc2b65bf6200e7f421d6af0134ed22990c8f0e3adc914995e977e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfYearPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekStart"))

    @week_start.setter
    def week_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673e0bc6392ea02ef7ee004691f8743fd686174bd0a3f01718f782c3beaf7db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekStart", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserConfig",
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
class LegacyServiceUserConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        :param name: Name of the user. Note that if you do not supply login_name this will be used as login_name. Check the `docs <https://docs.snowflake.net/manuals/sql-reference/sql/create-user.html#required-parameters>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#name LegacyServiceUser#name}
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#abort_detached_query LegacyServiceUser#abort_detached_query}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#autocommit LegacyServiceUser#autocommit}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#binary_input_format LegacyServiceUser#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#binary_output_format LegacyServiceUser#binary_output_format}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_memory_limit LegacyServiceUser#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_metadata_request_use_connection_ctx LegacyServiceUser#client_metadata_request_use_connection_ctx}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_prefetch_threads LegacyServiceUser#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_result_chunk_size LegacyServiceUser#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_result_column_case_insensitive LegacyServiceUser#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_session_keep_alive LegacyServiceUser#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_session_keep_alive_heartbeat_frequency LegacyServiceUser#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_timestamp_type_mapping LegacyServiceUser#client_timestamp_type_mapping}
        :param comment: Specifies a comment for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#comment LegacyServiceUser#comment}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#date_input_format LegacyServiceUser#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#date_output_format LegacyServiceUser#date_output_format}
        :param days_to_expiry: Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in. This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#days_to_expiry LegacyServiceUser#days_to_expiry}
        :param default_namespace: Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the namespace exists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_namespace LegacyServiceUser#default_namespace}
        :param default_role: Specifies the role that is active by default for the user’s session upon login. Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_role LegacyServiceUser#default_role}
        :param default_secondary_roles_option: Specifies the secondary roles that are active for the user’s session upon login. Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_secondary_roles_option LegacyServiceUser#default_secondary_roles_option}
        :param default_warehouse: Specifies the virtual warehouse that is active by default for the user’s session upon login. Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_warehouse LegacyServiceUser#default_warehouse}
        :param disabled: Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#disabled LegacyServiceUser#disabled}
        :param display_name: Name displayed for the user in the Snowflake web interface. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#display_name LegacyServiceUser#display_name}
        :param email: Email address for the user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#email LegacyServiceUser#email}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#enable_unload_physical_type_optimization LegacyServiceUser#enable_unload_physical_type_optimization}
        :param enable_unredacted_query_syntax_error: Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error. If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#enable_unredacted_query_syntax_error LegacyServiceUser#enable_unredacted_query_syntax_error}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#error_on_nondeterministic_merge LegacyServiceUser#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#error_on_nondeterministic_update LegacyServiceUser#error_on_nondeterministic_update}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#geography_output_format LegacyServiceUser#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#geometry_output_format LegacyServiceUser#geometry_output_format}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#id LegacyServiceUser#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_treat_decimal_as_int: Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_treat_decimal_as_int LegacyServiceUser#jdbc_treat_decimal_as_int}
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_treat_timestamp_ntz_as_utc LegacyServiceUser#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_use_session_timezone LegacyServiceUser#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#json_indent LegacyServiceUser#json_indent}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#lock_timeout LegacyServiceUser#lock_timeout}
        :param login_name: The name users use to log in. If not supplied, snowflake will use name instead. Login names are always case-insensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#login_name LegacyServiceUser#login_name}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#log_level LegacyServiceUser#log_level}
        :param mins_to_unlock: Specifies the number of minutes until the temporary lock on the user login is cleared. To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#mins_to_unlock LegacyServiceUser#mins_to_unlock}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#multi_statement_count LegacyServiceUser#multi_statement_count}
        :param must_change_password: Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#must_change_password LegacyServiceUser#must_change_password}
        :param network_policy: Specifies the network policy to enforce for your account. Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#network_policy LegacyServiceUser#network_policy}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#noorder_sequence_as_default LegacyServiceUser#noorder_sequence_as_default}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#odbc_treat_decimal_as_int LegacyServiceUser#odbc_treat_decimal_as_int}
        :param password: Password for the user. **WARNING:** this will put the password in the terraform state file. Use carefully. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#password LegacyServiceUser#password}
        :param prevent_unload_to_internal_stages: Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#prevent_unload_to_internal_stages LegacyServiceUser#prevent_unload_to_internal_stages}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#query_tag LegacyServiceUser#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#quoted_identifiers_ignore_case LegacyServiceUser#quoted_identifiers_ignore_case}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rows_per_resultset LegacyServiceUser#rows_per_resultset}
        :param rsa_public_key: Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rsa_public_key LegacyServiceUser#rsa_public_key}
        :param rsa_public_key2: Specifies the user’s second RSA public key; used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rsa_public_key_2 LegacyServiceUser#rsa_public_key_2}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#s3_stage_vpce_dns_name LegacyServiceUser#s3_stage_vpce_dns_name}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#search_path LegacyServiceUser#search_path}
        :param simulated_data_sharing_consumer: Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views. When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#simulated_data_sharing_consumer LegacyServiceUser#simulated_data_sharing_consumer}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#statement_queued_timeout_in_seconds LegacyServiceUser#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#statement_timeout_in_seconds LegacyServiceUser#statement_timeout_in_seconds}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#strict_json_output LegacyServiceUser#strict_json_output}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#time_input_format LegacyServiceUser#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#time_output_format LegacyServiceUser#time_output_format}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_day_is_always_24h LegacyServiceUser#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_input_format LegacyServiceUser#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_ltz_output_format LegacyServiceUser#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_ntz_output_format LegacyServiceUser#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_output_format LegacyServiceUser#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_type_mapping LegacyServiceUser#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_tz_output_format LegacyServiceUser#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timezone LegacyServiceUser#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#trace_level LegacyServiceUser#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#transaction_abort_on_error LegacyServiceUser#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#transaction_default_isolation_level LegacyServiceUser#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#two_digit_century_start LegacyServiceUser#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#unsupported_ddl_action LegacyServiceUser#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#use_cached_result LegacyServiceUser#use_cached_result}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#week_of_year_policy LegacyServiceUser#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#week_start LegacyServiceUser#week_start}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99eb0df6782edd67d1d1459f7ea4dc56c14115a7ac28dee520944d8178784265)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#name LegacyServiceUser#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def abort_detached_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#abort_detached_query LegacyServiceUser#abort_detached_query}
        '''
        result = self._values.get("abort_detached_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def autocommit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether autocommit is enabled for the session.

        Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#autocommit LegacyServiceUser#autocommit}
        '''
        result = self._values.get("autocommit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def binary_input_format(self) -> typing.Optional[builtins.str]:
        '''The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#binary_input_format LegacyServiceUser#binary_input_format}
        '''
        result = self._values.get("binary_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_output_format(self) -> typing.Optional[builtins.str]:
        '''The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#binary_output_format LegacyServiceUser#binary_output_format}
        '''
        result = self._values.get("binary_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_memory_limit(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB).

        For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_memory_limit LegacyServiceUser#client_memory_limit}
        '''
        result = self._values.get("client_memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema.

        The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_metadata_request_use_connection_ctx LegacyServiceUser#client_metadata_request_use_connection_ctx}
        '''
        result = self._values.get("client_metadata_request_use_connection_ctx")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_prefetch_threads(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the number of threads used by the client to pre-fetch large result sets.

        The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_prefetch_threads LegacyServiceUser#client_prefetch_threads}
        '''
        result = self._values.get("client_prefetch_threads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_chunk_size(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB).

        The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_result_chunk_size LegacyServiceUser#client_result_chunk_size}
        '''
        result = self._values.get("client_result_chunk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_column_case_insensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_result_column_case_insensitive LegacyServiceUser#client_result_column_case_insensitive}
        '''
        result = self._values.get("client_result_column_case_insensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to force a user to log in again after a period of inactivity in the session.

        For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_session_keep_alive LegacyServiceUser#client_session_keep_alive}
        '''
        result = self._values.get("client_session_keep_alive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_session_keep_alive_heartbeat_frequency LegacyServiceUser#client_session_keep_alive_heartbeat_frequency}
        '''
        result = self._values.get("client_session_keep_alive_heartbeat_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#client_timestamp_type_mapping LegacyServiceUser#client_timestamp_type_mapping}
        '''
        result = self._values.get("client_timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#comment LegacyServiceUser#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#date_input_format LegacyServiceUser#date_input_format}
        '''
        result = self._values.get("date_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#date_output_format LegacyServiceUser#date_output_format}
        '''
        result = self._values.get("date_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def days_to_expiry(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days after which the user status is set to ``Expired`` and the user is no longer allowed to log in.

        This is useful for defining temporary users (i.e. users who should only have access to Snowflake for a limited time period). In general, you should not set this property for `account administrators <https://docs.snowflake.com/en/user-guide/security-access-control-considerations.html#label-accountadmin-users>`_ (i.e. users with the ``ACCOUNTADMIN`` role) because Snowflake locks them out when they become ``Expired``. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#days_to_expiry LegacyServiceUser#days_to_expiry}
        '''
        result = self._values.get("days_to_expiry")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_namespace(self) -> typing.Optional[builtins.str]:
        '''Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login.

        Note that the CREATE USER operation does not verify that the namespace exists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_namespace LegacyServiceUser#default_namespace}
        '''
        result = self._values.get("default_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_role(self) -> typing.Optional[builtins.str]:
        '''Specifies the role that is active by default for the user’s session upon login.

        Note that specifying a default role for a user does **not** grant the role to the user. The role must be granted explicitly to the user using the `GRANT ROLE <https://docs.snowflake.com/en/sql-reference/sql/grant-role>`_ command. In addition, the CREATE USER operation does not verify that the role exists. For more information about this resource, see `docs <./account_role>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_role LegacyServiceUser#default_role}
        '''
        result = self._values.get("default_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_secondary_roles_option(self) -> typing.Optional[builtins.str]:
        '''Specifies the secondary roles that are active for the user’s session upon login.

        Valid values are (case-insensitive): ``DEFAULT`` | ``NONE`` | ``ALL``. More information can be found in `doc <https://docs.snowflake.com/en/sql-reference/sql/create-user#optional-object-properties-objectproperties>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_secondary_roles_option LegacyServiceUser#default_secondary_roles_option}
        '''
        result = self._values.get("default_secondary_roles_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_warehouse(self) -> typing.Optional[builtins.str]:
        '''Specifies the virtual warehouse that is active by default for the user’s session upon login.

        Note that the CREATE USER operation does not verify that the warehouse exists. For more information about this resource, see `docs <./warehouse>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#default_warehouse LegacyServiceUser#default_warehouse}
        '''
        result = self._values.get("default_warehouse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user is disabled, which prevents logging in and aborts all the currently-running queries for the user.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#disabled LegacyServiceUser#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Name displayed for the user in the Snowflake web interface.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#display_name LegacyServiceUser#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email address for the user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#email LegacyServiceUser#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_unload_physical_type_optimization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#enable_unload_physical_type_optimization LegacyServiceUser#enable_unload_physical_type_optimization}
        '''
        result = self._values.get("enable_unload_physical_type_optimization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_unredacted_query_syntax_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error.

        If ``FALSE``, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to ``TRUE`` for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#enable_unredacted_query_syntax_error LegacyServiceUser#enable_unredacted_query_syntax_error}
        '''
        result = self._values.get("enable_unredacted_query_syntax_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#error_on_nondeterministic_merge LegacyServiceUser#error_on_nondeterministic_merge}
        '''
        result = self._values.get("error_on_nondeterministic_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#error_on_nondeterministic_update LegacyServiceUser#error_on_nondeterministic_update}
        '''
        result = self._values.get("error_on_nondeterministic_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def geography_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#geography_output_format LegacyServiceUser#geography_output_format}
        '''
        result = self._values.get("geography_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geometry_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#geometry_output_format LegacyServiceUser#geometry_output_format}
        '''
        result = self._values.get("geometry_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#id LegacyServiceUser#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_treat_decimal_as_int LegacyServiceUser#jdbc_treat_decimal_as_int}
        '''
        result = self._values.get("jdbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how JDBC processes TIMESTAMP_NTZ values. For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_treat_timestamp_ntz_as_utc LegacyServiceUser#jdbc_treat_timestamp_ntz_as_utc}
        '''
        result = self._values.get("jdbc_treat_timestamp_ntz_as_utc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_use_session_timezone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#jdbc_use_session_timezone LegacyServiceUser#jdbc_use_session_timezone}
        '''
        result = self._values.get("jdbc_use_session_timezone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def json_indent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of blank spaces to indent each new element in JSON output in the session.

        Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#json_indent LegacyServiceUser#json_indent}
        '''
        result = self._values.get("json_indent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lock_timeout(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement.

        For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#lock_timeout LegacyServiceUser#lock_timeout}
        '''
        result = self._values.get("lock_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def login_name(self) -> typing.Optional[builtins.str]:
        '''The name users use to log in.

        If not supplied, snowflake will use name instead. Login names are always case-insensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#login_name LegacyServiceUser#login_name}
        '''
        result = self._values.get("login_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the severity level of messages that should be ingested and made available in the active event table.

        Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting log level <https://docs.snowflake.com/en/developer-guide/logging-tracing/logging-log-level>`_. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#log_level LegacyServiceUser#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mins_to_unlock(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of minutes until the temporary lock on the user login is cleared.

        To protect against unauthorized user login, Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts. When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes. To remove a lock immediately for a user, specify a value of 0 for this parameter. **Note** because this value changes continuously after setting it, the provider is currently NOT handling the external changes to it. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#mins_to_unlock LegacyServiceUser#mins_to_unlock}
        '''
        result = self._values.get("mins_to_unlock")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def multi_statement_count(self) -> typing.Optional[jsii.Number]:
        '''Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#multi_statement_count LegacyServiceUser#multi_statement_count}
        '''
        result = self._values.get("multi_statement_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def must_change_password(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#must_change_password LegacyServiceUser#must_change_password}
        '''
        result = self._values.get("must_change_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the network policy to enforce for your account.

        Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Any existing network policy (created using `CREATE NETWORK POLICY <https://docs.snowflake.com/en/sql-reference/sql/create-network-policy>`_). For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#network_policy LegacyServiceUser#network_policy}
        '''
        result = self._values.get("network_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def noorder_sequence_as_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column.

        The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#noorder_sequence_as_default LegacyServiceUser#noorder_sequence_as_default}
        '''
        result = self._values.get("noorder_sequence_as_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def odbc_treat_decimal_as_int(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#odbc_treat_decimal_as_int LegacyServiceUser#odbc_treat_decimal_as_int}
        '''
        result = self._values.get("odbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the user.

        **WARNING:** this will put the password in the terraform state file. Use carefully. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#password LegacyServiceUser#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prevent_unload_to_internal_stages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO  <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#prevent_unload_to_internal_stages LegacyServiceUser#prevent_unload_to_internal_stages}
        '''
        result = self._values.get("prevent_unload_to_internal_stages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_tag(self) -> typing.Optional[builtins.str]:
        '''Optional string that can be used to tag queries and other SQL statements executed within a session.

        The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#query_tag LegacyServiceUser#query_tag}
        '''
        result = self._values.get("query_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters.

        By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#quoted_identifiers_ignore_case LegacyServiceUser#quoted_identifiers_ignore_case}
        '''
        result = self._values.get("quoted_identifiers_ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rows_per_resultset(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of rows returned in a result set.

        A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rows_per_resultset LegacyServiceUser#rows_per_resultset}
        '''
        result = self._values.get("rows_per_resultset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the user’s RSA public key; used for key-pair authentication. Must be on 1 line without header and trailer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rsa_public_key LegacyServiceUser#rsa_public_key}
        '''
        result = self._values.get("rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_public_key2(self) -> typing.Optional[builtins.str]:
        '''Specifies the user’s second RSA public key;

        used to rotate the public and private keys for key-pair authentication based on an expiration schedule set by your organization. Must be on 1 line without header and trailer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#rsa_public_key_2 LegacyServiceUser#rsa_public_key_2}
        '''
        result = self._values.get("rsa_public_key2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_stage_vpce_dns_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the DNS name of an Amazon S3 interface endpoint.

        Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#s3_stage_vpce_dns_name LegacyServiceUser#s3_stage_vpce_dns_name}
        '''
        result = self._values.get("s3_stage_vpce_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_path(self) -> typing.Optional[builtins.str]:
        '''Specifies the path to search to resolve unqualified object names in queries.

        For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#search_path LegacyServiceUser#search_path}
        '''
        result = self._values.get("search_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def simulated_data_sharing_consumer(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views.

        When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, see `Introduction to Secure Data Sharing <https://docs.snowflake.com/en/user-guide/data-sharing-intro>`_ and `Working with shares <https://docs.snowflake.com/en/user-guide/data-sharing-provider>`_. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#simulated_data_sharing_consumer LegacyServiceUser#simulated_data_sharing_consumer}
        '''
        result = self._values.get("simulated_data_sharing_consumer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_queued_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#statement_queued_timeout_in_seconds LegacyServiceUser#statement_queued_timeout_in_seconds}
        '''
        result = self._values.get("statement_queued_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statement_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#statement_timeout_in_seconds LegacyServiceUser#statement_timeout_in_seconds}
        '''
        result = self._values.get("statement_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def strict_json_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#strict_json_output LegacyServiceUser#strict_json_output}
        '''
        result = self._values.get("strict_json_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#time_input_format LegacyServiceUser#time_input_format}
        '''
        result = self._values.get("time_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#time_output_format LegacyServiceUser#time_output_format}
        '''
        result = self._values.get("time_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_day_is_always24_h(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_day_is_always_24h LegacyServiceUser#timestamp_day_is_always_24h}
        '''
        result = self._values.get("timestamp_day_is_always24_h")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timestamp_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_input_format LegacyServiceUser#timestamp_input_format}
        '''
        result = self._values.get("timestamp_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ltz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_LTZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_ltz_output_format LegacyServiceUser#timestamp_ltz_output_format}
        '''
        result = self._values.get("timestamp_ltz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ntz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_ntz_output_format LegacyServiceUser#timestamp_ntz_output_format}
        '''
        result = self._values.get("timestamp_ntz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_output_format LegacyServiceUser#timestamp_output_format}
        '''
        result = self._values.get("timestamp_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_type_mapping LegacyServiceUser#timestamp_type_mapping}
        '''
        result = self._values.get("timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_tz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_TZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timestamp_tz_output_format LegacyServiceUser#timestamp_tz_output_format}
        '''
        result = self._values.get("timestamp_tz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone for the session.

        You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#timezone LegacyServiceUser#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Controls how trace events are ingested into the event table.

        For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#trace_level LegacyServiceUser#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_abort_on_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error.

        For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#transaction_abort_on_error LegacyServiceUser#transaction_abort_on_error}
        '''
        result = self._values.get("transaction_abort_on_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transaction_default_isolation_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the isolation level for transactions in the user session. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#transaction_default_isolation_level LegacyServiceUser#transaction_default_isolation_level}
        '''
        result = self._values.get("transaction_default_isolation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def two_digit_century_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#two_digit_century_start LegacyServiceUser#two_digit_century_start}
        '''
        result = self._values.get("two_digit_century_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unsupported_ddl_action(self) -> typing.Optional[builtins.str]:
        '''Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#unsupported_ddl_action LegacyServiceUser#unsupported_ddl_action}
        '''
        result = self._values.get("unsupported_ddl_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_cached_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to reuse persisted query results, if available, when a matching query is submitted.

        For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#use_cached_result LegacyServiceUser#use_cached_result}
        '''
        result = self._values.get("use_cached_result")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def week_of_year_policy(self) -> typing.Optional[jsii.Number]:
        '''Specifies how the weeks in a given year are computed.

        ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#week_of_year_policy LegacyServiceUser#week_of_year_policy}
        '''
        result = self._values.get("week_of_year_policy")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the first day of the week (used by week-related date functions).

        ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/legacy_service_user#week_start LegacyServiceUser#week_start}
        '''
        result = self._values.get("week_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersAbortDetachedQuery",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersAbortDetachedQuery:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersAbortDetachedQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersAbortDetachedQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersAbortDetachedQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__802a7103891fe7e47aa86eb7fade9ed61d53d2a596a3ce2e4568c224e13fddfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersAbortDetachedQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b223bf3d6ae39990fc4863019ca1d63bec939a18cb82ee5ce2fe53aba09311)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersAbortDetachedQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c0f2f7cdedbd51fb67ad055e75c4b5420a7bb6b923e3a8b32cfab483069f88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c998e256da88a452267c33249807c1f152c18eb7c51076fd8acc81a87eaa2dc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc60150074045750b94b46a79d6c2d81f551eb112a74518d3bc670eaabe7c79d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersAbortDetachedQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersAbortDetachedQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f85f2e648ee7c9dee447e555d95580c7db99219fb14f762662ceddf2cdbf63c)
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
    ) -> typing.Optional[LegacyServiceUserParametersAbortDetachedQuery]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersAbortDetachedQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersAbortDetachedQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a7c3405bcc29f20373a66b19136b43ce758f1b6525ec405fe047358246b7cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersAutocommit",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersAutocommit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersAutocommit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersAutocommitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersAutocommitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93e07fa880aa0f5361a076e3415585d4374cbf373de401e3dcd56d5e251da254)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersAutocommitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520c02e1d4c9468671523d057af4f9d09ad3651ebe3ae223642ed83590f54dd8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersAutocommitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72cd6237dfc94b8ecbf7cf6d8b90e3c0890c175e76f3ba836ba1a59a0225e89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b7de98dfd5b25a05cb0f440aeeb7f525544a083d0af058104bf8fc00c388285)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a7eec2cd4799acabf36b82a60d9a33c886c84f369b0b9555f7d7f7638c28a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersAutocommitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersAutocommitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e62afd8c1cab7c2b3b3760a9fecfb8f1fc4cdbc69971cd3d74acd22a0a23efb)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersAutocommit]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersAutocommit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersAutocommit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94042ba5878b538201b5eed993fefd0d5e9c0566afcddfbb5a5968426a859478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersBinaryInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersBinaryInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersBinaryInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersBinaryInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersBinaryInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fbf95dcb46794ae35abfc8269f0a7ba26de81b4506d40ff45a4ecfd7e1ee759)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersBinaryInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f235460074f228518bf0d819e1ab611dbccbc4ee229cb7dce18f153701762d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersBinaryInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d62b8c54913ff06416ff9167a67ff1a0259df963da936c57072d28cd962d8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0359514e77d02e75846252aa24611a81e093d08b8450d5e7a7e52689453f9abf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2752bb760fe444fde7af938b5e4f76e5ebef1b2e63c4c79e9b6943941da12179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersBinaryInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersBinaryInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47e5ec7021610687c77f30c952e10f6b382d6e1726c2e5d520c7ec2f23a563b8)
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
    ) -> typing.Optional[LegacyServiceUserParametersBinaryInputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersBinaryInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersBinaryInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17673472fa1d8ad035acca30ebe18d38de2ce829a4dd80f9e971c875fcf8cb7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersBinaryOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersBinaryOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersBinaryOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersBinaryOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersBinaryOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9023eda712d13c9d009671c94410abfa2b48f7616edf424332e9b301fef2c45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersBinaryOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f872afe0118ebf73ee04872318306f5d494ab0f589b8d0959232105e73b35c0e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersBinaryOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8a383b463d06a8b16d15dad6da27f5338438ef4fcf5360b10cddef87d7048f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1428677e4d53b722a5b43e30993d449a3bceccaef69d198b8d6e10390c268e1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a2d76c1adee4ae80af775b40ab583ec4b35daff04b32d35087f3fc0ade90146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersBinaryOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersBinaryOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a2f5d334a05d208454a5c286129b488bd42c3be083334ee703f00bb6901d1c7)
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
    ) -> typing.Optional[LegacyServiceUserParametersBinaryOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersBinaryOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersBinaryOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97948f3df67c51f5ed136765f787d67c0a38f82234df4629689a113c9e04821c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientMemoryLimit",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersClientMemoryLimit:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersClientMemoryLimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersClientMemoryLimitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientMemoryLimitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc2fb3d63c4e6612c1e9f4b5fe0878cba2d5a9cadb6a39b9a9e203c73a396861)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersClientMemoryLimitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8cf3e267b8de76e251972e71cd287fde029b65dd5f3ac94fad6a89df6e9b17)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersClientMemoryLimitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9029dfd0614d63b30889eef3d30e17343c438d892dbd5f7a2c30890a9a32c89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__751d3ef94108cc3f72be3894f912913a60f8cdbf4bff7eb2a0af6c9ee941faca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__979c996a4655900c0081e1a0b35a8f0b2548fcaaac7040178eb5ef48e294cadf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientMemoryLimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientMemoryLimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dc84252280d5614a68242137ec2239fd686028a3bdeac347ea3261035c38de8)
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
    ) -> typing.Optional[LegacyServiceUserParametersClientMemoryLimit]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersClientMemoryLimit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersClientMemoryLimit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f70a866897ce7a989d5eda87ebdb51e7a172c3306fac9d9cd60c672576f6fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientMetadataRequestUseConnectionCtx",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersClientMetadataRequestUseConnectionCtx:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersClientMetadataRequestUseConnectionCtx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3690898e759f11a509ea36bc18bb1305fa004c551adabab4360583d5772117c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24482ef1183c31a8426fd528cbe5b92e89b97feea9f3361bed4a56b35a3c2b46)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4539ac9c37553f52cdb5de4d0fd5a59bf8f7ea15de3d4b83a81ccbbd1a3458d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aae5c3a3a46c62a33b3812d7d0f61120b6723d9bba929447018082d230bec86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__162717b958f6f631ee861dd153e78926d940bae03a5ca5dbc2178adb9336173e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__973df2b2b8175fa79476fe08239a4ee54f8a8609055b3f406cde4b55a9020010)
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
    ) -> typing.Optional[LegacyServiceUserParametersClientMetadataRequestUseConnectionCtx]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersClientMetadataRequestUseConnectionCtx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersClientMetadataRequestUseConnectionCtx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dcd28afcd968c979069e17c5a9bc55bcdf6cec993e15497e4c4307442c7fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientPrefetchThreads",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersClientPrefetchThreads:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersClientPrefetchThreads(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersClientPrefetchThreadsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientPrefetchThreadsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e49f187f42f5a1cfaafc99ef1c6d5a4ebd326b8eed13beb1cacc93b2d4adbaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersClientPrefetchThreadsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954bfda998f93ce9e7be464fa5001d9ff756901d82741ec5f9fbe66c5e3bfa0e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersClientPrefetchThreadsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef3f85c127f5a81eb9c9eb923e8286f2c188370ed6ac02f9eeb8016331b93dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19e57fbdcf986f7529d67e887a62aabd25920726105c1c3e17e76baadc05aade)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0c336a5f3bb24a369f00cbbe59c835f3e0e8d1dd3920943e785193df22da3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientPrefetchThreadsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientPrefetchThreadsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__220a11ffd82a7e71ef7d325700c7f931c9feb46cb18848593f4f30bdc86efb76)
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
    ) -> typing.Optional[LegacyServiceUserParametersClientPrefetchThreads]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersClientPrefetchThreads], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersClientPrefetchThreads],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1904adfbaa229f167dfa36a288d9f5e9b9bc96a36b058e5ab435be8afbcf4de9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientResultChunkSize",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersClientResultChunkSize:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersClientResultChunkSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersClientResultChunkSizeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientResultChunkSizeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4300d9a164547a3a1a7ac1199c3bcd9af2c80e2997443cae161909f7e35d84d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersClientResultChunkSizeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc82c480141e59d2092cffed99f3e69f2057dc5527114d1df879a5201514f127)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersClientResultChunkSizeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57aaf7f7ffe606e3b26fdf1d6c8d2221c6590a1a486cc4c915e314bea40748e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__620ea4e27ce6d07b4ee6da7d9b83df9398a32db433f6a1e5725fd143e2ace052)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83357d086249aebff94f3062e628b104908a82372b4c59b14ad003e68d12cee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientResultChunkSizeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientResultChunkSizeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d29bdd326aafd564e080ea1f81ffdde4c2490ea29248e7c491d635276660c784)
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
    ) -> typing.Optional[LegacyServiceUserParametersClientResultChunkSize]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersClientResultChunkSize], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersClientResultChunkSize],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58d89ff4f4d51fd77f354ae8af48bac5c14ecfe6c7b0fa00699ff0f96e190fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientResultColumnCaseInsensitive",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersClientResultColumnCaseInsensitive:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersClientResultColumnCaseInsensitive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersClientResultColumnCaseInsensitiveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientResultColumnCaseInsensitiveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed06a378bab5cc4cf7f784f72f6f474c5996eb39f25a2cf5e470898694651555)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersClientResultColumnCaseInsensitiveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965ea5f78ac0baf1683cfc86d70312f40e32dd6daf8ea4b01459e460dae82888)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersClientResultColumnCaseInsensitiveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2758a6f73dcb8473c899447e98d69d3db2249b802fc90363aafb08905a486ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbccb9396809aa79857d377126ff69d83b32ccbb43e3bad1ef5b3617cce1a78c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__067427e3d7102edc6cf5be2c58d3d0bea25fa624efff35ef05aac6e4813f2484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientResultColumnCaseInsensitiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientResultColumnCaseInsensitiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e16b8b901b7e0796ac0a9dc555f2ad8e549e511c0dc26f2d518cf5b5b95cf9c4)
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
    ) -> typing.Optional[LegacyServiceUserParametersClientResultColumnCaseInsensitive]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersClientResultColumnCaseInsensitive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersClientResultColumnCaseInsensitive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549bebea10f4fcf8819c8fbd38d6481725d9867c8b3f8fcac393640affa113e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientSessionKeepAlive",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersClientSessionKeepAlive:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersClientSessionKeepAlive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequency",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequency:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa92387544457179b3334828315de0f0c5f763b8b1f257ad9e03c700be7fc96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d991f0fc7e86c0d8a71e53e69f197801c2ed53cc0623fa0fa3c1a0aeb3ebb2c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7419c5a9727635471720374f95dee62b2631d66714c0f0f4f21988fe74976270)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8fa84e9e057850c4afed9b642c51d997124555aa45d8d5e766d6607424b17b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a60d39ac0ddff2e8ae5c31083e4857dab001951104b4ce16a40d95ac7511a6f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f25d2bb10c164c2b766a9b66f3b72179b7e97d7e8318f00486db47ca2d1abbdd)
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
    ) -> typing.Optional[LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequency]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab0793869965b0076fa78f1e11a93e6f4e93159bb1129dd4cf9b93e7f4dd717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientSessionKeepAliveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientSessionKeepAliveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a8534651c479554dfdce4e2362072c412b30be26416a6aa5d852212ac676e3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersClientSessionKeepAliveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639dec214740d3eb6b001c40d5d8057d3d465eac1ddf00a607b8d224fa790145)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersClientSessionKeepAliveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbd00a20c8854da970377c77d0416000d640119908800e54e9120d900f14e20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53780811d985ef51a75a9c589cc81011b84b58ca3cd5f9cfb151326e93f74454)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06dfa016e205bbee71c615f5b1fa3f9e68bb1ff0869ed32b7e95bd579478ca04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientSessionKeepAliveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientSessionKeepAliveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c168202021881e6d0fe6ca1c7e2c482c2619e69ab7bbf02d27685f68b36e0c5)
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
    ) -> typing.Optional[LegacyServiceUserParametersClientSessionKeepAlive]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersClientSessionKeepAlive], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersClientSessionKeepAlive],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf53c6cc7245add3298a9e69e9e2baa795b2632db91ce911514ad5fc165d7699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientTimestampTypeMapping",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersClientTimestampTypeMapping:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersClientTimestampTypeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersClientTimestampTypeMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientTimestampTypeMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8512c189fd148404d6e39b44dae51b09449c54874c901f057ca323eb31c1a9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersClientTimestampTypeMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44655430ff54e53cf105e263048f5f676f7571506ea3b805d23a3218a49f6123)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersClientTimestampTypeMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dee515b8b0e5bc045507feab10e115431732a10f5c20ea4f18fcc0c32b94b75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a90904bfa4b9e68b322ff5d06b24517cb314e90f9baf7d2ab5682ef75078d28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab23b692a09d061d260549cc39690af79ab595c44aa698f707e290b63090668c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersClientTimestampTypeMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersClientTimestampTypeMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__552efec8759f33d284b0a25ffb5cd7efd0b4e2446e930403e3d33ac8025d9731)
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
    ) -> typing.Optional[LegacyServiceUserParametersClientTimestampTypeMapping]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersClientTimestampTypeMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersClientTimestampTypeMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8e2e8ae803a81d9b8d98379b583b76d351ab57b927770a90edf889b5c81fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersDateInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersDateInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersDateInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersDateInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersDateInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ab949c127d40db2dae8e1c54efdcd7d412becfbf22034c875ad54b95f78b354)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersDateInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b169443e177dfa1d618f1a7d16187f0fd0683d8e665ae01c70fffc696f094d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersDateInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59dab0585a40fab56ddc77b03caf7fbee5d49ee08e4b2fcbe0db9ecae025b8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcbf3f249ed41b03b8e7e6a51abe3142b852b6da658a1be1f2fa5660d88b1c93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__358c9aa714d3a554bf611a2589bfd8bc7fe6a6907559d8689fa2fd7c2bb0c1ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersDateInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersDateInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6dfefe66bad398e38550119298584da17cb89e72954b462f0d50315fc3007cd)
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
    ) -> typing.Optional[LegacyServiceUserParametersDateInputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersDateInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersDateInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b12946abe65b82a4539ac6d84f0e98b849a0c4576e03f1a68b1b30b1edff76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersDateOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersDateOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersDateOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersDateOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersDateOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6892e6c9e77ea3a03bfb87fde0ce62ca28ae211824a7deb8c42ec6a14012b9b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersDateOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980d1d86201cca4fbd941b39febe016c35022386e259c2e20dcdd41e85b4bcd8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersDateOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271f8f1e5cf9595274d6f6ee29bdcac83ba55db41bbc385b879dbd7cdd195273)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0af822b49afef2fdca888e829ded1eb55f3eb25ef0ca07fa46926caeb3a8f5bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bc0658d8be5c61f74763189946059e1f47456385a5ab17e98067f36f08eacdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersDateOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersDateOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f516bd11c74238f3cb55cf0e326133011df0b7ba8f0b5b50177c6b110f452e1)
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
    ) -> typing.Optional[LegacyServiceUserParametersDateOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersDateOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersDateOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80d91bbeef8b0cc8ae117d49b3ffbcda4af0d8cffd33496609f8bff19ea58d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimization",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimization:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1acdf2cc91ec12903cd00b7b1879092870023f9e17fa695c315a6ca657b66e83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e193a1212bda498aa13e0dbd4990a1a6332469584b9520bb2e5aae12bcdbf629)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8af5641e4741c2669c8c4cf0f33f5938a6fb8e1a207c54c91663cef61fc1ec1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00b7041c26f2540bc80129605afd7d0c71804e486474215a73fe2d04d0f82871)
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
            type_hints = typing.get_type_hints(_typecheckingstub__745d4af4775863d29a0cdf9a21e92781a2131725bdf532ae7f7f1df9bea2dd7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0abf9c83fdf383c4a60e5f717e57912a75af64136a408a3f26a12bc1d25e18b)
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
    ) -> typing.Optional[LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimization]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1043a83bafa947255d413c88f16f95d6296626e404301fc87e36a659bed56763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersEnableUnredactedQuerySyntaxError",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersEnableUnredactedQuerySyntaxError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersEnableUnredactedQuerySyntaxError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18496854d6c6dd85be6cd136cce25a592958c183f9e055f574840314225c767c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc4c84570b8985a5257e62f4ef2a8106ab3b5632bf47d183e33689934d88f5e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126634f7c7b33cc63c5b0c38f273e68df1eb1cd810c8a478d86e90d9f943e4a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1aa88b9526872b885d22e34e59c5b078a3b8a230b181565c73dd2e536af6978)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e25d48fd1983b4de70410e94f1c603f6991e6cdea97704db77b0a98c2d069c61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52792bbf47d41d1e4151c107c6b13d38e0bf7b44c9d20fa2b51fd224da36dc01)
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
    ) -> typing.Optional[LegacyServiceUserParametersEnableUnredactedQuerySyntaxError]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersEnableUnredactedQuerySyntaxError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersEnableUnredactedQuerySyntaxError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4660e3cacee3964dfdf72760e43be88bd046232629123e4c552747695c18a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersErrorOnNondeterministicMerge",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersErrorOnNondeterministicMerge:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersErrorOnNondeterministicMerge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersErrorOnNondeterministicMergeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersErrorOnNondeterministicMergeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91e9c2f0fe77a18453195dbe9f1c7bfb8b844a7966a321c28d72efb1d66b6e35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersErrorOnNondeterministicMergeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a1103a7a911befab9cbaabfb9d6b8c850c8dcdf162b5975ed0bdc08da935d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersErrorOnNondeterministicMergeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607e918278c453fa068564a2f14f54c0751db6f65100838c2584ba2434f9d847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf35483f3b690723a811fde09d07bc64b6c1660b27d167b88fc45a5ac23420da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__add326b4dbe6bd3cf01f9b50c59ea1401c3bd194eef5111855cfddc84e5766f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersErrorOnNondeterministicMergeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersErrorOnNondeterministicMergeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3840a06fb610e6ac121d3bcb183d3c5aca31637de7f11d8e43b0546e806af448)
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
    ) -> typing.Optional[LegacyServiceUserParametersErrorOnNondeterministicMerge]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersErrorOnNondeterministicMerge], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersErrorOnNondeterministicMerge],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fb8bd339ba8787d13e29766dbd511fe0ab9fdf87d64e90a573ece190063b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersErrorOnNondeterministicUpdate",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersErrorOnNondeterministicUpdate:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersErrorOnNondeterministicUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersErrorOnNondeterministicUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersErrorOnNondeterministicUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d03fdedf408220f23155f0f19745f6f1fc0acf8b8af4f1f6a737b71116cab55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersErrorOnNondeterministicUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b1e65514ac6146eaaa6be129771512e604531f522f07a980f133b11da40add)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersErrorOnNondeterministicUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0944318f6f2659e495d1150c0939e2cf587ffb58db591b6218cfd297bfaab79d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03e0e78cb63267cc6530953983952e47d14f4a60732a6d8ef94bd771790e4c4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e7daabca7d0f4ffeedc217538afb70199192364a09f3e39b4c427e84f5bbd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersErrorOnNondeterministicUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersErrorOnNondeterministicUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ad559a30692fa010e832b09bb2af561e33a541b97c4489a27847472459a4269)
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
    ) -> typing.Optional[LegacyServiceUserParametersErrorOnNondeterministicUpdate]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersErrorOnNondeterministicUpdate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersErrorOnNondeterministicUpdate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb3695d81e36aa5817a6eb1407120468a29de1ea56a90e864ed9fb80daa9448)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersGeographyOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersGeographyOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersGeographyOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersGeographyOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersGeographyOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d703ae6e2bf47fd3fff74f236658ac9af56d18b441e7d59e425ad1f98cd67a39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersGeographyOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704da61ff9a2ca405af0cbe4913df8e404e4780d285e26f9245f4f8e87045ead)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersGeographyOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854729c862f26c521601582af315e26ca08849610d6dea0af39453fa9b53420b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2def515991816019282a0ae59e741eae2bb02f74077eac1814204501db741ac5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd0b31d2e9d508e2bad817c08a5575174f54fc65666ee7cc89988ddaf84f7d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersGeographyOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersGeographyOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__377f397de1453e167cab79b09ffaad8c85ca5e1785d5c0dc73c411f0ff2dc2a1)
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
    ) -> typing.Optional[LegacyServiceUserParametersGeographyOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersGeographyOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersGeographyOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2af6c8f3fb8304c2433e125bb3d1241fd07cbf4a4dc0ca2ac610ff5d0a3d24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersGeometryOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersGeometryOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersGeometryOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersGeometryOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersGeometryOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f6a9621d1f8da56e16ed6d4a26f20192c4f56218e6823511f7b380862773e24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersGeometryOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5562b97dfe711be08b146ecc70b8fa5ee74b9e89035721cbf6e5c46530497b6b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersGeometryOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8b9ea059b5730711a72d92909dd3c464cd281c71c5973c8a5b56c4a9f2a15e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22287d22135cfe7019b4062212255baf7c15d0286cced61c271b3a766a3fbd24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8686a3c8814e4577a5f1e08a80affd5e8c15bcf2101474c70abc8526306c80b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersGeometryOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersGeometryOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__681306b86b5aa4f9287ad112ad5177e4ed62972d04e91ef7b13cfd0096ee2318)
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
    ) -> typing.Optional[LegacyServiceUserParametersGeometryOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersGeometryOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersGeometryOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266f7c130cadaa2a23d68cf6f882ddf3bfa4f90e64da54b9d33464779c0adb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcTreatDecimalAsInt",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersJdbcTreatDecimalAsInt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersJdbcTreatDecimalAsInt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersJdbcTreatDecimalAsIntList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcTreatDecimalAsIntList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2082183996b5f56676cd3fb053ab81d93c4b73b9629deeaace6c81fab823f62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersJdbcTreatDecimalAsIntOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c79c738a3975dbafc7b8ed03cb0dd293d006eb1abf2b6c2c3238d02cf39ba58)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersJdbcTreatDecimalAsIntOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcb99e0f113fd52554d0916c2f21ef363336866dc0d3e1a963b9023bc53d3a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bc4a15360160f9b4fb6b66c934a79412089fd30c6cad6f3f6bfa4bf295923c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb00711414709d6ce3b1f72c7d08df1c080060ec2171ec7ad9bd631bfb40c389)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersJdbcTreatDecimalAsIntOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcTreatDecimalAsIntOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73d7ef8ccbaf670a8d632822e9e081bebdd02521feb3ae1b0068504328fc9d75)
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
    ) -> typing.Optional[LegacyServiceUserParametersJdbcTreatDecimalAsInt]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersJdbcTreatDecimalAsInt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersJdbcTreatDecimalAsInt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a733906fec86df3275c2809d25b14097af2a952e338aea8d3f99d9d3ee37e3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtc",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtc:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e1673a1f8a62678ace9efd8133cc0c2e463db8e3063825a42788a951573c1a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad65303a0a2918527db6a0061b4c0bb9c8b9d6018c03d83aaeb7d895f805d3f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6154781df6d001d118fa36fcee7b86645857e732398f794ea1176c2c61110b74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81571d4eb4e21a61efe9fc347eb43c3d784ac291cea975cc1b1ba0f57e29e2ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcc73963df15987ba614c03bbda1faa81507e90a3dede00e34597c17e019dbde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c6e2a7fffb691a68dc7f9375e29fd3db0584aa9b46695c811a26a5dc6fccc8c)
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
    ) -> typing.Optional[LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtc]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d0e1ae4d0abea8bad75f0a7b850106eb5c33bcddd5bd42697e51707676bcf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcUseSessionTimezone",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersJdbcUseSessionTimezone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersJdbcUseSessionTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersJdbcUseSessionTimezoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcUseSessionTimezoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c63401b8fba4723b534885778df469a9a8a4c64c50e269c5f2660e723b964c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersJdbcUseSessionTimezoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4187eb00922c8a3ea8e3086e4e39c6423dc952ead5a5377206f867185eb6ad3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersJdbcUseSessionTimezoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f140e50c7ae532966b1359f5c527792f6bcd9a1bbc64dc2b7bf15d22b39e051)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9987f82b2321055377cee69e2ac86e85ac58a42fe9b84680a55d59a2424c06b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2461ef9539fcf9f676c7910ac77704db73300d92cb0d076d1b4ebb84dbacf38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersJdbcUseSessionTimezoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJdbcUseSessionTimezoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22beaa8ca94ea8e26361f953bf47c423fb0fac8b3f0905366256fb3f78e36594)
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
    ) -> typing.Optional[LegacyServiceUserParametersJdbcUseSessionTimezone]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersJdbcUseSessionTimezone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersJdbcUseSessionTimezone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa53d3c66e3274159e934be44f85e7c968f35b986d5191a55e7600212ac6bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJsonIndent",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersJsonIndent:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersJsonIndent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersJsonIndentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJsonIndentList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5791d3b04c426c469d5d9351a8bab401c4e59c5778271d15ea2565789a793c62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersJsonIndentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d8a480bab874b90795fefadd417e634cb30f6a077bb02087e506d5fa384d4d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersJsonIndentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06bcb9ed9186546b01b372051ae230a4360dc5b81b6d09f2a4a9ad44e0c4a37e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__796683a57aefc654c5b84316ae376fefd26557eec1f6a561e94cdc29c7a85425)
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
            type_hints = typing.get_type_hints(_typecheckingstub__908c0db80073669d29291a222cad838c5be6eb6b97931ce37ccaf0d5e7a2ddd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersJsonIndentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersJsonIndentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6637a9ff60b9d5cfda76d9a8aece24df1279670be45bc1e984d68771f20aab0c)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersJsonIndent]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersJsonIndent], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersJsonIndent],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5c9bdf42fe6c9e318272cc3e9b9649427d103dd2fce97963550927fea44681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd54b9808ab5e13658de7e44cf61b87deda13337a6d7c6e77ae983615f622186)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LegacyServiceUserParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ab06fb235bf180c3f1316601b9c23bbb4aa9fbcd2dc207cb2c9b019c94b328)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afa72e7dc731078fbdedf56683078b243b27dd830d69d3159af590462af59f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20acbcf24d57a93630af0d216aeadf2bf0fecea4629400c791730df4f5b2f384)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8618bd924e15b74a6a3e44d6a128a824dfff373c941caa8f203492aaea27777f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersLockTimeout",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersLockTimeout:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersLockTimeout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersLockTimeoutList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersLockTimeoutList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6772d7bd2a57a9ae6c8411d69b1445c363cf95344d0a4a1698a4cb2b48595ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersLockTimeoutOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34c1f8a4040ba8af3bd419592e8e8726770d6e3d307276611028e0d9fb4aec3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersLockTimeoutOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c1e0ffe136c313f83762579eaeda655d87a1dfca197cb5fb6052a74122a938)
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
            type_hints = typing.get_type_hints(_typecheckingstub__085cfa786aa13edc76619e5a01ff39e4832571f2a0fe0ef7481d6b1924dcb651)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8759949569667e5d5f11d10532f491bd3829e766bb8c2b03606cbef3b999a1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersLockTimeoutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersLockTimeoutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a3cea037897770a7318a8a06dc7f9b946bd4765ea90ee22bfcf853c61f47705)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersLockTimeout]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersLockTimeout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersLockTimeout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6eb5cb718ff1a8de01a9149a2b089aa2b8016a4237adb7316ecb5b75fafa737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3c78ca2aff4b8710e5760820c3e26536fa279c556acd1081a42032b8428ede2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8810021b7343905eb02293af3c43b477f81b6399cf2a5bb1969c0efdaaa9d911)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3001fecf16ea2f905dc0c3042832dfb34050822a3c937414ac06c1631389ee4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3653dee1d59d4e2da3f0b6dea19ed761d625ae77c892a4a7d1cbc08cf7443dd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__209f874ea92bbf8a409ece9fcd583c87c086e2864a6343d9dc2aff622ac0b0f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__707bc2e1910e914503ee15257d07f3111f530c74142b0f730a2e0f056f537460)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersLogLevel]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersLogLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae2625092c75d878a7f68505afbf55b319208cc69be20592250765e9d8ded4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersMultiStatementCount",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersMultiStatementCount:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersMultiStatementCount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersMultiStatementCountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersMultiStatementCountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0dee22f54e78f734832466e030094679a514b7c3fa83cc82a6ca060321de577)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersMultiStatementCountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1cc6f160f181a373df6dd064e79db07b6514d2aee53f7c34aff8f7774229c43)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersMultiStatementCountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b68daf241066e51dc1a96ef61cba359456df04082c1e64477a8db186548d9681)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9e885e140439f308521f0bbccfcbea8a50b4cdc83adb66c87f9ace9d7bd07d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74da12ecc0a86a98786621af6d6ae82aee4a103893dae32eed6c927c9bc36345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersMultiStatementCountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersMultiStatementCountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__226cf64f34d0a74b3f76a6b393713723b3d4caf8d2c4c61c2e1fa730bfab7d0b)
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
    ) -> typing.Optional[LegacyServiceUserParametersMultiStatementCount]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersMultiStatementCount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersMultiStatementCount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9411d15a3548503dda232ea4a3dbd1355c79292da4467099621adfa29d1449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersNetworkPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersNetworkPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersNetworkPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersNetworkPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersNetworkPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32435ed288eff0f07eaa971204c734c7a4a936e512243ce4b4870654bf4b4157)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersNetworkPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485cf19134473b5cdcdefa99b71c6b05af14774398e5f912951caafd835b00e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersNetworkPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21d34aec9229d337b8de9f94404a75eb2e6cc9db19a569366129920183bc3f00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__380baf0b3e4a13cb36d13aa1eb704fd088712520daf50bfb2482bb6e32dfe614)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f46a18a7e5245deaf863d708cd81d067d95058d7344bc16473bd0b732f358790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersNetworkPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersNetworkPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__043c4c82a51875951980d317b1a09e469f12e18ac973b865ec18e48249d3f67e)
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
    ) -> typing.Optional[LegacyServiceUserParametersNetworkPolicy]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersNetworkPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersNetworkPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a93c8f290b0f82a38ce2fcf1790c594610c0d939b8136551b0168f0f91d2b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersNoorderSequenceAsDefault",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersNoorderSequenceAsDefault:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersNoorderSequenceAsDefault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersNoorderSequenceAsDefaultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersNoorderSequenceAsDefaultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0b8219ac361368092b5155b5566dfbcb984ea624f662e24c5762efce04c9d8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersNoorderSequenceAsDefaultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8661f38924ae3470d0bfab9eae168ed0c68ab095abf2b5eef04c43057c7673ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersNoorderSequenceAsDefaultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecad989a9b5d75804877bdc2c7d9e41b8931810f601b2b0eaad379ea0da243cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89a9f7819071d6be6cfde2b3e0c6f11a417610563026c25df005366012354050)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d3bef1fef3171cd0073667b8127a686e96050071384cfe56b64b866aaee7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersNoorderSequenceAsDefaultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersNoorderSequenceAsDefaultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb47c253da852dd0d4941c4f1fd0ce0c761c3cf3462067c470200064713b4f9b)
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
    ) -> typing.Optional[LegacyServiceUserParametersNoorderSequenceAsDefault]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersNoorderSequenceAsDefault], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersNoorderSequenceAsDefault],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d50412ce1221e99d2ddb5f12d42100f682720a40a045a9b0bebd221fa28108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersOdbcTreatDecimalAsInt",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersOdbcTreatDecimalAsInt:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersOdbcTreatDecimalAsInt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersOdbcTreatDecimalAsIntList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersOdbcTreatDecimalAsIntList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d74d59ae53b7c3c7b6cc37945269c245eee1f9b2e7783455aa3ff580b3e53eb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersOdbcTreatDecimalAsIntOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e201b2c8e6fe93be614b05cb29096080538a43f50dc454b3656e8d727930776)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersOdbcTreatDecimalAsIntOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9df8d0efcd0cf7f8c37fbf9d4724ef8e746e2ae0d2345beb9cf4bdfe0d0750)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfbc1bb11bf62a721c87c9f4be7983801d1d7599f970d02b2fb4590cafe9b4c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e57cbd35d23655ccfdd1d57a60c68614d1efcdf0b84a9bda0d07f4b7561ba02d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersOdbcTreatDecimalAsIntOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersOdbcTreatDecimalAsIntOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a1d0f391459047f7d9e8fd5a6f9424a003dc16e81f7c5f5a997ca7d5d41d39b)
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
    ) -> typing.Optional[LegacyServiceUserParametersOdbcTreatDecimalAsInt]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersOdbcTreatDecimalAsInt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersOdbcTreatDecimalAsInt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c293933d5af6118a7e8af19fb485e94f09d537a98d5d2835340cf80bf758e918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__318c55afd48f042a831927a19de49175807f3fd0ff1fc83761ea7aaa6586603d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="abortDetachedQuery")
    def abort_detached_query(self) -> LegacyServiceUserParametersAbortDetachedQueryList:
        return typing.cast(LegacyServiceUserParametersAbortDetachedQueryList, jsii.get(self, "abortDetachedQuery"))

    @builtins.property
    @jsii.member(jsii_name="autocommit")
    def autocommit(self) -> LegacyServiceUserParametersAutocommitList:
        return typing.cast(LegacyServiceUserParametersAutocommitList, jsii.get(self, "autocommit"))

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> LegacyServiceUserParametersBinaryInputFormatList:
        return typing.cast(LegacyServiceUserParametersBinaryInputFormatList, jsii.get(self, "binaryInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> LegacyServiceUserParametersBinaryOutputFormatList:
        return typing.cast(LegacyServiceUserParametersBinaryOutputFormatList, jsii.get(self, "binaryOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> LegacyServiceUserParametersClientMemoryLimitList:
        return typing.cast(LegacyServiceUserParametersClientMemoryLimitList, jsii.get(self, "clientMemoryLimit"))

    @builtins.property
    @jsii.member(jsii_name="clientMetadataRequestUseConnectionCtx")
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxList:
        return typing.cast(LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxList, jsii.get(self, "clientMetadataRequestUseConnectionCtx"))

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(
        self,
    ) -> LegacyServiceUserParametersClientPrefetchThreadsList:
        return typing.cast(LegacyServiceUserParametersClientPrefetchThreadsList, jsii.get(self, "clientPrefetchThreads"))

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(
        self,
    ) -> LegacyServiceUserParametersClientResultChunkSizeList:
        return typing.cast(LegacyServiceUserParametersClientResultChunkSizeList, jsii.get(self, "clientResultChunkSize"))

    @builtins.property
    @jsii.member(jsii_name="clientResultColumnCaseInsensitive")
    def client_result_column_case_insensitive(
        self,
    ) -> LegacyServiceUserParametersClientResultColumnCaseInsensitiveList:
        return typing.cast(LegacyServiceUserParametersClientResultColumnCaseInsensitiveList, jsii.get(self, "clientResultColumnCaseInsensitive"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAlive")
    def client_session_keep_alive(
        self,
    ) -> LegacyServiceUserParametersClientSessionKeepAliveList:
        return typing.cast(LegacyServiceUserParametersClientSessionKeepAliveList, jsii.get(self, "clientSessionKeepAlive"))

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList:
        return typing.cast(LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(
        self,
    ) -> LegacyServiceUserParametersClientTimestampTypeMappingList:
        return typing.cast(LegacyServiceUserParametersClientTimestampTypeMappingList, jsii.get(self, "clientTimestampTypeMapping"))

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> LegacyServiceUserParametersDateInputFormatList:
        return typing.cast(LegacyServiceUserParametersDateInputFormatList, jsii.get(self, "dateInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> LegacyServiceUserParametersDateOutputFormatList:
        return typing.cast(LegacyServiceUserParametersDateOutputFormatList, jsii.get(self, "dateOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="enableUnloadPhysicalTypeOptimization")
    def enable_unload_physical_type_optimization(
        self,
    ) -> LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationList:
        return typing.cast(LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationList, jsii.get(self, "enableUnloadPhysicalTypeOptimization"))

    @builtins.property
    @jsii.member(jsii_name="enableUnredactedQuerySyntaxError")
    def enable_unredacted_query_syntax_error(
        self,
    ) -> LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorList:
        return typing.cast(LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorList, jsii.get(self, "enableUnredactedQuerySyntaxError"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicMerge")
    def error_on_nondeterministic_merge(
        self,
    ) -> LegacyServiceUserParametersErrorOnNondeterministicMergeList:
        return typing.cast(LegacyServiceUserParametersErrorOnNondeterministicMergeList, jsii.get(self, "errorOnNondeterministicMerge"))

    @builtins.property
    @jsii.member(jsii_name="errorOnNondeterministicUpdate")
    def error_on_nondeterministic_update(
        self,
    ) -> LegacyServiceUserParametersErrorOnNondeterministicUpdateList:
        return typing.cast(LegacyServiceUserParametersErrorOnNondeterministicUpdateList, jsii.get(self, "errorOnNondeterministicUpdate"))

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(
        self,
    ) -> LegacyServiceUserParametersGeographyOutputFormatList:
        return typing.cast(LegacyServiceUserParametersGeographyOutputFormatList, jsii.get(self, "geographyOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(
        self,
    ) -> LegacyServiceUserParametersGeometryOutputFormatList:
        return typing.cast(LegacyServiceUserParametersGeometryOutputFormatList, jsii.get(self, "geometryOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatDecimalAsInt")
    def jdbc_treat_decimal_as_int(
        self,
    ) -> LegacyServiceUserParametersJdbcTreatDecimalAsIntList:
        return typing.cast(LegacyServiceUserParametersJdbcTreatDecimalAsIntList, jsii.get(self, "jdbcTreatDecimalAsInt"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTreatTimestampNtzAsUtc")
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcList:
        return typing.cast(LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcList, jsii.get(self, "jdbcTreatTimestampNtzAsUtc"))

    @builtins.property
    @jsii.member(jsii_name="jdbcUseSessionTimezone")
    def jdbc_use_session_timezone(
        self,
    ) -> LegacyServiceUserParametersJdbcUseSessionTimezoneList:
        return typing.cast(LegacyServiceUserParametersJdbcUseSessionTimezoneList, jsii.get(self, "jdbcUseSessionTimezone"))

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> LegacyServiceUserParametersJsonIndentList:
        return typing.cast(LegacyServiceUserParametersJsonIndentList, jsii.get(self, "jsonIndent"))

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> LegacyServiceUserParametersLockTimeoutList:
        return typing.cast(LegacyServiceUserParametersLockTimeoutList, jsii.get(self, "lockTimeout"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> LegacyServiceUserParametersLogLevelList:
        return typing.cast(LegacyServiceUserParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(
        self,
    ) -> LegacyServiceUserParametersMultiStatementCountList:
        return typing.cast(LegacyServiceUserParametersMultiStatementCountList, jsii.get(self, "multiStatementCount"))

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> LegacyServiceUserParametersNetworkPolicyList:
        return typing.cast(LegacyServiceUserParametersNetworkPolicyList, jsii.get(self, "networkPolicy"))

    @builtins.property
    @jsii.member(jsii_name="noorderSequenceAsDefault")
    def noorder_sequence_as_default(
        self,
    ) -> LegacyServiceUserParametersNoorderSequenceAsDefaultList:
        return typing.cast(LegacyServiceUserParametersNoorderSequenceAsDefaultList, jsii.get(self, "noorderSequenceAsDefault"))

    @builtins.property
    @jsii.member(jsii_name="odbcTreatDecimalAsInt")
    def odbc_treat_decimal_as_int(
        self,
    ) -> LegacyServiceUserParametersOdbcTreatDecimalAsIntList:
        return typing.cast(LegacyServiceUserParametersOdbcTreatDecimalAsIntList, jsii.get(self, "odbcTreatDecimalAsInt"))

    @builtins.property
    @jsii.member(jsii_name="preventUnloadToInternalStages")
    def prevent_unload_to_internal_stages(
        self,
    ) -> "LegacyServiceUserParametersPreventUnloadToInternalStagesList":
        return typing.cast("LegacyServiceUserParametersPreventUnloadToInternalStagesList", jsii.get(self, "preventUnloadToInternalStages"))

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> "LegacyServiceUserParametersQueryTagList":
        return typing.cast("LegacyServiceUserParametersQueryTagList", jsii.get(self, "queryTag"))

    @builtins.property
    @jsii.member(jsii_name="quotedIdentifiersIgnoreCase")
    def quoted_identifiers_ignore_case(
        self,
    ) -> "LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseList":
        return typing.cast("LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseList", jsii.get(self, "quotedIdentifiersIgnoreCase"))

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> "LegacyServiceUserParametersRowsPerResultsetList":
        return typing.cast("LegacyServiceUserParametersRowsPerResultsetList", jsii.get(self, "rowsPerResultset"))

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(
        self,
    ) -> "LegacyServiceUserParametersS3StageVpceDnsNameList":
        return typing.cast("LegacyServiceUserParametersS3StageVpceDnsNameList", jsii.get(self, "s3StageVpceDnsName"))

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> "LegacyServiceUserParametersSearchPathList":
        return typing.cast("LegacyServiceUserParametersSearchPathList", jsii.get(self, "searchPath"))

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumer")
    def simulated_data_sharing_consumer(
        self,
    ) -> "LegacyServiceUserParametersSimulatedDataSharingConsumerList":
        return typing.cast("LegacyServiceUserParametersSimulatedDataSharingConsumerList", jsii.get(self, "simulatedDataSharingConsumer"))

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(
        self,
    ) -> "LegacyServiceUserParametersStatementQueuedTimeoutInSecondsList":
        return typing.cast("LegacyServiceUserParametersStatementQueuedTimeoutInSecondsList", jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(
        self,
    ) -> "LegacyServiceUserParametersStatementTimeoutInSecondsList":
        return typing.cast("LegacyServiceUserParametersStatementTimeoutInSecondsList", jsii.get(self, "statementTimeoutInSeconds"))

    @builtins.property
    @jsii.member(jsii_name="strictJsonOutput")
    def strict_json_output(self) -> "LegacyServiceUserParametersStrictJsonOutputList":
        return typing.cast("LegacyServiceUserParametersStrictJsonOutputList", jsii.get(self, "strictJsonOutput"))

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> "LegacyServiceUserParametersTimeInputFormatList":
        return typing.cast("LegacyServiceUserParametersTimeInputFormatList", jsii.get(self, "timeInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> "LegacyServiceUserParametersTimeOutputFormatList":
        return typing.cast("LegacyServiceUserParametersTimeOutputFormatList", jsii.get(self, "timeOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampDayIsAlways24H")
    def timestamp_day_is_always24_h(
        self,
    ) -> "LegacyServiceUserParametersTimestampDayIsAlways24HList":
        return typing.cast("LegacyServiceUserParametersTimestampDayIsAlways24HList", jsii.get(self, "timestampDayIsAlways24H"))

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(
        self,
    ) -> "LegacyServiceUserParametersTimestampInputFormatList":
        return typing.cast("LegacyServiceUserParametersTimestampInputFormatList", jsii.get(self, "timestampInputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(
        self,
    ) -> "LegacyServiceUserParametersTimestampLtzOutputFormatList":
        return typing.cast("LegacyServiceUserParametersTimestampLtzOutputFormatList", jsii.get(self, "timestampLtzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(
        self,
    ) -> "LegacyServiceUserParametersTimestampNtzOutputFormatList":
        return typing.cast("LegacyServiceUserParametersTimestampNtzOutputFormatList", jsii.get(self, "timestampNtzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(
        self,
    ) -> "LegacyServiceUserParametersTimestampOutputFormatList":
        return typing.cast("LegacyServiceUserParametersTimestampOutputFormatList", jsii.get(self, "timestampOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(
        self,
    ) -> "LegacyServiceUserParametersTimestampTypeMappingList":
        return typing.cast("LegacyServiceUserParametersTimestampTypeMappingList", jsii.get(self, "timestampTypeMapping"))

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(
        self,
    ) -> "LegacyServiceUserParametersTimestampTzOutputFormatList":
        return typing.cast("LegacyServiceUserParametersTimestampTzOutputFormatList", jsii.get(self, "timestampTzOutputFormat"))

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> "LegacyServiceUserParametersTimezoneList":
        return typing.cast("LegacyServiceUserParametersTimezoneList", jsii.get(self, "timezone"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "LegacyServiceUserParametersTraceLevelList":
        return typing.cast("LegacyServiceUserParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="transactionAbortOnError")
    def transaction_abort_on_error(
        self,
    ) -> "LegacyServiceUserParametersTransactionAbortOnErrorList":
        return typing.cast("LegacyServiceUserParametersTransactionAbortOnErrorList", jsii.get(self, "transactionAbortOnError"))

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(
        self,
    ) -> "LegacyServiceUserParametersTransactionDefaultIsolationLevelList":
        return typing.cast("LegacyServiceUserParametersTransactionDefaultIsolationLevelList", jsii.get(self, "transactionDefaultIsolationLevel"))

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(
        self,
    ) -> "LegacyServiceUserParametersTwoDigitCenturyStartList":
        return typing.cast("LegacyServiceUserParametersTwoDigitCenturyStartList", jsii.get(self, "twoDigitCenturyStart"))

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(
        self,
    ) -> "LegacyServiceUserParametersUnsupportedDdlActionList":
        return typing.cast("LegacyServiceUserParametersUnsupportedDdlActionList", jsii.get(self, "unsupportedDdlAction"))

    @builtins.property
    @jsii.member(jsii_name="useCachedResult")
    def use_cached_result(self) -> "LegacyServiceUserParametersUseCachedResultList":
        return typing.cast("LegacyServiceUserParametersUseCachedResultList", jsii.get(self, "useCachedResult"))

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> "LegacyServiceUserParametersWeekOfYearPolicyList":
        return typing.cast("LegacyServiceUserParametersWeekOfYearPolicyList", jsii.get(self, "weekOfYearPolicy"))

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> "LegacyServiceUserParametersWeekStartList":
        return typing.cast("LegacyServiceUserParametersWeekStartList", jsii.get(self, "weekStart"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LegacyServiceUserParameters]:
        return typing.cast(typing.Optional[LegacyServiceUserParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4aa41f0d20e83a9162eed7f5c3d5febab650d9cc793138dbcf096c3476ae178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersPreventUnloadToInternalStages",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersPreventUnloadToInternalStages:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersPreventUnloadToInternalStages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersPreventUnloadToInternalStagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersPreventUnloadToInternalStagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ae0416b56862e6400570489b983f4db667f43ac631d4c8d172bbc2042886e34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersPreventUnloadToInternalStagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa59a68b0317b6e15edd9bf04da3b24bc01fe0739bbcd66179a684fb8c460cae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersPreventUnloadToInternalStagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e054435c9e6a7fcaf6b64e02d1799a4be795c985d8319f44510cb682d41e5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a2e4c30b93dca8e277d6d793f25a215a9dfa1c15d9dc64e29013ddd6ee498a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72bb11b0d0e3a5fd84ede46cfe7d411edd357ca61248e2bfcf1153b563952b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersPreventUnloadToInternalStagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersPreventUnloadToInternalStagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40204a3427a8e7eceb6dfba322b9478a4afdbc9f696cf8f44cde113bc7f03820)
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
    ) -> typing.Optional[LegacyServiceUserParametersPreventUnloadToInternalStages]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersPreventUnloadToInternalStages], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersPreventUnloadToInternalStages],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc8a1f6f92cad640bc784a6195ffef9b168da61927a8152039ef9fffe2cf103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersQueryTag",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersQueryTag:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersQueryTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersQueryTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersQueryTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e9e482f465327e16ae0ec3554845618407e0d5978e557afac83af6336c455df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersQueryTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c723f13b0b9e01a42921ebca2d90f286a5d261355ec6b57e098e42a778d0a0a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersQueryTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978aa977cdef7b1c6d982521dca811f0db77b78ba5160606c7a8bf06dd5b3c75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd89ced9b83782873d86f7476c066eb67ebe7229274554ad3b90bc8a63de3f9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52dd5bec38e64a6974ae5ca24f2f15a140272ee5e2decf92192db54da6b1f1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersQueryTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersQueryTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b961b9efc6990fb913caab0e378658fafb7d28e74a6dd232a1c5397f04d3dd24)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersQueryTag]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersQueryTag], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersQueryTag],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39be3a642469384b14ee5837cd1f2df4ee7643de292077e0bb09738ebde2c784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersQuotedIdentifiersIgnoreCase",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersQuotedIdentifiersIgnoreCase:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersQuotedIdentifiersIgnoreCase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b5f4e297c4423f691494f7fdb007c76e4b21910e314c3ee59d379ac1ccd1093)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9e9a47de1d9625c68a29f8f15d884df57f68611e46efff90c6fc63772ffd65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0882761ab19e6b0e4655113d2d25d6ebaf06414b36e84588878378e09f607b58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c32f07a00c4f1712baaab3410d532afdb54feedf678b8b6efa153458f2600d73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c4a9134433653ebd9cbfbaa6918d5f050e958e1110a16ce1ad46b826865d4a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b53d4aa3a8dc9d2df95ba2c200d12a01b228d474636494784fb318f1acdbad1)
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
    ) -> typing.Optional[LegacyServiceUserParametersQuotedIdentifiersIgnoreCase]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersQuotedIdentifiersIgnoreCase], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersQuotedIdentifiersIgnoreCase],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924494282a899631f02f52074bf02df90701950cd33729ba5ab506d9c445ace7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersRowsPerResultset",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersRowsPerResultset:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersRowsPerResultset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersRowsPerResultsetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersRowsPerResultsetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49fb20a1e0d001449650f61a81712e7ac9f8c24c0c72c4bfb926b94f0788628b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersRowsPerResultsetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3570afdd6ed312cf822b10181c810d05d794da53642b8c278ddaf6d11619e5fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersRowsPerResultsetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__354d94021b21ab8e04d23c9cfb327360e1264e1e19cc4d14d20e654dbd419ccf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f29448960c39d6e7f3f14ff006ec6501527dff025d46bd17a15510dd5efe7712)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc8f71c2d16d4db6cb7ca2630d8e1678ff9e2d63ad242ee323abc3aececd6932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersRowsPerResultsetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersRowsPerResultsetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eac0ff3c2384caaf14f1a93cc8b7adba8d3c1c517ac12fd260eb8ad5fb4ef8ac)
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
    ) -> typing.Optional[LegacyServiceUserParametersRowsPerResultset]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersRowsPerResultset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersRowsPerResultset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96bdf2775ab60e48baa344413765d53a14d7ee86e1ceb6042bab7bc0babda920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersS3StageVpceDnsName",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersS3StageVpceDnsName:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersS3StageVpceDnsName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersS3StageVpceDnsNameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersS3StageVpceDnsNameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e291046cb66a00e0e1b334b1273b910eec22458e468a8c3daef8446ee0134051)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersS3StageVpceDnsNameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa242cb2cf2200521262f7fb2113c79a453042c67c5600a54cfa29dd7894e73e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersS3StageVpceDnsNameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea0e740fd0c60422cf80b9d2ecacb9f779f00ea09181a0a2f7488a56d59c8c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a16f52aaf1a412521b068b4d389520b99582406e512c51d7d4c81d01c1cd468)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dee3312552133fde7b4d1f74954d84e367cf9ca63c3089463b49ee3f6dbd574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersS3StageVpceDnsNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersS3StageVpceDnsNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e0b78feca010f51779e1e3df7b3a10d67af81adf5ae34b344f5f39666ffdd3c)
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
    ) -> typing.Optional[LegacyServiceUserParametersS3StageVpceDnsName]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersS3StageVpceDnsName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersS3StageVpceDnsName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69469ae76fa703d6ef416676196e7074161b4bfc7a5df482e8d9ceed20bc461a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersSearchPath",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersSearchPath:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersSearchPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersSearchPathList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersSearchPathList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fef3eae95f4dc27c772cdf5c8527137e8fb964dcf48de730b0db1e99cccae92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersSearchPathOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fec8c072d8038657ca7bbcadb42fc6ada8f90c5c1d1b327e95434448e45f00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersSearchPathOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d1737ecf539af3afaa8236b605d4ef31d1fa3c4027e6b492838f4b05072f91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6e580e7fe547a54e392ca59c8eb96f81f4caf25f2d6ebaf59c570661d889f86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a159dfa9480b17c018c4f0107dbe8ea40002f19b413750b8ac3cd69ff2ed5e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersSearchPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersSearchPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__083c29d4861d75739bdaa5fc0c7960c70ad5dd973038c5f23ec79d8bb45d1225)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersSearchPath]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersSearchPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersSearchPath],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0240e40520e270e90294db1d5ace5f52fc4c89a3341630e4a2d3f544c1652285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersSimulatedDataSharingConsumer",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersSimulatedDataSharingConsumer:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersSimulatedDataSharingConsumer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersSimulatedDataSharingConsumerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersSimulatedDataSharingConsumerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f4fddc4c8959916d3b3d47daa4c57c27ffc144fad028944577ef46c8aa4a8ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersSimulatedDataSharingConsumerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8694f063ab56126b68b58309e294812819159bb09c02a9a574751da065325c92)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersSimulatedDataSharingConsumerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8871b815b938c2140e334ad3bba19b914207d1d82970ae97d4cf74c65091f345)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07010fb3d7f0bb71ae884eb3a2f4bbd7f1fe17940d805865204ca795eddefedb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5758f4667044dbf9445ba91abbadfda964db84ceca50bfa211eeec459eb0e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersSimulatedDataSharingConsumerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersSimulatedDataSharingConsumerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c448ed22983ec7bce0adfb2668d35a317bd120d0c19ea0f45d4af7fef130bb38)
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
    ) -> typing.Optional[LegacyServiceUserParametersSimulatedDataSharingConsumer]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersSimulatedDataSharingConsumer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersSimulatedDataSharingConsumer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071a5ca78bc6b75fd46ccc0c2ed3a0b53fc06bbf10f836f9d7416599366df065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStatementQueuedTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersStatementQueuedTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersStatementQueuedTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersStatementQueuedTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStatementQueuedTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b23c4f5f572e7c85ab16c5a57425082345a0012f7fc5d51953e892d2f2777c6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71038defdc910e2790b0af4eed8653ddfe613af44a15fc1aef661dd289558f42)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0fd068421aeca0c73e6d57c86b67589999521433b33eee71f43a605abf35bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a3abe04b568fc0cdb57b66fee3c16adfaf3baea6210e100fe41d16c37ffcaa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e30cdba06d10c53f7e56643ef86c356f5537bdbf2ff5797e3bf51b35fa68a87b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21591816b28bb614d3d52a8342b21c0e684fad0e14c8fea344b78f24cc8e56e1)
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
    ) -> typing.Optional[LegacyServiceUserParametersStatementQueuedTimeoutInSeconds]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersStatementQueuedTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersStatementQueuedTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef97998bda5864d2a09efeaff82138871c0d3f1407a3d6012a4e509a75b978d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStatementTimeoutInSeconds",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersStatementTimeoutInSeconds:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersStatementTimeoutInSeconds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersStatementTimeoutInSecondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStatementTimeoutInSecondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__480159c20e5abf6a4e4edb92fe3cb649e1b5a5f7f91941ba059596b40bc284d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersStatementTimeoutInSecondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9cc84ae45a7fc31a3584750b08ab23c1d87228f03af852f3576eae6d433d36e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersStatementTimeoutInSecondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad807311c9e4508ba4ce2a18332269b66540fee3884ced18df4b9945152d96b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__073a651936284640440f050d5b41406ea0557b72c07eb62933a608c665ac0cd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a12e4cf6e0a5a1d08169b868469088dac111bbdb42f07a619639d4a1c8a4e947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersStatementTimeoutInSecondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStatementTimeoutInSecondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b33648b7ee6c6834d66d8a326ae2f4b94e6c7cf5c79ea674053471d0bc9b06d)
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
    ) -> typing.Optional[LegacyServiceUserParametersStatementTimeoutInSeconds]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersStatementTimeoutInSeconds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersStatementTimeoutInSeconds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41dd84a2630c950f652db81228b5ac57a2c76633ae032f2beba7b864d0260f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStrictJsonOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersStrictJsonOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersStrictJsonOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersStrictJsonOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStrictJsonOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ff576d8680745404797e279b85d0c479a54df7fd0cc9ddc820e415878b9f51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersStrictJsonOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7885b138718d240e815ba49678de64ab888dc95655f87e2fd246a64d86fcb22)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersStrictJsonOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5232f63716d9b51436c66c9bda51a8dfbd1a9b3397f0ec06671c07954aaa3b55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e63a2ee0926552dbfefd7e7eae7a780f42aa4c71ec7fc8c082f5c55d2fd22d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11e9ba713df1e6c350b33261de19d57a0faf7182ede7929c3a664561f1835b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersStrictJsonOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersStrictJsonOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de66ecfe9e56adfe7dd1f3c185657cdc66f10d872ef7d2b11d5183577b43e70)
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
    ) -> typing.Optional[LegacyServiceUserParametersStrictJsonOutput]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersStrictJsonOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersStrictJsonOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426bf0e3e1ab8949202db778c393c9da90289b982d02b39204f7fdd9c416c319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimeInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimeInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimeInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimeInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimeInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b5c68d56049e4950ac1d61e005655856c388be0d25f47de46fbbc53af9bc92a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimeInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a491f42e6600b875c636bc4ebeba589bc78da7523ab5f0f44ce7f7d274bb8cc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimeInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4a6a3ca748d9c5d253c249ef1fa8a4e1271b2e50c64d9fd8b3a73c0c93f82f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d8545eacd84ae4662d7843db0da7cab3eb0dde338feb54a149ed12c5acb7c5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03cf913db6d35becbcd9b84d129745476d5bc5b9830ef459f9cfb22488494610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimeInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimeInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93c4ea545752615d54aff545d5d3a2656849b02445f7ffc37f4ee04360808a88)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimeInputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimeInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimeInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1884be8bc8025fa49fc2a8f4f4ef58ac2062583475d29275e55d73842f0e3cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimeOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimeOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimeOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimeOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimeOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__422228cb599b3362c489dbd63343542ef0584c23a05ce01aa5050cbf1e369212)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimeOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2fd4aaf803e476bb581ed5faf2a100cf24c45cba42b652a28814903e463e78)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimeOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9d9887839274e2d44ff4b7f61d6cc835acdaf646bb80c6d86db459c1f33dd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f31fded41b4846e35a1dcafc0ebecef4d407d7945121c0c82470b158e2229ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5262892c9aa30fc9a90f418e84268f616e6c87ef739c697bf119b4bf3e8e5db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimeOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimeOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1300837b0e6454bb6b14c3a7255e8496b2045b0c6d499253dbd0b0d8d022af30)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimeOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimeOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimeOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1782ab9e983a012e7117647a748dba2c68b189a0f449875249ea0ebf8b458a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampDayIsAlways24H",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimestampDayIsAlways24H:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimestampDayIsAlways24H(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimestampDayIsAlways24HList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampDayIsAlways24HList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a6300b5a4945916befd280077b4fdc31db4fc7e13126c2841de4196ef69d616)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimestampDayIsAlways24HOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488025d51dca0fb0b59f58f34e46dd52befcc5bf61eb43e2ade4f1f7e04fc3af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimestampDayIsAlways24HOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067e6b646647651ddd5fe721442d9800c28f79f5377ae88f109c9f25dabfbb61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ba559f2d2cc1698bd04e807e91f9b4dbcdef3fa1ecf3f45b907f6c2222720cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__072b044ba6c36e863df70144b3dbd7f077c6f7efc87a8404e17e59883c874d1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimestampDayIsAlways24HOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampDayIsAlways24HOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5d89c585861112ca98a444c19d3364c1e81d91159b567382da2011261739be)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimestampDayIsAlways24H]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimestampDayIsAlways24H], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimestampDayIsAlways24H],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2acf758c1f9d134e8723f0ec714bf62c0795d6eaa6721ee6ad3fc134c7ed73be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampInputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimestampInputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimestampInputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimestampInputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampInputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff66b230915186094502b3f9aaf1f3ef56e506351433a420f08f40bb34671cdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimestampInputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48a8389952d910dbda76551aabc4ab86f43d7c247b400ec7882d97083661a7f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimestampInputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b1b6636ca81eb392827ee41bb735a3a5b47266826992682a07dd3d4edda46b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90a32a2fc44c295d575dd8145b4a9e9ab47a6515ebca6c60baabc7f6b4f65057)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec6266196aed248e2ef181b1ecea6802f6116d324e46cf668c6fe2fdb13462e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimestampInputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampInputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd8026adb1dcbec36a807a7515cf4f0a789c76e3faa3ba50a668bdeae4d01d6b)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimestampInputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimestampInputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimestampInputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__485a4723e84aeb6cd0accb409cc7fa243c58431d01203b33a20b8777f768b980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampLtzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimestampLtzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimestampLtzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimestampLtzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampLtzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__765e7aefcc9c293fca51a342badbf5b81442d197f05b0665f19ae8b4458ac058)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimestampLtzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2799292a394e3d894c035b36299de4136b3051cb9dbc2f8948671593cf5c4d2e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimestampLtzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca38f99cc14fce0f712a5c918f00dc78c553df30d5ca3e956096e03a4a68c923)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0e58a8cda4120a1ca443702564c70a4077115d56e2c580bdf8fd16b1a56ffd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff26bf2272c34e14ebc2af338df117583a72336fcdaa7ef326aa9ef60cc9f4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimestampLtzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampLtzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54438b59f01cc505a1f5f810631789d66e11053330e4775e39727bf1844b3735)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimestampLtzOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimestampLtzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimestampLtzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7693c83b2308a18fc639f73bb2c59bd127b1a62102ed63aa8d8495fb831e9b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampNtzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimestampNtzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimestampNtzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimestampNtzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampNtzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba13d5006f37edb7810e3d1b357fa9f947b7514ec1b4c7710b232a261a46b733)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimestampNtzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6814cd65d233fbca077247c0456baf76f176319e0296bfcde99c34760321b5da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimestampNtzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489ec0c2f4571f1e0f3b3d6d7a38bd234dcb3c7494bf702d4e6360174dd03e75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__def9e33c3e2bb3d2876f2d46c2304977ea35373bd6ab58c9ca42b51c620db30a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c26389fa57c8ff7aea7a030646a046656f1dd1392b2a79a1fa1ccf3cd8323d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimestampNtzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampNtzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3e368f004c037e8d17d2d4901b0bd5b50491c1c5fc3d96b5d35408fbcd7c3e0)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimestampNtzOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimestampNtzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimestampNtzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16aaa2b422c3fe94be4aaa29420b83ff6214668c7d35aef97d7bb3a01011f0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimestampOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimestampOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimestampOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a26e0d3dc2b517f1d0a3790e99268c804b00a4c984bd8d11844d95f5ca1519)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimestampOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7553400b6b89f8c560d7509ba28a0c015ec1fcf61ec628a7e119245931aa47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimestampOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb16f72cc52f1e04656e7bd2a7416ad8f2aa39808accbfdef2a8c8a696e78de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__299111b7ecd0fd073eb5219cae3a7cfe2d6c959e7e63d875ce248fac161fb855)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a64a6a06ce8fffdb0a873358d768e53069f979dd8e526224555520cceb5671a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimestampOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c198716554242cd329138c30644af763b2c9e710d02314b02e8cecacb8e6e591)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimestampOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimestampOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimestampOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bba413daa5dc4d985d3694217bf6094989c3b92610ab8181bffd10e901a71ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampTypeMapping",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimestampTypeMapping:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimestampTypeMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimestampTypeMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampTypeMappingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__016512c17a04dc2e385b5d8e0ce57f01d2a7d80bb801664a6cf2aeb67d64ae79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimestampTypeMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ec78ddc67ba3650ada1705f91863cfceebf7832d4b33151dbb996b6915b17f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimestampTypeMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c301f3dac85d70774fcbb0036758261ef11b3928dbe47f51e976136460078f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6948ce19ea0e3a620b7a91f9d0fcbc225ff23e86c20e534ae60f84bf25ca763)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebc58b46ae67e08682cbaa0f086a2ef7331e77dc1e7d10944a429a0a9e17cb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimestampTypeMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampTypeMappingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__272c95bd87c9116fb4c51b26369c2b58fecc7d44e29dbadf32f5172e0f6c9436)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimestampTypeMapping]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimestampTypeMapping], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimestampTypeMapping],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825d3a11016997d9490008a8966fa401eb947f8185d1ae06b014a34c3003b2b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampTzOutputFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimestampTzOutputFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimestampTzOutputFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimestampTzOutputFormatList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampTzOutputFormatList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__572a18a1df08b637b4020068615e4a9d5c59823fe146521bc90244e5f68079ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimestampTzOutputFormatOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39ef352bfa3b8d12474d89f113bc36ddbf76e18a399a8cb91c1ae687911b717c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimestampTzOutputFormatOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fae1093f8131c0a8646d7ac6f5c52bdfc31041974612c5f2c4b7ea5017bb0f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c04c82762b767c50c28e9daef0c4239846e53a58c85ec12e6a8ca42da1eb40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6c3c9066129961c7f53dee0bc1548629c820a765c95ddfa9961dee1fce4601a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimestampTzOutputFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimestampTzOutputFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c4ec177707f895a764c23dfc330f7b6d77bae6991d22502f678ca37606fd55e)
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
    ) -> typing.Optional[LegacyServiceUserParametersTimestampTzOutputFormat]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimestampTzOutputFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimestampTzOutputFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4496f1b86c37d1cc0fb037f1e8b879965f5471b1eccd601a18e62541a423a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimezone",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTimezone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTimezoneList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimezoneList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c76be2c12c16e07c0678806f11c6d0b84afa57e7bb6f742dd8a072e4ba21dd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTimezoneOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e18c23ffb0d9a862dbb9d8df69bcd215bb203c6495f9cac5fa95e030a456d4df)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTimezoneOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c80aa76570b77d74de998d2037223de90703ef3b20d047a3e419d3cd7f62a0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d2d4b56be08236b5486febe8c823ab6f0278d4e167a12fbfaa7079726de2f47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f7f393e11f9a5712c6fb0a9e81455c8da99f0de3b2621398c680043b1148c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTimezoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTimezoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7868cd2f629aabeedd84c5cacd5bd75cd001a266a2cc4e0871dc438032fe98f4)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersTimezone]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTimezone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTimezone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e57b3f0449850260069b1c98aa3d00a3de4e58ad11d0d2d9be496684519893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae859c84c26d69f3f5a1152848fe771bdb69b74ec38e8cbb18843b5a6e5ab357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b57cb0a8dd8f6a53f9ba98c215afa82430d8c67095a74c02957f58c8a749b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e366f8b9ea0e988230176774f9527403ac927a67f42ce7ad2d16fb1a893fc80e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20dbc254df7e6e322aa36b967540ab2515900abcd24afb615a0763cd61cec5e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17cf8e73ca081c38d1b01c59e564d6f5db66b1d20de9f04c5220497ccf2c77ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41fc686f46c1131fea35ade00efee8499150a6389cb1132f6dd057a821648fc1)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersTraceLevel]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8053b532503c27a8e1a2291e41a24379c246e89f1ffb7f10221521a6d042f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTransactionAbortOnError",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTransactionAbortOnError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTransactionAbortOnError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTransactionAbortOnErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTransactionAbortOnErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb26655a70f561efd86523bf9cc3e38ee1c7d024af83c84bc7369e6ad9406d68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTransactionAbortOnErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8981d29e1c1a729279b734bd1c020e7c7b2d4b56f7d1de64bd2e547ee8fc46d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTransactionAbortOnErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a7a435fa6e7ca663423cc138a365c3d108416a3b8df7e9915fd35499f63ec0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2249e945d4a53448904a6072a3d4930f14aaee4bc2db83fa0e3baac3b85cadc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fb8d2c4033422d8e3bd5a473abf6470412768b8e37113fb43ab8baae6e25af8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTransactionAbortOnErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTransactionAbortOnErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfe6368482e167351db50edf9cee6c2ba8bcb7847ca3149f7c5a2bad581962f3)
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
    ) -> typing.Optional[LegacyServiceUserParametersTransactionAbortOnError]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTransactionAbortOnError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTransactionAbortOnError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40c821edb97a47fca1efd56103e8297e3511f687968cc93df847ca2b5bdef9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTransactionDefaultIsolationLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTransactionDefaultIsolationLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTransactionDefaultIsolationLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTransactionDefaultIsolationLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTransactionDefaultIsolationLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25311d40b46b6e9d946ae63512e03d3571e1217da6f5725e01ef22d7d410bd8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTransactionDefaultIsolationLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192f7d71b27903b30650578d78ed2d93f528dd4924f13d1d2df7bd53dfae5d74)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTransactionDefaultIsolationLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a49e732ca754de20b1c89e524a786e2e563402be6e1ca7bffeee05b9ffa6d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da55c4b0ef9fb3732e974f50a587c03f05c070dbf1219b8c353be0498f0e3c88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f34c93bd0b571edf1aa1f479568798fbf322696083b6c05b89b957f8b9a6ead9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTransactionDefaultIsolationLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTransactionDefaultIsolationLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8eabe1e7707603a13251f262833bf47c8ac1b9744fa08a638ccda9e0a3a54c4)
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
    ) -> typing.Optional[LegacyServiceUserParametersTransactionDefaultIsolationLevel]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTransactionDefaultIsolationLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTransactionDefaultIsolationLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d7b0cf128ca448648c7f382748b6e8a3bf7509202642dc14193ef3675300e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTwoDigitCenturyStart",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersTwoDigitCenturyStart:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersTwoDigitCenturyStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersTwoDigitCenturyStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTwoDigitCenturyStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72103b3d050c772867103f5692885b5fa6059a41b38c132d040d834bda0de3b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersTwoDigitCenturyStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67668336839ebedbaf024ba1a70e780319d99c8e8d04dd12979edbef23933c7a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersTwoDigitCenturyStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572f0171f3a50bf7075644cb057a4e1c7a4afdb25027dbea3188107e253fa1dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__766e126f62ea96638689d2770f04289c365a1973402ee13a0fdd1493b058af7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ac8a168895550cf8e883bcf6bc0e565e176aa2dd96a6b117498168d756dccc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersTwoDigitCenturyStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersTwoDigitCenturyStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00bee63f542f93332931ce641ca20cbca012aad08b7202e36b3631019f5e0ce1)
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
    ) -> typing.Optional[LegacyServiceUserParametersTwoDigitCenturyStart]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersTwoDigitCenturyStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersTwoDigitCenturyStart],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d56687470d5b92be658aa74e2fa37eb67db2d77c562f4ce1b0df630a548e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersUnsupportedDdlAction",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersUnsupportedDdlAction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersUnsupportedDdlAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersUnsupportedDdlActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersUnsupportedDdlActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8ede19b74ab017e8c93364ab2026e775a848eb0abc8c622c9b35dfa47b258f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersUnsupportedDdlActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4cc1700485cdcf6dcdb47349bf667deb40af93f7afbd6208e84f9e10110308)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersUnsupportedDdlActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6fe4176900853cd2934f6a95036f8a6966dda8b745d2a5718c0af5b4eee0c8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bd553e95ceb1b5febcfdfd586280ec2c6bc4a59c1802468c94183bfcfec94eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b4f92389db871354f3d0b349c76bda49ad548fa1e313b15b6c490a4d64a0ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersUnsupportedDdlActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersUnsupportedDdlActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e64a2095447bde886418e0ad73afc10a79098ea5617410fff99d8b5b581a4a6)
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
    ) -> typing.Optional[LegacyServiceUserParametersUnsupportedDdlAction]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersUnsupportedDdlAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersUnsupportedDdlAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9cac12eda053b59cdac9fe8d5a551a6238fe1414560bac3e9ae43348bafa3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersUseCachedResult",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersUseCachedResult:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersUseCachedResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersUseCachedResultList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersUseCachedResultList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f27fc45b5f860fa700e60aee18e11d3643739473430a93bde880a41e3819db7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersUseCachedResultOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915c2ef095a7e0f3ec55be32fc599b009b301e5c2ff7b65343877a4854269e9f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersUseCachedResultOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc2c14f1bdf08e1809c656663056440f97373d578e48c6eef975020f939f6560)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfe9627c8f40ddddedb16799ef1063e0a72c69e51b4fa1df8a5b21a49254964b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da874565f085348cef41fed3e2881220f99c46756bef8cbf834255580a2deea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersUseCachedResultOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersUseCachedResultOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32bda884f0abbaa6336d10465b79885355c1c96108bbab017f0c7690d5a0938c)
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
    ) -> typing.Optional[LegacyServiceUserParametersUseCachedResult]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersUseCachedResult], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersUseCachedResult],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b6d4c245ece897b85ae56bd61ea9aa1dbb98bb3d6d3a96b703e65ea87e1555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersWeekOfYearPolicy",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersWeekOfYearPolicy:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersWeekOfYearPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersWeekOfYearPolicyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersWeekOfYearPolicyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bd9ef6308364c4cd31322950544970462409338556d1af9a17e298d6cb23ec8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersWeekOfYearPolicyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59894af18d472f2fdf32a2d6e9df9e237238fb4ce9bf0798742b990e8d40e16c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersWeekOfYearPolicyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1087c22cf5de111ad9c7c1373786999dffacdf9d2589525ff34586b76bb08bfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__429ad1fce069dbb1bdcc846031b18c6a2061de6a7673865237b49e94b4439a70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e4fe702b26b3414e75de1fbe8737b56d3f218f9eed3167ff028b78435901c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersWeekOfYearPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersWeekOfYearPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7108062349abfd68c0ba9ecc47ebdebbec99182aefa9352a9b0e55a31433eae)
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
    ) -> typing.Optional[LegacyServiceUserParametersWeekOfYearPolicy]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersWeekOfYearPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersWeekOfYearPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f287ffb47cd3cae38082ad97110e97ba21a430f0e90dbc2e17f27403752806a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersWeekStart",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserParametersWeekStart:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserParametersWeekStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserParametersWeekStartList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersWeekStartList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da85b84da1155d644263a5987773dac09f56e606d035431a1af08c4332b6a198)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LegacyServiceUserParametersWeekStartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3af8422b28724d7e1220a21cf0160677d62f2e759269fdef4f0d506d2e9761)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserParametersWeekStartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2b1733148fbf96b3fe58102cc95db2cb0c09f7955a7de12f5ba00878c38942)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26c65513046b77b670c7f417773908417e4cf0cb67b703a4ab625488cf195ba3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae283fb4b6fa56f864e4946a44141347917a5371b40a4c59f62cb6d4ae548d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserParametersWeekStartOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserParametersWeekStartOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcaa2cb64cb1238b4c31a19ab7c1e7da3a1c3d03c11914f63d49c4176184e137)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserParametersWeekStart]:
        return typing.cast(typing.Optional[LegacyServiceUserParametersWeekStart], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserParametersWeekStart],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca7503fca5f669ae6be260483a2ab6d57cb0da0850e36ab408e5430aa8567fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class LegacyServiceUserShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyServiceUserShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LegacyServiceUserShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a88ac73d9ce0bab3617a68f44fb4d19f56a872f8d06146b3521718d4b5c9e8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LegacyServiceUserShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7efb88ed73b043da578a526b3997dec7fd70d56a5e92140356b6b2961848ed1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LegacyServiceUserShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c722ede57af8dd23859090b97630d29bb4109196e004ffb5f5b5a170b6d79eeb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f10d8633b1d7d17749ade9209c766e9fa5c0aca44ecd7bc0daa6d64960ff5ce1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e98ce1513160b91325662b9fdf9d637653501747757d12e5884aec7f08f9fc03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LegacyServiceUserShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.legacyServiceUser.LegacyServiceUserShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa7035e592dcd83005839d4d4cbb972205b1276686f5769247538a1175a6531)
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
    def internal_value(self) -> typing.Optional[LegacyServiceUserShowOutput]:
        return typing.cast(typing.Optional[LegacyServiceUserShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LegacyServiceUserShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e682cb278ba1d73e66b32a08f91a02be522aebb45c5d758c58881214068e5096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LegacyServiceUser",
    "LegacyServiceUserConfig",
    "LegacyServiceUserParameters",
    "LegacyServiceUserParametersAbortDetachedQuery",
    "LegacyServiceUserParametersAbortDetachedQueryList",
    "LegacyServiceUserParametersAbortDetachedQueryOutputReference",
    "LegacyServiceUserParametersAutocommit",
    "LegacyServiceUserParametersAutocommitList",
    "LegacyServiceUserParametersAutocommitOutputReference",
    "LegacyServiceUserParametersBinaryInputFormat",
    "LegacyServiceUserParametersBinaryInputFormatList",
    "LegacyServiceUserParametersBinaryInputFormatOutputReference",
    "LegacyServiceUserParametersBinaryOutputFormat",
    "LegacyServiceUserParametersBinaryOutputFormatList",
    "LegacyServiceUserParametersBinaryOutputFormatOutputReference",
    "LegacyServiceUserParametersClientMemoryLimit",
    "LegacyServiceUserParametersClientMemoryLimitList",
    "LegacyServiceUserParametersClientMemoryLimitOutputReference",
    "LegacyServiceUserParametersClientMetadataRequestUseConnectionCtx",
    "LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxList",
    "LegacyServiceUserParametersClientMetadataRequestUseConnectionCtxOutputReference",
    "LegacyServiceUserParametersClientPrefetchThreads",
    "LegacyServiceUserParametersClientPrefetchThreadsList",
    "LegacyServiceUserParametersClientPrefetchThreadsOutputReference",
    "LegacyServiceUserParametersClientResultChunkSize",
    "LegacyServiceUserParametersClientResultChunkSizeList",
    "LegacyServiceUserParametersClientResultChunkSizeOutputReference",
    "LegacyServiceUserParametersClientResultColumnCaseInsensitive",
    "LegacyServiceUserParametersClientResultColumnCaseInsensitiveList",
    "LegacyServiceUserParametersClientResultColumnCaseInsensitiveOutputReference",
    "LegacyServiceUserParametersClientSessionKeepAlive",
    "LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequency",
    "LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyList",
    "LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequencyOutputReference",
    "LegacyServiceUserParametersClientSessionKeepAliveList",
    "LegacyServiceUserParametersClientSessionKeepAliveOutputReference",
    "LegacyServiceUserParametersClientTimestampTypeMapping",
    "LegacyServiceUserParametersClientTimestampTypeMappingList",
    "LegacyServiceUserParametersClientTimestampTypeMappingOutputReference",
    "LegacyServiceUserParametersDateInputFormat",
    "LegacyServiceUserParametersDateInputFormatList",
    "LegacyServiceUserParametersDateInputFormatOutputReference",
    "LegacyServiceUserParametersDateOutputFormat",
    "LegacyServiceUserParametersDateOutputFormatList",
    "LegacyServiceUserParametersDateOutputFormatOutputReference",
    "LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimization",
    "LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationList",
    "LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimizationOutputReference",
    "LegacyServiceUserParametersEnableUnredactedQuerySyntaxError",
    "LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorList",
    "LegacyServiceUserParametersEnableUnredactedQuerySyntaxErrorOutputReference",
    "LegacyServiceUserParametersErrorOnNondeterministicMerge",
    "LegacyServiceUserParametersErrorOnNondeterministicMergeList",
    "LegacyServiceUserParametersErrorOnNondeterministicMergeOutputReference",
    "LegacyServiceUserParametersErrorOnNondeterministicUpdate",
    "LegacyServiceUserParametersErrorOnNondeterministicUpdateList",
    "LegacyServiceUserParametersErrorOnNondeterministicUpdateOutputReference",
    "LegacyServiceUserParametersGeographyOutputFormat",
    "LegacyServiceUserParametersGeographyOutputFormatList",
    "LegacyServiceUserParametersGeographyOutputFormatOutputReference",
    "LegacyServiceUserParametersGeometryOutputFormat",
    "LegacyServiceUserParametersGeometryOutputFormatList",
    "LegacyServiceUserParametersGeometryOutputFormatOutputReference",
    "LegacyServiceUserParametersJdbcTreatDecimalAsInt",
    "LegacyServiceUserParametersJdbcTreatDecimalAsIntList",
    "LegacyServiceUserParametersJdbcTreatDecimalAsIntOutputReference",
    "LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtc",
    "LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcList",
    "LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtcOutputReference",
    "LegacyServiceUserParametersJdbcUseSessionTimezone",
    "LegacyServiceUserParametersJdbcUseSessionTimezoneList",
    "LegacyServiceUserParametersJdbcUseSessionTimezoneOutputReference",
    "LegacyServiceUserParametersJsonIndent",
    "LegacyServiceUserParametersJsonIndentList",
    "LegacyServiceUserParametersJsonIndentOutputReference",
    "LegacyServiceUserParametersList",
    "LegacyServiceUserParametersLockTimeout",
    "LegacyServiceUserParametersLockTimeoutList",
    "LegacyServiceUserParametersLockTimeoutOutputReference",
    "LegacyServiceUserParametersLogLevel",
    "LegacyServiceUserParametersLogLevelList",
    "LegacyServiceUserParametersLogLevelOutputReference",
    "LegacyServiceUserParametersMultiStatementCount",
    "LegacyServiceUserParametersMultiStatementCountList",
    "LegacyServiceUserParametersMultiStatementCountOutputReference",
    "LegacyServiceUserParametersNetworkPolicy",
    "LegacyServiceUserParametersNetworkPolicyList",
    "LegacyServiceUserParametersNetworkPolicyOutputReference",
    "LegacyServiceUserParametersNoorderSequenceAsDefault",
    "LegacyServiceUserParametersNoorderSequenceAsDefaultList",
    "LegacyServiceUserParametersNoorderSequenceAsDefaultOutputReference",
    "LegacyServiceUserParametersOdbcTreatDecimalAsInt",
    "LegacyServiceUserParametersOdbcTreatDecimalAsIntList",
    "LegacyServiceUserParametersOdbcTreatDecimalAsIntOutputReference",
    "LegacyServiceUserParametersOutputReference",
    "LegacyServiceUserParametersPreventUnloadToInternalStages",
    "LegacyServiceUserParametersPreventUnloadToInternalStagesList",
    "LegacyServiceUserParametersPreventUnloadToInternalStagesOutputReference",
    "LegacyServiceUserParametersQueryTag",
    "LegacyServiceUserParametersQueryTagList",
    "LegacyServiceUserParametersQueryTagOutputReference",
    "LegacyServiceUserParametersQuotedIdentifiersIgnoreCase",
    "LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseList",
    "LegacyServiceUserParametersQuotedIdentifiersIgnoreCaseOutputReference",
    "LegacyServiceUserParametersRowsPerResultset",
    "LegacyServiceUserParametersRowsPerResultsetList",
    "LegacyServiceUserParametersRowsPerResultsetOutputReference",
    "LegacyServiceUserParametersS3StageVpceDnsName",
    "LegacyServiceUserParametersS3StageVpceDnsNameList",
    "LegacyServiceUserParametersS3StageVpceDnsNameOutputReference",
    "LegacyServiceUserParametersSearchPath",
    "LegacyServiceUserParametersSearchPathList",
    "LegacyServiceUserParametersSearchPathOutputReference",
    "LegacyServiceUserParametersSimulatedDataSharingConsumer",
    "LegacyServiceUserParametersSimulatedDataSharingConsumerList",
    "LegacyServiceUserParametersSimulatedDataSharingConsumerOutputReference",
    "LegacyServiceUserParametersStatementQueuedTimeoutInSeconds",
    "LegacyServiceUserParametersStatementQueuedTimeoutInSecondsList",
    "LegacyServiceUserParametersStatementQueuedTimeoutInSecondsOutputReference",
    "LegacyServiceUserParametersStatementTimeoutInSeconds",
    "LegacyServiceUserParametersStatementTimeoutInSecondsList",
    "LegacyServiceUserParametersStatementTimeoutInSecondsOutputReference",
    "LegacyServiceUserParametersStrictJsonOutput",
    "LegacyServiceUserParametersStrictJsonOutputList",
    "LegacyServiceUserParametersStrictJsonOutputOutputReference",
    "LegacyServiceUserParametersTimeInputFormat",
    "LegacyServiceUserParametersTimeInputFormatList",
    "LegacyServiceUserParametersTimeInputFormatOutputReference",
    "LegacyServiceUserParametersTimeOutputFormat",
    "LegacyServiceUserParametersTimeOutputFormatList",
    "LegacyServiceUserParametersTimeOutputFormatOutputReference",
    "LegacyServiceUserParametersTimestampDayIsAlways24H",
    "LegacyServiceUserParametersTimestampDayIsAlways24HList",
    "LegacyServiceUserParametersTimestampDayIsAlways24HOutputReference",
    "LegacyServiceUserParametersTimestampInputFormat",
    "LegacyServiceUserParametersTimestampInputFormatList",
    "LegacyServiceUserParametersTimestampInputFormatOutputReference",
    "LegacyServiceUserParametersTimestampLtzOutputFormat",
    "LegacyServiceUserParametersTimestampLtzOutputFormatList",
    "LegacyServiceUserParametersTimestampLtzOutputFormatOutputReference",
    "LegacyServiceUserParametersTimestampNtzOutputFormat",
    "LegacyServiceUserParametersTimestampNtzOutputFormatList",
    "LegacyServiceUserParametersTimestampNtzOutputFormatOutputReference",
    "LegacyServiceUserParametersTimestampOutputFormat",
    "LegacyServiceUserParametersTimestampOutputFormatList",
    "LegacyServiceUserParametersTimestampOutputFormatOutputReference",
    "LegacyServiceUserParametersTimestampTypeMapping",
    "LegacyServiceUserParametersTimestampTypeMappingList",
    "LegacyServiceUserParametersTimestampTypeMappingOutputReference",
    "LegacyServiceUserParametersTimestampTzOutputFormat",
    "LegacyServiceUserParametersTimestampTzOutputFormatList",
    "LegacyServiceUserParametersTimestampTzOutputFormatOutputReference",
    "LegacyServiceUserParametersTimezone",
    "LegacyServiceUserParametersTimezoneList",
    "LegacyServiceUserParametersTimezoneOutputReference",
    "LegacyServiceUserParametersTraceLevel",
    "LegacyServiceUserParametersTraceLevelList",
    "LegacyServiceUserParametersTraceLevelOutputReference",
    "LegacyServiceUserParametersTransactionAbortOnError",
    "LegacyServiceUserParametersTransactionAbortOnErrorList",
    "LegacyServiceUserParametersTransactionAbortOnErrorOutputReference",
    "LegacyServiceUserParametersTransactionDefaultIsolationLevel",
    "LegacyServiceUserParametersTransactionDefaultIsolationLevelList",
    "LegacyServiceUserParametersTransactionDefaultIsolationLevelOutputReference",
    "LegacyServiceUserParametersTwoDigitCenturyStart",
    "LegacyServiceUserParametersTwoDigitCenturyStartList",
    "LegacyServiceUserParametersTwoDigitCenturyStartOutputReference",
    "LegacyServiceUserParametersUnsupportedDdlAction",
    "LegacyServiceUserParametersUnsupportedDdlActionList",
    "LegacyServiceUserParametersUnsupportedDdlActionOutputReference",
    "LegacyServiceUserParametersUseCachedResult",
    "LegacyServiceUserParametersUseCachedResultList",
    "LegacyServiceUserParametersUseCachedResultOutputReference",
    "LegacyServiceUserParametersWeekOfYearPolicy",
    "LegacyServiceUserParametersWeekOfYearPolicyList",
    "LegacyServiceUserParametersWeekOfYearPolicyOutputReference",
    "LegacyServiceUserParametersWeekStart",
    "LegacyServiceUserParametersWeekStartList",
    "LegacyServiceUserParametersWeekStartOutputReference",
    "LegacyServiceUserShowOutput",
    "LegacyServiceUserShowOutputList",
    "LegacyServiceUserShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__d69630f43fbeb2a408edfc00c0b91025ccf040b24379615b2e291ee1012259b2(
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

def _typecheckingstub__7548a07c04bbe7e7b86232f4787d852ed608b98b355212ca567ca2a6852c5216(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06574f68bbb9e1ea92e32544aeb09ee3c1b213cd9f79168d63a88dbaaa395761(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb2fe363bb4e64def429c72d63b50d4504fb6caf4b5481b8a41b0faa86862ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7504488019a8a575ee6af2aaef135591bc6b4b0884697683cb7e7113eac949f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2020ae6c8337680f777cdbd9439e7c9b8d9737c0c10cc9f58d9a75b3bed3cddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a943167309219c9ed0b0b9f6aa886d14144da1920a9c9e7daaaa4dae355e7ec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36751af9349828b7add3135a40012c8b4849edb457e0b0e90be1a11e5a15271a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c68ae6ce1c83ba8d38b203309eceb7aee7f07301c6b5358c793f514a8a95851(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__626abe5ce03a6bec30f860294fdb3447031e0543e6f4dab22fd926064ae51925(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353e201d1815d0858f4c19603d23891a43975cb27851b1a2066961a1065c0eb4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af30eef3207c378127df7d81c27594247d56f6d9e29df22c7ed0041787954e77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653a923b6b0eff6b930375acc51629406e60c93306c6458edc4696722d1852dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__414bb2cf4abccbd1adb8f5d9119fa91066c09e83b3f5556cca92cb38fe6dad58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19840ecff5c6f2e78854e6054c8e13c00067a3a57c0d3da2baca382fead13e2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a16f744a47563ce1bcf5cff7660f05ee1c718feff667315946154cf0d9a26b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a901d25ad7962af9039aeff21b7fc98717a2b7b72e44751e0906d6c29790a29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a11820f94118c939352b754316cef0fb25c9b2e52a05633fa979725b40c4d0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6722495e06006c649a61a34a99de02381722dee8a605c8330f1f248f06c0c15d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739bddf713d6767b347436b4143cab7c6e8a936361692160a4e918714169cfd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf76e58ce722a52ffe4e1e88f79923c8723b4b80531fdd1136d633428ef3baf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd61c1ae18b80098d2c613fad0bf0de5366732c855f459cf28d4c7fb9bae4f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47eaed1b7cfb0774bc130d10871936c962cdd181e133c434960464d00fb73e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b934df9774bb30633bddc4acbb41013125a00319dc6102e29288b74b682a2fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d461224ef3ab99c820f4131a0ba879ac8a940ea2f78e189b8747fc55241a33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456371b4e8e09b0a6f15bc6a1a6eb1ad0babecbe1f4384aeedd9f00e6757f973(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__870eb69d4f559eeae23693b254b2307881b92770dc9c5d6f62c3b20f32d1833e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22bfeb7dfbd77693408cbf9c127006c3f702af0040736d98900357c93dece2d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9a384ccb413ab992a92a2e678974dcc4535f7d2b914b6c4dee8dfbce682459(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59814e740a29a81da7b17f13311410600f25dec3eedddbd6531bd90951569c2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70bd21d97088b12ee60bd43ddbc70488732278a899aef397759e2f391507fc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e1bb086716b33c54adba545db912c33e2271f4069469ee9c8070a5cf31e2f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e4391ad2c59c00fdc66f6f3b7c4b0411c004a5d1535773dd008c080db325d0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde1696e894bfb96a3583ec496f8cb494c6951788d463d9885964409bdd03b6a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712414e94f7cc1841bab26e9ea5c3f5cff4240fcca79c8c2a246241e8d627c36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9147de55c57ce8fca87aaebe4f30cf8b4776642228b6f2c1ce057834aac833a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1393fcb894418e178bd244169a86a9c8f423690469ba834da884f88eea9ad81(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8557679734f29d00d791932d1458404b9d68d4997b5450efc10177546d73c9fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286e24a2526006d8492309171a291ff866392b7a3295178d93fc36164706b27a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f79555f4369d160c0bfc3e54f811305e7a8a92040463dba627d0b21440ffe5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b219505a893e0f25b63f7d9cb6e125af61d9e6c873ed27fb16de66aca3b052d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6393f28e015127f48a204ae95e08bf4a752639966b09c74ada4888a253288fca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__878f2363e21b478ba3a255b61e91893a62715d22f096e042e88d12e2bb5dfdc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a05f15a6eb7060ca6e0ea25bac286db47ca1efbbe84128272c8a52d88f9de34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ca6ce72ed1da2c3c6accddddcf7ba5bd63be967826ee9d2b7580a106cddeb3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd724a12abe89080a649738dabe448567c131d6d0685acb3dceabf945917ff39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c128492c797a26500b61a25d80bd965d31ad5a340799995fb640286fdc2d5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b3e3d446350c96f9708595eca42786fb795a74fb81a35da927d26f66361efb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8b294148a01e4c82e7076aa18a445a0225b0988b019812c0ad817720cb311e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2542748f230ff5a96d5f8eed64eb069a01c171820908cffea5637e0a3d3b857b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29456820d8c039dbaba63f0d9e30288c54c8f7480732481b386f8bb446c27fb7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb6ac83b07ccd59e89f81c5d54876dc201c9018fbb4b1b84addb8fdbd875f869(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8783d1de83a0f13cff4c1158cda200c67c63a2f130846c1761f39e43e49f07a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5341249a662b0c3d4617b425e3c874ada04ead78742040ae9b59eff2c96c9241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c31d06e473662415d466fdda395a9fd08debe2f91c37711728fcdb1d00ace3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50f0224d75ab10c8cbbd0d9212856b79a2e73b67e216d266964cad4395c9a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0f9e853567042025649e09582de602fd9fb5243d6a29151a44c4429dc74fd0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b552c0267e37be0f3c7759c10c4d91b1176a3180a68fa7905d67177df435d6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ca1c49720f351f872a6c8a48dade977bb3af0ec0c78c0d6b9a3eefcb56cfd6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e47cf61e2f8a8565b3def133fd6ace457e0620af22a6d87a296fe4f65418ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192f0febc3f9d51548a1818f3fe32c0cba4f5054c3a56c1fdd2c9a7349d8fec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf82e8e51fcf6501e03eb14781869ca1071412f45c6c6a12991889a8c63c316f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd9876bb26222908e667532399dff019cbda265fb3e5e444481d311ddb428e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36050674a95feb01612004170e920340cad72c5da943c088f78f38735a347169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4dffd2b24ec25617e3d2e25e26853b3dc04cc95fedec4f15510b137e7743629(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a03f2169a897f0b88c1c7c58111213eed4983d0f74df638d76db8ef5ab10b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97665c9eee7623cf489064fde7c29eedbf15c7bd9f9e5e9502454a639fc9934a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3da795d17f8c68a31ae16e7145980f88248cb487969308fd539f7571358f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99caf7e73d8838378206bbc74141bea6fba0009d3b58d387e148d32891730518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb23777b1a0f4c0ab7c0f6081d384f68e743736e66649a02d2e62485c8675460(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01b1a4cd2e6e6e193568cb070e842861d99ad22fa44379af50fdb5c158de2a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3192b3007f706b31e8411127c7ebe0bdd4db2f7f505d81bca8bfc03cc4a24a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9123eac23616f74bbc53b5af1320edbdc413bb29aba473e906dd01e4364d83de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb200aba10efb86a0b865d740cc7886719c616828e5ddd0c0fb009ec8ce25a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1997e6a92de47354105c80522c69bdd586228e6d5b2e03e7d627ba423e1993(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46128413dcbc2b65bf6200e7f421d6af0134ed22990c8f0e3adc914995e977e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673e0bc6392ea02ef7ee004691f8743fd686174bd0a3f01718f782c3beaf7db1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99eb0df6782edd67d1d1459f7ea4dc56c14115a7ac28dee520944d8178784265(
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

def _typecheckingstub__802a7103891fe7e47aa86eb7fade9ed61d53d2a596a3ce2e4568c224e13fddfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b223bf3d6ae39990fc4863019ca1d63bec939a18cb82ee5ce2fe53aba09311(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c0f2f7cdedbd51fb67ad055e75c4b5420a7bb6b923e3a8b32cfab483069f88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c998e256da88a452267c33249807c1f152c18eb7c51076fd8acc81a87eaa2dc1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc60150074045750b94b46a79d6c2d81f551eb112a74518d3bc670eaabe7c79d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f85f2e648ee7c9dee447e555d95580c7db99219fb14f762662ceddf2cdbf63c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a7c3405bcc29f20373a66b19136b43ce758f1b6525ec405fe047358246b7cc(
    value: typing.Optional[LegacyServiceUserParametersAbortDetachedQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e07fa880aa0f5361a076e3415585d4374cbf373de401e3dcd56d5e251da254(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520c02e1d4c9468671523d057af4f9d09ad3651ebe3ae223642ed83590f54dd8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72cd6237dfc94b8ecbf7cf6d8b90e3c0890c175e76f3ba836ba1a59a0225e89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7de98dfd5b25a05cb0f440aeeb7f525544a083d0af058104bf8fc00c388285(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7eec2cd4799acabf36b82a60d9a33c886c84f369b0b9555f7d7f7638c28a88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e62afd8c1cab7c2b3b3760a9fecfb8f1fc4cdbc69971cd3d74acd22a0a23efb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94042ba5878b538201b5eed993fefd0d5e9c0566afcddfbb5a5968426a859478(
    value: typing.Optional[LegacyServiceUserParametersAutocommit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbf95dcb46794ae35abfc8269f0a7ba26de81b4506d40ff45a4ecfd7e1ee759(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f235460074f228518bf0d819e1ab611dbccbc4ee229cb7dce18f153701762d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d62b8c54913ff06416ff9167a67ff1a0259df963da936c57072d28cd962d8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0359514e77d02e75846252aa24611a81e093d08b8450d5e7a7e52689453f9abf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2752bb760fe444fde7af938b5e4f76e5ebef1b2e63c4c79e9b6943941da12179(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e5ec7021610687c77f30c952e10f6b382d6e1726c2e5d520c7ec2f23a563b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17673472fa1d8ad035acca30ebe18d38de2ce829a4dd80f9e971c875fcf8cb7e(
    value: typing.Optional[LegacyServiceUserParametersBinaryInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9023eda712d13c9d009671c94410abfa2b48f7616edf424332e9b301fef2c45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f872afe0118ebf73ee04872318306f5d494ab0f589b8d0959232105e73b35c0e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8a383b463d06a8b16d15dad6da27f5338438ef4fcf5360b10cddef87d7048f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1428677e4d53b722a5b43e30993d449a3bceccaef69d198b8d6e10390c268e1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2d76c1adee4ae80af775b40ab583ec4b35daff04b32d35087f3fc0ade90146(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2f5d334a05d208454a5c286129b488bd42c3be083334ee703f00bb6901d1c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97948f3df67c51f5ed136765f787d67c0a38f82234df4629689a113c9e04821c(
    value: typing.Optional[LegacyServiceUserParametersBinaryOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2fb3d63c4e6612c1e9f4b5fe0878cba2d5a9cadb6a39b9a9e203c73a396861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8cf3e267b8de76e251972e71cd287fde029b65dd5f3ac94fad6a89df6e9b17(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9029dfd0614d63b30889eef3d30e17343c438d892dbd5f7a2c30890a9a32c89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751d3ef94108cc3f72be3894f912913a60f8cdbf4bff7eb2a0af6c9ee941faca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979c996a4655900c0081e1a0b35a8f0b2548fcaaac7040178eb5ef48e294cadf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc84252280d5614a68242137ec2239fd686028a3bdeac347ea3261035c38de8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f70a866897ce7a989d5eda87ebdb51e7a172c3306fac9d9cd60c672576f6fb(
    value: typing.Optional[LegacyServiceUserParametersClientMemoryLimit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3690898e759f11a509ea36bc18bb1305fa004c551adabab4360583d5772117c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24482ef1183c31a8426fd528cbe5b92e89b97feea9f3361bed4a56b35a3c2b46(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4539ac9c37553f52cdb5de4d0fd5a59bf8f7ea15de3d4b83a81ccbbd1a3458d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aae5c3a3a46c62a33b3812d7d0f61120b6723d9bba929447018082d230bec86(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162717b958f6f631ee861dd153e78926d940bae03a5ca5dbc2178adb9336173e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973df2b2b8175fa79476fe08239a4ee54f8a8609055b3f406cde4b55a9020010(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dcd28afcd968c979069e17c5a9bc55bcdf6cec993e15497e4c4307442c7fdc(
    value: typing.Optional[LegacyServiceUserParametersClientMetadataRequestUseConnectionCtx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e49f187f42f5a1cfaafc99ef1c6d5a4ebd326b8eed13beb1cacc93b2d4adbaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954bfda998f93ce9e7be464fa5001d9ff756901d82741ec5f9fbe66c5e3bfa0e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef3f85c127f5a81eb9c9eb923e8286f2c188370ed6ac02f9eeb8016331b93dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e57fbdcf986f7529d67e887a62aabd25920726105c1c3e17e76baadc05aade(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c336a5f3bb24a369f00cbbe59c835f3e0e8d1dd3920943e785193df22da3f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220a11ffd82a7e71ef7d325700c7f931c9feb46cb18848593f4f30bdc86efb76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1904adfbaa229f167dfa36a288d9f5e9b9bc96a36b058e5ab435be8afbcf4de9(
    value: typing.Optional[LegacyServiceUserParametersClientPrefetchThreads],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4300d9a164547a3a1a7ac1199c3bcd9af2c80e2997443cae161909f7e35d84d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc82c480141e59d2092cffed99f3e69f2057dc5527114d1df879a5201514f127(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57aaf7f7ffe606e3b26fdf1d6c8d2221c6590a1a486cc4c915e314bea40748e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620ea4e27ce6d07b4ee6da7d9b83df9398a32db433f6a1e5725fd143e2ace052(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83357d086249aebff94f3062e628b104908a82372b4c59b14ad003e68d12cee8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29bdd326aafd564e080ea1f81ffdde4c2490ea29248e7c491d635276660c784(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d89ff4f4d51fd77f354ae8af48bac5c14ecfe6c7b0fa00699ff0f96e190fa7(
    value: typing.Optional[LegacyServiceUserParametersClientResultChunkSize],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed06a378bab5cc4cf7f784f72f6f474c5996eb39f25a2cf5e470898694651555(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965ea5f78ac0baf1683cfc86d70312f40e32dd6daf8ea4b01459e460dae82888(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2758a6f73dcb8473c899447e98d69d3db2249b802fc90363aafb08905a486ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbccb9396809aa79857d377126ff69d83b32ccbb43e3bad1ef5b3617cce1a78c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067427e3d7102edc6cf5be2c58d3d0bea25fa624efff35ef05aac6e4813f2484(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16b8b901b7e0796ac0a9dc555f2ad8e549e511c0dc26f2d518cf5b5b95cf9c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549bebea10f4fcf8819c8fbd38d6481725d9867c8b3f8fcac393640affa113e5(
    value: typing.Optional[LegacyServiceUserParametersClientResultColumnCaseInsensitive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa92387544457179b3334828315de0f0c5f763b8b1f257ad9e03c700be7fc96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d991f0fc7e86c0d8a71e53e69f197801c2ed53cc0623fa0fa3c1a0aeb3ebb2c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7419c5a9727635471720374f95dee62b2631d66714c0f0f4f21988fe74976270(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fa84e9e057850c4afed9b642c51d997124555aa45d8d5e766d6607424b17b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60d39ac0ddff2e8ae5c31083e4857dab001951104b4ce16a40d95ac7511a6f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25d2bb10c164c2b766a9b66f3b72179b7e97d7e8318f00486db47ca2d1abbdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab0793869965b0076fa78f1e11a93e6f4e93159bb1129dd4cf9b93e7f4dd717(
    value: typing.Optional[LegacyServiceUserParametersClientSessionKeepAliveHeartbeatFrequency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8534651c479554dfdce4e2362072c412b30be26416a6aa5d852212ac676e3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639dec214740d3eb6b001c40d5d8057d3d465eac1ddf00a607b8d224fa790145(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbd00a20c8854da970377c77d0416000d640119908800e54e9120d900f14e20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53780811d985ef51a75a9c589cc81011b84b58ca3cd5f9cfb151326e93f74454(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06dfa016e205bbee71c615f5b1fa3f9e68bb1ff0869ed32b7e95bd579478ca04(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c168202021881e6d0fe6ca1c7e2c482c2619e69ab7bbf02d27685f68b36e0c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf53c6cc7245add3298a9e69e9e2baa795b2632db91ce911514ad5fc165d7699(
    value: typing.Optional[LegacyServiceUserParametersClientSessionKeepAlive],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8512c189fd148404d6e39b44dae51b09449c54874c901f057ca323eb31c1a9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44655430ff54e53cf105e263048f5f676f7571506ea3b805d23a3218a49f6123(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dee515b8b0e5bc045507feab10e115431732a10f5c20ea4f18fcc0c32b94b75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a90904bfa4b9e68b322ff5d06b24517cb314e90f9baf7d2ab5682ef75078d28(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab23b692a09d061d260549cc39690af79ab595c44aa698f707e290b63090668c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552efec8759f33d284b0a25ffb5cd7efd0b4e2446e930403e3d33ac8025d9731(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8e2e8ae803a81d9b8d98379b583b76d351ab57b927770a90edf889b5c81fa7(
    value: typing.Optional[LegacyServiceUserParametersClientTimestampTypeMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab949c127d40db2dae8e1c54efdcd7d412becfbf22034c875ad54b95f78b354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b169443e177dfa1d618f1a7d16187f0fd0683d8e665ae01c70fffc696f094d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59dab0585a40fab56ddc77b03caf7fbee5d49ee08e4b2fcbe0db9ecae025b8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbf3f249ed41b03b8e7e6a51abe3142b852b6da658a1be1f2fa5660d88b1c93(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358c9aa714d3a554bf611a2589bfd8bc7fe6a6907559d8689fa2fd7c2bb0c1ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6dfefe66bad398e38550119298584da17cb89e72954b462f0d50315fc3007cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b12946abe65b82a4539ac6d84f0e98b849a0c4576e03f1a68b1b30b1edff76(
    value: typing.Optional[LegacyServiceUserParametersDateInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6892e6c9e77ea3a03bfb87fde0ce62ca28ae211824a7deb8c42ec6a14012b9b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980d1d86201cca4fbd941b39febe016c35022386e259c2e20dcdd41e85b4bcd8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271f8f1e5cf9595274d6f6ee29bdcac83ba55db41bbc385b879dbd7cdd195273(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af822b49afef2fdca888e829ded1eb55f3eb25ef0ca07fa46926caeb3a8f5bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc0658d8be5c61f74763189946059e1f47456385a5ab17e98067f36f08eacdd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f516bd11c74238f3cb55cf0e326133011df0b7ba8f0b5b50177c6b110f452e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80d91bbeef8b0cc8ae117d49b3ffbcda4af0d8cffd33496609f8bff19ea58d1(
    value: typing.Optional[LegacyServiceUserParametersDateOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acdf2cc91ec12903cd00b7b1879092870023f9e17fa695c315a6ca657b66e83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e193a1212bda498aa13e0dbd4990a1a6332469584b9520bb2e5aae12bcdbf629(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8af5641e4741c2669c8c4cf0f33f5938a6fb8e1a207c54c91663cef61fc1ec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b7041c26f2540bc80129605afd7d0c71804e486474215a73fe2d04d0f82871(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745d4af4775863d29a0cdf9a21e92781a2131725bdf532ae7f7f1df9bea2dd7c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0abf9c83fdf383c4a60e5f717e57912a75af64136a408a3f26a12bc1d25e18b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1043a83bafa947255d413c88f16f95d6296626e404301fc87e36a659bed56763(
    value: typing.Optional[LegacyServiceUserParametersEnableUnloadPhysicalTypeOptimization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18496854d6c6dd85be6cd136cce25a592958c183f9e055f574840314225c767c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc4c84570b8985a5257e62f4ef2a8106ab3b5632bf47d183e33689934d88f5e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126634f7c7b33cc63c5b0c38f273e68df1eb1cd810c8a478d86e90d9f943e4a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1aa88b9526872b885d22e34e59c5b078a3b8a230b181565c73dd2e536af6978(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25d48fd1983b4de70410e94f1c603f6991e6cdea97704db77b0a98c2d069c61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52792bbf47d41d1e4151c107c6b13d38e0bf7b44c9d20fa2b51fd224da36dc01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4660e3cacee3964dfdf72760e43be88bd046232629123e4c552747695c18a89(
    value: typing.Optional[LegacyServiceUserParametersEnableUnredactedQuerySyntaxError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e9c2f0fe77a18453195dbe9f1c7bfb8b844a7966a321c28d72efb1d66b6e35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a1103a7a911befab9cbaabfb9d6b8c850c8dcdf162b5975ed0bdc08da935d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607e918278c453fa068564a2f14f54c0751db6f65100838c2584ba2434f9d847(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf35483f3b690723a811fde09d07bc64b6c1660b27d167b88fc45a5ac23420da(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add326b4dbe6bd3cf01f9b50c59ea1401c3bd194eef5111855cfddc84e5766f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3840a06fb610e6ac121d3bcb183d3c5aca31637de7f11d8e43b0546e806af448(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fb8bd339ba8787d13e29766dbd511fe0ab9fdf87d64e90a573ece190063b55(
    value: typing.Optional[LegacyServiceUserParametersErrorOnNondeterministicMerge],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d03fdedf408220f23155f0f19745f6f1fc0acf8b8af4f1f6a737b71116cab55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b1e65514ac6146eaaa6be129771512e604531f522f07a980f133b11da40add(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0944318f6f2659e495d1150c0939e2cf587ffb58db591b6218cfd297bfaab79d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e0e78cb63267cc6530953983952e47d14f4a60732a6d8ef94bd771790e4c4b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e7daabca7d0f4ffeedc217538afb70199192364a09f3e39b4c427e84f5bbd4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad559a30692fa010e832b09bb2af561e33a541b97c4489a27847472459a4269(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb3695d81e36aa5817a6eb1407120468a29de1ea56a90e864ed9fb80daa9448(
    value: typing.Optional[LegacyServiceUserParametersErrorOnNondeterministicUpdate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d703ae6e2bf47fd3fff74f236658ac9af56d18b441e7d59e425ad1f98cd67a39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704da61ff9a2ca405af0cbe4913df8e404e4780d285e26f9245f4f8e87045ead(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854729c862f26c521601582af315e26ca08849610d6dea0af39453fa9b53420b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2def515991816019282a0ae59e741eae2bb02f74077eac1814204501db741ac5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0b31d2e9d508e2bad817c08a5575174f54fc65666ee7cc89988ddaf84f7d4f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377f397de1453e167cab79b09ffaad8c85ca5e1785d5c0dc73c411f0ff2dc2a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2af6c8f3fb8304c2433e125bb3d1241fd07cbf4a4dc0ca2ac610ff5d0a3d24(
    value: typing.Optional[LegacyServiceUserParametersGeographyOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6a9621d1f8da56e16ed6d4a26f20192c4f56218e6823511f7b380862773e24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5562b97dfe711be08b146ecc70b8fa5ee74b9e89035721cbf6e5c46530497b6b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8b9ea059b5730711a72d92909dd3c464cd281c71c5973c8a5b56c4a9f2a15e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22287d22135cfe7019b4062212255baf7c15d0286cced61c271b3a766a3fbd24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8686a3c8814e4577a5f1e08a80affd5e8c15bcf2101474c70abc8526306c80b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681306b86b5aa4f9287ad112ad5177e4ed62972d04e91ef7b13cfd0096ee2318(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266f7c130cadaa2a23d68cf6f882ddf3bfa4f90e64da54b9d33464779c0adb71(
    value: typing.Optional[LegacyServiceUserParametersGeometryOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2082183996b5f56676cd3fb053ab81d93c4b73b9629deeaace6c81fab823f62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c79c738a3975dbafc7b8ed03cb0dd293d006eb1abf2b6c2c3238d02cf39ba58(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcb99e0f113fd52554d0916c2f21ef363336866dc0d3e1a963b9023bc53d3a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bc4a15360160f9b4fb6b66c934a79412089fd30c6cad6f3f6bfa4bf295923c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb00711414709d6ce3b1f72c7d08df1c080060ec2171ec7ad9bd631bfb40c389(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d7ef8ccbaf670a8d632822e9e081bebdd02521feb3ae1b0068504328fc9d75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a733906fec86df3275c2809d25b14097af2a952e338aea8d3f99d9d3ee37e3b8(
    value: typing.Optional[LegacyServiceUserParametersJdbcTreatDecimalAsInt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1673a1f8a62678ace9efd8133cc0c2e463db8e3063825a42788a951573c1a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad65303a0a2918527db6a0061b4c0bb9c8b9d6018c03d83aaeb7d895f805d3f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6154781df6d001d118fa36fcee7b86645857e732398f794ea1176c2c61110b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81571d4eb4e21a61efe9fc347eb43c3d784ac291cea975cc1b1ba0f57e29e2ed(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc73963df15987ba614c03bbda1faa81507e90a3dede00e34597c17e019dbde(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6e2a7fffb691a68dc7f9375e29fd3db0584aa9b46695c811a26a5dc6fccc8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d0e1ae4d0abea8bad75f0a7b850106eb5c33bcddd5bd42697e51707676bcf0(
    value: typing.Optional[LegacyServiceUserParametersJdbcTreatTimestampNtzAsUtc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c63401b8fba4723b534885778df469a9a8a4c64c50e269c5f2660e723b964c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4187eb00922c8a3ea8e3086e4e39c6423dc952ead5a5377206f867185eb6ad3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f140e50c7ae532966b1359f5c527792f6bcd9a1bbc64dc2b7bf15d22b39e051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9987f82b2321055377cee69e2ac86e85ac58a42fe9b84680a55d59a2424c06b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2461ef9539fcf9f676c7910ac77704db73300d92cb0d076d1b4ebb84dbacf38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22beaa8ca94ea8e26361f953bf47c423fb0fac8b3f0905366256fb3f78e36594(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa53d3c66e3274159e934be44f85e7c968f35b986d5191a55e7600212ac6bc1(
    value: typing.Optional[LegacyServiceUserParametersJdbcUseSessionTimezone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5791d3b04c426c469d5d9351a8bab401c4e59c5778271d15ea2565789a793c62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d8a480bab874b90795fefadd417e634cb30f6a077bb02087e506d5fa384d4d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06bcb9ed9186546b01b372051ae230a4360dc5b81b6d09f2a4a9ad44e0c4a37e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796683a57aefc654c5b84316ae376fefd26557eec1f6a561e94cdc29c7a85425(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908c0db80073669d29291a222cad838c5be6eb6b97931ce37ccaf0d5e7a2ddd2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6637a9ff60b9d5cfda76d9a8aece24df1279670be45bc1e984d68771f20aab0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5c9bdf42fe6c9e318272cc3e9b9649427d103dd2fce97963550927fea44681(
    value: typing.Optional[LegacyServiceUserParametersJsonIndent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd54b9808ab5e13658de7e44cf61b87deda13337a6d7c6e77ae983615f622186(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ab06fb235bf180c3f1316601b9c23bbb4aa9fbcd2dc207cb2c9b019c94b328(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afa72e7dc731078fbdedf56683078b243b27dd830d69d3159af590462af59f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20acbcf24d57a93630af0d216aeadf2bf0fecea4629400c791730df4f5b2f384(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8618bd924e15b74a6a3e44d6a128a824dfff373c941caa8f203492aaea27777f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6772d7bd2a57a9ae6c8411d69b1445c363cf95344d0a4a1698a4cb2b48595ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34c1f8a4040ba8af3bd419592e8e8726770d6e3d307276611028e0d9fb4aec3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c1e0ffe136c313f83762579eaeda655d87a1dfca197cb5fb6052a74122a938(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085cfa786aa13edc76619e5a01ff39e4832571f2a0fe0ef7481d6b1924dcb651(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8759949569667e5d5f11d10532f491bd3829e766bb8c2b03606cbef3b999a1aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3cea037897770a7318a8a06dc7f9b946bd4765ea90ee22bfcf853c61f47705(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6eb5cb718ff1a8de01a9149a2b089aa2b8016a4237adb7316ecb5b75fafa737(
    value: typing.Optional[LegacyServiceUserParametersLockTimeout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c78ca2aff4b8710e5760820c3e26536fa279c556acd1081a42032b8428ede2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8810021b7343905eb02293af3c43b477f81b6399cf2a5bb1969c0efdaaa9d911(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3001fecf16ea2f905dc0c3042832dfb34050822a3c937414ac06c1631389ee4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3653dee1d59d4e2da3f0b6dea19ed761d625ae77c892a4a7d1cbc08cf7443dd7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209f874ea92bbf8a409ece9fcd583c87c086e2864a6343d9dc2aff622ac0b0f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707bc2e1910e914503ee15257d07f3111f530c74142b0f730a2e0f056f537460(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae2625092c75d878a7f68505afbf55b319208cc69be20592250765e9d8ded4d(
    value: typing.Optional[LegacyServiceUserParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dee22f54e78f734832466e030094679a514b7c3fa83cc82a6ca060321de577(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1cc6f160f181a373df6dd064e79db07b6514d2aee53f7c34aff8f7774229c43(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68daf241066e51dc1a96ef61cba359456df04082c1e64477a8db186548d9681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e885e140439f308521f0bbccfcbea8a50b4cdc83adb66c87f9ace9d7bd07d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74da12ecc0a86a98786621af6d6ae82aee4a103893dae32eed6c927c9bc36345(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226cf64f34d0a74b3f76a6b393713723b3d4caf8d2c4c61c2e1fa730bfab7d0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9411d15a3548503dda232ea4a3dbd1355c79292da4467099621adfa29d1449(
    value: typing.Optional[LegacyServiceUserParametersMultiStatementCount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32435ed288eff0f07eaa971204c734c7a4a936e512243ce4b4870654bf4b4157(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485cf19134473b5cdcdefa99b71c6b05af14774398e5f912951caafd835b00e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d34aec9229d337b8de9f94404a75eb2e6cc9db19a569366129920183bc3f00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380baf0b3e4a13cb36d13aa1eb704fd088712520daf50bfb2482bb6e32dfe614(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46a18a7e5245deaf863d708cd81d067d95058d7344bc16473bd0b732f358790(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043c4c82a51875951980d317b1a09e469f12e18ac973b865ec18e48249d3f67e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a93c8f290b0f82a38ce2fcf1790c594610c0d939b8136551b0168f0f91d2b1d(
    value: typing.Optional[LegacyServiceUserParametersNetworkPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b8219ac361368092b5155b5566dfbcb984ea624f662e24c5762efce04c9d8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8661f38924ae3470d0bfab9eae168ed0c68ab095abf2b5eef04c43057c7673ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecad989a9b5d75804877bdc2c7d9e41b8931810f601b2b0eaad379ea0da243cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a9f7819071d6be6cfde2b3e0c6f11a417610563026c25df005366012354050(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d3bef1fef3171cd0073667b8127a686e96050071384cfe56b64b866aaee7b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb47c253da852dd0d4941c4f1fd0ce0c761c3cf3462067c470200064713b4f9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d50412ce1221e99d2ddb5f12d42100f682720a40a045a9b0bebd221fa28108(
    value: typing.Optional[LegacyServiceUserParametersNoorderSequenceAsDefault],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74d59ae53b7c3c7b6cc37945269c245eee1f9b2e7783455aa3ff580b3e53eb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e201b2c8e6fe93be614b05cb29096080538a43f50dc454b3656e8d727930776(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9df8d0efcd0cf7f8c37fbf9d4724ef8e746e2ae0d2345beb9cf4bdfe0d0750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfbc1bb11bf62a721c87c9f4be7983801d1d7599f970d02b2fb4590cafe9b4c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57cbd35d23655ccfdd1d57a60c68614d1efcdf0b84a9bda0d07f4b7561ba02d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1d0f391459047f7d9e8fd5a6f9424a003dc16e81f7c5f5a997ca7d5d41d39b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c293933d5af6118a7e8af19fb485e94f09d537a98d5d2835340cf80bf758e918(
    value: typing.Optional[LegacyServiceUserParametersOdbcTreatDecimalAsInt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318c55afd48f042a831927a19de49175807f3fd0ff1fc83761ea7aaa6586603d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4aa41f0d20e83a9162eed7f5c3d5febab650d9cc793138dbcf096c3476ae178(
    value: typing.Optional[LegacyServiceUserParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae0416b56862e6400570489b983f4db667f43ac631d4c8d172bbc2042886e34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa59a68b0317b6e15edd9bf04da3b24bc01fe0739bbcd66179a684fb8c460cae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e054435c9e6a7fcaf6b64e02d1799a4be795c985d8319f44510cb682d41e5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a2e4c30b93dca8e277d6d793f25a215a9dfa1c15d9dc64e29013ddd6ee498a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bb11b0d0e3a5fd84ede46cfe7d411edd357ca61248e2bfcf1153b563952b1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40204a3427a8e7eceb6dfba322b9478a4afdbc9f696cf8f44cde113bc7f03820(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc8a1f6f92cad640bc784a6195ffef9b168da61927a8152039ef9fffe2cf103(
    value: typing.Optional[LegacyServiceUserParametersPreventUnloadToInternalStages],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9e482f465327e16ae0ec3554845618407e0d5978e557afac83af6336c455df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c723f13b0b9e01a42921ebca2d90f286a5d261355ec6b57e098e42a778d0a0a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978aa977cdef7b1c6d982521dca811f0db77b78ba5160606c7a8bf06dd5b3c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd89ced9b83782873d86f7476c066eb67ebe7229274554ad3b90bc8a63de3f9c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52dd5bec38e64a6974ae5ca24f2f15a140272ee5e2decf92192db54da6b1f1e4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b961b9efc6990fb913caab0e378658fafb7d28e74a6dd232a1c5397f04d3dd24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39be3a642469384b14ee5837cd1f2df4ee7643de292077e0bb09738ebde2c784(
    value: typing.Optional[LegacyServiceUserParametersQueryTag],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5f4e297c4423f691494f7fdb007c76e4b21910e314c3ee59d379ac1ccd1093(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9e9a47de1d9625c68a29f8f15d884df57f68611e46efff90c6fc63772ffd65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0882761ab19e6b0e4655113d2d25d6ebaf06414b36e84588878378e09f607b58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32f07a00c4f1712baaab3410d532afdb54feedf678b8b6efa153458f2600d73(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4a9134433653ebd9cbfbaa6918d5f050e958e1110a16ce1ad46b826865d4a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b53d4aa3a8dc9d2df95ba2c200d12a01b228d474636494784fb318f1acdbad1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924494282a899631f02f52074bf02df90701950cd33729ba5ab506d9c445ace7(
    value: typing.Optional[LegacyServiceUserParametersQuotedIdentifiersIgnoreCase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fb20a1e0d001449650f61a81712e7ac9f8c24c0c72c4bfb926b94f0788628b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3570afdd6ed312cf822b10181c810d05d794da53642b8c278ddaf6d11619e5fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354d94021b21ab8e04d23c9cfb327360e1264e1e19cc4d14d20e654dbd419ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29448960c39d6e7f3f14ff006ec6501527dff025d46bd17a15510dd5efe7712(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc8f71c2d16d4db6cb7ca2630d8e1678ff9e2d63ad242ee323abc3aececd6932(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac0ff3c2384caaf14f1a93cc8b7adba8d3c1c517ac12fd260eb8ad5fb4ef8ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bdf2775ab60e48baa344413765d53a14d7ee86e1ceb6042bab7bc0babda920(
    value: typing.Optional[LegacyServiceUserParametersRowsPerResultset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e291046cb66a00e0e1b334b1273b910eec22458e468a8c3daef8446ee0134051(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa242cb2cf2200521262f7fb2113c79a453042c67c5600a54cfa29dd7894e73e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea0e740fd0c60422cf80b9d2ecacb9f779f00ea09181a0a2f7488a56d59c8c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a16f52aaf1a412521b068b4d389520b99582406e512c51d7d4c81d01c1cd468(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dee3312552133fde7b4d1f74954d84e367cf9ca63c3089463b49ee3f6dbd574(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0b78feca010f51779e1e3df7b3a10d67af81adf5ae34b344f5f39666ffdd3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69469ae76fa703d6ef416676196e7074161b4bfc7a5df482e8d9ceed20bc461a(
    value: typing.Optional[LegacyServiceUserParametersS3StageVpceDnsName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fef3eae95f4dc27c772cdf5c8527137e8fb964dcf48de730b0db1e99cccae92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fec8c072d8038657ca7bbcadb42fc6ada8f90c5c1d1b327e95434448e45f00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d1737ecf539af3afaa8236b605d4ef31d1fa3c4027e6b492838f4b05072f91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6e580e7fe547a54e392ca59c8eb96f81f4caf25f2d6ebaf59c570661d889f86(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a159dfa9480b17c018c4f0107dbe8ea40002f19b413750b8ac3cd69ff2ed5e0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083c29d4861d75739bdaa5fc0c7960c70ad5dd973038c5f23ec79d8bb45d1225(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0240e40520e270e90294db1d5ace5f52fc4c89a3341630e4a2d3f544c1652285(
    value: typing.Optional[LegacyServiceUserParametersSearchPath],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4fddc4c8959916d3b3d47daa4c57c27ffc144fad028944577ef46c8aa4a8ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8694f063ab56126b68b58309e294812819159bb09c02a9a574751da065325c92(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8871b815b938c2140e334ad3bba19b914207d1d82970ae97d4cf74c65091f345(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07010fb3d7f0bb71ae884eb3a2f4bbd7f1fe17940d805865204ca795eddefedb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5758f4667044dbf9445ba91abbadfda964db84ceca50bfa211eeec459eb0e4c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c448ed22983ec7bce0adfb2668d35a317bd120d0c19ea0f45d4af7fef130bb38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071a5ca78bc6b75fd46ccc0c2ed3a0b53fc06bbf10f836f9d7416599366df065(
    value: typing.Optional[LegacyServiceUserParametersSimulatedDataSharingConsumer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23c4f5f572e7c85ab16c5a57425082345a0012f7fc5d51953e892d2f2777c6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71038defdc910e2790b0af4eed8653ddfe613af44a15fc1aef661dd289558f42(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0fd068421aeca0c73e6d57c86b67589999521433b33eee71f43a605abf35bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3abe04b568fc0cdb57b66fee3c16adfaf3baea6210e100fe41d16c37ffcaa5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e30cdba06d10c53f7e56643ef86c356f5537bdbf2ff5797e3bf51b35fa68a87b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21591816b28bb614d3d52a8342b21c0e684fad0e14c8fea344b78f24cc8e56e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef97998bda5864d2a09efeaff82138871c0d3f1407a3d6012a4e509a75b978d0(
    value: typing.Optional[LegacyServiceUserParametersStatementQueuedTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480159c20e5abf6a4e4edb92fe3cb649e1b5a5f7f91941ba059596b40bc284d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cc84ae45a7fc31a3584750b08ab23c1d87228f03af852f3576eae6d433d36e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad807311c9e4508ba4ce2a18332269b66540fee3884ced18df4b9945152d96b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073a651936284640440f050d5b41406ea0557b72c07eb62933a608c665ac0cd2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a12e4cf6e0a5a1d08169b868469088dac111bbdb42f07a619639d4a1c8a4e947(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b33648b7ee6c6834d66d8a326ae2f4b94e6c7cf5c79ea674053471d0bc9b06d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41dd84a2630c950f652db81228b5ac57a2c76633ae032f2beba7b864d0260f3(
    value: typing.Optional[LegacyServiceUserParametersStatementTimeoutInSeconds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ff576d8680745404797e279b85d0c479a54df7fd0cc9ddc820e415878b9f51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7885b138718d240e815ba49678de64ab888dc95655f87e2fd246a64d86fcb22(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5232f63716d9b51436c66c9bda51a8dfbd1a9b3397f0ec06671c07954aaa3b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e63a2ee0926552dbfefd7e7eae7a780f42aa4c71ec7fc8c082f5c55d2fd22d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e9ba713df1e6c350b33261de19d57a0faf7182ede7929c3a664561f1835b4f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de66ecfe9e56adfe7dd1f3c185657cdc66f10d872ef7d2b11d5183577b43e70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426bf0e3e1ab8949202db778c393c9da90289b982d02b39204f7fdd9c416c319(
    value: typing.Optional[LegacyServiceUserParametersStrictJsonOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5c68d56049e4950ac1d61e005655856c388be0d25f47de46fbbc53af9bc92a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a491f42e6600b875c636bc4ebeba589bc78da7523ab5f0f44ce7f7d274bb8cc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4a6a3ca748d9c5d253c249ef1fa8a4e1271b2e50c64d9fd8b3a73c0c93f82f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8545eacd84ae4662d7843db0da7cab3eb0dde338feb54a149ed12c5acb7c5a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cf913db6d35becbcd9b84d129745476d5bc5b9830ef459f9cfb22488494610(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c4ea545752615d54aff545d5d3a2656849b02445f7ffc37f4ee04360808a88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1884be8bc8025fa49fc2a8f4f4ef58ac2062583475d29275e55d73842f0e3cf1(
    value: typing.Optional[LegacyServiceUserParametersTimeInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422228cb599b3362c489dbd63343542ef0584c23a05ce01aa5050cbf1e369212(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2fd4aaf803e476bb581ed5faf2a100cf24c45cba42b652a28814903e463e78(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9d9887839274e2d44ff4b7f61d6cc835acdaf646bb80c6d86db459c1f33dd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f31fded41b4846e35a1dcafc0ebecef4d407d7945121c0c82470b158e2229ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5262892c9aa30fc9a90f418e84268f616e6c87ef739c697bf119b4bf3e8e5db1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1300837b0e6454bb6b14c3a7255e8496b2045b0c6d499253dbd0b0d8d022af30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1782ab9e983a012e7117647a748dba2c68b189a0f449875249ea0ebf8b458a(
    value: typing.Optional[LegacyServiceUserParametersTimeOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6300b5a4945916befd280077b4fdc31db4fc7e13126c2841de4196ef69d616(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488025d51dca0fb0b59f58f34e46dd52befcc5bf61eb43e2ade4f1f7e04fc3af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067e6b646647651ddd5fe721442d9800c28f79f5377ae88f109c9f25dabfbb61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba559f2d2cc1698bd04e807e91f9b4dbcdef3fa1ecf3f45b907f6c2222720cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072b044ba6c36e863df70144b3dbd7f077c6f7efc87a8404e17e59883c874d1c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5d89c585861112ca98a444c19d3364c1e81d91159b567382da2011261739be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2acf758c1f9d134e8723f0ec714bf62c0795d6eaa6721ee6ad3fc134c7ed73be(
    value: typing.Optional[LegacyServiceUserParametersTimestampDayIsAlways24H],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff66b230915186094502b3f9aaf1f3ef56e506351433a420f08f40bb34671cdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48a8389952d910dbda76551aabc4ab86f43d7c247b400ec7882d97083661a7f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b1b6636ca81eb392827ee41bb735a3a5b47266826992682a07dd3d4edda46b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a32a2fc44c295d575dd8145b4a9e9ab47a6515ebca6c60baabc7f6b4f65057(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec6266196aed248e2ef181b1ecea6802f6116d324e46cf668c6fe2fdb13462e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8026adb1dcbec36a807a7515cf4f0a789c76e3faa3ba50a668bdeae4d01d6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__485a4723e84aeb6cd0accb409cc7fa243c58431d01203b33a20b8777f768b980(
    value: typing.Optional[LegacyServiceUserParametersTimestampInputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765e7aefcc9c293fca51a342badbf5b81442d197f05b0665f19ae8b4458ac058(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2799292a394e3d894c035b36299de4136b3051cb9dbc2f8948671593cf5c4d2e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca38f99cc14fce0f712a5c918f00dc78c553df30d5ca3e956096e03a4a68c923(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e58a8cda4120a1ca443702564c70a4077115d56e2c580bdf8fd16b1a56ffd0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff26bf2272c34e14ebc2af338df117583a72336fcdaa7ef326aa9ef60cc9f4c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54438b59f01cc505a1f5f810631789d66e11053330e4775e39727bf1844b3735(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7693c83b2308a18fc639f73bb2c59bd127b1a62102ed63aa8d8495fb831e9b6(
    value: typing.Optional[LegacyServiceUserParametersTimestampLtzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba13d5006f37edb7810e3d1b357fa9f947b7514ec1b4c7710b232a261a46b733(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6814cd65d233fbca077247c0456baf76f176319e0296bfcde99c34760321b5da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489ec0c2f4571f1e0f3b3d6d7a38bd234dcb3c7494bf702d4e6360174dd03e75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def9e33c3e2bb3d2876f2d46c2304977ea35373bd6ab58c9ca42b51c620db30a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c26389fa57c8ff7aea7a030646a046656f1dd1392b2a79a1fa1ccf3cd8323d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e368f004c037e8d17d2d4901b0bd5b50491c1c5fc3d96b5d35408fbcd7c3e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16aaa2b422c3fe94be4aaa29420b83ff6214668c7d35aef97d7bb3a01011f0c(
    value: typing.Optional[LegacyServiceUserParametersTimestampNtzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a26e0d3dc2b517f1d0a3790e99268c804b00a4c984bd8d11844d95f5ca1519(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7553400b6b89f8c560d7509ba28a0c015ec1fcf61ec628a7e119245931aa47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb16f72cc52f1e04656e7bd2a7416ad8f2aa39808accbfdef2a8c8a696e78de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299111b7ecd0fd073eb5219cae3a7cfe2d6c959e7e63d875ce248fac161fb855(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64a6a06ce8fffdb0a873358d768e53069f979dd8e526224555520cceb5671a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c198716554242cd329138c30644af763b2c9e710d02314b02e8cecacb8e6e591(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bba413daa5dc4d985d3694217bf6094989c3b92610ab8181bffd10e901a71ae(
    value: typing.Optional[LegacyServiceUserParametersTimestampOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016512c17a04dc2e385b5d8e0ce57f01d2a7d80bb801664a6cf2aeb67d64ae79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ec78ddc67ba3650ada1705f91863cfceebf7832d4b33151dbb996b6915b17f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c301f3dac85d70774fcbb0036758261ef11b3928dbe47f51e976136460078f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6948ce19ea0e3a620b7a91f9d0fcbc225ff23e86c20e534ae60f84bf25ca763(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc58b46ae67e08682cbaa0f086a2ef7331e77dc1e7d10944a429a0a9e17cb53(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272c95bd87c9116fb4c51b26369c2b58fecc7d44e29dbadf32f5172e0f6c9436(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825d3a11016997d9490008a8966fa401eb947f8185d1ae06b014a34c3003b2b0(
    value: typing.Optional[LegacyServiceUserParametersTimestampTypeMapping],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572a18a1df08b637b4020068615e4a9d5c59823fe146521bc90244e5f68079ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ef352bfa3b8d12474d89f113bc36ddbf76e18a399a8cb91c1ae687911b717c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fae1093f8131c0a8646d7ac6f5c52bdfc31041974612c5f2c4b7ea5017bb0f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c04c82762b767c50c28e9daef0c4239846e53a58c85ec12e6a8ca42da1eb40(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c3c9066129961c7f53dee0bc1548629c820a765c95ddfa9961dee1fce4601a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4ec177707f895a764c23dfc330f7b6d77bae6991d22502f678ca37606fd55e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4496f1b86c37d1cc0fb037f1e8b879965f5471b1eccd601a18e62541a423a66(
    value: typing.Optional[LegacyServiceUserParametersTimestampTzOutputFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c76be2c12c16e07c0678806f11c6d0b84afa57e7bb6f742dd8a072e4ba21dd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18c23ffb0d9a862dbb9d8df69bcd215bb203c6495f9cac5fa95e030a456d4df(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c80aa76570b77d74de998d2037223de90703ef3b20d047a3e419d3cd7f62a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2d4b56be08236b5486febe8c823ab6f0278d4e167a12fbfaa7079726de2f47(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7f393e11f9a5712c6fb0a9e81455c8da99f0de3b2621398c680043b1148c9f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7868cd2f629aabeedd84c5cacd5bd75cd001a266a2cc4e0871dc438032fe98f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e57b3f0449850260069b1c98aa3d00a3de4e58ad11d0d2d9be496684519893(
    value: typing.Optional[LegacyServiceUserParametersTimezone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae859c84c26d69f3f5a1152848fe771bdb69b74ec38e8cbb18843b5a6e5ab357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b57cb0a8dd8f6a53f9ba98c215afa82430d8c67095a74c02957f58c8a749b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e366f8b9ea0e988230176774f9527403ac927a67f42ce7ad2d16fb1a893fc80e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dbc254df7e6e322aa36b967540ab2515900abcd24afb615a0763cd61cec5e2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17cf8e73ca081c38d1b01c59e564d6f5db66b1d20de9f04c5220497ccf2c77ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41fc686f46c1131fea35ade00efee8499150a6389cb1132f6dd057a821648fc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8053b532503c27a8e1a2291e41a24379c246e89f1ffb7f10221521a6d042f4(
    value: typing.Optional[LegacyServiceUserParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb26655a70f561efd86523bf9cc3e38ee1c7d024af83c84bc7369e6ad9406d68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8981d29e1c1a729279b734bd1c020e7c7b2d4b56f7d1de64bd2e547ee8fc46d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a7a435fa6e7ca663423cc138a365c3d108416a3b8df7e9915fd35499f63ec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2249e945d4a53448904a6072a3d4930f14aaee4bc2db83fa0e3baac3b85cadc4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb8d2c4033422d8e3bd5a473abf6470412768b8e37113fb43ab8baae6e25af8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe6368482e167351db50edf9cee6c2ba8bcb7847ca3149f7c5a2bad581962f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40c821edb97a47fca1efd56103e8297e3511f687968cc93df847ca2b5bdef9b(
    value: typing.Optional[LegacyServiceUserParametersTransactionAbortOnError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25311d40b46b6e9d946ae63512e03d3571e1217da6f5725e01ef22d7d410bd8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192f7d71b27903b30650578d78ed2d93f528dd4924f13d1d2df7bd53dfae5d74(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a49e732ca754de20b1c89e524a786e2e563402be6e1ca7bffeee05b9ffa6d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da55c4b0ef9fb3732e974f50a587c03f05c070dbf1219b8c353be0498f0e3c88(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34c93bd0b571edf1aa1f479568798fbf322696083b6c05b89b957f8b9a6ead9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8eabe1e7707603a13251f262833bf47c8ac1b9744fa08a638ccda9e0a3a54c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d7b0cf128ca448648c7f382748b6e8a3bf7509202642dc14193ef3675300e7(
    value: typing.Optional[LegacyServiceUserParametersTransactionDefaultIsolationLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72103b3d050c772867103f5692885b5fa6059a41b38c132d040d834bda0de3b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67668336839ebedbaf024ba1a70e780319d99c8e8d04dd12979edbef23933c7a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572f0171f3a50bf7075644cb057a4e1c7a4afdb25027dbea3188107e253fa1dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766e126f62ea96638689d2770f04289c365a1973402ee13a0fdd1493b058af7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac8a168895550cf8e883bcf6bc0e565e176aa2dd96a6b117498168d756dccc3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00bee63f542f93332931ce641ca20cbca012aad08b7202e36b3631019f5e0ce1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d56687470d5b92be658aa74e2fa37eb67db2d77c562f4ce1b0df630a548e47(
    value: typing.Optional[LegacyServiceUserParametersTwoDigitCenturyStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ede19b74ab017e8c93364ab2026e775a848eb0abc8c622c9b35dfa47b258f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4cc1700485cdcf6dcdb47349bf667deb40af93f7afbd6208e84f9e10110308(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fe4176900853cd2934f6a95036f8a6966dda8b745d2a5718c0af5b4eee0c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd553e95ceb1b5febcfdfd586280ec2c6bc4a59c1802468c94183bfcfec94eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4f92389db871354f3d0b349c76bda49ad548fa1e313b15b6c490a4d64a0ac4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e64a2095447bde886418e0ad73afc10a79098ea5617410fff99d8b5b581a4a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cac12eda053b59cdac9fe8d5a551a6238fe1414560bac3e9ae43348bafa3b4(
    value: typing.Optional[LegacyServiceUserParametersUnsupportedDdlAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f27fc45b5f860fa700e60aee18e11d3643739473430a93bde880a41e3819db7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915c2ef095a7e0f3ec55be32fc599b009b301e5c2ff7b65343877a4854269e9f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2c14f1bdf08e1809c656663056440f97373d578e48c6eef975020f939f6560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe9627c8f40ddddedb16799ef1063e0a72c69e51b4fa1df8a5b21a49254964b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da874565f085348cef41fed3e2881220f99c46756bef8cbf834255580a2deea7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32bda884f0abbaa6336d10465b79885355c1c96108bbab017f0c7690d5a0938c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b6d4c245ece897b85ae56bd61ea9aa1dbb98bb3d6d3a96b703e65ea87e1555(
    value: typing.Optional[LegacyServiceUserParametersUseCachedResult],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd9ef6308364c4cd31322950544970462409338556d1af9a17e298d6cb23ec8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59894af18d472f2fdf32a2d6e9df9e237238fb4ce9bf0798742b990e8d40e16c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1087c22cf5de111ad9c7c1373786999dffacdf9d2589525ff34586b76bb08bfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429ad1fce069dbb1bdcc846031b18c6a2061de6a7673865237b49e94b4439a70(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4fe702b26b3414e75de1fbe8737b56d3f218f9eed3167ff028b78435901c48(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7108062349abfd68c0ba9ecc47ebdebbec99182aefa9352a9b0e55a31433eae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f287ffb47cd3cae38082ad97110e97ba21a430f0e90dbc2e17f27403752806a8(
    value: typing.Optional[LegacyServiceUserParametersWeekOfYearPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da85b84da1155d644263a5987773dac09f56e606d035431a1af08c4332b6a198(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3af8422b28724d7e1220a21cf0160677d62f2e759269fdef4f0d506d2e9761(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2b1733148fbf96b3fe58102cc95db2cb0c09f7955a7de12f5ba00878c38942(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c65513046b77b670c7f417773908417e4cf0cb67b703a4ab625488cf195ba3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae283fb4b6fa56f864e4946a44141347917a5371b40a4c59f62cb6d4ae548d26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcaa2cb64cb1238b4c31a19ab7c1e7da3a1c3d03c11914f63d49c4176184e137(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca7503fca5f669ae6be260483a2ab6d57cb0da0850e36ab408e5430aa8567fe(
    value: typing.Optional[LegacyServiceUserParametersWeekStart],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a88ac73d9ce0bab3617a68f44fb4d19f56a872f8d06146b3521718d4b5c9e8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7efb88ed73b043da578a526b3997dec7fd70d56a5e92140356b6b2961848ed1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c722ede57af8dd23859090b97630d29bb4109196e004ffb5f5b5a170b6d79eeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10d8633b1d7d17749ade9209c766e9fa5c0aca44ecd7bc0daa6d64960ff5ce1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98ce1513160b91325662b9fdf9d637653501747757d12e5884aec7f08f9fc03(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa7035e592dcd83005839d4d4cbb972205b1276686f5769247538a1175a6531(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e682cb278ba1d73e66b32a08f91a02be522aebb45c5d758c58881214068e5096(
    value: typing.Optional[LegacyServiceUserShowOutput],
) -> None:
    """Type checking stubs"""
    pass
