r'''
# `snowflake_current_account`

Refer to the Terraform Registry for docs: [`snowflake_current_account`](https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account).
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


class CurrentAccount(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.currentAccount.CurrentAccount",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account snowflake_current_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        active_python_profiler: typing.Optional[builtins.str] = None,
        allow_client_mfa_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        authentication_policy: typing.Optional[builtins.str] = None,
        autocommit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        base_location_prefix: typing.Optional[builtins.str] = None,
        binary_input_format: typing.Optional[builtins.str] = None,
        binary_output_format: typing.Optional[builtins.str] = None,
        catalog: typing.Optional[builtins.str] = None,
        catalog_sync: typing.Optional[builtins.str] = None,
        client_enable_log_info_statement_parameters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_encryption_key_size: typing.Optional[jsii.Number] = None,
        client_memory_limit: typing.Optional[jsii.Number] = None,
        client_metadata_request_use_connection_ctx: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_metadata_use_session_database: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_prefetch_threads: typing.Optional[jsii.Number] = None,
        client_result_chunk_size: typing.Optional[jsii.Number] = None,
        client_result_column_case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_session_keep_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_session_keep_alive_heartbeat_frequency: typing.Optional[jsii.Number] = None,
        client_timestamp_type_mapping: typing.Optional[builtins.str] = None,
        cortex_enabled_cross_region: typing.Optional[builtins.str] = None,
        cortex_models_allowlist: typing.Optional[builtins.str] = None,
        csv_timestamp_format: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        date_input_format: typing.Optional[builtins.str] = None,
        date_output_format: typing.Optional[builtins.str] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        default_notebook_compute_pool_cpu: typing.Optional[builtins.str] = None,
        default_notebook_compute_pool_gpu: typing.Optional[builtins.str] = None,
        default_null_ordering: typing.Optional[builtins.str] = None,
        default_streamlit_notebook_warehouse: typing.Optional[builtins.str] = None,
        disable_ui_download_button: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_user_privilege_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_automatic_sensitive_data_classification_log: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_egress_cost_optimizer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_identifier_first_login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_internal_stages_privatelink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_tri_secret_and_rekey_opt_out_for_image_repository: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unhandled_exceptions_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unredacted_secure_object_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_network_rules_for_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_table: typing.Optional[builtins.str] = None,
        external_oauth_add_privileged_roles_to_blocked_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_volume: typing.Optional[builtins.str] = None,
        feature_policy: typing.Optional[builtins.str] = None,
        geography_output_format: typing.Optional[builtins.str] = None,
        geometry_output_format: typing.Optional[builtins.str] = None,
        hybrid_table_lock_timeout: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        initial_replication_size_limit_in_tb: typing.Optional[builtins.str] = None,
        jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_indent: typing.Optional[jsii.Number] = None,
        js_treat_integer_as_bigint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        listing_auto_fulfillment_replication_refresh_schedule: typing.Optional[builtins.str] = None,
        lock_timeout: typing.Optional[jsii.Number] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_concurrency_level: typing.Optional[jsii.Number] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
        metric_level: typing.Optional[builtins.str] = None,
        min_data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        multi_statement_count: typing.Optional[jsii.Number] = None,
        network_policy: typing.Optional[builtins.str] = None,
        noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oauth_add_privileged_roles_to_blocked_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        packages_policy: typing.Optional[builtins.str] = None,
        password_policy: typing.Optional[builtins.str] = None,
        periodic_data_rekeying: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pipe_execution_paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_unload_to_inline_url: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_unload_to_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        python_profiler_modules: typing.Optional[builtins.str] = None,
        python_profiler_target_stage: typing.Optional[builtins.str] = None,
        query_tag: typing.Optional[builtins.str] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_storage_integration_for_stage_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_storage_integration_for_stage_operation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_monitor: typing.Optional[builtins.str] = None,
        rows_per_resultset: typing.Optional[jsii.Number] = None,
        s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
        saml_identity_provider: typing.Optional[builtins.str] = None,
        search_path: typing.Optional[builtins.str] = None,
        serverless_task_max_statement_size: typing.Optional[builtins.str] = None,
        serverless_task_min_statement_size: typing.Optional[builtins.str] = None,
        session_policy: typing.Optional[builtins.str] = None,
        simulated_data_sharing_consumer: typing.Optional[builtins.str] = None,
        sso_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        storage_serialization_policy: typing.Optional[builtins.str] = None,
        strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
        task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
        time_input_format: typing.Optional[builtins.str] = None,
        time_output_format: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CurrentAccountTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account snowflake_current_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#abort_detached_query CurrentAccount#abort_detached_query}
        :param active_python_profiler: Sets the profiler to use for the session when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. Valid values are (case-insensitive): ``LINE`` | ``MEMORY``. For more information, check `ACTIVE_PYTHON_PROFILER docs <https://docs.snowflake.com/en/sql-reference/parameters#active-python-profiler>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#active_python_profiler CurrentAccount#active_python_profiler}
        :param allow_client_mfa_caching: Specifies whether an MFA token can be saved in the client-side operating system keystore to promote continuous, secure connectivity without users needing to respond to an MFA prompt at the start of each connection attempt to Snowflake. For details and the list of supported Snowflake-provided clients, see `Using MFA token caching to minimize the number of prompts during authentication — optional. <https://docs.snowflake.com/en/user-guide/security-mfa.html#label-mfa-token-caching>`_ For more information, check `ALLOW_CLIENT_MFA_CACHING docs <https://docs.snowflake.com/en/sql-reference/parameters#allow-client-mfa-caching>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#allow_client_mfa_caching CurrentAccount#allow_client_mfa_caching}
        :param allow_id_token: Specifies whether a connection token can be saved in the client-side operating system keystore to promote continuous, secure connectivity without users needing to enter login credentials at the start of each connection attempt to Snowflake. For details and the list of supported Snowflake-provided clients, see `Using connection caching to minimize the number of prompts for authentication — optional. <https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-use.html#label-browser-based-sso-connection-caching>`_ For more information, check `ALLOW_ID_TOKEN docs <https://docs.snowflake.com/en/sql-reference/parameters#allow-id-token>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#allow_id_token CurrentAccount#allow_id_token}
        :param authentication_policy: Specifies `authentication policy <https://docs.snowflake.com/en/user-guide/authentication-policies>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#authentication_policy CurrentAccount#authentication_policy}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#autocommit CurrentAccount#autocommit}
        :param base_location_prefix: Specifies a prefix for Snowflake to use in the write path for Snowflake-managed Apache Iceberg™ tables. For more information, see `data and metadata directories for Iceberg tables <https://docs.snowflake.com/en/user-guide/tables-iceberg-storage.html#label-tables-iceberg-configure-external-volume-base-location>`_. For more information, check `BASE_LOCATION_PREFIX docs <https://docs.snowflake.com/en/sql-reference/parameters#base-location-prefix>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#base_location_prefix CurrentAccount#base_location_prefix}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. Valid values are (case-insensitive): ``HEX`` | ``BASE64`` | ``UTF8``. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#binary_input_format CurrentAccount#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. Valid values are (case-insensitive): ``HEX`` | ``BASE64``. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#binary_output_format CurrentAccount#binary_output_format}
        :param catalog: Specifies the catalog for Apache Iceberg™ tables. For more information, see the `Iceberg table documentation <https://docs.snowflake.com/en/user-guide/tables-iceberg.html#label-tables-iceberg-catalog-def>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `CATALOG docs <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#catalog CurrentAccount#catalog}
        :param catalog_sync: Specifies the name of your catalog integration for `Snowflake Open Catalog <https://other-docs.snowflake.com/en/opencatalog/overview>`_. Snowflake syncs tables that use the specified catalog integration with your Snowflake Open Catalog account. For more information, see `Sync a Snowflake-managed table with Snowflake Open Catalog <https://docs.snowflake.com/en/user-guide/tables-iceberg-open-catalog-sync>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `CATALOG_SYNC docs <https://docs.snowflake.com/en/sql-reference/parameters#catalog-sync>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#catalog_sync CurrentAccount#catalog_sync}
        :param client_enable_log_info_statement_parameters: Enables users to log the data values bound to `PreparedStatements <https://docs.snowflake.com/en/developer-guide/jdbc/jdbc-api.html#label-jdbc-api-preparedstatement>`_ (`more details <https://docs.snowflake.com/en/sql-reference/parameters#client-enable-log-info-statement-parameters>`_). For more information, check `CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-enable-log-info-statement-parameters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_enable_log_info_statement_parameters CurrentAccount#client_enable_log_info_statement_parameters}
        :param client_encryption_key_size: Specifies the AES encryption key size, in bits, used by Snowflake to encrypt/decrypt files stored on internal stages (for loading/unloading data) when you use the SNOWFLAKE_FULL encryption type. For more information, check `CLIENT_ENCRYPTION_KEY_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-encryption-key-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_encryption_key_size CurrentAccount#client_encryption_key_size}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_memory_limit CurrentAccount#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_metadata_request_use_connection_ctx CurrentAccount#client_metadata_request_use_connection_ctx}
        :param client_metadata_use_session_database: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases to the current database. The narrower search typically returns fewer rows and executes more quickly (`more details on the usage <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-use-session-database>`_). For more information, check `CLIENT_METADATA_USE_SESSION_DATABASE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-use-session-database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_metadata_use_session_database CurrentAccount#client_metadata_use_session_database}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_prefetch_threads CurrentAccount#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_result_chunk_size CurrentAccount#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_result_column_case_insensitive CurrentAccount#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_session_keep_alive CurrentAccount#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_session_keep_alive_heartbeat_frequency CurrentAccount#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. Valid values are (case-insensitive): ``TIMESTAMP_LTZ`` | ``TIMESTAMP_NTZ``. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_timestamp_type_mapping CurrentAccount#client_timestamp_type_mapping}
        :param cortex_enabled_cross_region: Specifies the regions where an inference request may be processed in case the request cannot be processed in the region where request is originally placed. Specifying DISABLED disables cross-region inferencing. For examples and details, see `Cross-region inference <https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference>`_. For more information, check `CORTEX_ENABLED_CROSS_REGION docs <https://docs.snowflake.com/en/sql-reference/parameters#cortex-enabled-cross-region>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#cortex_enabled_cross_region CurrentAccount#cortex_enabled_cross_region}
        :param cortex_models_allowlist: Specifies the models that users in the account can access. Use this parameter to allowlist models for all users in the account. If you need to provide specific users with access beyond what you’ve specified in the allowlist, use role-based access control instead. For more information, see `Model allowlist <https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql.html#label-cortex-llm-allowlist>`_. For more information, check `CORTEX_MODELS_ALLOWLIST docs <https://docs.snowflake.com/en/sql-reference/parameters#cortex-models-allowlist>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#cortex_models_allowlist CurrentAccount#cortex_models_allowlist}
        :param csv_timestamp_format: Specifies the format for TIMESTAMP values in CSV files downloaded from Snowsight. If this parameter is not set, `TIMESTAMP_LTZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-ltz-output-format>`_ will be used for TIMESTAMP_LTZ values, `TIMESTAMP_TZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-tz-output-format>`_ will be used for TIMESTAMP_TZ and `TIMESTAMP_NTZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-ntz-output-format>`_ for TIMESTAMP_NTZ values. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_ or `Download your query results <https://docs.snowflake.com/en/user-guide/ui-snowsight-query.html#label-snowsight-download-query-results>`_. For more information, check `CSV_TIMESTAMP_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#csv-timestamp-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#csv_timestamp_format CurrentAccount#csv_timestamp_format}
        :param data_retention_time_in_days: Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database, schema, or table. For more information, see `Understanding & using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. For more information, check `DATA_RETENTION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#data-retention-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#data_retention_time_in_days CurrentAccount#data_retention_time_in_days}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#date_input_format CurrentAccount#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#date_output_format CurrentAccount#date_output_format}
        :param default_ddl_collation: Sets the default collation used for the following DDL operations: `CREATE TABLE <https://docs.snowflake.com/en/sql-reference/sql/create-table>`_, `ALTER TABLE <https://docs.snowflake.com/en/sql-reference/sql/alter-table>`_ … ADD COLUMN. Setting this parameter forces all subsequently-created columns in the affected objects (table, schema, database, or account) to have the specified collation as the default, unless the collation for the column is explicitly defined in the DDL. For more information, check `DEFAULT_DDL_COLLATION docs <https://docs.snowflake.com/en/sql-reference/parameters#default-ddl-collation>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_ddl_collation CurrentAccount#default_ddl_collation}
        :param default_notebook_compute_pool_cpu: Sets the preferred CPU compute pool used for `Notebooks on CPU Container Runtime <https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU docs <https://docs.snowflake.com/en/sql-reference/parameters#default-notebook-compute-pool-cpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_notebook_compute_pool_cpu CurrentAccount#default_notebook_compute_pool_cpu}
        :param default_notebook_compute_pool_gpu: Sets the preferred GPU compute pool used for `Notebooks on GPU Container Runtime <https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU docs <https://docs.snowflake.com/en/sql-reference/parameters#default-notebook-compute-pool-gpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_notebook_compute_pool_gpu CurrentAccount#default_notebook_compute_pool_gpu}
        :param default_null_ordering: Specifies the default ordering of NULL values in a result set (`more details <https://docs.snowflake.com/en/sql-reference/parameters#default-null-ordering>`_). Valid values are (case-insensitive): ``FIRST`` | ``LAST``. For more information, check `DEFAULT_NULL_ORDERING docs <https://docs.snowflake.com/en/sql-reference/parameters#default-null-ordering>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_null_ordering CurrentAccount#default_null_ordering}
        :param default_streamlit_notebook_warehouse: Specifies the name of the default warehouse to use when creating a notebook. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE docs <https://docs.snowflake.com/en/sql-reference/parameters#default-streamlit-notebook-warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_streamlit_notebook_warehouse CurrentAccount#default_streamlit_notebook_warehouse}
        :param disable_ui_download_button: Controls whether users in an account see a button to download data in Snowsight or the Classic Console, such as a table returned from running a query in a worksheet. If the button to download is hidden in Snowsight or the Classic Console, users can still download or export data using `third-party software <https://docs.snowflake.com/en/user-guide/ecosystem>`_. For more information, check `DISABLE_UI_DOWNLOAD_BUTTON docs <https://docs.snowflake.com/en/sql-reference/parameters#disable-ui-download-button>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#disable_ui_download_button CurrentAccount#disable_ui_download_button}
        :param disable_user_privilege_grants: Controls whether users in an account can grant privileges directly to other users. Disabling user privilege grants (that is, setting DISABLE_USER_PRIVILEGE_GRANTS to TRUE) does not affect existing grants to users. Existing grants to users continue to confer privileges to those users. For more information, see `GRANT … TO USER <https://docs.snowflake.com/en/sql-reference/sql/grant-privilege-user>`_. For more information, check `DISABLE_USER_PRIVILEGE_GRANTS docs <https://docs.snowflake.com/en/sql-reference/parameters#disable-user-privilege-grants>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#disable_user_privilege_grants CurrentAccount#disable_user_privilege_grants}
        :param enable_automatic_sensitive_data_classification_log: Controls whether events from `automatic sensitive data classification <https://docs.snowflake.com/en/user-guide/classify-auto>`_ are logged in the user event table. For more information, check `ENABLE_AUTOMATIC_SENSITIVE_DATA_CLASSIFICATION_LOG docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-automatic-sensitive-data-classification-log>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_automatic_sensitive_data_classification_log CurrentAccount#enable_automatic_sensitive_data_classification_log}
        :param enable_egress_cost_optimizer: Enables or disables the Listing Cross-cloud auto-fulfillment Egress cost optimizer. For more information, check `ENABLE_EGRESS_COST_OPTIMIZER docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-egress-cost-optimizer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_egress_cost_optimizer CurrentAccount#enable_egress_cost_optimizer}
        :param enable_identifier_first_login: Determines the login flow for users. When enabled, Snowflake prompts users for their username or email address before presenting authentication methods. For details, see `Identifier-first login <https://docs.snowflake.com/en/user-guide/identifier-first-login>`_. For more information, check `ENABLE_IDENTIFIER_FIRST_LOGIN docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-identifier-first-login>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_identifier_first_login CurrentAccount#enable_identifier_first_login}
        :param enable_internal_stages_privatelink: Specifies whether the `SYSTEM$GET_PRIVATELINK_CONFIG <https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_config>`_ function returns the private-internal-stages key in the query result. The corresponding value in the query result is used during the configuration process for private connectivity to internal stages. For more information, check `ENABLE_INTERNAL_STAGES_PRIVATELINK docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-internal-stages-privatelink>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_internal_stages_privatelink CurrentAccount#enable_internal_stages_privatelink}
        :param enable_tri_secret_and_rekey_opt_out_for_image_repository: Specifies choice for the `image repository <https://docs.snowflake.com/en/developer-guide/snowpark-container-services/working-with-registry-repository.html#label-registry-and-repository-image-repository>`_ to opt out of Tri-Secret Secure and `Periodic rekeying <https://docs.snowflake.com/en/user-guide/security-encryption-manage.html#label-periodic-rekeying>`_. For more information, check `ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_IMAGE_REPOSITORY docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-tri-secret-and-rekey-opt-out-for-image-repository>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_tri_secret_and_rekey_opt_out_for_image_repository CurrentAccount#enable_tri_secret_and_rekey_opt_out_for_image_repository}
        :param enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage: Specifies the choice for the `Snowpark Container Services block storage volume <https://docs.snowflake.com/en/developer-guide/snowpark-container-services/block-storage-volume>`_ to opt out of Tri-Secret Secure and `Periodic rekeying <https://docs.snowflake.com/en/user-guide/security-encryption-manage.html#label-periodic-rekeying>`_. For more information, check `ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_SPCS_BLOCK_STORAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-tri-secret-and-rekey-opt-out-for-spcs-block-storage>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage CurrentAccount#enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage}
        :param enable_unhandled_exceptions_reporting: Specifies whether Snowflake may capture – in an event table – log messages or trace event data for unhandled exceptions in procedure or UDF handler code. For more information, see `Capturing messages from unhandled exceptions <https://docs.snowflake.com/en/developer-guide/logging-tracing/unhandled-exception-messages>`_. For more information, check `ENABLE_UNHANDLED_EXCEPTIONS_REPORTING docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unhandled-exceptions-reporting>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unhandled_exceptions_reporting CurrentAccount#enable_unhandled_exceptions_reporting}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unload_physical_type_optimization CurrentAccount#enable_unload_physical_type_optimization}
        :param enable_unredacted_query_syntax_error: Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error. If FALSE, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to TRUE for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unredacted_query_syntax_error CurrentAccount#enable_unredacted_query_syntax_error}
        :param enable_unredacted_secure_object_error: Controls whether error messages related to secure objects are redacted in metadata. For more information, see `Secure objects: Redaction of information in error messages <https://docs.snowflake.com/en/release-notes/bcr-bundles/un-bundled/bcr-1858>`_. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_SECURE_OBJECT_ERROR parameter. When using the ALTER USER command to set the parameter to TRUE for a particular user, modify the user that you want to see the redacted error messages in metadata, not the user who caused the error. For more information, check `ENABLE_UNREDACTED_SECURE_OBJECT_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-secure-object-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unredacted_secure_object_error CurrentAccount#enable_unredacted_secure_object_error}
        :param enforce_network_rules_for_internal_stages: Specifies whether a network policy that uses network rules can restrict access to AWS internal stages. This parameter has no effect on network policies that do not use network rules. This account-level parameter affects both account-level and user-level network policies. For details about using network policies and network rules to restrict access to AWS internal stages, including the use of this parameter, see `Protecting internal stages on AWS <https://docs.snowflake.com/en/user-guide/network-policies.html#label-network-policies-rules-stages>`_. For more information, check `ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#enforce-network-rules-for-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enforce_network_rules_for_internal_stages CurrentAccount#enforce_network_rules_for_internal_stages}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#error_on_nondeterministic_merge CurrentAccount#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#error_on_nondeterministic_update CurrentAccount#error_on_nondeterministic_update}
        :param event_table: Specifies the name of the event table for logging messages from stored procedures and UDFs contained by the object with which the event table is associated. Associating an event table with a database is available in `Enterprise Edition or higher <https://docs.snowflake.com/en/user-guide/intro-editions>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `EVENT_TABLE docs <https://docs.snowflake.com/en/sql-reference/parameters#event-table>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#event_table CurrentAccount#event_table}
        :param external_oauth_add_privileged_roles_to_blocked_list: Determines whether the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles can be used as the primary role when creating a Snowflake session based on the access token from the External OAuth authorization server. For more information, check `EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST docs <https://docs.snowflake.com/en/sql-reference/parameters#external-oauth-add-privileged-roles-to-blocked-list>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#external_oauth_add_privileged_roles_to_blocked_list CurrentAccount#external_oauth_add_privileged_roles_to_blocked_list}
        :param external_volume: Specifies the external volume for Apache Iceberg™ tables. For more information, see the `Iceberg table documentation <https://docs.snowflake.com/en/user-guide/tables-iceberg.html#label-tables-iceberg-external-volume-def>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `EXTERNAL_VOLUME docs <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#external_volume CurrentAccount#external_volume}
        :param feature_policy: Specifies `feature policy <https://docs.snowflake.com/en/developer-guide/native-apps/ui-consumer-feature-policies>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#feature_policy CurrentAccount#feature_policy}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. Valid values are (case-insensitive): ``GeoJSON`` | ``WKT`` | ``WKB`` | ``EWKT`` | ``EWKB``. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#geography_output_format CurrentAccount#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. Valid values are (case-insensitive): ``GeoJSON`` | ``WKT`` | ``WKB`` | ``EWKT`` | ``EWKB``. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#geometry_output_format CurrentAccount#geometry_output_format}
        :param hybrid_table_lock_timeout: Number of seconds to wait while trying to acquire row-level locks on a hybrid table, before timing out and aborting the statement. For more information, check `HYBRID_TABLE_LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#hybrid-table-lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#hybrid_table_lock_timeout CurrentAccount#hybrid_table_lock_timeout}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#id CurrentAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_replication_size_limit_in_tb: Sets the maximum estimated size limit for the initial replication of a primary database to a secondary database (in TB). Set this parameter on any account that stores a secondary database. This size limit helps prevent accounts from accidentally incurring large database replication charges. To remove the size limit, set the value to 0.0. It is required to pass numbers with scale of at least 1 (e.g. 20.5, 32.25, 33.333, etc.). For more information, check `INITIAL_REPLICATION_SIZE_LIMIT_IN_TB docs <https://docs.snowflake.com/en/sql-reference/parameters#initial-replication-size-limit-in-tb>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#initial_replication_size_limit_in_tb CurrentAccount#initial_replication_size_limit_in_tb}
        :param jdbc_treat_decimal_as_int: Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_treat_decimal_as_int CurrentAccount#jdbc_treat_decimal_as_int}
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values (`more details <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_). For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_treat_timestamp_ntz_as_utc CurrentAccount#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_use_session_timezone CurrentAccount#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#json_indent CurrentAccount#json_indent}
        :param js_treat_integer_as_bigint: Specifies how the Snowflake Node.js Driver processes numeric columns that have a scale of zero (0), for example INTEGER or NUMBER(p, 0). For more information, check `JS_TREAT_INTEGER_AS_BIGINT docs <https://docs.snowflake.com/en/sql-reference/parameters#js-treat-integer-as-bigint>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#js_treat_integer_as_bigint CurrentAccount#js_treat_integer_as_bigint}
        :param listing_auto_fulfillment_replication_refresh_schedule: Sets the time interval used to refresh the application package based data products to other regions. For more information, check `LISTING_AUTO_FULFILLMENT_REPLICATION_REFRESH_SCHEDULE docs <https://docs.snowflake.com/en/sql-reference/parameters#listing-auto-fulfillment-replication-refresh-schedule>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#listing_auto_fulfillment_replication_refresh_schedule CurrentAccount#listing_auto_fulfillment_replication_refresh_schedule}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#lock_timeout CurrentAccount#lock_timeout}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting levels for logging, metrics, and tracing <https://docs.snowflake.com/en/developer-guide/logging-tracing/telemetry-levels>`_. Valid values are (case-insensitive): ``TRACE`` | ``DEBUG`` | ``INFO`` | ``WARN`` | ``ERROR`` | ``FATAL`` | ``OFF``. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#log_level CurrentAccount#log_level}
        :param max_concurrency_level: Specifies the concurrency level for SQL statements (that is, queries and DML) executed by a warehouse (`more details <https://docs.snowflake.com/en/sql-reference/parameters#max-concurrency-level>`_). For more information, check `MAX_CONCURRENCY_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#max-concurrency-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#max_concurrency_level CurrentAccount#max_concurrency_level}
        :param max_data_extension_time_in_days: Maximum number of days Snowflake can extend the data retention period for tables to prevent streams on the tables from becoming stale. By default, if the `DATA_RETENTION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters#data-retention-time-in-days>`_ setting for a source table is less than 14 days, and a stream has not been consumed, Snowflake temporarily extends this period to the stream’s offset, up to a maximum of 14 days, regardless of the `Snowflake Edition <https://docs.snowflake.com/en/user-guide/intro-editions>`_ for your account. The MAX_DATA_EXTENSION_TIME_IN_DAYS parameter enables you to limit this automatic extension period to control storage costs for data retention or for compliance reasons. For more information, check `MAX_DATA_EXTENSION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#max-data-extension-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#max_data_extension_time_in_days CurrentAccount#max_data_extension_time_in_days}
        :param metric_level: Controls how metrics data is ingested into the event table. For more information about metric levels, see `Setting levels for logging, metrics, and tracing <https://docs.snowflake.com/en/developer-guide/logging-tracing/telemetry-levels>`_. Valid values are (case-insensitive): ``ALL`` | ``NONE``. For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#metric_level CurrentAccount#metric_level}
        :param min_data_retention_time_in_days: Minimum number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on an object. If a minimum number of days for data retention is set on an account, the data retention period for an object is determined by MAX(`DATA_RETENTION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters#label-data-retention-time-in-days>`_, MIN_DATA_RETENTION_TIME_IN_DAYS). For more information, check `MIN_DATA_RETENTION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#min-data-retention-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#min_data_retention_time_in_days CurrentAccount#min_data_retention_time_in_days}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#multi_statement_count CurrentAccount#multi_statement_count}
        :param network_policy: Specifies the network policy to enforce for your account. Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#network_policy CurrentAccount#network_policy}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#noorder_sequence_as_default CurrentAccount#noorder_sequence_as_default}
        :param oauth_add_privileged_roles_to_blocked_list: Determines whether the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles can be used as the primary role when creating a Snowflake session based on the access token from Snowflake’s authorization server. For more information, check `OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST docs <https://docs.snowflake.com/en/sql-reference/parameters#oauth-add-privileged-roles-to-blocked-list>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#oauth_add_privileged_roles_to_blocked_list CurrentAccount#oauth_add_privileged_roles_to_blocked_list}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#odbc_treat_decimal_as_int CurrentAccount#odbc_treat_decimal_as_int}
        :param packages_policy: Specifies `packages policy <https://docs.snowflake.com/en/developer-guide/udf/python/packages-policy>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#packages_policy CurrentAccount#packages_policy}
        :param password_policy: Specifies `password policy <https://docs.snowflake.com/en/user-guide/password-authentication#label-using-password-policies>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#password_policy CurrentAccount#password_policy}
        :param periodic_data_rekeying: It enables/disables re-encryption of table data with new keys on a yearly basis to provide additional levels of data protection (`more details <https://docs.snowflake.com/en/sql-reference/parameters#periodic-data-rekeying>`_). For more information, check `PERIODIC_DATA_REKEYING docs <https://docs.snowflake.com/en/sql-reference/parameters#periodic-data-rekeying>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#periodic_data_rekeying CurrentAccount#periodic_data_rekeying}
        :param pipe_execution_paused: Specifies whether to pause a running pipe, primarily in preparation for transferring ownership of the pipe to a different role (`more details <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_). For more information, check `PIPE_EXECUTION_PAUSED docs <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#pipe_execution_paused CurrentAccount#pipe_execution_paused}
        :param prevent_unload_to_inline_url: Specifies whether to prevent ad hoc data unload operations to external cloud storage locations (that is, `COPY INTO location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements that specify the cloud storage URL and access settings directly in the statement). For an example, see `Unloading data from a table directly to files in an external location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html#label-copy-into-location-ad-hoc>`_. For more information, check `PREVENT_UNLOAD_TO_INLINE_URL docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-inline-url>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#prevent_unload_to_inline_url CurrentAccount#prevent_unload_to_inline_url}
        :param prevent_unload_to_internal_stages: Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#prevent_unload_to_internal_stages CurrentAccount#prevent_unload_to_internal_stages}
        :param python_profiler_modules: Specifies the list of Python modules to include in a report when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. For more information, check `PYTHON_PROFILER_MODULES docs <https://docs.snowflake.com/en/sql-reference/parameters#python-profiler-modules>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#python_profiler_modules CurrentAccount#python_profiler_modules}
        :param python_profiler_target_stage: Specifies the fully-qualified name of the stage in which to save a report when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. For more information, check `PYTHON_PROFILER_TARGET_STAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#python-profiler-target-stage>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#python_profiler_target_stage CurrentAccount#python_profiler_target_stage}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#query_tag CurrentAccount#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#quoted_identifiers_ignore_case CurrentAccount#quoted_identifiers_ignore_case}
        :param replace_invalid_characters: Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for `Apache Iceberg™ tables <https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table>`_ that use an external catalog. For more information, check `REPLACE_INVALID_CHARACTERS docs <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#replace_invalid_characters CurrentAccount#replace_invalid_characters}
        :param require_storage_integration_for_stage_creation: Specifies whether to require a storage integration object as cloud credentials when creating a named external stage (using `CREATE STAGE <https://docs.snowflake.com/en/sql-reference/sql/create-stage>`_) to access a private cloud storage location. For more information, check `REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION docs <https://docs.snowflake.com/en/sql-reference/parameters#require-storage-integration-for-stage-creation>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#require_storage_integration_for_stage_creation CurrentAccount#require_storage_integration_for_stage_creation}
        :param require_storage_integration_for_stage_operation: Specifies whether to require using a named external stage that references a storage integration object as cloud credentials when loading data from or unloading data to a private cloud storage location. For more information, check `REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION docs <https://docs.snowflake.com/en/sql-reference/parameters#require-storage-integration-for-stage-operation>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#require_storage_integration_for_stage_operation CurrentAccount#require_storage_integration_for_stage_operation}
        :param resource_monitor: Parameter that specifies the name of the resource monitor used to control all virtual warehouses created in the account. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#resource_monitor CurrentAccount#resource_monitor}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#rows_per_resultset CurrentAccount#rows_per_resultset}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#s3_stage_vpce_dns_name CurrentAccount#s3_stage_vpce_dns_name}
        :param saml_identity_provider: Enables federated authentication. This deprecated parameter enables federated authentication (`more details <https://docs.snowflake.com/en/sql-reference/parameters#saml-identity-provider>`_). For more information, check `SAML_IDENTITY_PROVIDER docs <https://docs.snowflake.com/en/sql-reference/parameters#saml-identity-provider>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#saml_identity_provider CurrentAccount#saml_identity_provider}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#search_path CurrentAccount#search_path}
        :param serverless_task_max_statement_size: Specifies the maximum allowed warehouse size for `Serverless tasks <https://docs.snowflake.com/en/user-guide/tasks-intro.html#label-tasks-compute-resources-serverless>`_. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `SERVERLESS_TASK_MAX_STATEMENT_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#serverless-task-max-statement-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#serverless_task_max_statement_size CurrentAccount#serverless_task_max_statement_size}
        :param serverless_task_min_statement_size: Specifies the minimum allowed warehouse size for `Serverless tasks <https://docs.snowflake.com/en/user-guide/tasks-intro.html#label-tasks-compute-resources-serverless>`_. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `SERVERLESS_TASK_MIN_STATEMENT_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#serverless-task-min-statement-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#serverless_task_min_statement_size CurrentAccount#serverless_task_min_statement_size}
        :param session_policy: Specifies `session policy <https://docs.snowflake.com/en/user-guide/session-policies-using>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#session_policy CurrentAccount#session_policy}
        :param simulated_data_sharing_consumer: Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views. When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#simulated_data_sharing_consumer CurrentAccount#simulated_data_sharing_consumer}
        :param sso_login_page: This deprecated parameter disables preview mode for testing SSO (after enabling federated authentication) before rolling it out to users. For more information, check `SSO_LOGIN_PAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#sso-login-page>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#sso_login_page CurrentAccount#sso_login_page}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#statement_queued_timeout_in_seconds CurrentAccount#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#statement_timeout_in_seconds CurrentAccount#statement_timeout_in_seconds}
        :param storage_serialization_policy: Specifies the storage serialization policy for Snowflake-managed `Apache Iceberg™ tables <https://docs.snowflake.com/en/user-guide/tables-iceberg>`_. Valid values are (case-insensitive): ``COMPATIBLE`` | ``OPTIMIZED``. For more information, check `STORAGE_SERIALIZATION_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#storage_serialization_policy CurrentAccount#storage_serialization_policy}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#strict_json_output CurrentAccount#strict_json_output}
        :param suspend_task_after_num_failures: Specifies the number of consecutive failed task runs after which the current task is suspended automatically. The default is 0 (no automatic suspension). For more information, check `SUSPEND_TASK_AFTER_NUM_FAILURES docs <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#suspend_task_after_num_failures CurrentAccount#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Specifies the number of automatic task graph retry attempts. If any task graphs complete in a FAILED state, Snowflake can automatically retry the task graphs from the last task in the graph that failed. For more information, check `TASK_AUTO_RETRY_ATTEMPTS docs <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#task_auto_retry_attempts CurrentAccount#task_auto_retry_attempts}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#time_input_format CurrentAccount#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#time_output_format CurrentAccount#time_output_format}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timeouts CurrentAccount#timeouts}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_day_is_always_24h CurrentAccount#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_input_format CurrentAccount#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_ltz_output_format CurrentAccount#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_ntz_output_format CurrentAccount#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_output_format CurrentAccount#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. Valid values are (case-insensitive): ``TIMESTAMP_LTZ`` | ``TIMESTAMP_NTZ`` | ``TIMESTAMP_TZ``. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_type_mapping CurrentAccount#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_tz_output_format CurrentAccount#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timezone CurrentAccount#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. Valid values are (case-insensitive): ``ALWAYS`` | ``ON_EVENT`` | ``PROPAGATE`` | ``OFF``. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#trace_level CurrentAccount#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#transaction_abort_on_error CurrentAccount#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. Valid values are (case-insensitive): ``READ COMMITTED``. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#transaction_default_isolation_level CurrentAccount#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#two_digit_century_start CurrentAccount#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#unsupported_ddl_action CurrentAccount#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#use_cached_result CurrentAccount#use_cached_result}
        :param user_task_managed_initial_warehouse_size: Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size. Once a task has successfully completed a few runs, Snowflake ignores this parameter setting. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_managed_initial_warehouse_size CurrentAccount#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds For more information, check `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-minimum-trigger-interval-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_minimum_trigger_interval_in_seconds CurrentAccount#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: Specifies the time limit on a single run of the task before it times out (in milliseconds). For more information, check `USER_TASK_TIMEOUT_MS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_timeout_ms CurrentAccount#user_task_timeout_ms}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#week_of_year_policy CurrentAccount#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#week_start CurrentAccount#week_start}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f566e7fa58e1c5c8bb6ae78cffb5d10b4382c9e69d7b4f44ed253bb80bd6e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CurrentAccountConfig(
            abort_detached_query=abort_detached_query,
            active_python_profiler=active_python_profiler,
            allow_client_mfa_caching=allow_client_mfa_caching,
            allow_id_token=allow_id_token,
            authentication_policy=authentication_policy,
            autocommit=autocommit,
            base_location_prefix=base_location_prefix,
            binary_input_format=binary_input_format,
            binary_output_format=binary_output_format,
            catalog=catalog,
            catalog_sync=catalog_sync,
            client_enable_log_info_statement_parameters=client_enable_log_info_statement_parameters,
            client_encryption_key_size=client_encryption_key_size,
            client_memory_limit=client_memory_limit,
            client_metadata_request_use_connection_ctx=client_metadata_request_use_connection_ctx,
            client_metadata_use_session_database=client_metadata_use_session_database,
            client_prefetch_threads=client_prefetch_threads,
            client_result_chunk_size=client_result_chunk_size,
            client_result_column_case_insensitive=client_result_column_case_insensitive,
            client_session_keep_alive=client_session_keep_alive,
            client_session_keep_alive_heartbeat_frequency=client_session_keep_alive_heartbeat_frequency,
            client_timestamp_type_mapping=client_timestamp_type_mapping,
            cortex_enabled_cross_region=cortex_enabled_cross_region,
            cortex_models_allowlist=cortex_models_allowlist,
            csv_timestamp_format=csv_timestamp_format,
            data_retention_time_in_days=data_retention_time_in_days,
            date_input_format=date_input_format,
            date_output_format=date_output_format,
            default_ddl_collation=default_ddl_collation,
            default_notebook_compute_pool_cpu=default_notebook_compute_pool_cpu,
            default_notebook_compute_pool_gpu=default_notebook_compute_pool_gpu,
            default_null_ordering=default_null_ordering,
            default_streamlit_notebook_warehouse=default_streamlit_notebook_warehouse,
            disable_ui_download_button=disable_ui_download_button,
            disable_user_privilege_grants=disable_user_privilege_grants,
            enable_automatic_sensitive_data_classification_log=enable_automatic_sensitive_data_classification_log,
            enable_egress_cost_optimizer=enable_egress_cost_optimizer,
            enable_identifier_first_login=enable_identifier_first_login,
            enable_internal_stages_privatelink=enable_internal_stages_privatelink,
            enable_tri_secret_and_rekey_opt_out_for_image_repository=enable_tri_secret_and_rekey_opt_out_for_image_repository,
            enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage=enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage,
            enable_unhandled_exceptions_reporting=enable_unhandled_exceptions_reporting,
            enable_unload_physical_type_optimization=enable_unload_physical_type_optimization,
            enable_unredacted_query_syntax_error=enable_unredacted_query_syntax_error,
            enable_unredacted_secure_object_error=enable_unredacted_secure_object_error,
            enforce_network_rules_for_internal_stages=enforce_network_rules_for_internal_stages,
            error_on_nondeterministic_merge=error_on_nondeterministic_merge,
            error_on_nondeterministic_update=error_on_nondeterministic_update,
            event_table=event_table,
            external_oauth_add_privileged_roles_to_blocked_list=external_oauth_add_privileged_roles_to_blocked_list,
            external_volume=external_volume,
            feature_policy=feature_policy,
            geography_output_format=geography_output_format,
            geometry_output_format=geometry_output_format,
            hybrid_table_lock_timeout=hybrid_table_lock_timeout,
            id=id,
            initial_replication_size_limit_in_tb=initial_replication_size_limit_in_tb,
            jdbc_treat_decimal_as_int=jdbc_treat_decimal_as_int,
            jdbc_treat_timestamp_ntz_as_utc=jdbc_treat_timestamp_ntz_as_utc,
            jdbc_use_session_timezone=jdbc_use_session_timezone,
            json_indent=json_indent,
            js_treat_integer_as_bigint=js_treat_integer_as_bigint,
            listing_auto_fulfillment_replication_refresh_schedule=listing_auto_fulfillment_replication_refresh_schedule,
            lock_timeout=lock_timeout,
            log_level=log_level,
            max_concurrency_level=max_concurrency_level,
            max_data_extension_time_in_days=max_data_extension_time_in_days,
            metric_level=metric_level,
            min_data_retention_time_in_days=min_data_retention_time_in_days,
            multi_statement_count=multi_statement_count,
            network_policy=network_policy,
            noorder_sequence_as_default=noorder_sequence_as_default,
            oauth_add_privileged_roles_to_blocked_list=oauth_add_privileged_roles_to_blocked_list,
            odbc_treat_decimal_as_int=odbc_treat_decimal_as_int,
            packages_policy=packages_policy,
            password_policy=password_policy,
            periodic_data_rekeying=periodic_data_rekeying,
            pipe_execution_paused=pipe_execution_paused,
            prevent_unload_to_inline_url=prevent_unload_to_inline_url,
            prevent_unload_to_internal_stages=prevent_unload_to_internal_stages,
            python_profiler_modules=python_profiler_modules,
            python_profiler_target_stage=python_profiler_target_stage,
            query_tag=query_tag,
            quoted_identifiers_ignore_case=quoted_identifiers_ignore_case,
            replace_invalid_characters=replace_invalid_characters,
            require_storage_integration_for_stage_creation=require_storage_integration_for_stage_creation,
            require_storage_integration_for_stage_operation=require_storage_integration_for_stage_operation,
            resource_monitor=resource_monitor,
            rows_per_resultset=rows_per_resultset,
            s3_stage_vpce_dns_name=s3_stage_vpce_dns_name,
            saml_identity_provider=saml_identity_provider,
            search_path=search_path,
            serverless_task_max_statement_size=serverless_task_max_statement_size,
            serverless_task_min_statement_size=serverless_task_min_statement_size,
            session_policy=session_policy,
            simulated_data_sharing_consumer=simulated_data_sharing_consumer,
            sso_login_page=sso_login_page,
            statement_queued_timeout_in_seconds=statement_queued_timeout_in_seconds,
            statement_timeout_in_seconds=statement_timeout_in_seconds,
            storage_serialization_policy=storage_serialization_policy,
            strict_json_output=strict_json_output,
            suspend_task_after_num_failures=suspend_task_after_num_failures,
            task_auto_retry_attempts=task_auto_retry_attempts,
            time_input_format=time_input_format,
            time_output_format=time_output_format,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a CurrentAccount resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CurrentAccount to import.
        :param import_from_id: The id of the existing CurrentAccount that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CurrentAccount to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8092f7b9c0214c6775bed7e05149e54603a0f64373a4674bb195b682c8145688)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#create CurrentAccount#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#delete CurrentAccount#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#read CurrentAccount#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#update CurrentAccount#update}.
        '''
        value = CurrentAccountTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAbortDetachedQuery")
    def reset_abort_detached_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbortDetachedQuery", []))

    @jsii.member(jsii_name="resetActivePythonProfiler")
    def reset_active_python_profiler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActivePythonProfiler", []))

    @jsii.member(jsii_name="resetAllowClientMfaCaching")
    def reset_allow_client_mfa_caching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowClientMfaCaching", []))

    @jsii.member(jsii_name="resetAllowIdToken")
    def reset_allow_id_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowIdToken", []))

    @jsii.member(jsii_name="resetAuthenticationPolicy")
    def reset_authentication_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationPolicy", []))

    @jsii.member(jsii_name="resetAutocommit")
    def reset_autocommit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutocommit", []))

    @jsii.member(jsii_name="resetBaseLocationPrefix")
    def reset_base_location_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseLocationPrefix", []))

    @jsii.member(jsii_name="resetBinaryInputFormat")
    def reset_binary_input_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryInputFormat", []))

    @jsii.member(jsii_name="resetBinaryOutputFormat")
    def reset_binary_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryOutputFormat", []))

    @jsii.member(jsii_name="resetCatalog")
    def reset_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalog", []))

    @jsii.member(jsii_name="resetCatalogSync")
    def reset_catalog_sync(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalogSync", []))

    @jsii.member(jsii_name="resetClientEnableLogInfoStatementParameters")
    def reset_client_enable_log_info_statement_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientEnableLogInfoStatementParameters", []))

    @jsii.member(jsii_name="resetClientEncryptionKeySize")
    def reset_client_encryption_key_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientEncryptionKeySize", []))

    @jsii.member(jsii_name="resetClientMemoryLimit")
    def reset_client_memory_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientMemoryLimit", []))

    @jsii.member(jsii_name="resetClientMetadataRequestUseConnectionCtx")
    def reset_client_metadata_request_use_connection_ctx(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientMetadataRequestUseConnectionCtx", []))

    @jsii.member(jsii_name="resetClientMetadataUseSessionDatabase")
    def reset_client_metadata_use_session_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientMetadataUseSessionDatabase", []))

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

    @jsii.member(jsii_name="resetCortexEnabledCrossRegion")
    def reset_cortex_enabled_cross_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCortexEnabledCrossRegion", []))

    @jsii.member(jsii_name="resetCortexModelsAllowlist")
    def reset_cortex_models_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCortexModelsAllowlist", []))

    @jsii.member(jsii_name="resetCsvTimestampFormat")
    def reset_csv_timestamp_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCsvTimestampFormat", []))

    @jsii.member(jsii_name="resetDataRetentionTimeInDays")
    def reset_data_retention_time_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataRetentionTimeInDays", []))

    @jsii.member(jsii_name="resetDateInputFormat")
    def reset_date_input_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateInputFormat", []))

    @jsii.member(jsii_name="resetDateOutputFormat")
    def reset_date_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateOutputFormat", []))

    @jsii.member(jsii_name="resetDefaultDdlCollation")
    def reset_default_ddl_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDdlCollation", []))

    @jsii.member(jsii_name="resetDefaultNotebookComputePoolCpu")
    def reset_default_notebook_compute_pool_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultNotebookComputePoolCpu", []))

    @jsii.member(jsii_name="resetDefaultNotebookComputePoolGpu")
    def reset_default_notebook_compute_pool_gpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultNotebookComputePoolGpu", []))

    @jsii.member(jsii_name="resetDefaultNullOrdering")
    def reset_default_null_ordering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultNullOrdering", []))

    @jsii.member(jsii_name="resetDefaultStreamlitNotebookWarehouse")
    def reset_default_streamlit_notebook_warehouse(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultStreamlitNotebookWarehouse", []))

    @jsii.member(jsii_name="resetDisableUiDownloadButton")
    def reset_disable_ui_download_button(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUiDownloadButton", []))

    @jsii.member(jsii_name="resetDisableUserPrivilegeGrants")
    def reset_disable_user_privilege_grants(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUserPrivilegeGrants", []))

    @jsii.member(jsii_name="resetEnableAutomaticSensitiveDataClassificationLog")
    def reset_enable_automatic_sensitive_data_classification_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAutomaticSensitiveDataClassificationLog", []))

    @jsii.member(jsii_name="resetEnableEgressCostOptimizer")
    def reset_enable_egress_cost_optimizer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEgressCostOptimizer", []))

    @jsii.member(jsii_name="resetEnableIdentifierFirstLogin")
    def reset_enable_identifier_first_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIdentifierFirstLogin", []))

    @jsii.member(jsii_name="resetEnableInternalStagesPrivatelink")
    def reset_enable_internal_stages_privatelink(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableInternalStagesPrivatelink", []))

    @jsii.member(jsii_name="resetEnableTriSecretAndRekeyOptOutForImageRepository")
    def reset_enable_tri_secret_and_rekey_opt_out_for_image_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableTriSecretAndRekeyOptOutForImageRepository", []))

    @jsii.member(jsii_name="resetEnableTriSecretAndRekeyOptOutForSpcsBlockStorage")
    def reset_enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableTriSecretAndRekeyOptOutForSpcsBlockStorage", []))

    @jsii.member(jsii_name="resetEnableUnhandledExceptionsReporting")
    def reset_enable_unhandled_exceptions_reporting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUnhandledExceptionsReporting", []))

    @jsii.member(jsii_name="resetEnableUnloadPhysicalTypeOptimization")
    def reset_enable_unload_physical_type_optimization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUnloadPhysicalTypeOptimization", []))

    @jsii.member(jsii_name="resetEnableUnredactedQuerySyntaxError")
    def reset_enable_unredacted_query_syntax_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUnredactedQuerySyntaxError", []))

    @jsii.member(jsii_name="resetEnableUnredactedSecureObjectError")
    def reset_enable_unredacted_secure_object_error(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableUnredactedSecureObjectError", []))

    @jsii.member(jsii_name="resetEnforceNetworkRulesForInternalStages")
    def reset_enforce_network_rules_for_internal_stages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceNetworkRulesForInternalStages", []))

    @jsii.member(jsii_name="resetErrorOnNondeterministicMerge")
    def reset_error_on_nondeterministic_merge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOnNondeterministicMerge", []))

    @jsii.member(jsii_name="resetErrorOnNondeterministicUpdate")
    def reset_error_on_nondeterministic_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetErrorOnNondeterministicUpdate", []))

    @jsii.member(jsii_name="resetEventTable")
    def reset_event_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventTable", []))

    @jsii.member(jsii_name="resetExternalOauthAddPrivilegedRolesToBlockedList")
    def reset_external_oauth_add_privileged_roles_to_blocked_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalOauthAddPrivilegedRolesToBlockedList", []))

    @jsii.member(jsii_name="resetExternalVolume")
    def reset_external_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalVolume", []))

    @jsii.member(jsii_name="resetFeaturePolicy")
    def reset_feature_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeaturePolicy", []))

    @jsii.member(jsii_name="resetGeographyOutputFormat")
    def reset_geography_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeographyOutputFormat", []))

    @jsii.member(jsii_name="resetGeometryOutputFormat")
    def reset_geometry_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeometryOutputFormat", []))

    @jsii.member(jsii_name="resetHybridTableLockTimeout")
    def reset_hybrid_table_lock_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHybridTableLockTimeout", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitialReplicationSizeLimitInTb")
    def reset_initial_replication_size_limit_in_tb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialReplicationSizeLimitInTb", []))

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

    @jsii.member(jsii_name="resetJsTreatIntegerAsBigint")
    def reset_js_treat_integer_as_bigint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsTreatIntegerAsBigint", []))

    @jsii.member(jsii_name="resetListingAutoFulfillmentReplicationRefreshSchedule")
    def reset_listing_auto_fulfillment_replication_refresh_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetListingAutoFulfillmentReplicationRefreshSchedule", []))

    @jsii.member(jsii_name="resetLockTimeout")
    def reset_lock_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockTimeout", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetMaxConcurrencyLevel")
    def reset_max_concurrency_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrencyLevel", []))

    @jsii.member(jsii_name="resetMaxDataExtensionTimeInDays")
    def reset_max_data_extension_time_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDataExtensionTimeInDays", []))

    @jsii.member(jsii_name="resetMetricLevel")
    def reset_metric_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricLevel", []))

    @jsii.member(jsii_name="resetMinDataRetentionTimeInDays")
    def reset_min_data_retention_time_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinDataRetentionTimeInDays", []))

    @jsii.member(jsii_name="resetMultiStatementCount")
    def reset_multi_statement_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiStatementCount", []))

    @jsii.member(jsii_name="resetNetworkPolicy")
    def reset_network_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkPolicy", []))

    @jsii.member(jsii_name="resetNoorderSequenceAsDefault")
    def reset_noorder_sequence_as_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoorderSequenceAsDefault", []))

    @jsii.member(jsii_name="resetOauthAddPrivilegedRolesToBlockedList")
    def reset_oauth_add_privileged_roles_to_blocked_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthAddPrivilegedRolesToBlockedList", []))

    @jsii.member(jsii_name="resetOdbcTreatDecimalAsInt")
    def reset_odbc_treat_decimal_as_int(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOdbcTreatDecimalAsInt", []))

    @jsii.member(jsii_name="resetPackagesPolicy")
    def reset_packages_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackagesPolicy", []))

    @jsii.member(jsii_name="resetPasswordPolicy")
    def reset_password_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordPolicy", []))

    @jsii.member(jsii_name="resetPeriodicDataRekeying")
    def reset_periodic_data_rekeying(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodicDataRekeying", []))

    @jsii.member(jsii_name="resetPipeExecutionPaused")
    def reset_pipe_execution_paused(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipeExecutionPaused", []))

    @jsii.member(jsii_name="resetPreventUnloadToInlineUrl")
    def reset_prevent_unload_to_inline_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventUnloadToInlineUrl", []))

    @jsii.member(jsii_name="resetPreventUnloadToInternalStages")
    def reset_prevent_unload_to_internal_stages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventUnloadToInternalStages", []))

    @jsii.member(jsii_name="resetPythonProfilerModules")
    def reset_python_profiler_modules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonProfilerModules", []))

    @jsii.member(jsii_name="resetPythonProfilerTargetStage")
    def reset_python_profiler_target_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonProfilerTargetStage", []))

    @jsii.member(jsii_name="resetQueryTag")
    def reset_query_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryTag", []))

    @jsii.member(jsii_name="resetQuotedIdentifiersIgnoreCase")
    def reset_quoted_identifiers_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuotedIdentifiersIgnoreCase", []))

    @jsii.member(jsii_name="resetReplaceInvalidCharacters")
    def reset_replace_invalid_characters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplaceInvalidCharacters", []))

    @jsii.member(jsii_name="resetRequireStorageIntegrationForStageCreation")
    def reset_require_storage_integration_for_stage_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireStorageIntegrationForStageCreation", []))

    @jsii.member(jsii_name="resetRequireStorageIntegrationForStageOperation")
    def reset_require_storage_integration_for_stage_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireStorageIntegrationForStageOperation", []))

    @jsii.member(jsii_name="resetResourceMonitor")
    def reset_resource_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceMonitor", []))

    @jsii.member(jsii_name="resetRowsPerResultset")
    def reset_rows_per_resultset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowsPerResultset", []))

    @jsii.member(jsii_name="resetS3StageVpceDnsName")
    def reset_s3_stage_vpce_dns_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3StageVpceDnsName", []))

    @jsii.member(jsii_name="resetSamlIdentityProvider")
    def reset_saml_identity_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamlIdentityProvider", []))

    @jsii.member(jsii_name="resetSearchPath")
    def reset_search_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchPath", []))

    @jsii.member(jsii_name="resetServerlessTaskMaxStatementSize")
    def reset_serverless_task_max_statement_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerlessTaskMaxStatementSize", []))

    @jsii.member(jsii_name="resetServerlessTaskMinStatementSize")
    def reset_serverless_task_min_statement_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerlessTaskMinStatementSize", []))

    @jsii.member(jsii_name="resetSessionPolicy")
    def reset_session_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionPolicy", []))

    @jsii.member(jsii_name="resetSimulatedDataSharingConsumer")
    def reset_simulated_data_sharing_consumer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSimulatedDataSharingConsumer", []))

    @jsii.member(jsii_name="resetSsoLoginPage")
    def reset_sso_login_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsoLoginPage", []))

    @jsii.member(jsii_name="resetStatementQueuedTimeoutInSeconds")
    def reset_statement_queued_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementQueuedTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetStatementTimeoutInSeconds")
    def reset_statement_timeout_in_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatementTimeoutInSeconds", []))

    @jsii.member(jsii_name="resetStorageSerializationPolicy")
    def reset_storage_serialization_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageSerializationPolicy", []))

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

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CurrentAccountTimeoutsOutputReference":
        return typing.cast("CurrentAccountTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="abortDetachedQueryInput")
    def abort_detached_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "abortDetachedQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="activePythonProfilerInput")
    def active_python_profiler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "activePythonProfilerInput"))

    @builtins.property
    @jsii.member(jsii_name="allowClientMfaCachingInput")
    def allow_client_mfa_caching_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowClientMfaCachingInput"))

    @builtins.property
    @jsii.member(jsii_name="allowIdTokenInput")
    def allow_id_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowIdTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationPolicyInput")
    def authentication_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="autocommitInput")
    def autocommit_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autocommitInput"))

    @builtins.property
    @jsii.member(jsii_name="baseLocationPrefixInput")
    def base_location_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseLocationPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormatInput")
    def binary_input_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryInputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormatInput")
    def binary_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="catalogSyncInput")
    def catalog_sync_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogSyncInput"))

    @builtins.property
    @jsii.member(jsii_name="clientEnableLogInfoStatementParametersInput")
    def client_enable_log_info_statement_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientEnableLogInfoStatementParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="clientEncryptionKeySizeInput")
    def client_encryption_key_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientEncryptionKeySizeInput"))

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
    @jsii.member(jsii_name="clientMetadataUseSessionDatabaseInput")
    def client_metadata_use_session_database_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientMetadataUseSessionDatabaseInput"))

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
    @jsii.member(jsii_name="cortexEnabledCrossRegionInput")
    def cortex_enabled_cross_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cortexEnabledCrossRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="cortexModelsAllowlistInput")
    def cortex_models_allowlist_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cortexModelsAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="csvTimestampFormatInput")
    def csv_timestamp_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "csvTimestampFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDaysInput")
    def data_retention_time_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataRetentionTimeInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="dateInputFormatInput")
    def date_input_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateInputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormatInput")
    def date_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDdlCollationInput")
    def default_ddl_collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDdlCollationInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultNotebookComputePoolCpuInput")
    def default_notebook_compute_pool_cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultNotebookComputePoolCpuInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultNotebookComputePoolGpuInput")
    def default_notebook_compute_pool_gpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultNotebookComputePoolGpuInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultNullOrderingInput")
    def default_null_ordering_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultNullOrderingInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultStreamlitNotebookWarehouseInput")
    def default_streamlit_notebook_warehouse_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultStreamlitNotebookWarehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUiDownloadButtonInput")
    def disable_ui_download_button_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUiDownloadButtonInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUserPrivilegeGrantsInput")
    def disable_user_privilege_grants_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUserPrivilegeGrantsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticSensitiveDataClassificationLogInput")
    def enable_automatic_sensitive_data_classification_log_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAutomaticSensitiveDataClassificationLogInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEgressCostOptimizerInput")
    def enable_egress_cost_optimizer_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEgressCostOptimizerInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIdentifierFirstLoginInput")
    def enable_identifier_first_login_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIdentifierFirstLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInternalStagesPrivatelinkInput")
    def enable_internal_stages_privatelink_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInternalStagesPrivatelinkInput"))

    @builtins.property
    @jsii.member(jsii_name="enableTriSecretAndRekeyOptOutForImageRepositoryInput")
    def enable_tri_secret_and_rekey_opt_out_for_image_repository_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableTriSecretAndRekeyOptOutForImageRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="enableTriSecretAndRekeyOptOutForSpcsBlockStorageInput")
    def enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableTriSecretAndRekeyOptOutForSpcsBlockStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="enableUnhandledExceptionsReportingInput")
    def enable_unhandled_exceptions_reporting_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableUnhandledExceptionsReportingInput"))

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
    @jsii.member(jsii_name="enableUnredactedSecureObjectErrorInput")
    def enable_unredacted_secure_object_error_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableUnredactedSecureObjectErrorInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceNetworkRulesForInternalStagesInput")
    def enforce_network_rules_for_internal_stages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enforceNetworkRulesForInternalStagesInput"))

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
    @jsii.member(jsii_name="eventTableInput")
    def event_table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventTableInput"))

    @builtins.property
    @jsii.member(jsii_name="externalOauthAddPrivilegedRolesToBlockedListInput")
    def external_oauth_add_privileged_roles_to_blocked_list_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "externalOauthAddPrivilegedRolesToBlockedListInput"))

    @builtins.property
    @jsii.member(jsii_name="externalVolumeInput")
    def external_volume_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="featurePolicyInput")
    def feature_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featurePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormatInput")
    def geography_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geographyOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormatInput")
    def geometry_output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geometryOutputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="hybridTableLockTimeoutInput")
    def hybrid_table_lock_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hybridTableLockTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialReplicationSizeLimitInTbInput")
    def initial_replication_size_limit_in_tb_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initialReplicationSizeLimitInTbInput"))

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
    @jsii.member(jsii_name="jsTreatIntegerAsBigintInput")
    def js_treat_integer_as_bigint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jsTreatIntegerAsBigintInput"))

    @builtins.property
    @jsii.member(jsii_name="listingAutoFulfillmentReplicationRefreshScheduleInput")
    def listing_auto_fulfillment_replication_refresh_schedule_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listingAutoFulfillmentReplicationRefreshScheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="lockTimeoutInput")
    def lock_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lockTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyLevelInput")
    def max_concurrency_level_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrencyLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDataExtensionTimeInDaysInput")
    def max_data_extension_time_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDataExtensionTimeInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="metricLevelInput")
    def metric_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="minDataRetentionTimeInDaysInput")
    def min_data_retention_time_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minDataRetentionTimeInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="multiStatementCountInput")
    def multi_statement_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "multiStatementCountInput"))

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
    @jsii.member(jsii_name="oauthAddPrivilegedRolesToBlockedListInput")
    def oauth_add_privileged_roles_to_blocked_list_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "oauthAddPrivilegedRolesToBlockedListInput"))

    @builtins.property
    @jsii.member(jsii_name="odbcTreatDecimalAsIntInput")
    def odbc_treat_decimal_as_int_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "odbcTreatDecimalAsIntInput"))

    @builtins.property
    @jsii.member(jsii_name="packagesPolicyInput")
    def packages_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "packagesPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordPolicyInput")
    def password_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="periodicDataRekeyingInput")
    def periodic_data_rekeying_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "periodicDataRekeyingInput"))

    @builtins.property
    @jsii.member(jsii_name="pipeExecutionPausedInput")
    def pipe_execution_paused_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pipeExecutionPausedInput"))

    @builtins.property
    @jsii.member(jsii_name="preventUnloadToInlineUrlInput")
    def prevent_unload_to_inline_url_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventUnloadToInlineUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="preventUnloadToInternalStagesInput")
    def prevent_unload_to_internal_stages_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventUnloadToInternalStagesInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonProfilerModulesInput")
    def python_profiler_modules_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pythonProfilerModulesInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonProfilerTargetStageInput")
    def python_profiler_target_stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pythonProfilerTargetStageInput"))

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
    @jsii.member(jsii_name="replaceInvalidCharactersInput")
    def replace_invalid_characters_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replaceInvalidCharactersInput"))

    @builtins.property
    @jsii.member(jsii_name="requireStorageIntegrationForStageCreationInput")
    def require_storage_integration_for_stage_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireStorageIntegrationForStageCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="requireStorageIntegrationForStageOperationInput")
    def require_storage_integration_for_stage_operation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireStorageIntegrationForStageOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceMonitorInput")
    def resource_monitor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceMonitorInput"))

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultsetInput")
    def rows_per_resultset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowsPerResultsetInput"))

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsNameInput")
    def s3_stage_vpce_dns_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3StageVpceDnsNameInput"))

    @builtins.property
    @jsii.member(jsii_name="samlIdentityProviderInput")
    def saml_identity_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "samlIdentityProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="searchPathInput")
    def search_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchPathInput"))

    @builtins.property
    @jsii.member(jsii_name="serverlessTaskMaxStatementSizeInput")
    def serverless_task_max_statement_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverlessTaskMaxStatementSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="serverlessTaskMinStatementSizeInput")
    def serverless_task_min_statement_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverlessTaskMinStatementSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionPolicyInput")
    def session_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumerInput")
    def simulated_data_sharing_consumer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "simulatedDataSharingConsumerInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoLoginPageInput")
    def sso_login_page_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ssoLoginPageInput"))

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSecondsInput")
    def statement_queued_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statementQueuedTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSecondsInput")
    def statement_timeout_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statementTimeoutInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSerializationPolicyInput")
    def storage_serialization_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageSerializationPolicyInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CurrentAccountTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CurrentAccountTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ff2047342a26c301f150f888a22eb603d208c3bd63d8eb419d65c34f9f77f317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "abortDetachedQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="activePythonProfiler")
    def active_python_profiler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "activePythonProfiler"))

    @active_python_profiler.setter
    def active_python_profiler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba4c882ad6ae4d6c0e54fd76d884bdc8d31014238877552279fd269eeed39f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activePythonProfiler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowClientMfaCaching")
    def allow_client_mfa_caching(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowClientMfaCaching"))

    @allow_client_mfa_caching.setter
    def allow_client_mfa_caching(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809cc4f9bc24b69f76716f3780159970245c4d74cf1490318c28d26ea0171906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowClientMfaCaching", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowIdToken")
    def allow_id_token(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowIdToken"))

    @allow_id_token.setter
    def allow_id_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9df216d73b1647111e5fa878d3f7b0b3cb7d85c8a2eafdbf1c47e36aa5832e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowIdToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticationPolicy")
    def authentication_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationPolicy"))

    @authentication_policy.setter
    def authentication_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eef508ddb3e2a728023cc8f890355294f74e24c9a17415c5664cc82813e122d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationPolicy", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__2ad0ad993cb38e5e548652a49207f68c295402b8e168f7491c609bce370bfddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autocommit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseLocationPrefix")
    def base_location_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseLocationPrefix"))

    @base_location_prefix.setter
    def base_location_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6393dd99353ec11fe21d60b1921d013fdfa1a71663de9b04d75d0e01295a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseLocationPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryInputFormat")
    def binary_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryInputFormat"))

    @binary_input_format.setter
    def binary_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d99850086dc114c04076f20fbd361a142d90b8e6089153652870ae3b155e788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryOutputFormat")
    def binary_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryOutputFormat"))

    @binary_output_format.setter
    def binary_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa15d6cc073fc8e78263b1b9a708581ecbc68367bdad82f49a54a58904e7d579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43cf7833a9cd2e1464db8c787e310cd1f88e3e38305695c5c8739a6b68eb7dfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="catalogSync")
    def catalog_sync(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogSync"))

    @catalog_sync.setter
    def catalog_sync(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc31abee3aeec07123a902ec39d9ad275c3a6c7750a1a437ef61295d04e951c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalogSync", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientEnableLogInfoStatementParameters")
    def client_enable_log_info_statement_parameters(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientEnableLogInfoStatementParameters"))

    @client_enable_log_info_statement_parameters.setter
    def client_enable_log_info_statement_parameters(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c70e6bdfac085993bc7970bea872c98db17c08601715f09b8547800c921846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientEnableLogInfoStatementParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientEncryptionKeySize")
    def client_encryption_key_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientEncryptionKeySize"))

    @client_encryption_key_size.setter
    def client_encryption_key_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65107c569f5e8d5d853ee6a6bb92d0c3326cdd7f78aa0cd192307d3cd1ea3c65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientEncryptionKeySize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientMemoryLimit")
    def client_memory_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientMemoryLimit"))

    @client_memory_limit.setter
    def client_memory_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac09a778a468581f2a11792a682337c75f6f3c90cde67ac814e696f672e2556)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68c96809f48fcab87a3e210547221c47210389596cac96a67b330ad52e6ff537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientMetadataRequestUseConnectionCtx", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientMetadataUseSessionDatabase")
    def client_metadata_use_session_database(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientMetadataUseSessionDatabase"))

    @client_metadata_use_session_database.setter
    def client_metadata_use_session_database(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089c82fb1a132a3ce09cb1d5403db36669a029fce187e4ae44616ae835c2c575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientMetadataUseSessionDatabase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientPrefetchThreads")
    def client_prefetch_threads(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientPrefetchThreads"))

    @client_prefetch_threads.setter
    def client_prefetch_threads(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ccc61dcc80df55e84bd2d8cdbd3e3464e2b4ff3006a6679c7a24e40cf839bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientPrefetchThreads", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientResultChunkSize")
    def client_result_chunk_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientResultChunkSize"))

    @client_result_chunk_size.setter
    def client_result_chunk_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6a5b9011604b225277c578f5c4e9b1e6043ddecd59468b915ada99bec41d0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5500191a2f8492d871b1b73dc2e13f085dedbd561ec5f9f3be632d2b37d1f65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f3f7df5de185fc2c6571ac2555eec8598fe0f40bdb55ad0ed663d62445362e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAlive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSessionKeepAliveHeartbeatFrequency")
    def client_session_keep_alive_heartbeat_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clientSessionKeepAliveHeartbeatFrequency"))

    @client_session_keep_alive_heartbeat_frequency.setter
    def client_session_keep_alive_heartbeat_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2527c33b3147efd602219ce8249a448304cadefd800f84b4d332320bd6bf4a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSessionKeepAliveHeartbeatFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTimestampTypeMapping")
    def client_timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientTimestampTypeMapping"))

    @client_timestamp_type_mapping.setter
    def client_timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e86f908490016487c56a70dc6aaf0b1d912157c1190f3cea276a2be874a07e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cortexEnabledCrossRegion")
    def cortex_enabled_cross_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cortexEnabledCrossRegion"))

    @cortex_enabled_cross_region.setter
    def cortex_enabled_cross_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25643de2c010d8eb1c20dccdeb86199ca7639b43322b8e451dec38275e334fb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cortexEnabledCrossRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cortexModelsAllowlist")
    def cortex_models_allowlist(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cortexModelsAllowlist"))

    @cortex_models_allowlist.setter
    def cortex_models_allowlist(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e8b2adf229f9aa07b8c2439f15283797421a79c7045e53e0b97eb6d3921c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cortexModelsAllowlist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="csvTimestampFormat")
    def csv_timestamp_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "csvTimestampFormat"))

    @csv_timestamp_format.setter
    def csv_timestamp_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7021fad4fe2c550e01d3272011046a700f6a208d772592c6d5844151549e128e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "csvTimestampFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataRetentionTimeInDays")
    def data_retention_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataRetentionTimeInDays"))

    @data_retention_time_in_days.setter
    def data_retention_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88540fe652d1aaea92a9edcfe9bb4baa6dbc6fbc045e886d8bcea0c0cf18f07d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRetentionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateInputFormat")
    def date_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateInputFormat"))

    @date_input_format.setter
    def date_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef9adcfd62e0abcbb1bc43bb9c6286b3bf6e617c957ab3b4535658899101e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dateOutputFormat")
    def date_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateOutputFormat"))

    @date_output_format.setter
    def date_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97565bbf19dd395e14278235645fa84e28812d0cceafaf98ddb00daefaa3a1c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDdlCollation")
    def default_ddl_collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDdlCollation"))

    @default_ddl_collation.setter
    def default_ddl_collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ca359cfb0313c53b2f5a0d410e3ee0ece8afecbf6bc12c0d38da5365fe2d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDdlCollation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultNotebookComputePoolCpu")
    def default_notebook_compute_pool_cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultNotebookComputePoolCpu"))

    @default_notebook_compute_pool_cpu.setter
    def default_notebook_compute_pool_cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1244bb183454057017fda99f9df330aacf20210c4cbb6fff90f439a8fc502ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultNotebookComputePoolCpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultNotebookComputePoolGpu")
    def default_notebook_compute_pool_gpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultNotebookComputePoolGpu"))

    @default_notebook_compute_pool_gpu.setter
    def default_notebook_compute_pool_gpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a609f6c911a165949008370de3ced40d9446ab4ec8e58ce90d74cc1c24ab8d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultNotebookComputePoolGpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultNullOrdering")
    def default_null_ordering(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultNullOrdering"))

    @default_null_ordering.setter
    def default_null_ordering(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca19aadca7808e6c79b197cc95d4d3ace19f526004baa8b77acf03484b312d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultNullOrdering", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultStreamlitNotebookWarehouse")
    def default_streamlit_notebook_warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultStreamlitNotebookWarehouse"))

    @default_streamlit_notebook_warehouse.setter
    def default_streamlit_notebook_warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d465fb726b539c22b047212d19b87b8c585b30bd93a91a4ac74336631d8844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultStreamlitNotebookWarehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableUiDownloadButton")
    def disable_ui_download_button(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUiDownloadButton"))

    @disable_ui_download_button.setter
    def disable_ui_download_button(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c86c8822d0a5b43e291ef84a3bdbb4835f593cc0fc8f49feed0786ba333d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUiDownloadButton", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableUserPrivilegeGrants")
    def disable_user_privilege_grants(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUserPrivilegeGrants"))

    @disable_user_privilege_grants.setter
    def disable_user_privilege_grants(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90484c9faea6debc29c6e919faaf5928b69e77cb11a9a77be30108cf9d7733d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUserPrivilegeGrants", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticSensitiveDataClassificationLog")
    def enable_automatic_sensitive_data_classification_log(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAutomaticSensitiveDataClassificationLog"))

    @enable_automatic_sensitive_data_classification_log.setter
    def enable_automatic_sensitive_data_classification_log(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953f099809403b6d05b194269ed8aa2fa91ec9907a9161fe14e1ddf59a1f9d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutomaticSensitiveDataClassificationLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableEgressCostOptimizer")
    def enable_egress_cost_optimizer(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEgressCostOptimizer"))

    @enable_egress_cost_optimizer.setter
    def enable_egress_cost_optimizer(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427967fba0933221c546a6c26e3a0796630df913949b952c28f4220d67ec6437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEgressCostOptimizer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableIdentifierFirstLogin")
    def enable_identifier_first_login(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIdentifierFirstLogin"))

    @enable_identifier_first_login.setter
    def enable_identifier_first_login(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814acad29b366dd1e17082e0e8f897e574b9e50b40424daca2a04b09d559b298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIdentifierFirstLogin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableInternalStagesPrivatelink")
    def enable_internal_stages_privatelink(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInternalStagesPrivatelink"))

    @enable_internal_stages_privatelink.setter
    def enable_internal_stages_privatelink(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293370260f12206a92011d498e1e6139afbbd5afe9f64781e7da850819a5ef58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInternalStagesPrivatelink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableTriSecretAndRekeyOptOutForImageRepository")
    def enable_tri_secret_and_rekey_opt_out_for_image_repository(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableTriSecretAndRekeyOptOutForImageRepository"))

    @enable_tri_secret_and_rekey_opt_out_for_image_repository.setter
    def enable_tri_secret_and_rekey_opt_out_for_image_repository(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af248520e7a6fc02a2af14ab43105932580c57a9880cc454095b93a6c0ca4d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableTriSecretAndRekeyOptOutForImageRepository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableTriSecretAndRekeyOptOutForSpcsBlockStorage")
    def enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableTriSecretAndRekeyOptOutForSpcsBlockStorage"))

    @enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage.setter
    def enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98790e56a9d2be95843d63e178943ea22c556f3b6b7786d2ba41490408b77c6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableTriSecretAndRekeyOptOutForSpcsBlockStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableUnhandledExceptionsReporting")
    def enable_unhandled_exceptions_reporting(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableUnhandledExceptionsReporting"))

    @enable_unhandled_exceptions_reporting.setter
    def enable_unhandled_exceptions_reporting(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1f8bf45a613b39467daf31b6d861d24850f04b82137881e5c64320aa37fcd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUnhandledExceptionsReporting", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__4d11a5ae3d39d05c57129c4421c1725a52aaf991acb82c56442b410d97e485ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee3aab39f5bdda9d0837673babed3a4ae0817688caa3c55b3301808921135045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUnredactedQuerySyntaxError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableUnredactedSecureObjectError")
    def enable_unredacted_secure_object_error(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableUnredactedSecureObjectError"))

    @enable_unredacted_secure_object_error.setter
    def enable_unredacted_secure_object_error(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b181fdb1e72a623f95ca5a512a5877a19f1b1aeffe722809883470ab95f42e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableUnredactedSecureObjectError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceNetworkRulesForInternalStages")
    def enforce_network_rules_for_internal_stages(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enforceNetworkRulesForInternalStages"))

    @enforce_network_rules_for_internal_stages.setter
    def enforce_network_rules_for_internal_stages(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a611a612a0b034275d961831b1a772393f7eb9af05d167c500b6b4b7c3da86a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceNetworkRulesForInternalStages", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__740a2366cc5ca3d0ee388b50f0c667c23a08cb336bde5c90cf939dea62c3933b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f475575d21f9c5c540199c1275e200b2681032cda55184dfd781827e4a40a5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorOnNondeterministicUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventTable")
    def event_table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventTable"))

    @event_table.setter
    def event_table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a114ed5b6059f5a8b5f2f9d6cae0d2f98291613bb60cabac53ed1a703ff392f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalOauthAddPrivilegedRolesToBlockedList")
    def external_oauth_add_privileged_roles_to_blocked_list(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "externalOauthAddPrivilegedRolesToBlockedList"))

    @external_oauth_add_privileged_roles_to_blocked_list.setter
    def external_oauth_add_privileged_roles_to_blocked_list(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6facb7f9e787436d00bbd20de95ef1d0d7042c8134c7000506f4e8c0948e670f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalOauthAddPrivilegedRolesToBlockedList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalVolume")
    def external_volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalVolume"))

    @external_volume.setter
    def external_volume(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5629ef3e7c6b3bfbfbb09098800ae399d12ad0583e42de5e6e210df30909c345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalVolume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="featurePolicy")
    def feature_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featurePolicy"))

    @feature_policy.setter
    def feature_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdaa01e9ada20536d88dd38de9432647b82f2b242e2a92853200cd7dc6032c81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featurePolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geographyOutputFormat")
    def geography_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geographyOutputFormat"))

    @geography_output_format.setter
    def geography_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0267c69ee565092154d6c47966b3172739ad12348cd689341873c6bf06bc306c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geographyOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geometryOutputFormat")
    def geometry_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geometryOutputFormat"))

    @geometry_output_format.setter
    def geometry_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de228176e9a4e1f01631c98307d0df33646e11d1a291ea5836cc368430a4ee3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geometryOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hybridTableLockTimeout")
    def hybrid_table_lock_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hybridTableLockTimeout"))

    @hybrid_table_lock_timeout.setter
    def hybrid_table_lock_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b19e8e107ab04584cc87e9fd6af754d4f994f4d4dbcec9910a9d1edfe0b607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hybridTableLockTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd771e9fa0f4d806cdb0e30e95355b2c71135728310fe1a2883bc4ec293a9178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialReplicationSizeLimitInTb")
    def initial_replication_size_limit_in_tb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initialReplicationSizeLimitInTb"))

    @initial_replication_size_limit_in_tb.setter
    def initial_replication_size_limit_in_tb(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed18a91a76853d5733faaa271478c73986b74892c002eb97642d068b10dd4e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialReplicationSizeLimitInTb", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__58b5e3a824838c607eeff6176729ec8b39d19aadcd3e616f7390479945ac14ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3356453194f7657bc6be88f501c4ca8ce72249916012c347a270855d300bcfa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1dc3bceaefedd72773724c5891a65f02d33601afd315b063bc376c8b3f41855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jdbcUseSessionTimezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsonIndent")
    def json_indent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "jsonIndent"))

    @json_indent.setter
    def json_indent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b94c15ccd0c225e23149b48a942711d590f93bcc4ef5e86f5f189f3395f4a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsonIndent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jsTreatIntegerAsBigint")
    def js_treat_integer_as_bigint(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jsTreatIntegerAsBigint"))

    @js_treat_integer_as_bigint.setter
    def js_treat_integer_as_bigint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bc214c9b3795213c478e7faa04f851608cb47ca70b038bdf3228d2f4b84a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jsTreatIntegerAsBigint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="listingAutoFulfillmentReplicationRefreshSchedule")
    def listing_auto_fulfillment_replication_refresh_schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listingAutoFulfillmentReplicationRefreshSchedule"))

    @listing_auto_fulfillment_replication_refresh_schedule.setter
    def listing_auto_fulfillment_replication_refresh_schedule(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c49327d2c5a16b2fcf15bdd371a62d3eb4fb5dce2a1d54810279e017618c148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listingAutoFulfillmentReplicationRefreshSchedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lockTimeout")
    def lock_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lockTimeout"))

    @lock_timeout.setter
    def lock_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a883fe9259a1f44a127aff1a2dd59b61a00a7f3b1257df16e36357caf992f614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26062c6b10b8c0b769b73893a797b50dcdf2aa5b8af1b0bf523de88a59929615)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxConcurrencyLevel")
    def max_concurrency_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrencyLevel"))

    @max_concurrency_level.setter
    def max_concurrency_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e9ab726258d4c2ea27cab555510d4a323f932ded4c9359b7db6095f74d0ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrencyLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDataExtensionTimeInDays")
    def max_data_extension_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDataExtensionTimeInDays"))

    @max_data_extension_time_in_days.setter
    def max_data_extension_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ed6b9cf62ce17f2cc3469ba861f4d8d4da5cdf4d48f7ad529f823f6befaf7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDataExtensionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricLevel"))

    @metric_level.setter
    def metric_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05bd888580f527a4416d153391097c0dc48fb19b5d5aa6fc1ea4d2435376d951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minDataRetentionTimeInDays")
    def min_data_retention_time_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minDataRetentionTimeInDays"))

    @min_data_retention_time_in_days.setter
    def min_data_retention_time_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__949ea780448ec6403c01b7c1a0c22fd81fd2623c4e37624f02b90f4d0cfeac6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minDataRetentionTimeInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multiStatementCount")
    def multi_statement_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiStatementCount"))

    @multi_statement_count.setter
    def multi_statement_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc03a098bb663656d69de583d3a0047d83e321f00862ed55b4bff5c52f3f8a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiStatementCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkPolicy")
    def network_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkPolicy"))

    @network_policy.setter
    def network_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4c9dedb836473f5336b3850e25dbf122bba07d9a9b8957f712705b0fd4a9a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a0c94cb5f139e4b6d20e53a7e8496bebd88975b3733874c6179a7510a7c0f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noorderSequenceAsDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthAddPrivilegedRolesToBlockedList")
    def oauth_add_privileged_roles_to_blocked_list(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "oauthAddPrivilegedRolesToBlockedList"))

    @oauth_add_privileged_roles_to_blocked_list.setter
    def oauth_add_privileged_roles_to_blocked_list(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35382c3ac5a3df76733472ddafcdf5205d420e18ee87d61b66b35ab1b5d9808f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthAddPrivilegedRolesToBlockedList", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__53f547f1c14ef82c60675e65995dbb00f20cc8907b9d1cb46ee7d7efa74914bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "odbcTreatDecimalAsInt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packagesPolicy")
    def packages_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "packagesPolicy"))

    @packages_policy.setter
    def packages_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b1796495fbcff84cb60240e12230a3d4d8e508d89dc2e94f2b15f4e9b80582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packagesPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordPolicy")
    def password_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordPolicy"))

    @password_policy.setter
    def password_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462c2e2e1b8f7cff68407f9c45c6c8798f3cdbd7a10c09672fdb3254a1088dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodicDataRekeying")
    def periodic_data_rekeying(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "periodicDataRekeying"))

    @periodic_data_rekeying.setter
    def periodic_data_rekeying(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052cdc2aac7e11f5eaa4fbca2f0b37d7b8c6f69767660069700c30277da0c0bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodicDataRekeying", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__8f6ebfa9b0e605d6cb61b8cf0b60006654a51d68bde3ac47e788e1a23e6ca9f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipeExecutionPaused", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preventUnloadToInlineUrl")
    def prevent_unload_to_inline_url(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventUnloadToInlineUrl"))

    @prevent_unload_to_inline_url.setter
    def prevent_unload_to_inline_url(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e973e91e50a60009ff668b8f6a0a41427e8ae9c6ceaa75fab0cd83d1b3680ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventUnloadToInlineUrl", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ca0d5bb142a3f8fef23acaa7e7e8df327029c060c2f6030d1f18ef3be9de365f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventUnloadToInternalStages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonProfilerModules")
    def python_profiler_modules(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonProfilerModules"))

    @python_profiler_modules.setter
    def python_profiler_modules(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900a43ed635b85c00a9ee312a15b8e0b4f521955666eaa0f3aa9b9c1d8bc47a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonProfilerModules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonProfilerTargetStage")
    def python_profiler_target_stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonProfilerTargetStage"))

    @python_profiler_target_stage.setter
    def python_profiler_target_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8ce9c2e83e930374aa6234d2801cdce8002297e832a29da1129e881c1a0fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonProfilerTargetStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryTag")
    def query_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryTag"))

    @query_tag.setter
    def query_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9872a34ca6f14ab9219575ff77d3d97b28724237856f59e677ff8089d842febe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f77d5917225c57e75b061c49007a02359d4c64591c383dceec5198b44c9223b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf60506bbb105f40ccbf8f9b13125d8670a40b4c26b7e3f5257130bc49721ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceInvalidCharacters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireStorageIntegrationForStageCreation")
    def require_storage_integration_for_stage_creation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireStorageIntegrationForStageCreation"))

    @require_storage_integration_for_stage_creation.setter
    def require_storage_integration_for_stage_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83079e35b11e7e931b3f9c1687788d86133626ef84b541aaa62f280ba915e03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireStorageIntegrationForStageCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireStorageIntegrationForStageOperation")
    def require_storage_integration_for_stage_operation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireStorageIntegrationForStageOperation"))

    @require_storage_integration_for_stage_operation.setter
    def require_storage_integration_for_stage_operation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e962dac0d86f28b6188ee8f40e335142b288ebe8136a5dd29f8e3e3b4e8b509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireStorageIntegrationForStageOperation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceMonitor")
    def resource_monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceMonitor"))

    @resource_monitor.setter
    def resource_monitor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8506aa69451a39a69fec2759bda49c6f9c670d723548ef0b968deb4a6c2a6362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceMonitor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rowsPerResultset")
    def rows_per_resultset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rowsPerResultset"))

    @rows_per_resultset.setter
    def rows_per_resultset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0abe063aa5bdef91dc393768afa775541dbf8e1f4b70d5048ceea49abfed305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowsPerResultset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3StageVpceDnsName")
    def s3_stage_vpce_dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3StageVpceDnsName"))

    @s3_stage_vpce_dns_name.setter
    def s3_stage_vpce_dns_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060bdee7f0aecc9dba9675c975d6ad563d075f32cd2d8511929377ec68163907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3StageVpceDnsName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samlIdentityProvider")
    def saml_identity_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "samlIdentityProvider"))

    @saml_identity_provider.setter
    def saml_identity_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778b8732228f2f4396aae1fc9c0bcf25e314494bc6f0cebdf63a63a11492d6b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlIdentityProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchPath")
    def search_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchPath"))

    @search_path.setter
    def search_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106bf81abdd7c21d99330ec722d9b77a02df3b8b5ce3d1a23cd424bb9a75c9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverlessTaskMaxStatementSize")
    def serverless_task_max_statement_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverlessTaskMaxStatementSize"))

    @serverless_task_max_statement_size.setter
    def serverless_task_max_statement_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5fb62a241a5254152b31a594cb662b37185d65571f2dae9fc39b73a1fd9eb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverlessTaskMaxStatementSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverlessTaskMinStatementSize")
    def serverless_task_min_statement_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverlessTaskMinStatementSize"))

    @serverless_task_min_statement_size.setter
    def serverless_task_min_statement_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892ca3ae486d5bc8e72c5d6375429cdadd84c95eb7b73479a50cf4ac92700d93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverlessTaskMinStatementSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionPolicy")
    def session_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionPolicy"))

    @session_policy.setter
    def session_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092607976f1a149943e1da16e0052678ac1fc62a41a7899b80c0d00d6b613838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="simulatedDataSharingConsumer")
    def simulated_data_sharing_consumer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "simulatedDataSharingConsumer"))

    @simulated_data_sharing_consumer.setter
    def simulated_data_sharing_consumer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aaadee6704f5d38efd0a0d63dbb1f06bac9e8af0dddfc8a0abe780d64c99dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simulatedDataSharingConsumer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ssoLoginPage")
    def sso_login_page(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ssoLoginPage"))

    @sso_login_page.setter
    def sso_login_page(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6151e5cb45fe56382744b393e30cc8e0f56b58cd704e4407befc978b8ddd5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoLoginPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementQueuedTimeoutInSeconds")
    def statement_queued_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementQueuedTimeoutInSeconds"))

    @statement_queued_timeout_in_seconds.setter
    def statement_queued_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b257e21f06043cb9acd2d9731745f0117dd98999adf9141d4cd19ecb11c7d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementQueuedTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statementTimeoutInSeconds")
    def statement_timeout_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statementTimeoutInSeconds"))

    @statement_timeout_in_seconds.setter
    def statement_timeout_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9446e715566c10c86b28e136d0cd0022808b8e9f97800888a23140f08d1dba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementTimeoutInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSerializationPolicy")
    def storage_serialization_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSerializationPolicy"))

    @storage_serialization_policy.setter
    def storage_serialization_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ed68c93da6cf73d962a5fde98837d7fa8c0f9a2fc61c71e41bfec3b75c820d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSerializationPolicy", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__2b4f1fe4deb3803cd7436a28f2bc0573bfbbbc8d5a58a70fdf2160da93b1d459)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictJsonOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspendTaskAfterNumFailures")
    def suspend_task_after_num_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspendTaskAfterNumFailures"))

    @suspend_task_after_num_failures.setter
    def suspend_task_after_num_failures(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cf011e3fa56ae23f584a2485871969c3af7835802fc339690ee05d50474df6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspendTaskAfterNumFailures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskAutoRetryAttempts")
    def task_auto_retry_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskAutoRetryAttempts"))

    @task_auto_retry_attempts.setter
    def task_auto_retry_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136fa345520af7040b0f006365a8ca1bdb02081de141515caad0953610e5d3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskAutoRetryAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeInputFormat")
    def time_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeInputFormat"))

    @time_input_format.setter
    def time_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36bfe87797af8f1e867f295c9622ea81f46024992f83176266cd457c36fbaf26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeOutputFormat")
    def time_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeOutputFormat"))

    @time_output_format.setter
    def time_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff291df3ea4ce8dd455f6e41990d7e4d7420f36c86c29a99fbc7261e65bdf5df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee497298fa3dd542a629d6fa74aef162ed6ed3027859e2aeec054d7091f840e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampDayIsAlways24H", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampInputFormat")
    def timestamp_input_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampInputFormat"))

    @timestamp_input_format.setter
    def timestamp_input_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4cb7357f75c5611fc67d89fecaff3c34a646d7bd6d6c2f8704bc1c2022301c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampInputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampLtzOutputFormat")
    def timestamp_ltz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampLtzOutputFormat"))

    @timestamp_ltz_output_format.setter
    def timestamp_ltz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e819c9a6210eae033df8c71ab8cc45ca814124cb28ad3554ac1afc6256e5ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampLtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampNtzOutputFormat")
    def timestamp_ntz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampNtzOutputFormat"))

    @timestamp_ntz_output_format.setter
    def timestamp_ntz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2070723d5135f6b9d18823e707b57a452fd950da868df5a8e992a80de6d06bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampNtzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampOutputFormat")
    def timestamp_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampOutputFormat"))

    @timestamp_output_format.setter
    def timestamp_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dc6a90c714d5f947876ccdcec9e5ac46b2f79777fb483a5a24793cf9c0a17f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTypeMapping")
    def timestamp_type_mapping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTypeMapping"))

    @timestamp_type_mapping.setter
    def timestamp_type_mapping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2180a1bd0828eab82ef850481bbe62112db93e1babc02ed9441a0f3b34a199aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTypeMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timestampTzOutputFormat")
    def timestamp_tz_output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampTzOutputFormat"))

    @timestamp_tz_output_format.setter
    def timestamp_tz_output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2056caf88f8bef0dd0b7976bc28e3e1f84c03b23fe151f8fcaa140c269cba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampTzOutputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75183c46de8ed168c4177b3a3f4e8bad1e69dc3be3a177e4603534d13f4c4bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26d81116cbd83028d0dcbe613f94f27fc7c57105f5ebbc37a9cde763cbcf949)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7360f1a9047f428dd309831b1cbe6a86065b997196cd4ae7db3ef31d471f3c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionAbortOnError", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transactionDefaultIsolationLevel")
    def transaction_default_isolation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transactionDefaultIsolationLevel"))

    @transaction_default_isolation_level.setter
    def transaction_default_isolation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e89dab914aa427f511d457bb58aa9228bbd5396efe06ced60255af0d38e3f77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionDefaultIsolationLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="twoDigitCenturyStart")
    def two_digit_century_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "twoDigitCenturyStart"))

    @two_digit_century_start.setter
    def two_digit_century_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc6e949a13ffb6764ffe85a72438f0e0856df1e4462c017289819cc0d5977b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "twoDigitCenturyStart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unsupportedDdlAction")
    def unsupported_ddl_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unsupportedDdlAction"))

    @unsupported_ddl_action.setter
    def unsupported_ddl_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06fd2f443b6df55ceb02862eba53bd95d93161ef1458903a88caf2be755b7cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c1709f1aa9211a0f2931c324143a1fd545c18a63cfa1eeb5b960486c2668e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCachedResult", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskManagedInitialWarehouseSize")
    def user_task_managed_initial_warehouse_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userTaskManagedInitialWarehouseSize"))

    @user_task_managed_initial_warehouse_size.setter
    def user_task_managed_initial_warehouse_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc2af3339643cef2ecaae334a5f2514d3ffba7f4d51ec53a9049d4752cf0fff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskManagedInitialWarehouseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskMinimumTriggerIntervalInSeconds")
    def user_task_minimum_trigger_interval_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskMinimumTriggerIntervalInSeconds"))

    @user_task_minimum_trigger_interval_in_seconds.setter
    def user_task_minimum_trigger_interval_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799045fe95d407effc22db8aff0dfaa85ac154f93099ff2f7afa76e1127c53f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskMinimumTriggerIntervalInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userTaskTimeoutMs")
    def user_task_timeout_ms(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "userTaskTimeoutMs"))

    @user_task_timeout_ms.setter
    def user_task_timeout_ms(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ee7dea0ceb25bb3f278b7ab3675435b08d6fe702f41bd25a929456b7a855fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTaskTimeoutMs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfYearPolicy")
    def week_of_year_policy(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOfYearPolicy"))

    @week_of_year_policy.setter
    def week_of_year_policy(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f7f99a630c5cd404967455190d8e3010fd39ba46424ec830e735e9fa355433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfYearPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekStart")
    def week_start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekStart"))

    @week_start.setter
    def week_start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1fb4578ac1c61d8a3c465eb6ef1469c08ffa85a75fc30deb99fbab8fddeb3f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekStart", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.currentAccount.CurrentAccountConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "abort_detached_query": "abortDetachedQuery",
        "active_python_profiler": "activePythonProfiler",
        "allow_client_mfa_caching": "allowClientMfaCaching",
        "allow_id_token": "allowIdToken",
        "authentication_policy": "authenticationPolicy",
        "autocommit": "autocommit",
        "base_location_prefix": "baseLocationPrefix",
        "binary_input_format": "binaryInputFormat",
        "binary_output_format": "binaryOutputFormat",
        "catalog": "catalog",
        "catalog_sync": "catalogSync",
        "client_enable_log_info_statement_parameters": "clientEnableLogInfoStatementParameters",
        "client_encryption_key_size": "clientEncryptionKeySize",
        "client_memory_limit": "clientMemoryLimit",
        "client_metadata_request_use_connection_ctx": "clientMetadataRequestUseConnectionCtx",
        "client_metadata_use_session_database": "clientMetadataUseSessionDatabase",
        "client_prefetch_threads": "clientPrefetchThreads",
        "client_result_chunk_size": "clientResultChunkSize",
        "client_result_column_case_insensitive": "clientResultColumnCaseInsensitive",
        "client_session_keep_alive": "clientSessionKeepAlive",
        "client_session_keep_alive_heartbeat_frequency": "clientSessionKeepAliveHeartbeatFrequency",
        "client_timestamp_type_mapping": "clientTimestampTypeMapping",
        "cortex_enabled_cross_region": "cortexEnabledCrossRegion",
        "cortex_models_allowlist": "cortexModelsAllowlist",
        "csv_timestamp_format": "csvTimestampFormat",
        "data_retention_time_in_days": "dataRetentionTimeInDays",
        "date_input_format": "dateInputFormat",
        "date_output_format": "dateOutputFormat",
        "default_ddl_collation": "defaultDdlCollation",
        "default_notebook_compute_pool_cpu": "defaultNotebookComputePoolCpu",
        "default_notebook_compute_pool_gpu": "defaultNotebookComputePoolGpu",
        "default_null_ordering": "defaultNullOrdering",
        "default_streamlit_notebook_warehouse": "defaultStreamlitNotebookWarehouse",
        "disable_ui_download_button": "disableUiDownloadButton",
        "disable_user_privilege_grants": "disableUserPrivilegeGrants",
        "enable_automatic_sensitive_data_classification_log": "enableAutomaticSensitiveDataClassificationLog",
        "enable_egress_cost_optimizer": "enableEgressCostOptimizer",
        "enable_identifier_first_login": "enableIdentifierFirstLogin",
        "enable_internal_stages_privatelink": "enableInternalStagesPrivatelink",
        "enable_tri_secret_and_rekey_opt_out_for_image_repository": "enableTriSecretAndRekeyOptOutForImageRepository",
        "enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage": "enableTriSecretAndRekeyOptOutForSpcsBlockStorage",
        "enable_unhandled_exceptions_reporting": "enableUnhandledExceptionsReporting",
        "enable_unload_physical_type_optimization": "enableUnloadPhysicalTypeOptimization",
        "enable_unredacted_query_syntax_error": "enableUnredactedQuerySyntaxError",
        "enable_unredacted_secure_object_error": "enableUnredactedSecureObjectError",
        "enforce_network_rules_for_internal_stages": "enforceNetworkRulesForInternalStages",
        "error_on_nondeterministic_merge": "errorOnNondeterministicMerge",
        "error_on_nondeterministic_update": "errorOnNondeterministicUpdate",
        "event_table": "eventTable",
        "external_oauth_add_privileged_roles_to_blocked_list": "externalOauthAddPrivilegedRolesToBlockedList",
        "external_volume": "externalVolume",
        "feature_policy": "featurePolicy",
        "geography_output_format": "geographyOutputFormat",
        "geometry_output_format": "geometryOutputFormat",
        "hybrid_table_lock_timeout": "hybridTableLockTimeout",
        "id": "id",
        "initial_replication_size_limit_in_tb": "initialReplicationSizeLimitInTb",
        "jdbc_treat_decimal_as_int": "jdbcTreatDecimalAsInt",
        "jdbc_treat_timestamp_ntz_as_utc": "jdbcTreatTimestampNtzAsUtc",
        "jdbc_use_session_timezone": "jdbcUseSessionTimezone",
        "json_indent": "jsonIndent",
        "js_treat_integer_as_bigint": "jsTreatIntegerAsBigint",
        "listing_auto_fulfillment_replication_refresh_schedule": "listingAutoFulfillmentReplicationRefreshSchedule",
        "lock_timeout": "lockTimeout",
        "log_level": "logLevel",
        "max_concurrency_level": "maxConcurrencyLevel",
        "max_data_extension_time_in_days": "maxDataExtensionTimeInDays",
        "metric_level": "metricLevel",
        "min_data_retention_time_in_days": "minDataRetentionTimeInDays",
        "multi_statement_count": "multiStatementCount",
        "network_policy": "networkPolicy",
        "noorder_sequence_as_default": "noorderSequenceAsDefault",
        "oauth_add_privileged_roles_to_blocked_list": "oauthAddPrivilegedRolesToBlockedList",
        "odbc_treat_decimal_as_int": "odbcTreatDecimalAsInt",
        "packages_policy": "packagesPolicy",
        "password_policy": "passwordPolicy",
        "periodic_data_rekeying": "periodicDataRekeying",
        "pipe_execution_paused": "pipeExecutionPaused",
        "prevent_unload_to_inline_url": "preventUnloadToInlineUrl",
        "prevent_unload_to_internal_stages": "preventUnloadToInternalStages",
        "python_profiler_modules": "pythonProfilerModules",
        "python_profiler_target_stage": "pythonProfilerTargetStage",
        "query_tag": "queryTag",
        "quoted_identifiers_ignore_case": "quotedIdentifiersIgnoreCase",
        "replace_invalid_characters": "replaceInvalidCharacters",
        "require_storage_integration_for_stage_creation": "requireStorageIntegrationForStageCreation",
        "require_storage_integration_for_stage_operation": "requireStorageIntegrationForStageOperation",
        "resource_monitor": "resourceMonitor",
        "rows_per_resultset": "rowsPerResultset",
        "s3_stage_vpce_dns_name": "s3StageVpceDnsName",
        "saml_identity_provider": "samlIdentityProvider",
        "search_path": "searchPath",
        "serverless_task_max_statement_size": "serverlessTaskMaxStatementSize",
        "serverless_task_min_statement_size": "serverlessTaskMinStatementSize",
        "session_policy": "sessionPolicy",
        "simulated_data_sharing_consumer": "simulatedDataSharingConsumer",
        "sso_login_page": "ssoLoginPage",
        "statement_queued_timeout_in_seconds": "statementQueuedTimeoutInSeconds",
        "statement_timeout_in_seconds": "statementTimeoutInSeconds",
        "storage_serialization_policy": "storageSerializationPolicy",
        "strict_json_output": "strictJsonOutput",
        "suspend_task_after_num_failures": "suspendTaskAfterNumFailures",
        "task_auto_retry_attempts": "taskAutoRetryAttempts",
        "time_input_format": "timeInputFormat",
        "time_output_format": "timeOutputFormat",
        "timeouts": "timeouts",
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
        "week_of_year_policy": "weekOfYearPolicy",
        "week_start": "weekStart",
    },
)
class CurrentAccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        active_python_profiler: typing.Optional[builtins.str] = None,
        allow_client_mfa_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        authentication_policy: typing.Optional[builtins.str] = None,
        autocommit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        base_location_prefix: typing.Optional[builtins.str] = None,
        binary_input_format: typing.Optional[builtins.str] = None,
        binary_output_format: typing.Optional[builtins.str] = None,
        catalog: typing.Optional[builtins.str] = None,
        catalog_sync: typing.Optional[builtins.str] = None,
        client_enable_log_info_statement_parameters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_encryption_key_size: typing.Optional[jsii.Number] = None,
        client_memory_limit: typing.Optional[jsii.Number] = None,
        client_metadata_request_use_connection_ctx: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_metadata_use_session_database: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_prefetch_threads: typing.Optional[jsii.Number] = None,
        client_result_chunk_size: typing.Optional[jsii.Number] = None,
        client_result_column_case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_session_keep_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_session_keep_alive_heartbeat_frequency: typing.Optional[jsii.Number] = None,
        client_timestamp_type_mapping: typing.Optional[builtins.str] = None,
        cortex_enabled_cross_region: typing.Optional[builtins.str] = None,
        cortex_models_allowlist: typing.Optional[builtins.str] = None,
        csv_timestamp_format: typing.Optional[builtins.str] = None,
        data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        date_input_format: typing.Optional[builtins.str] = None,
        date_output_format: typing.Optional[builtins.str] = None,
        default_ddl_collation: typing.Optional[builtins.str] = None,
        default_notebook_compute_pool_cpu: typing.Optional[builtins.str] = None,
        default_notebook_compute_pool_gpu: typing.Optional[builtins.str] = None,
        default_null_ordering: typing.Optional[builtins.str] = None,
        default_streamlit_notebook_warehouse: typing.Optional[builtins.str] = None,
        disable_ui_download_button: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_user_privilege_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_automatic_sensitive_data_classification_log: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_egress_cost_optimizer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_identifier_first_login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_internal_stages_privatelink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_tri_secret_and_rekey_opt_out_for_image_repository: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unhandled_exceptions_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_unredacted_secure_object_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enforce_network_rules_for_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_table: typing.Optional[builtins.str] = None,
        external_oauth_add_privileged_roles_to_blocked_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_volume: typing.Optional[builtins.str] = None,
        feature_policy: typing.Optional[builtins.str] = None,
        geography_output_format: typing.Optional[builtins.str] = None,
        geometry_output_format: typing.Optional[builtins.str] = None,
        hybrid_table_lock_timeout: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        initial_replication_size_limit_in_tb: typing.Optional[builtins.str] = None,
        jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        json_indent: typing.Optional[jsii.Number] = None,
        js_treat_integer_as_bigint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        listing_auto_fulfillment_replication_refresh_schedule: typing.Optional[builtins.str] = None,
        lock_timeout: typing.Optional[jsii.Number] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_concurrency_level: typing.Optional[jsii.Number] = None,
        max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
        metric_level: typing.Optional[builtins.str] = None,
        min_data_retention_time_in_days: typing.Optional[jsii.Number] = None,
        multi_statement_count: typing.Optional[jsii.Number] = None,
        network_policy: typing.Optional[builtins.str] = None,
        noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oauth_add_privileged_roles_to_blocked_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        packages_policy: typing.Optional[builtins.str] = None,
        password_policy: typing.Optional[builtins.str] = None,
        periodic_data_rekeying: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pipe_execution_paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_unload_to_inline_url: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_unload_to_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        python_profiler_modules: typing.Optional[builtins.str] = None,
        python_profiler_target_stage: typing.Optional[builtins.str] = None,
        query_tag: typing.Optional[builtins.str] = None,
        quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_storage_integration_for_stage_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_storage_integration_for_stage_operation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_monitor: typing.Optional[builtins.str] = None,
        rows_per_resultset: typing.Optional[jsii.Number] = None,
        s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
        saml_identity_provider: typing.Optional[builtins.str] = None,
        search_path: typing.Optional[builtins.str] = None,
        serverless_task_max_statement_size: typing.Optional[builtins.str] = None,
        serverless_task_min_statement_size: typing.Optional[builtins.str] = None,
        session_policy: typing.Optional[builtins.str] = None,
        simulated_data_sharing_consumer: typing.Optional[builtins.str] = None,
        sso_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        storage_serialization_policy: typing.Optional[builtins.str] = None,
        strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
        task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
        time_input_format: typing.Optional[builtins.str] = None,
        time_output_format: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CurrentAccountTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param abort_detached_query: Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#abort_detached_query CurrentAccount#abort_detached_query}
        :param active_python_profiler: Sets the profiler to use for the session when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. Valid values are (case-insensitive): ``LINE`` | ``MEMORY``. For more information, check `ACTIVE_PYTHON_PROFILER docs <https://docs.snowflake.com/en/sql-reference/parameters#active-python-profiler>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#active_python_profiler CurrentAccount#active_python_profiler}
        :param allow_client_mfa_caching: Specifies whether an MFA token can be saved in the client-side operating system keystore to promote continuous, secure connectivity without users needing to respond to an MFA prompt at the start of each connection attempt to Snowflake. For details and the list of supported Snowflake-provided clients, see `Using MFA token caching to minimize the number of prompts during authentication — optional. <https://docs.snowflake.com/en/user-guide/security-mfa.html#label-mfa-token-caching>`_ For more information, check `ALLOW_CLIENT_MFA_CACHING docs <https://docs.snowflake.com/en/sql-reference/parameters#allow-client-mfa-caching>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#allow_client_mfa_caching CurrentAccount#allow_client_mfa_caching}
        :param allow_id_token: Specifies whether a connection token can be saved in the client-side operating system keystore to promote continuous, secure connectivity without users needing to enter login credentials at the start of each connection attempt to Snowflake. For details and the list of supported Snowflake-provided clients, see `Using connection caching to minimize the number of prompts for authentication — optional. <https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-use.html#label-browser-based-sso-connection-caching>`_ For more information, check `ALLOW_ID_TOKEN docs <https://docs.snowflake.com/en/sql-reference/parameters#allow-id-token>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#allow_id_token CurrentAccount#allow_id_token}
        :param authentication_policy: Specifies `authentication policy <https://docs.snowflake.com/en/user-guide/authentication-policies>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#authentication_policy CurrentAccount#authentication_policy}
        :param autocommit: Specifies whether autocommit is enabled for the session. Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#autocommit CurrentAccount#autocommit}
        :param base_location_prefix: Specifies a prefix for Snowflake to use in the write path for Snowflake-managed Apache Iceberg™ tables. For more information, see `data and metadata directories for Iceberg tables <https://docs.snowflake.com/en/user-guide/tables-iceberg-storage.html#label-tables-iceberg-configure-external-volume-base-location>`_. For more information, check `BASE_LOCATION_PREFIX docs <https://docs.snowflake.com/en/sql-reference/parameters#base-location-prefix>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#base_location_prefix CurrentAccount#base_location_prefix}
        :param binary_input_format: The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. Valid values are (case-insensitive): ``HEX`` | ``BASE64`` | ``UTF8``. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#binary_input_format CurrentAccount#binary_input_format}
        :param binary_output_format: The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. Valid values are (case-insensitive): ``HEX`` | ``BASE64``. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#binary_output_format CurrentAccount#binary_output_format}
        :param catalog: Specifies the catalog for Apache Iceberg™ tables. For more information, see the `Iceberg table documentation <https://docs.snowflake.com/en/user-guide/tables-iceberg.html#label-tables-iceberg-catalog-def>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `CATALOG docs <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#catalog CurrentAccount#catalog}
        :param catalog_sync: Specifies the name of your catalog integration for `Snowflake Open Catalog <https://other-docs.snowflake.com/en/opencatalog/overview>`_. Snowflake syncs tables that use the specified catalog integration with your Snowflake Open Catalog account. For more information, see `Sync a Snowflake-managed table with Snowflake Open Catalog <https://docs.snowflake.com/en/user-guide/tables-iceberg-open-catalog-sync>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `CATALOG_SYNC docs <https://docs.snowflake.com/en/sql-reference/parameters#catalog-sync>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#catalog_sync CurrentAccount#catalog_sync}
        :param client_enable_log_info_statement_parameters: Enables users to log the data values bound to `PreparedStatements <https://docs.snowflake.com/en/developer-guide/jdbc/jdbc-api.html#label-jdbc-api-preparedstatement>`_ (`more details <https://docs.snowflake.com/en/sql-reference/parameters#client-enable-log-info-statement-parameters>`_). For more information, check `CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-enable-log-info-statement-parameters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_enable_log_info_statement_parameters CurrentAccount#client_enable_log_info_statement_parameters}
        :param client_encryption_key_size: Specifies the AES encryption key size, in bits, used by Snowflake to encrypt/decrypt files stored on internal stages (for loading/unloading data) when you use the SNOWFLAKE_FULL encryption type. For more information, check `CLIENT_ENCRYPTION_KEY_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-encryption-key-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_encryption_key_size CurrentAccount#client_encryption_key_size}
        :param client_memory_limit: Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB). For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_memory_limit CurrentAccount#client_memory_limit}
        :param client_metadata_request_use_connection_ctx: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema. The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_metadata_request_use_connection_ctx CurrentAccount#client_metadata_request_use_connection_ctx}
        :param client_metadata_use_session_database: For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases to the current database. The narrower search typically returns fewer rows and executes more quickly (`more details on the usage <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-use-session-database>`_). For more information, check `CLIENT_METADATA_USE_SESSION_DATABASE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-use-session-database>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_metadata_use_session_database CurrentAccount#client_metadata_use_session_database}
        :param client_prefetch_threads: Parameter that specifies the number of threads used by the client to pre-fetch large result sets. The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_prefetch_threads CurrentAccount#client_prefetch_threads}
        :param client_result_chunk_size: Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB). The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_result_chunk_size CurrentAccount#client_result_chunk_size}
        :param client_result_column_case_insensitive: Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_result_column_case_insensitive CurrentAccount#client_result_column_case_insensitive}
        :param client_session_keep_alive: Parameter that indicates whether to force a user to log in again after a period of inactivity in the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_session_keep_alive CurrentAccount#client_session_keep_alive}
        :param client_session_keep_alive_heartbeat_frequency: Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_session_keep_alive_heartbeat_frequency CurrentAccount#client_session_keep_alive_heartbeat_frequency}
        :param client_timestamp_type_mapping: Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. Valid values are (case-insensitive): ``TIMESTAMP_LTZ`` | ``TIMESTAMP_NTZ``. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_timestamp_type_mapping CurrentAccount#client_timestamp_type_mapping}
        :param cortex_enabled_cross_region: Specifies the regions where an inference request may be processed in case the request cannot be processed in the region where request is originally placed. Specifying DISABLED disables cross-region inferencing. For examples and details, see `Cross-region inference <https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference>`_. For more information, check `CORTEX_ENABLED_CROSS_REGION docs <https://docs.snowflake.com/en/sql-reference/parameters#cortex-enabled-cross-region>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#cortex_enabled_cross_region CurrentAccount#cortex_enabled_cross_region}
        :param cortex_models_allowlist: Specifies the models that users in the account can access. Use this parameter to allowlist models for all users in the account. If you need to provide specific users with access beyond what you’ve specified in the allowlist, use role-based access control instead. For more information, see `Model allowlist <https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql.html#label-cortex-llm-allowlist>`_. For more information, check `CORTEX_MODELS_ALLOWLIST docs <https://docs.snowflake.com/en/sql-reference/parameters#cortex-models-allowlist>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#cortex_models_allowlist CurrentAccount#cortex_models_allowlist}
        :param csv_timestamp_format: Specifies the format for TIMESTAMP values in CSV files downloaded from Snowsight. If this parameter is not set, `TIMESTAMP_LTZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-ltz-output-format>`_ will be used for TIMESTAMP_LTZ values, `TIMESTAMP_TZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-tz-output-format>`_ will be used for TIMESTAMP_TZ and `TIMESTAMP_NTZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-ntz-output-format>`_ for TIMESTAMP_NTZ values. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_ or `Download your query results <https://docs.snowflake.com/en/user-guide/ui-snowsight-query.html#label-snowsight-download-query-results>`_. For more information, check `CSV_TIMESTAMP_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#csv-timestamp-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#csv_timestamp_format CurrentAccount#csv_timestamp_format}
        :param data_retention_time_in_days: Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object. A value of 0 effectively disables Time Travel for the specified database, schema, or table. For more information, see `Understanding & using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. For more information, check `DATA_RETENTION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#data-retention-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#data_retention_time_in_days CurrentAccount#data_retention_time_in_days}
        :param date_input_format: Specifies the input format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#date_input_format CurrentAccount#date_input_format}
        :param date_output_format: Specifies the display format for the DATE data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#date_output_format CurrentAccount#date_output_format}
        :param default_ddl_collation: Sets the default collation used for the following DDL operations: `CREATE TABLE <https://docs.snowflake.com/en/sql-reference/sql/create-table>`_, `ALTER TABLE <https://docs.snowflake.com/en/sql-reference/sql/alter-table>`_ … ADD COLUMN. Setting this parameter forces all subsequently-created columns in the affected objects (table, schema, database, or account) to have the specified collation as the default, unless the collation for the column is explicitly defined in the DDL. For more information, check `DEFAULT_DDL_COLLATION docs <https://docs.snowflake.com/en/sql-reference/parameters#default-ddl-collation>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_ddl_collation CurrentAccount#default_ddl_collation}
        :param default_notebook_compute_pool_cpu: Sets the preferred CPU compute pool used for `Notebooks on CPU Container Runtime <https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU docs <https://docs.snowflake.com/en/sql-reference/parameters#default-notebook-compute-pool-cpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_notebook_compute_pool_cpu CurrentAccount#default_notebook_compute_pool_cpu}
        :param default_notebook_compute_pool_gpu: Sets the preferred GPU compute pool used for `Notebooks on GPU Container Runtime <https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU docs <https://docs.snowflake.com/en/sql-reference/parameters#default-notebook-compute-pool-gpu>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_notebook_compute_pool_gpu CurrentAccount#default_notebook_compute_pool_gpu}
        :param default_null_ordering: Specifies the default ordering of NULL values in a result set (`more details <https://docs.snowflake.com/en/sql-reference/parameters#default-null-ordering>`_). Valid values are (case-insensitive): ``FIRST`` | ``LAST``. For more information, check `DEFAULT_NULL_ORDERING docs <https://docs.snowflake.com/en/sql-reference/parameters#default-null-ordering>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_null_ordering CurrentAccount#default_null_ordering}
        :param default_streamlit_notebook_warehouse: Specifies the name of the default warehouse to use when creating a notebook. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE docs <https://docs.snowflake.com/en/sql-reference/parameters#default-streamlit-notebook-warehouse>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_streamlit_notebook_warehouse CurrentAccount#default_streamlit_notebook_warehouse}
        :param disable_ui_download_button: Controls whether users in an account see a button to download data in Snowsight or the Classic Console, such as a table returned from running a query in a worksheet. If the button to download is hidden in Snowsight or the Classic Console, users can still download or export data using `third-party software <https://docs.snowflake.com/en/user-guide/ecosystem>`_. For more information, check `DISABLE_UI_DOWNLOAD_BUTTON docs <https://docs.snowflake.com/en/sql-reference/parameters#disable-ui-download-button>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#disable_ui_download_button CurrentAccount#disable_ui_download_button}
        :param disable_user_privilege_grants: Controls whether users in an account can grant privileges directly to other users. Disabling user privilege grants (that is, setting DISABLE_USER_PRIVILEGE_GRANTS to TRUE) does not affect existing grants to users. Existing grants to users continue to confer privileges to those users. For more information, see `GRANT … TO USER <https://docs.snowflake.com/en/sql-reference/sql/grant-privilege-user>`_. For more information, check `DISABLE_USER_PRIVILEGE_GRANTS docs <https://docs.snowflake.com/en/sql-reference/parameters#disable-user-privilege-grants>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#disable_user_privilege_grants CurrentAccount#disable_user_privilege_grants}
        :param enable_automatic_sensitive_data_classification_log: Controls whether events from `automatic sensitive data classification <https://docs.snowflake.com/en/user-guide/classify-auto>`_ are logged in the user event table. For more information, check `ENABLE_AUTOMATIC_SENSITIVE_DATA_CLASSIFICATION_LOG docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-automatic-sensitive-data-classification-log>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_automatic_sensitive_data_classification_log CurrentAccount#enable_automatic_sensitive_data_classification_log}
        :param enable_egress_cost_optimizer: Enables or disables the Listing Cross-cloud auto-fulfillment Egress cost optimizer. For more information, check `ENABLE_EGRESS_COST_OPTIMIZER docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-egress-cost-optimizer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_egress_cost_optimizer CurrentAccount#enable_egress_cost_optimizer}
        :param enable_identifier_first_login: Determines the login flow for users. When enabled, Snowflake prompts users for their username or email address before presenting authentication methods. For details, see `Identifier-first login <https://docs.snowflake.com/en/user-guide/identifier-first-login>`_. For more information, check `ENABLE_IDENTIFIER_FIRST_LOGIN docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-identifier-first-login>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_identifier_first_login CurrentAccount#enable_identifier_first_login}
        :param enable_internal_stages_privatelink: Specifies whether the `SYSTEM$GET_PRIVATELINK_CONFIG <https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_config>`_ function returns the private-internal-stages key in the query result. The corresponding value in the query result is used during the configuration process for private connectivity to internal stages. For more information, check `ENABLE_INTERNAL_STAGES_PRIVATELINK docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-internal-stages-privatelink>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_internal_stages_privatelink CurrentAccount#enable_internal_stages_privatelink}
        :param enable_tri_secret_and_rekey_opt_out_for_image_repository: Specifies choice for the `image repository <https://docs.snowflake.com/en/developer-guide/snowpark-container-services/working-with-registry-repository.html#label-registry-and-repository-image-repository>`_ to opt out of Tri-Secret Secure and `Periodic rekeying <https://docs.snowflake.com/en/user-guide/security-encryption-manage.html#label-periodic-rekeying>`_. For more information, check `ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_IMAGE_REPOSITORY docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-tri-secret-and-rekey-opt-out-for-image-repository>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_tri_secret_and_rekey_opt_out_for_image_repository CurrentAccount#enable_tri_secret_and_rekey_opt_out_for_image_repository}
        :param enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage: Specifies the choice for the `Snowpark Container Services block storage volume <https://docs.snowflake.com/en/developer-guide/snowpark-container-services/block-storage-volume>`_ to opt out of Tri-Secret Secure and `Periodic rekeying <https://docs.snowflake.com/en/user-guide/security-encryption-manage.html#label-periodic-rekeying>`_. For more information, check `ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_SPCS_BLOCK_STORAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-tri-secret-and-rekey-opt-out-for-spcs-block-storage>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage CurrentAccount#enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage}
        :param enable_unhandled_exceptions_reporting: Specifies whether Snowflake may capture – in an event table – log messages or trace event data for unhandled exceptions in procedure or UDF handler code. For more information, see `Capturing messages from unhandled exceptions <https://docs.snowflake.com/en/developer-guide/logging-tracing/unhandled-exception-messages>`_. For more information, check `ENABLE_UNHANDLED_EXCEPTIONS_REPORTING docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unhandled-exceptions-reporting>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unhandled_exceptions_reporting CurrentAccount#enable_unhandled_exceptions_reporting}
        :param enable_unload_physical_type_optimization: Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unload_physical_type_optimization CurrentAccount#enable_unload_physical_type_optimization}
        :param enable_unredacted_query_syntax_error: Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error. If FALSE, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to TRUE for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unredacted_query_syntax_error CurrentAccount#enable_unredacted_query_syntax_error}
        :param enable_unredacted_secure_object_error: Controls whether error messages related to secure objects are redacted in metadata. For more information, see `Secure objects: Redaction of information in error messages <https://docs.snowflake.com/en/release-notes/bcr-bundles/un-bundled/bcr-1858>`_. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_SECURE_OBJECT_ERROR parameter. When using the ALTER USER command to set the parameter to TRUE for a particular user, modify the user that you want to see the redacted error messages in metadata, not the user who caused the error. For more information, check `ENABLE_UNREDACTED_SECURE_OBJECT_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-secure-object-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unredacted_secure_object_error CurrentAccount#enable_unredacted_secure_object_error}
        :param enforce_network_rules_for_internal_stages: Specifies whether a network policy that uses network rules can restrict access to AWS internal stages. This parameter has no effect on network policies that do not use network rules. This account-level parameter affects both account-level and user-level network policies. For details about using network policies and network rules to restrict access to AWS internal stages, including the use of this parameter, see `Protecting internal stages on AWS <https://docs.snowflake.com/en/user-guide/network-policies.html#label-network-policies-rules-stages>`_. For more information, check `ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#enforce-network-rules-for-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enforce_network_rules_for_internal_stages CurrentAccount#enforce_network_rules_for_internal_stages}
        :param error_on_nondeterministic_merge: Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#error_on_nondeterministic_merge CurrentAccount#error_on_nondeterministic_merge}
        :param error_on_nondeterministic_update: Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#error_on_nondeterministic_update CurrentAccount#error_on_nondeterministic_update}
        :param event_table: Specifies the name of the event table for logging messages from stored procedures and UDFs contained by the object with which the event table is associated. Associating an event table with a database is available in `Enterprise Edition or higher <https://docs.snowflake.com/en/user-guide/intro-editions>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `EVENT_TABLE docs <https://docs.snowflake.com/en/sql-reference/parameters#event-table>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#event_table CurrentAccount#event_table}
        :param external_oauth_add_privileged_roles_to_blocked_list: Determines whether the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles can be used as the primary role when creating a Snowflake session based on the access token from the External OAuth authorization server. For more information, check `EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST docs <https://docs.snowflake.com/en/sql-reference/parameters#external-oauth-add-privileged-roles-to-blocked-list>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#external_oauth_add_privileged_roles_to_blocked_list CurrentAccount#external_oauth_add_privileged_roles_to_blocked_list}
        :param external_volume: Specifies the external volume for Apache Iceberg™ tables. For more information, see the `Iceberg table documentation <https://docs.snowflake.com/en/user-guide/tables-iceberg.html#label-tables-iceberg-external-volume-def>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `EXTERNAL_VOLUME docs <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#external_volume CurrentAccount#external_volume}
        :param feature_policy: Specifies `feature policy <https://docs.snowflake.com/en/developer-guide/native-apps/ui-consumer-feature-policies>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#feature_policy CurrentAccount#feature_policy}
        :param geography_output_format: Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. Valid values are (case-insensitive): ``GeoJSON`` | ``WKT`` | ``WKB`` | ``EWKT`` | ``EWKB``. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#geography_output_format CurrentAccount#geography_output_format}
        :param geometry_output_format: Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. Valid values are (case-insensitive): ``GeoJSON`` | ``WKT`` | ``WKB`` | ``EWKT`` | ``EWKB``. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#geometry_output_format CurrentAccount#geometry_output_format}
        :param hybrid_table_lock_timeout: Number of seconds to wait while trying to acquire row-level locks on a hybrid table, before timing out and aborting the statement. For more information, check `HYBRID_TABLE_LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#hybrid-table-lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#hybrid_table_lock_timeout CurrentAccount#hybrid_table_lock_timeout}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#id CurrentAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initial_replication_size_limit_in_tb: Sets the maximum estimated size limit for the initial replication of a primary database to a secondary database (in TB). Set this parameter on any account that stores a secondary database. This size limit helps prevent accounts from accidentally incurring large database replication charges. To remove the size limit, set the value to 0.0. It is required to pass numbers with scale of at least 1 (e.g. 20.5, 32.25, 33.333, etc.). For more information, check `INITIAL_REPLICATION_SIZE_LIMIT_IN_TB docs <https://docs.snowflake.com/en/sql-reference/parameters#initial-replication-size-limit-in-tb>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#initial_replication_size_limit_in_tb CurrentAccount#initial_replication_size_limit_in_tb}
        :param jdbc_treat_decimal_as_int: Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_treat_decimal_as_int CurrentAccount#jdbc_treat_decimal_as_int}
        :param jdbc_treat_timestamp_ntz_as_utc: Specifies how JDBC processes TIMESTAMP_NTZ values (`more details <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_). For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_treat_timestamp_ntz_as_utc CurrentAccount#jdbc_treat_timestamp_ntz_as_utc}
        :param jdbc_use_session_timezone: Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_use_session_timezone CurrentAccount#jdbc_use_session_timezone}
        :param json_indent: Specifies the number of blank spaces to indent each new element in JSON output in the session. Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#json_indent CurrentAccount#json_indent}
        :param js_treat_integer_as_bigint: Specifies how the Snowflake Node.js Driver processes numeric columns that have a scale of zero (0), for example INTEGER or NUMBER(p, 0). For more information, check `JS_TREAT_INTEGER_AS_BIGINT docs <https://docs.snowflake.com/en/sql-reference/parameters#js-treat-integer-as-bigint>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#js_treat_integer_as_bigint CurrentAccount#js_treat_integer_as_bigint}
        :param listing_auto_fulfillment_replication_refresh_schedule: Sets the time interval used to refresh the application package based data products to other regions. For more information, check `LISTING_AUTO_FULFILLMENT_REPLICATION_REFRESH_SCHEDULE docs <https://docs.snowflake.com/en/sql-reference/parameters#listing-auto-fulfillment-replication-refresh-schedule>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#listing_auto_fulfillment_replication_refresh_schedule CurrentAccount#listing_auto_fulfillment_replication_refresh_schedule}
        :param lock_timeout: Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement. For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#lock_timeout CurrentAccount#lock_timeout}
        :param log_level: Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting levels for logging, metrics, and tracing <https://docs.snowflake.com/en/developer-guide/logging-tracing/telemetry-levels>`_. Valid values are (case-insensitive): ``TRACE`` | ``DEBUG`` | ``INFO`` | ``WARN`` | ``ERROR`` | ``FATAL`` | ``OFF``. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#log_level CurrentAccount#log_level}
        :param max_concurrency_level: Specifies the concurrency level for SQL statements (that is, queries and DML) executed by a warehouse (`more details <https://docs.snowflake.com/en/sql-reference/parameters#max-concurrency-level>`_). For more information, check `MAX_CONCURRENCY_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#max-concurrency-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#max_concurrency_level CurrentAccount#max_concurrency_level}
        :param max_data_extension_time_in_days: Maximum number of days Snowflake can extend the data retention period for tables to prevent streams on the tables from becoming stale. By default, if the `DATA_RETENTION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters#data-retention-time-in-days>`_ setting for a source table is less than 14 days, and a stream has not been consumed, Snowflake temporarily extends this period to the stream’s offset, up to a maximum of 14 days, regardless of the `Snowflake Edition <https://docs.snowflake.com/en/user-guide/intro-editions>`_ for your account. The MAX_DATA_EXTENSION_TIME_IN_DAYS parameter enables you to limit this automatic extension period to control storage costs for data retention or for compliance reasons. For more information, check `MAX_DATA_EXTENSION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#max-data-extension-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#max_data_extension_time_in_days CurrentAccount#max_data_extension_time_in_days}
        :param metric_level: Controls how metrics data is ingested into the event table. For more information about metric levels, see `Setting levels for logging, metrics, and tracing <https://docs.snowflake.com/en/developer-guide/logging-tracing/telemetry-levels>`_. Valid values are (case-insensitive): ``ALL`` | ``NONE``. For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#metric_level CurrentAccount#metric_level}
        :param min_data_retention_time_in_days: Minimum number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on an object. If a minimum number of days for data retention is set on an account, the data retention period for an object is determined by MAX(`DATA_RETENTION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters#label-data-retention-time-in-days>`_, MIN_DATA_RETENTION_TIME_IN_DAYS). For more information, check `MIN_DATA_RETENTION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#min-data-retention-time-in-days>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#min_data_retention_time_in_days CurrentAccount#min_data_retention_time_in_days}
        :param multi_statement_count: Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#multi_statement_count CurrentAccount#multi_statement_count}
        :param network_policy: Specifies the network policy to enforce for your account. Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#network_policy CurrentAccount#network_policy}
        :param noorder_sequence_as_default: Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column. The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#noorder_sequence_as_default CurrentAccount#noorder_sequence_as_default}
        :param oauth_add_privileged_roles_to_blocked_list: Determines whether the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles can be used as the primary role when creating a Snowflake session based on the access token from Snowflake’s authorization server. For more information, check `OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST docs <https://docs.snowflake.com/en/sql-reference/parameters#oauth-add-privileged-roles-to-blocked-list>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#oauth_add_privileged_roles_to_blocked_list CurrentAccount#oauth_add_privileged_roles_to_blocked_list}
        :param odbc_treat_decimal_as_int: Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#odbc_treat_decimal_as_int CurrentAccount#odbc_treat_decimal_as_int}
        :param packages_policy: Specifies `packages policy <https://docs.snowflake.com/en/developer-guide/udf/python/packages-policy>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#packages_policy CurrentAccount#packages_policy}
        :param password_policy: Specifies `password policy <https://docs.snowflake.com/en/user-guide/password-authentication#label-using-password-policies>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#password_policy CurrentAccount#password_policy}
        :param periodic_data_rekeying: It enables/disables re-encryption of table data with new keys on a yearly basis to provide additional levels of data protection (`more details <https://docs.snowflake.com/en/sql-reference/parameters#periodic-data-rekeying>`_). For more information, check `PERIODIC_DATA_REKEYING docs <https://docs.snowflake.com/en/sql-reference/parameters#periodic-data-rekeying>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#periodic_data_rekeying CurrentAccount#periodic_data_rekeying}
        :param pipe_execution_paused: Specifies whether to pause a running pipe, primarily in preparation for transferring ownership of the pipe to a different role (`more details <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_). For more information, check `PIPE_EXECUTION_PAUSED docs <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#pipe_execution_paused CurrentAccount#pipe_execution_paused}
        :param prevent_unload_to_inline_url: Specifies whether to prevent ad hoc data unload operations to external cloud storage locations (that is, `COPY INTO location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements that specify the cloud storage URL and access settings directly in the statement). For an example, see `Unloading data from a table directly to files in an external location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html#label-copy-into-location-ad-hoc>`_. For more information, check `PREVENT_UNLOAD_TO_INLINE_URL docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-inline-url>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#prevent_unload_to_inline_url CurrentAccount#prevent_unload_to_inline_url}
        :param prevent_unload_to_internal_stages: Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#prevent_unload_to_internal_stages CurrentAccount#prevent_unload_to_internal_stages}
        :param python_profiler_modules: Specifies the list of Python modules to include in a report when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. For more information, check `PYTHON_PROFILER_MODULES docs <https://docs.snowflake.com/en/sql-reference/parameters#python-profiler-modules>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#python_profiler_modules CurrentAccount#python_profiler_modules}
        :param python_profiler_target_stage: Specifies the fully-qualified name of the stage in which to save a report when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. For more information, check `PYTHON_PROFILER_TARGET_STAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#python-profiler-target-stage>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#python_profiler_target_stage CurrentAccount#python_profiler_target_stage}
        :param query_tag: Optional string that can be used to tag queries and other SQL statements executed within a session. The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#query_tag CurrentAccount#query_tag}
        :param quoted_identifiers_ignore_case: Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters. By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#quoted_identifiers_ignore_case CurrentAccount#quoted_identifiers_ignore_case}
        :param replace_invalid_characters: Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for `Apache Iceberg™ tables <https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table>`_ that use an external catalog. For more information, check `REPLACE_INVALID_CHARACTERS docs <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#replace_invalid_characters CurrentAccount#replace_invalid_characters}
        :param require_storage_integration_for_stage_creation: Specifies whether to require a storage integration object as cloud credentials when creating a named external stage (using `CREATE STAGE <https://docs.snowflake.com/en/sql-reference/sql/create-stage>`_) to access a private cloud storage location. For more information, check `REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION docs <https://docs.snowflake.com/en/sql-reference/parameters#require-storage-integration-for-stage-creation>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#require_storage_integration_for_stage_creation CurrentAccount#require_storage_integration_for_stage_creation}
        :param require_storage_integration_for_stage_operation: Specifies whether to require using a named external stage that references a storage integration object as cloud credentials when loading data from or unloading data to a private cloud storage location. For more information, check `REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION docs <https://docs.snowflake.com/en/sql-reference/parameters#require-storage-integration-for-stage-operation>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#require_storage_integration_for_stage_operation CurrentAccount#require_storage_integration_for_stage_operation}
        :param resource_monitor: Parameter that specifies the name of the resource monitor used to control all virtual warehouses created in the account. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#resource_monitor CurrentAccount#resource_monitor}
        :param rows_per_resultset: Specifies the maximum number of rows returned in a result set. A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#rows_per_resultset CurrentAccount#rows_per_resultset}
        :param s3_stage_vpce_dns_name: Specifies the DNS name of an Amazon S3 interface endpoint. Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#s3_stage_vpce_dns_name CurrentAccount#s3_stage_vpce_dns_name}
        :param saml_identity_provider: Enables federated authentication. This deprecated parameter enables federated authentication (`more details <https://docs.snowflake.com/en/sql-reference/parameters#saml-identity-provider>`_). For more information, check `SAML_IDENTITY_PROVIDER docs <https://docs.snowflake.com/en/sql-reference/parameters#saml-identity-provider>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#saml_identity_provider CurrentAccount#saml_identity_provider}
        :param search_path: Specifies the path to search to resolve unqualified object names in queries. For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#search_path CurrentAccount#search_path}
        :param serverless_task_max_statement_size: Specifies the maximum allowed warehouse size for `Serverless tasks <https://docs.snowflake.com/en/user-guide/tasks-intro.html#label-tasks-compute-resources-serverless>`_. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `SERVERLESS_TASK_MAX_STATEMENT_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#serverless-task-max-statement-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#serverless_task_max_statement_size CurrentAccount#serverless_task_max_statement_size}
        :param serverless_task_min_statement_size: Specifies the minimum allowed warehouse size for `Serverless tasks <https://docs.snowflake.com/en/user-guide/tasks-intro.html#label-tasks-compute-resources-serverless>`_. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `SERVERLESS_TASK_MIN_STATEMENT_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#serverless-task-min-statement-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#serverless_task_min_statement_size CurrentAccount#serverless_task_min_statement_size}
        :param session_policy: Specifies `session policy <https://docs.snowflake.com/en/user-guide/session-policies-using>`_ for the current account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#session_policy CurrentAccount#session_policy}
        :param simulated_data_sharing_consumer: Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views. When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#simulated_data_sharing_consumer CurrentAccount#simulated_data_sharing_consumer}
        :param sso_login_page: This deprecated parameter disables preview mode for testing SSO (after enabling federated authentication) before rolling it out to users. For more information, check `SSO_LOGIN_PAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#sso-login-page>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#sso_login_page CurrentAccount#sso_login_page}
        :param statement_queued_timeout_in_seconds: Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#statement_queued_timeout_in_seconds CurrentAccount#statement_queued_timeout_in_seconds}
        :param statement_timeout_in_seconds: Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#statement_timeout_in_seconds CurrentAccount#statement_timeout_in_seconds}
        :param storage_serialization_policy: Specifies the storage serialization policy for Snowflake-managed `Apache Iceberg™ tables <https://docs.snowflake.com/en/user-guide/tables-iceberg>`_. Valid values are (case-insensitive): ``COMPATIBLE`` | ``OPTIMIZED``. For more information, check `STORAGE_SERIALIZATION_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#storage_serialization_policy CurrentAccount#storage_serialization_policy}
        :param strict_json_output: This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#strict_json_output CurrentAccount#strict_json_output}
        :param suspend_task_after_num_failures: Specifies the number of consecutive failed task runs after which the current task is suspended automatically. The default is 0 (no automatic suspension). For more information, check `SUSPEND_TASK_AFTER_NUM_FAILURES docs <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#suspend_task_after_num_failures CurrentAccount#suspend_task_after_num_failures}
        :param task_auto_retry_attempts: Specifies the number of automatic task graph retry attempts. If any task graphs complete in a FAILED state, Snowflake can automatically retry the task graphs from the last task in the graph that failed. For more information, check `TASK_AUTO_RETRY_ATTEMPTS docs <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#task_auto_retry_attempts CurrentAccount#task_auto_retry_attempts}
        :param time_input_format: Specifies the input format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#time_input_format CurrentAccount#time_input_format}
        :param time_output_format: Specifies the display format for the TIME data type. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#time_output_format CurrentAccount#time_output_format}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timeouts CurrentAccount#timeouts}
        :param timestamp_day_is_always24_h: Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_day_is_always_24h CurrentAccount#timestamp_day_is_always_24h}
        :param timestamp_input_format: Specifies the input format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_input_format CurrentAccount#timestamp_input_format}
        :param timestamp_ltz_output_format: Specifies the display format for the TIMESTAMP_LTZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_ltz_output_format CurrentAccount#timestamp_ltz_output_format}
        :param timestamp_ntz_output_format: Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_ntz_output_format CurrentAccount#timestamp_ntz_output_format}
        :param timestamp_output_format: Specifies the display format for the TIMESTAMP data type alias. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_output_format CurrentAccount#timestamp_output_format}
        :param timestamp_type_mapping: Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to. Valid values are (case-insensitive): ``TIMESTAMP_LTZ`` | ``TIMESTAMP_NTZ`` | ``TIMESTAMP_TZ``. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_type_mapping CurrentAccount#timestamp_type_mapping}
        :param timestamp_tz_output_format: Specifies the display format for the TIMESTAMP_TZ data type. If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_tz_output_format CurrentAccount#timestamp_tz_output_format}
        :param timezone: Specifies the time zone for the session. You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timezone CurrentAccount#timezone}
        :param trace_level: Controls how trace events are ingested into the event table. For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. Valid values are (case-insensitive): ``ALWAYS`` | ``ON_EVENT`` | ``PROPAGATE`` | ``OFF``. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#trace_level CurrentAccount#trace_level}
        :param transaction_abort_on_error: Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error. For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#transaction_abort_on_error CurrentAccount#transaction_abort_on_error}
        :param transaction_default_isolation_level: Specifies the isolation level for transactions in the user session. Valid values are (case-insensitive): ``READ COMMITTED``. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#transaction_default_isolation_level CurrentAccount#transaction_default_isolation_level}
        :param two_digit_century_start: Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#two_digit_century_start CurrentAccount#two_digit_century_start}
        :param unsupported_ddl_action: Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#unsupported_ddl_action CurrentAccount#unsupported_ddl_action}
        :param use_cached_result: Specifies whether to reuse persisted query results, if available, when a matching query is submitted. For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#use_cached_result CurrentAccount#use_cached_result}
        :param user_task_managed_initial_warehouse_size: Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size. Once a task has successfully completed a few runs, Snowflake ignores this parameter setting. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_managed_initial_warehouse_size CurrentAccount#user_task_managed_initial_warehouse_size}
        :param user_task_minimum_trigger_interval_in_seconds: Minimum amount of time between Triggered Task executions in seconds For more information, check `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-minimum-trigger-interval-in-seconds>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_minimum_trigger_interval_in_seconds CurrentAccount#user_task_minimum_trigger_interval_in_seconds}
        :param user_task_timeout_ms: Specifies the time limit on a single run of the task before it times out (in milliseconds). For more information, check `USER_TASK_TIMEOUT_MS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_timeout_ms CurrentAccount#user_task_timeout_ms}
        :param week_of_year_policy: Specifies how the weeks in a given year are computed. ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#week_of_year_policy CurrentAccount#week_of_year_policy}
        :param week_start: Specifies the first day of the week (used by week-related date functions). ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#week_start CurrentAccount#week_start}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = CurrentAccountTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874092e4c779217cedf530a98d8b63a694bf8fad7ac9ff5d46fe8d69f55b1ca5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument abort_detached_query", value=abort_detached_query, expected_type=type_hints["abort_detached_query"])
            check_type(argname="argument active_python_profiler", value=active_python_profiler, expected_type=type_hints["active_python_profiler"])
            check_type(argname="argument allow_client_mfa_caching", value=allow_client_mfa_caching, expected_type=type_hints["allow_client_mfa_caching"])
            check_type(argname="argument allow_id_token", value=allow_id_token, expected_type=type_hints["allow_id_token"])
            check_type(argname="argument authentication_policy", value=authentication_policy, expected_type=type_hints["authentication_policy"])
            check_type(argname="argument autocommit", value=autocommit, expected_type=type_hints["autocommit"])
            check_type(argname="argument base_location_prefix", value=base_location_prefix, expected_type=type_hints["base_location_prefix"])
            check_type(argname="argument binary_input_format", value=binary_input_format, expected_type=type_hints["binary_input_format"])
            check_type(argname="argument binary_output_format", value=binary_output_format, expected_type=type_hints["binary_output_format"])
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument catalog_sync", value=catalog_sync, expected_type=type_hints["catalog_sync"])
            check_type(argname="argument client_enable_log_info_statement_parameters", value=client_enable_log_info_statement_parameters, expected_type=type_hints["client_enable_log_info_statement_parameters"])
            check_type(argname="argument client_encryption_key_size", value=client_encryption_key_size, expected_type=type_hints["client_encryption_key_size"])
            check_type(argname="argument client_memory_limit", value=client_memory_limit, expected_type=type_hints["client_memory_limit"])
            check_type(argname="argument client_metadata_request_use_connection_ctx", value=client_metadata_request_use_connection_ctx, expected_type=type_hints["client_metadata_request_use_connection_ctx"])
            check_type(argname="argument client_metadata_use_session_database", value=client_metadata_use_session_database, expected_type=type_hints["client_metadata_use_session_database"])
            check_type(argname="argument client_prefetch_threads", value=client_prefetch_threads, expected_type=type_hints["client_prefetch_threads"])
            check_type(argname="argument client_result_chunk_size", value=client_result_chunk_size, expected_type=type_hints["client_result_chunk_size"])
            check_type(argname="argument client_result_column_case_insensitive", value=client_result_column_case_insensitive, expected_type=type_hints["client_result_column_case_insensitive"])
            check_type(argname="argument client_session_keep_alive", value=client_session_keep_alive, expected_type=type_hints["client_session_keep_alive"])
            check_type(argname="argument client_session_keep_alive_heartbeat_frequency", value=client_session_keep_alive_heartbeat_frequency, expected_type=type_hints["client_session_keep_alive_heartbeat_frequency"])
            check_type(argname="argument client_timestamp_type_mapping", value=client_timestamp_type_mapping, expected_type=type_hints["client_timestamp_type_mapping"])
            check_type(argname="argument cortex_enabled_cross_region", value=cortex_enabled_cross_region, expected_type=type_hints["cortex_enabled_cross_region"])
            check_type(argname="argument cortex_models_allowlist", value=cortex_models_allowlist, expected_type=type_hints["cortex_models_allowlist"])
            check_type(argname="argument csv_timestamp_format", value=csv_timestamp_format, expected_type=type_hints["csv_timestamp_format"])
            check_type(argname="argument data_retention_time_in_days", value=data_retention_time_in_days, expected_type=type_hints["data_retention_time_in_days"])
            check_type(argname="argument date_input_format", value=date_input_format, expected_type=type_hints["date_input_format"])
            check_type(argname="argument date_output_format", value=date_output_format, expected_type=type_hints["date_output_format"])
            check_type(argname="argument default_ddl_collation", value=default_ddl_collation, expected_type=type_hints["default_ddl_collation"])
            check_type(argname="argument default_notebook_compute_pool_cpu", value=default_notebook_compute_pool_cpu, expected_type=type_hints["default_notebook_compute_pool_cpu"])
            check_type(argname="argument default_notebook_compute_pool_gpu", value=default_notebook_compute_pool_gpu, expected_type=type_hints["default_notebook_compute_pool_gpu"])
            check_type(argname="argument default_null_ordering", value=default_null_ordering, expected_type=type_hints["default_null_ordering"])
            check_type(argname="argument default_streamlit_notebook_warehouse", value=default_streamlit_notebook_warehouse, expected_type=type_hints["default_streamlit_notebook_warehouse"])
            check_type(argname="argument disable_ui_download_button", value=disable_ui_download_button, expected_type=type_hints["disable_ui_download_button"])
            check_type(argname="argument disable_user_privilege_grants", value=disable_user_privilege_grants, expected_type=type_hints["disable_user_privilege_grants"])
            check_type(argname="argument enable_automatic_sensitive_data_classification_log", value=enable_automatic_sensitive_data_classification_log, expected_type=type_hints["enable_automatic_sensitive_data_classification_log"])
            check_type(argname="argument enable_egress_cost_optimizer", value=enable_egress_cost_optimizer, expected_type=type_hints["enable_egress_cost_optimizer"])
            check_type(argname="argument enable_identifier_first_login", value=enable_identifier_first_login, expected_type=type_hints["enable_identifier_first_login"])
            check_type(argname="argument enable_internal_stages_privatelink", value=enable_internal_stages_privatelink, expected_type=type_hints["enable_internal_stages_privatelink"])
            check_type(argname="argument enable_tri_secret_and_rekey_opt_out_for_image_repository", value=enable_tri_secret_and_rekey_opt_out_for_image_repository, expected_type=type_hints["enable_tri_secret_and_rekey_opt_out_for_image_repository"])
            check_type(argname="argument enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage", value=enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage, expected_type=type_hints["enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage"])
            check_type(argname="argument enable_unhandled_exceptions_reporting", value=enable_unhandled_exceptions_reporting, expected_type=type_hints["enable_unhandled_exceptions_reporting"])
            check_type(argname="argument enable_unload_physical_type_optimization", value=enable_unload_physical_type_optimization, expected_type=type_hints["enable_unload_physical_type_optimization"])
            check_type(argname="argument enable_unredacted_query_syntax_error", value=enable_unredacted_query_syntax_error, expected_type=type_hints["enable_unredacted_query_syntax_error"])
            check_type(argname="argument enable_unredacted_secure_object_error", value=enable_unredacted_secure_object_error, expected_type=type_hints["enable_unredacted_secure_object_error"])
            check_type(argname="argument enforce_network_rules_for_internal_stages", value=enforce_network_rules_for_internal_stages, expected_type=type_hints["enforce_network_rules_for_internal_stages"])
            check_type(argname="argument error_on_nondeterministic_merge", value=error_on_nondeterministic_merge, expected_type=type_hints["error_on_nondeterministic_merge"])
            check_type(argname="argument error_on_nondeterministic_update", value=error_on_nondeterministic_update, expected_type=type_hints["error_on_nondeterministic_update"])
            check_type(argname="argument event_table", value=event_table, expected_type=type_hints["event_table"])
            check_type(argname="argument external_oauth_add_privileged_roles_to_blocked_list", value=external_oauth_add_privileged_roles_to_blocked_list, expected_type=type_hints["external_oauth_add_privileged_roles_to_blocked_list"])
            check_type(argname="argument external_volume", value=external_volume, expected_type=type_hints["external_volume"])
            check_type(argname="argument feature_policy", value=feature_policy, expected_type=type_hints["feature_policy"])
            check_type(argname="argument geography_output_format", value=geography_output_format, expected_type=type_hints["geography_output_format"])
            check_type(argname="argument geometry_output_format", value=geometry_output_format, expected_type=type_hints["geometry_output_format"])
            check_type(argname="argument hybrid_table_lock_timeout", value=hybrid_table_lock_timeout, expected_type=type_hints["hybrid_table_lock_timeout"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initial_replication_size_limit_in_tb", value=initial_replication_size_limit_in_tb, expected_type=type_hints["initial_replication_size_limit_in_tb"])
            check_type(argname="argument jdbc_treat_decimal_as_int", value=jdbc_treat_decimal_as_int, expected_type=type_hints["jdbc_treat_decimal_as_int"])
            check_type(argname="argument jdbc_treat_timestamp_ntz_as_utc", value=jdbc_treat_timestamp_ntz_as_utc, expected_type=type_hints["jdbc_treat_timestamp_ntz_as_utc"])
            check_type(argname="argument jdbc_use_session_timezone", value=jdbc_use_session_timezone, expected_type=type_hints["jdbc_use_session_timezone"])
            check_type(argname="argument json_indent", value=json_indent, expected_type=type_hints["json_indent"])
            check_type(argname="argument js_treat_integer_as_bigint", value=js_treat_integer_as_bigint, expected_type=type_hints["js_treat_integer_as_bigint"])
            check_type(argname="argument listing_auto_fulfillment_replication_refresh_schedule", value=listing_auto_fulfillment_replication_refresh_schedule, expected_type=type_hints["listing_auto_fulfillment_replication_refresh_schedule"])
            check_type(argname="argument lock_timeout", value=lock_timeout, expected_type=type_hints["lock_timeout"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument max_concurrency_level", value=max_concurrency_level, expected_type=type_hints["max_concurrency_level"])
            check_type(argname="argument max_data_extension_time_in_days", value=max_data_extension_time_in_days, expected_type=type_hints["max_data_extension_time_in_days"])
            check_type(argname="argument metric_level", value=metric_level, expected_type=type_hints["metric_level"])
            check_type(argname="argument min_data_retention_time_in_days", value=min_data_retention_time_in_days, expected_type=type_hints["min_data_retention_time_in_days"])
            check_type(argname="argument multi_statement_count", value=multi_statement_count, expected_type=type_hints["multi_statement_count"])
            check_type(argname="argument network_policy", value=network_policy, expected_type=type_hints["network_policy"])
            check_type(argname="argument noorder_sequence_as_default", value=noorder_sequence_as_default, expected_type=type_hints["noorder_sequence_as_default"])
            check_type(argname="argument oauth_add_privileged_roles_to_blocked_list", value=oauth_add_privileged_roles_to_blocked_list, expected_type=type_hints["oauth_add_privileged_roles_to_blocked_list"])
            check_type(argname="argument odbc_treat_decimal_as_int", value=odbc_treat_decimal_as_int, expected_type=type_hints["odbc_treat_decimal_as_int"])
            check_type(argname="argument packages_policy", value=packages_policy, expected_type=type_hints["packages_policy"])
            check_type(argname="argument password_policy", value=password_policy, expected_type=type_hints["password_policy"])
            check_type(argname="argument periodic_data_rekeying", value=periodic_data_rekeying, expected_type=type_hints["periodic_data_rekeying"])
            check_type(argname="argument pipe_execution_paused", value=pipe_execution_paused, expected_type=type_hints["pipe_execution_paused"])
            check_type(argname="argument prevent_unload_to_inline_url", value=prevent_unload_to_inline_url, expected_type=type_hints["prevent_unload_to_inline_url"])
            check_type(argname="argument prevent_unload_to_internal_stages", value=prevent_unload_to_internal_stages, expected_type=type_hints["prevent_unload_to_internal_stages"])
            check_type(argname="argument python_profiler_modules", value=python_profiler_modules, expected_type=type_hints["python_profiler_modules"])
            check_type(argname="argument python_profiler_target_stage", value=python_profiler_target_stage, expected_type=type_hints["python_profiler_target_stage"])
            check_type(argname="argument query_tag", value=query_tag, expected_type=type_hints["query_tag"])
            check_type(argname="argument quoted_identifiers_ignore_case", value=quoted_identifiers_ignore_case, expected_type=type_hints["quoted_identifiers_ignore_case"])
            check_type(argname="argument replace_invalid_characters", value=replace_invalid_characters, expected_type=type_hints["replace_invalid_characters"])
            check_type(argname="argument require_storage_integration_for_stage_creation", value=require_storage_integration_for_stage_creation, expected_type=type_hints["require_storage_integration_for_stage_creation"])
            check_type(argname="argument require_storage_integration_for_stage_operation", value=require_storage_integration_for_stage_operation, expected_type=type_hints["require_storage_integration_for_stage_operation"])
            check_type(argname="argument resource_monitor", value=resource_monitor, expected_type=type_hints["resource_monitor"])
            check_type(argname="argument rows_per_resultset", value=rows_per_resultset, expected_type=type_hints["rows_per_resultset"])
            check_type(argname="argument s3_stage_vpce_dns_name", value=s3_stage_vpce_dns_name, expected_type=type_hints["s3_stage_vpce_dns_name"])
            check_type(argname="argument saml_identity_provider", value=saml_identity_provider, expected_type=type_hints["saml_identity_provider"])
            check_type(argname="argument search_path", value=search_path, expected_type=type_hints["search_path"])
            check_type(argname="argument serverless_task_max_statement_size", value=serverless_task_max_statement_size, expected_type=type_hints["serverless_task_max_statement_size"])
            check_type(argname="argument serverless_task_min_statement_size", value=serverless_task_min_statement_size, expected_type=type_hints["serverless_task_min_statement_size"])
            check_type(argname="argument session_policy", value=session_policy, expected_type=type_hints["session_policy"])
            check_type(argname="argument simulated_data_sharing_consumer", value=simulated_data_sharing_consumer, expected_type=type_hints["simulated_data_sharing_consumer"])
            check_type(argname="argument sso_login_page", value=sso_login_page, expected_type=type_hints["sso_login_page"])
            check_type(argname="argument statement_queued_timeout_in_seconds", value=statement_queued_timeout_in_seconds, expected_type=type_hints["statement_queued_timeout_in_seconds"])
            check_type(argname="argument statement_timeout_in_seconds", value=statement_timeout_in_seconds, expected_type=type_hints["statement_timeout_in_seconds"])
            check_type(argname="argument storage_serialization_policy", value=storage_serialization_policy, expected_type=type_hints["storage_serialization_policy"])
            check_type(argname="argument strict_json_output", value=strict_json_output, expected_type=type_hints["strict_json_output"])
            check_type(argname="argument suspend_task_after_num_failures", value=suspend_task_after_num_failures, expected_type=type_hints["suspend_task_after_num_failures"])
            check_type(argname="argument task_auto_retry_attempts", value=task_auto_retry_attempts, expected_type=type_hints["task_auto_retry_attempts"])
            check_type(argname="argument time_input_format", value=time_input_format, expected_type=type_hints["time_input_format"])
            check_type(argname="argument time_output_format", value=time_output_format, expected_type=type_hints["time_output_format"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
            check_type(argname="argument week_of_year_policy", value=week_of_year_policy, expected_type=type_hints["week_of_year_policy"])
            check_type(argname="argument week_start", value=week_start, expected_type=type_hints["week_start"])
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
        if abort_detached_query is not None:
            self._values["abort_detached_query"] = abort_detached_query
        if active_python_profiler is not None:
            self._values["active_python_profiler"] = active_python_profiler
        if allow_client_mfa_caching is not None:
            self._values["allow_client_mfa_caching"] = allow_client_mfa_caching
        if allow_id_token is not None:
            self._values["allow_id_token"] = allow_id_token
        if authentication_policy is not None:
            self._values["authentication_policy"] = authentication_policy
        if autocommit is not None:
            self._values["autocommit"] = autocommit
        if base_location_prefix is not None:
            self._values["base_location_prefix"] = base_location_prefix
        if binary_input_format is not None:
            self._values["binary_input_format"] = binary_input_format
        if binary_output_format is not None:
            self._values["binary_output_format"] = binary_output_format
        if catalog is not None:
            self._values["catalog"] = catalog
        if catalog_sync is not None:
            self._values["catalog_sync"] = catalog_sync
        if client_enable_log_info_statement_parameters is not None:
            self._values["client_enable_log_info_statement_parameters"] = client_enable_log_info_statement_parameters
        if client_encryption_key_size is not None:
            self._values["client_encryption_key_size"] = client_encryption_key_size
        if client_memory_limit is not None:
            self._values["client_memory_limit"] = client_memory_limit
        if client_metadata_request_use_connection_ctx is not None:
            self._values["client_metadata_request_use_connection_ctx"] = client_metadata_request_use_connection_ctx
        if client_metadata_use_session_database is not None:
            self._values["client_metadata_use_session_database"] = client_metadata_use_session_database
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
        if cortex_enabled_cross_region is not None:
            self._values["cortex_enabled_cross_region"] = cortex_enabled_cross_region
        if cortex_models_allowlist is not None:
            self._values["cortex_models_allowlist"] = cortex_models_allowlist
        if csv_timestamp_format is not None:
            self._values["csv_timestamp_format"] = csv_timestamp_format
        if data_retention_time_in_days is not None:
            self._values["data_retention_time_in_days"] = data_retention_time_in_days
        if date_input_format is not None:
            self._values["date_input_format"] = date_input_format
        if date_output_format is not None:
            self._values["date_output_format"] = date_output_format
        if default_ddl_collation is not None:
            self._values["default_ddl_collation"] = default_ddl_collation
        if default_notebook_compute_pool_cpu is not None:
            self._values["default_notebook_compute_pool_cpu"] = default_notebook_compute_pool_cpu
        if default_notebook_compute_pool_gpu is not None:
            self._values["default_notebook_compute_pool_gpu"] = default_notebook_compute_pool_gpu
        if default_null_ordering is not None:
            self._values["default_null_ordering"] = default_null_ordering
        if default_streamlit_notebook_warehouse is not None:
            self._values["default_streamlit_notebook_warehouse"] = default_streamlit_notebook_warehouse
        if disable_ui_download_button is not None:
            self._values["disable_ui_download_button"] = disable_ui_download_button
        if disable_user_privilege_grants is not None:
            self._values["disable_user_privilege_grants"] = disable_user_privilege_grants
        if enable_automatic_sensitive_data_classification_log is not None:
            self._values["enable_automatic_sensitive_data_classification_log"] = enable_automatic_sensitive_data_classification_log
        if enable_egress_cost_optimizer is not None:
            self._values["enable_egress_cost_optimizer"] = enable_egress_cost_optimizer
        if enable_identifier_first_login is not None:
            self._values["enable_identifier_first_login"] = enable_identifier_first_login
        if enable_internal_stages_privatelink is not None:
            self._values["enable_internal_stages_privatelink"] = enable_internal_stages_privatelink
        if enable_tri_secret_and_rekey_opt_out_for_image_repository is not None:
            self._values["enable_tri_secret_and_rekey_opt_out_for_image_repository"] = enable_tri_secret_and_rekey_opt_out_for_image_repository
        if enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage is not None:
            self._values["enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage"] = enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage
        if enable_unhandled_exceptions_reporting is not None:
            self._values["enable_unhandled_exceptions_reporting"] = enable_unhandled_exceptions_reporting
        if enable_unload_physical_type_optimization is not None:
            self._values["enable_unload_physical_type_optimization"] = enable_unload_physical_type_optimization
        if enable_unredacted_query_syntax_error is not None:
            self._values["enable_unredacted_query_syntax_error"] = enable_unredacted_query_syntax_error
        if enable_unredacted_secure_object_error is not None:
            self._values["enable_unredacted_secure_object_error"] = enable_unredacted_secure_object_error
        if enforce_network_rules_for_internal_stages is not None:
            self._values["enforce_network_rules_for_internal_stages"] = enforce_network_rules_for_internal_stages
        if error_on_nondeterministic_merge is not None:
            self._values["error_on_nondeterministic_merge"] = error_on_nondeterministic_merge
        if error_on_nondeterministic_update is not None:
            self._values["error_on_nondeterministic_update"] = error_on_nondeterministic_update
        if event_table is not None:
            self._values["event_table"] = event_table
        if external_oauth_add_privileged_roles_to_blocked_list is not None:
            self._values["external_oauth_add_privileged_roles_to_blocked_list"] = external_oauth_add_privileged_roles_to_blocked_list
        if external_volume is not None:
            self._values["external_volume"] = external_volume
        if feature_policy is not None:
            self._values["feature_policy"] = feature_policy
        if geography_output_format is not None:
            self._values["geography_output_format"] = geography_output_format
        if geometry_output_format is not None:
            self._values["geometry_output_format"] = geometry_output_format
        if hybrid_table_lock_timeout is not None:
            self._values["hybrid_table_lock_timeout"] = hybrid_table_lock_timeout
        if id is not None:
            self._values["id"] = id
        if initial_replication_size_limit_in_tb is not None:
            self._values["initial_replication_size_limit_in_tb"] = initial_replication_size_limit_in_tb
        if jdbc_treat_decimal_as_int is not None:
            self._values["jdbc_treat_decimal_as_int"] = jdbc_treat_decimal_as_int
        if jdbc_treat_timestamp_ntz_as_utc is not None:
            self._values["jdbc_treat_timestamp_ntz_as_utc"] = jdbc_treat_timestamp_ntz_as_utc
        if jdbc_use_session_timezone is not None:
            self._values["jdbc_use_session_timezone"] = jdbc_use_session_timezone
        if json_indent is not None:
            self._values["json_indent"] = json_indent
        if js_treat_integer_as_bigint is not None:
            self._values["js_treat_integer_as_bigint"] = js_treat_integer_as_bigint
        if listing_auto_fulfillment_replication_refresh_schedule is not None:
            self._values["listing_auto_fulfillment_replication_refresh_schedule"] = listing_auto_fulfillment_replication_refresh_schedule
        if lock_timeout is not None:
            self._values["lock_timeout"] = lock_timeout
        if log_level is not None:
            self._values["log_level"] = log_level
        if max_concurrency_level is not None:
            self._values["max_concurrency_level"] = max_concurrency_level
        if max_data_extension_time_in_days is not None:
            self._values["max_data_extension_time_in_days"] = max_data_extension_time_in_days
        if metric_level is not None:
            self._values["metric_level"] = metric_level
        if min_data_retention_time_in_days is not None:
            self._values["min_data_retention_time_in_days"] = min_data_retention_time_in_days
        if multi_statement_count is not None:
            self._values["multi_statement_count"] = multi_statement_count
        if network_policy is not None:
            self._values["network_policy"] = network_policy
        if noorder_sequence_as_default is not None:
            self._values["noorder_sequence_as_default"] = noorder_sequence_as_default
        if oauth_add_privileged_roles_to_blocked_list is not None:
            self._values["oauth_add_privileged_roles_to_blocked_list"] = oauth_add_privileged_roles_to_blocked_list
        if odbc_treat_decimal_as_int is not None:
            self._values["odbc_treat_decimal_as_int"] = odbc_treat_decimal_as_int
        if packages_policy is not None:
            self._values["packages_policy"] = packages_policy
        if password_policy is not None:
            self._values["password_policy"] = password_policy
        if periodic_data_rekeying is not None:
            self._values["periodic_data_rekeying"] = periodic_data_rekeying
        if pipe_execution_paused is not None:
            self._values["pipe_execution_paused"] = pipe_execution_paused
        if prevent_unload_to_inline_url is not None:
            self._values["prevent_unload_to_inline_url"] = prevent_unload_to_inline_url
        if prevent_unload_to_internal_stages is not None:
            self._values["prevent_unload_to_internal_stages"] = prevent_unload_to_internal_stages
        if python_profiler_modules is not None:
            self._values["python_profiler_modules"] = python_profiler_modules
        if python_profiler_target_stage is not None:
            self._values["python_profiler_target_stage"] = python_profiler_target_stage
        if query_tag is not None:
            self._values["query_tag"] = query_tag
        if quoted_identifiers_ignore_case is not None:
            self._values["quoted_identifiers_ignore_case"] = quoted_identifiers_ignore_case
        if replace_invalid_characters is not None:
            self._values["replace_invalid_characters"] = replace_invalid_characters
        if require_storage_integration_for_stage_creation is not None:
            self._values["require_storage_integration_for_stage_creation"] = require_storage_integration_for_stage_creation
        if require_storage_integration_for_stage_operation is not None:
            self._values["require_storage_integration_for_stage_operation"] = require_storage_integration_for_stage_operation
        if resource_monitor is not None:
            self._values["resource_monitor"] = resource_monitor
        if rows_per_resultset is not None:
            self._values["rows_per_resultset"] = rows_per_resultset
        if s3_stage_vpce_dns_name is not None:
            self._values["s3_stage_vpce_dns_name"] = s3_stage_vpce_dns_name
        if saml_identity_provider is not None:
            self._values["saml_identity_provider"] = saml_identity_provider
        if search_path is not None:
            self._values["search_path"] = search_path
        if serverless_task_max_statement_size is not None:
            self._values["serverless_task_max_statement_size"] = serverless_task_max_statement_size
        if serverless_task_min_statement_size is not None:
            self._values["serverless_task_min_statement_size"] = serverless_task_min_statement_size
        if session_policy is not None:
            self._values["session_policy"] = session_policy
        if simulated_data_sharing_consumer is not None:
            self._values["simulated_data_sharing_consumer"] = simulated_data_sharing_consumer
        if sso_login_page is not None:
            self._values["sso_login_page"] = sso_login_page
        if statement_queued_timeout_in_seconds is not None:
            self._values["statement_queued_timeout_in_seconds"] = statement_queued_timeout_in_seconds
        if statement_timeout_in_seconds is not None:
            self._values["statement_timeout_in_seconds"] = statement_timeout_in_seconds
        if storage_serialization_policy is not None:
            self._values["storage_serialization_policy"] = storage_serialization_policy
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
        if timeouts is not None:
            self._values["timeouts"] = timeouts
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
    def abort_detached_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action that Snowflake performs for in-progress queries if connectivity is lost due to abrupt termination of a session (e.g. network outage, browser termination, service interruption). For more information, check `ABORT_DETACHED_QUERY docs <https://docs.snowflake.com/en/sql-reference/parameters#abort-detached-query>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#abort_detached_query CurrentAccount#abort_detached_query}
        '''
        result = self._values.get("abort_detached_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def active_python_profiler(self) -> typing.Optional[builtins.str]:
        '''Sets the profiler to use for the session when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. Valid values are (case-insensitive): ``LINE`` | ``MEMORY``. For more information, check `ACTIVE_PYTHON_PROFILER docs <https://docs.snowflake.com/en/sql-reference/parameters#active-python-profiler>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#active_python_profiler CurrentAccount#active_python_profiler}
        '''
        result = self._values.get("active_python_profiler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_client_mfa_caching(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether an MFA token can be saved in the client-side operating system keystore to promote continuous, secure connectivity without users needing to respond to an MFA prompt at the start of each connection attempt to Snowflake.

        For details and the list of supported Snowflake-provided clients, see `Using MFA token caching to minimize the number of prompts during authentication — optional. <https://docs.snowflake.com/en/user-guide/security-mfa.html#label-mfa-token-caching>`_ For more information, check `ALLOW_CLIENT_MFA_CACHING docs <https://docs.snowflake.com/en/sql-reference/parameters#allow-client-mfa-caching>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#allow_client_mfa_caching CurrentAccount#allow_client_mfa_caching}
        '''
        result = self._values.get("allow_client_mfa_caching")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_id_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether a connection token can be saved in the client-side operating system keystore to promote continuous, secure connectivity without users needing to enter login credentials at the start of each connection attempt to Snowflake.

        For details and the list of supported Snowflake-provided clients, see `Using connection caching to minimize the number of prompts for authentication — optional. <https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-use.html#label-browser-based-sso-connection-caching>`_ For more information, check `ALLOW_ID_TOKEN docs <https://docs.snowflake.com/en/sql-reference/parameters#allow-id-token>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#allow_id_token CurrentAccount#allow_id_token}
        '''
        result = self._values.get("allow_id_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def authentication_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies `authentication policy <https://docs.snowflake.com/en/user-guide/authentication-policies>`_ for the current account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#authentication_policy CurrentAccount#authentication_policy}
        '''
        result = self._values.get("authentication_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def autocommit(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether autocommit is enabled for the session.

        Autocommit determines whether a DML statement, when executed without an active transaction, is automatically committed after the statement successfully completes. For more information, see `Transactions <https://docs.snowflake.com/en/sql-reference/transactions>`_. For more information, check `AUTOCOMMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#autocommit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#autocommit CurrentAccount#autocommit}
        '''
        result = self._values.get("autocommit")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def base_location_prefix(self) -> typing.Optional[builtins.str]:
        '''Specifies a prefix for Snowflake to use in the write path for Snowflake-managed Apache Iceberg™ tables.

        For more information, see `data and metadata directories for Iceberg tables <https://docs.snowflake.com/en/user-guide/tables-iceberg-storage.html#label-tables-iceberg-configure-external-volume-base-location>`_. For more information, check `BASE_LOCATION_PREFIX docs <https://docs.snowflake.com/en/sql-reference/parameters#base-location-prefix>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#base_location_prefix CurrentAccount#base_location_prefix}
        '''
        result = self._values.get("base_location_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_input_format(self) -> typing.Optional[builtins.str]:
        '''The format of VARCHAR values passed as input to VARCHAR-to-BINARY conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. Valid values are (case-insensitive): ``HEX`` | ``BASE64`` | ``UTF8``. For more information, check `BINARY_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#binary_input_format CurrentAccount#binary_input_format}
        '''
        result = self._values.get("binary_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_output_format(self) -> typing.Optional[builtins.str]:
        '''The format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions.

        For more information, see `Binary input and output <https://docs.snowflake.com/en/sql-reference/binary-input-output>`_. Valid values are (case-insensitive): ``HEX`` | ``BASE64``. For more information, check `BINARY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#binary-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#binary_output_format CurrentAccount#binary_output_format}
        '''
        result = self._values.get("binary_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''Specifies the catalog for Apache Iceberg™ tables.

        For more information, see the `Iceberg table documentation <https://docs.snowflake.com/en/user-guide/tables-iceberg.html#label-tables-iceberg-catalog-def>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `CATALOG docs <https://docs.snowflake.com/en/sql-reference/parameters#catalog>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#catalog CurrentAccount#catalog}
        '''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def catalog_sync(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of your catalog integration for `Snowflake Open Catalog <https://other-docs.snowflake.com/en/opencatalog/overview>`_. Snowflake syncs tables that use the specified catalog integration with your Snowflake Open Catalog account. For more information, see `Sync a Snowflake-managed table with Snowflake Open Catalog <https://docs.snowflake.com/en/user-guide/tables-iceberg-open-catalog-sync>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `CATALOG_SYNC docs <https://docs.snowflake.com/en/sql-reference/parameters#catalog-sync>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#catalog_sync CurrentAccount#catalog_sync}
        '''
        result = self._values.get("catalog_sync")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_enable_log_info_statement_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables users to log the data values bound to `PreparedStatements <https://docs.snowflake.com/en/developer-guide/jdbc/jdbc-api.html#label-jdbc-api-preparedstatement>`_ (`more details <https://docs.snowflake.com/en/sql-reference/parameters#client-enable-log-info-statement-parameters>`_). For more information, check `CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-enable-log-info-statement-parameters>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_enable_log_info_statement_parameters CurrentAccount#client_enable_log_info_statement_parameters}
        '''
        result = self._values.get("client_enable_log_info_statement_parameters")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_encryption_key_size(self) -> typing.Optional[jsii.Number]:
        '''Specifies the AES encryption key size, in bits, used by Snowflake to encrypt/decrypt files stored on internal stages (for loading/unloading data) when you use the SNOWFLAKE_FULL encryption type.

        For more information, check `CLIENT_ENCRYPTION_KEY_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-encryption-key-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_encryption_key_size CurrentAccount#client_encryption_key_size}
        '''
        result = self._values.get("client_encryption_key_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_memory_limit(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum amount of memory the JDBC driver or ODBC driver should use for the result set from queries (in MB).

        For more information, check `CLIENT_MEMORY_LIMIT docs <https://docs.snowflake.com/en/sql-reference/parameters#client-memory-limit>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_memory_limit CurrentAccount#client_memory_limit}
        '''
        result = self._values.get("client_memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_metadata_request_use_connection_ctx(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases/schemas to the current database/schema.

        The narrower search typically returns fewer rows and executes more quickly. For more information, check `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-request-use-connection-ctx>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_metadata_request_use_connection_ctx CurrentAccount#client_metadata_request_use_connection_ctx}
        '''
        result = self._values.get("client_metadata_request_use_connection_ctx")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_metadata_use_session_database(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''For specific ODBC functions and JDBC methods, this parameter can change the default search scope from all databases to the current database.

        The narrower search typically returns fewer rows and executes more quickly (`more details on the usage <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-use-session-database>`_). For more information, check `CLIENT_METADATA_USE_SESSION_DATABASE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-metadata-use-session-database>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_metadata_use_session_database CurrentAccount#client_metadata_use_session_database}
        '''
        result = self._values.get("client_metadata_use_session_database")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_prefetch_threads(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the number of threads used by the client to pre-fetch large result sets.

        The driver will attempt to honor the parameter value, but defines the minimum and maximum values (depending on your system’s resources) to improve performance. For more information, check `CLIENT_PREFETCH_THREADS docs <https://docs.snowflake.com/en/sql-reference/parameters#client-prefetch-threads>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_prefetch_threads CurrentAccount#client_prefetch_threads}
        '''
        result = self._values.get("client_prefetch_threads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_chunk_size(self) -> typing.Optional[jsii.Number]:
        '''Parameter that specifies the maximum size of each set (or chunk) of query results to download (in MB).

        The JDBC driver downloads query results in chunks. For more information, check `CLIENT_RESULT_CHUNK_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-chunk-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_result_chunk_size CurrentAccount#client_result_chunk_size}
        '''
        result = self._values.get("client_result_chunk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_result_column_case_insensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to match column name case-insensitively in ResultSet.get* methods in JDBC. For more information, check `CLIENT_RESULT_COLUMN_CASE_INSENSITIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-result-column-case-insensitive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_result_column_case_insensitive CurrentAccount#client_result_column_case_insensitive}
        '''
        result = self._values.get("client_result_column_case_insensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Parameter that indicates whether to force a user to log in again after a period of inactivity in the session.

        For more information, check `CLIENT_SESSION_KEEP_ALIVE docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_session_keep_alive CurrentAccount#client_session_keep_alive}
        '''
        result = self._values.get("client_session_keep_alive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_session_keep_alive_heartbeat_frequency(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Number of seconds in-between client attempts to update the token for the session. For more information, check `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY docs <https://docs.snowflake.com/en/sql-reference/parameters#client-session-keep-alive-heartbeat-frequency>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_session_keep_alive_heartbeat_frequency CurrentAccount#client_session_keep_alive_heartbeat_frequency}
        '''
        result = self._values.get("client_session_keep_alive_heartbeat_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def client_timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the `TIMESTAMP_* variation <https://docs.snowflake.com/en/sql-reference/data-types-datetime.html#label-datatypes-timestamp-variations>`_ to use when binding timestamp variables for JDBC or ODBC applications that use the bind API to load data. Valid values are (case-insensitive): ``TIMESTAMP_LTZ`` | ``TIMESTAMP_NTZ``. For more information, check `CLIENT_TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#client-timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#client_timestamp_type_mapping CurrentAccount#client_timestamp_type_mapping}
        '''
        result = self._values.get("client_timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cortex_enabled_cross_region(self) -> typing.Optional[builtins.str]:
        '''Specifies the regions where an inference request may be processed in case the request cannot be processed in the region where request is originally placed.

        Specifying DISABLED disables cross-region inferencing. For examples and details, see `Cross-region inference <https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference>`_. For more information, check `CORTEX_ENABLED_CROSS_REGION docs <https://docs.snowflake.com/en/sql-reference/parameters#cortex-enabled-cross-region>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#cortex_enabled_cross_region CurrentAccount#cortex_enabled_cross_region}
        '''
        result = self._values.get("cortex_enabled_cross_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cortex_models_allowlist(self) -> typing.Optional[builtins.str]:
        '''Specifies the models that users in the account can access.

        Use this parameter to allowlist models for all users in the account. If you need to provide specific users with access beyond what you’ve specified in the allowlist, use role-based access control instead. For more information, see `Model allowlist <https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql.html#label-cortex-llm-allowlist>`_. For more information, check `CORTEX_MODELS_ALLOWLIST docs <https://docs.snowflake.com/en/sql-reference/parameters#cortex-models-allowlist>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#cortex_models_allowlist CurrentAccount#cortex_models_allowlist}
        '''
        result = self._values.get("cortex_models_allowlist")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def csv_timestamp_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the format for TIMESTAMP values in CSV files downloaded from Snowsight.

        If this parameter is not set, `TIMESTAMP_LTZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-ltz-output-format>`_ will be used for TIMESTAMP_LTZ values, `TIMESTAMP_TZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-tz-output-format>`_ will be used for TIMESTAMP_TZ and `TIMESTAMP_NTZ_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-ntz-output-format>`_ for TIMESTAMP_NTZ values. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_ or `Download your query results <https://docs.snowflake.com/en/user-guide/ui-snowsight-query.html#label-snowsight-download-query-results>`_. For more information, check `CSV_TIMESTAMP_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#csv-timestamp-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#csv_timestamp_format CurrentAccount#csv_timestamp_format}
        '''
        result = self._values.get("csv_timestamp_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_retention_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on the object.

        A value of 0 effectively disables Time Travel for the specified database, schema, or table. For more information, see `Understanding & using Time Travel <https://docs.snowflake.com/en/user-guide/data-time-travel>`_. For more information, check `DATA_RETENTION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#data-retention-time-in-days>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#data_retention_time_in_days CurrentAccount#data_retention_time_in_days}
        '''
        result = self._values.get("data_retention_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def date_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#date_input_format CurrentAccount#date_input_format}
        '''
        result = self._values.get("date_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the DATE data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `DATE_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#date-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#date_output_format CurrentAccount#date_output_format}
        '''
        result = self._values.get("date_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_ddl_collation(self) -> typing.Optional[builtins.str]:
        '''Sets the default collation used for the following DDL operations: `CREATE TABLE <https://docs.snowflake.com/en/sql-reference/sql/create-table>`_, `ALTER TABLE <https://docs.snowflake.com/en/sql-reference/sql/alter-table>`_ … ADD COLUMN. Setting this parameter forces all subsequently-created columns in the affected objects (table, schema, database, or account) to have the specified collation as the default, unless the collation for the column is explicitly defined in the DDL. For more information, check `DEFAULT_DDL_COLLATION docs <https://docs.snowflake.com/en/sql-reference/parameters#default-ddl-collation>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_ddl_collation CurrentAccount#default_ddl_collation}
        '''
        result = self._values.get("default_ddl_collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_notebook_compute_pool_cpu(self) -> typing.Optional[builtins.str]:
        '''Sets the preferred CPU compute pool used for `Notebooks on CPU Container Runtime <https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU docs <https://docs.snowflake.com/en/sql-reference/parameters#default-notebook-compute-pool-cpu>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_notebook_compute_pool_cpu CurrentAccount#default_notebook_compute_pool_cpu}
        '''
        result = self._values.get("default_notebook_compute_pool_cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_notebook_compute_pool_gpu(self) -> typing.Optional[builtins.str]:
        '''Sets the preferred GPU compute pool used for `Notebooks on GPU Container Runtime <https://docs.snowflake.com/en/developer-guide/snowflake-ml/notebooks-on-spcs>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU docs <https://docs.snowflake.com/en/sql-reference/parameters#default-notebook-compute-pool-gpu>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_notebook_compute_pool_gpu CurrentAccount#default_notebook_compute_pool_gpu}
        '''
        result = self._values.get("default_notebook_compute_pool_gpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_null_ordering(self) -> typing.Optional[builtins.str]:
        '''Specifies the default ordering of NULL values in a result set (`more details <https://docs.snowflake.com/en/sql-reference/parameters#default-null-ordering>`_). Valid values are (case-insensitive): ``FIRST`` | ``LAST``. For more information, check `DEFAULT_NULL_ORDERING docs <https://docs.snowflake.com/en/sql-reference/parameters#default-null-ordering>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_null_ordering CurrentAccount#default_null_ordering}
        '''
        result = self._values.get("default_null_ordering")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_streamlit_notebook_warehouse(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the default warehouse to use when creating a notebook.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE docs <https://docs.snowflake.com/en/sql-reference/parameters#default-streamlit-notebook-warehouse>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#default_streamlit_notebook_warehouse CurrentAccount#default_streamlit_notebook_warehouse}
        '''
        result = self._values.get("default_streamlit_notebook_warehouse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_ui_download_button(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether users in an account see a button to download data in Snowsight or the Classic Console, such as a table returned from running a query in a worksheet.

        If the button to download is hidden in Snowsight or the Classic Console, users can still download or export data using `third-party software <https://docs.snowflake.com/en/user-guide/ecosystem>`_. For more information, check `DISABLE_UI_DOWNLOAD_BUTTON docs <https://docs.snowflake.com/en/sql-reference/parameters#disable-ui-download-button>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#disable_ui_download_button CurrentAccount#disable_ui_download_button}
        '''
        result = self._values.get("disable_ui_download_button")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_user_privilege_grants(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether users in an account can grant privileges directly to other users.

        Disabling user privilege grants (that is, setting DISABLE_USER_PRIVILEGE_GRANTS to TRUE) does not affect existing grants to users. Existing grants to users continue to confer privileges to those users. For more information, see `GRANT  … TO USER <https://docs.snowflake.com/en/sql-reference/sql/grant-privilege-user>`_. For more information, check `DISABLE_USER_PRIVILEGE_GRANTS docs <https://docs.snowflake.com/en/sql-reference/parameters#disable-user-privilege-grants>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#disable_user_privilege_grants CurrentAccount#disable_user_privilege_grants}
        '''
        result = self._values.get("disable_user_privilege_grants")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_automatic_sensitive_data_classification_log(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether events from `automatic sensitive data classification <https://docs.snowflake.com/en/user-guide/classify-auto>`_ are logged in the user event table. For more information, check `ENABLE_AUTOMATIC_SENSITIVE_DATA_CLASSIFICATION_LOG docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-automatic-sensitive-data-classification-log>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_automatic_sensitive_data_classification_log CurrentAccount#enable_automatic_sensitive_data_classification_log}
        '''
        result = self._values.get("enable_automatic_sensitive_data_classification_log")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_egress_cost_optimizer(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables or disables the Listing Cross-cloud auto-fulfillment Egress cost optimizer. For more information, check `ENABLE_EGRESS_COST_OPTIMIZER docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-egress-cost-optimizer>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_egress_cost_optimizer CurrentAccount#enable_egress_cost_optimizer}
        '''
        result = self._values.get("enable_egress_cost_optimizer")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_identifier_first_login(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines the login flow for users.

        When enabled, Snowflake prompts users for their username or email address before presenting authentication methods. For details, see `Identifier-first login <https://docs.snowflake.com/en/user-guide/identifier-first-login>`_. For more information, check `ENABLE_IDENTIFIER_FIRST_LOGIN docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-identifier-first-login>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_identifier_first_login CurrentAccount#enable_identifier_first_login}
        '''
        result = self._values.get("enable_identifier_first_login")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_internal_stages_privatelink(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the `SYSTEM$GET_PRIVATELINK_CONFIG <https://docs.snowflake.com/en/sql-reference/functions/system_get_privatelink_config>`_ function returns the private-internal-stages key in the query result. The corresponding value in the query result is used during the configuration process for private connectivity to internal stages. For more information, check `ENABLE_INTERNAL_STAGES_PRIVATELINK docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-internal-stages-privatelink>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_internal_stages_privatelink CurrentAccount#enable_internal_stages_privatelink}
        '''
        result = self._values.get("enable_internal_stages_privatelink")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_tri_secret_and_rekey_opt_out_for_image_repository(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies choice for the `image repository <https://docs.snowflake.com/en/developer-guide/snowpark-container-services/working-with-registry-repository.html#label-registry-and-repository-image-repository>`_ to opt out of Tri-Secret Secure and `Periodic rekeying <https://docs.snowflake.com/en/user-guide/security-encryption-manage.html#label-periodic-rekeying>`_. For more information, check `ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_IMAGE_REPOSITORY docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-tri-secret-and-rekey-opt-out-for-image-repository>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_tri_secret_and_rekey_opt_out_for_image_repository CurrentAccount#enable_tri_secret_and_rekey_opt_out_for_image_repository}
        '''
        result = self._values.get("enable_tri_secret_and_rekey_opt_out_for_image_repository")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the choice for the `Snowpark Container Services block storage volume <https://docs.snowflake.com/en/developer-guide/snowpark-container-services/block-storage-volume>`_ to opt out of Tri-Secret Secure and `Periodic rekeying <https://docs.snowflake.com/en/user-guide/security-encryption-manage.html#label-periodic-rekeying>`_. For more information, check `ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_SPCS_BLOCK_STORAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-tri-secret-and-rekey-opt-out-for-spcs-block-storage>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage CurrentAccount#enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage}
        '''
        result = self._values.get("enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_unhandled_exceptions_reporting(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether Snowflake may capture – in an event table – log messages or trace event data for unhandled exceptions in procedure or UDF handler code.

        For more information, see `Capturing messages from unhandled exceptions <https://docs.snowflake.com/en/developer-guide/logging-tracing/unhandled-exception-messages>`_. For more information, check `ENABLE_UNHANDLED_EXCEPTIONS_REPORTING docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unhandled-exceptions-reporting>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unhandled_exceptions_reporting CurrentAccount#enable_unhandled_exceptions_reporting}
        '''
        result = self._values.get("enable_unhandled_exceptions_reporting")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_unload_physical_type_optimization(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to set the schema for unloaded Parquet files based on the logical column data types (i.e. the types in the unload SQL query or source table) or on the unloaded column values (i.e. the smallest data types and precision that support the values in the output columns of the unload SQL statement or source table). For more information, check `ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unload-physical-type-optimization>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unload_physical_type_optimization CurrentAccount#enable_unload_physical_type_optimization}
        '''
        result = self._values.get("enable_unload_physical_type_optimization")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_unredacted_query_syntax_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether query text is redacted if a SQL query fails due to a syntax or parsing error.

        If FALSE, the content of a failed query is redacted in the views, pages, and functions that provide a query history. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR parameter. When using the ALTER USER command to set the parameter to TRUE for a particular user, modify the user that you want to see the query text, not the user who executed the query (if those are different users). For more information, check `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-query-syntax-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unredacted_query_syntax_error CurrentAccount#enable_unredacted_query_syntax_error}
        '''
        result = self._values.get("enable_unredacted_query_syntax_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_unredacted_secure_object_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Controls whether error messages related to secure objects are redacted in metadata.

        For more information, see `Secure objects: Redaction of information in error messages <https://docs.snowflake.com/en/release-notes/bcr-bundles/un-bundled/bcr-1858>`_. Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE_UNREDACTED_SECURE_OBJECT_ERROR parameter. When using the ALTER USER command to set the parameter to TRUE for a particular user, modify the user that you want to see the redacted error messages in metadata, not the user who caused the error. For more information, check `ENABLE_UNREDACTED_SECURE_OBJECT_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-unredacted-secure-object-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enable_unredacted_secure_object_error CurrentAccount#enable_unredacted_secure_object_error}
        '''
        result = self._values.get("enable_unredacted_secure_object_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enforce_network_rules_for_internal_stages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether a network policy that uses network rules can restrict access to AWS internal stages.

        This parameter has no effect on network policies that do not use network rules. This account-level parameter affects both account-level and user-level network policies. For details about using network policies and network rules to restrict access to AWS internal stages, including the use of this parameter, see `Protecting internal stages on AWS <https://docs.snowflake.com/en/user-guide/network-policies.html#label-network-policies-rules-stages>`_. For more information, check `ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#enforce-network-rules-for-internal-stages>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#enforce_network_rules_for_internal_stages CurrentAccount#enforce_network_rules_for_internal_stages}
        '''
        result = self._values.get("enforce_network_rules_for_internal_stages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_merge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `MERGE <https://docs.snowflake.com/en/sql-reference/sql/merge>`_ command is used to update or delete a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_MERGE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-merge>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#error_on_nondeterministic_merge CurrentAccount#error_on_nondeterministic_merge}
        '''
        result = self._values.get("error_on_nondeterministic_merge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def error_on_nondeterministic_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to return an error when the `UPDATE <https://docs.snowflake.com/en/sql-reference/sql/update>`_ command is used to update a target row that joins multiple source rows and the system cannot determine the action to perform on the target row. For more information, check `ERROR_ON_NONDETERMINISTIC_UPDATE docs <https://docs.snowflake.com/en/sql-reference/parameters#error-on-nondeterministic-update>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#error_on_nondeterministic_update CurrentAccount#error_on_nondeterministic_update}
        '''
        result = self._values.get("error_on_nondeterministic_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_table(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the event table for logging messages from stored procedures and UDFs contained by the object with which the event table is associated.

        Associating an event table with a database is available in `Enterprise Edition or higher <https://docs.snowflake.com/en/user-guide/intro-editions>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `EVENT_TABLE docs <https://docs.snowflake.com/en/sql-reference/parameters#event-table>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#event_table CurrentAccount#event_table}
        '''
        result = self._values.get("event_table")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_oauth_add_privileged_roles_to_blocked_list(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles can be used as the primary role when creating a Snowflake session based on the access token from the External OAuth authorization server.

        For more information, check `EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST docs <https://docs.snowflake.com/en/sql-reference/parameters#external-oauth-add-privileged-roles-to-blocked-list>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#external_oauth_add_privileged_roles_to_blocked_list CurrentAccount#external_oauth_add_privileged_roles_to_blocked_list}
        '''
        result = self._values.get("external_oauth_add_privileged_roles_to_blocked_list")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_volume(self) -> typing.Optional[builtins.str]:
        '''Specifies the external volume for Apache Iceberg™ tables.

        For more information, see the `Iceberg table documentation <https://docs.snowflake.com/en/user-guide/tables-iceberg.html#label-tables-iceberg-external-volume-def>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `EXTERNAL_VOLUME docs <https://docs.snowflake.com/en/sql-reference/parameters#external-volume>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#external_volume CurrentAccount#external_volume}
        '''
        result = self._values.get("external_volume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def feature_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies `feature policy <https://docs.snowflake.com/en/developer-guide/native-apps/ui-consumer-feature-policies>`_ for the current account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#feature_policy CurrentAccount#feature_policy}
        '''
        result = self._values.get("feature_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geography_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOGRAPHY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geography>`_. Valid values are (case-insensitive): ``GeoJSON`` | ``WKT`` | ``WKB`` | ``EWKT`` | ``EWKB``. For more information, check `GEOGRAPHY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geography-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#geography_output_format CurrentAccount#geography_output_format}
        '''
        result = self._values.get("geography_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geometry_output_format(self) -> typing.Optional[builtins.str]:
        '''Display format for `GEOMETRY values <https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html#label-data-types-geometry>`_. Valid values are (case-insensitive): ``GeoJSON`` | ``WKT`` | ``WKB`` | ``EWKT`` | ``EWKB``. For more information, check `GEOMETRY_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#geometry-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#geometry_output_format CurrentAccount#geometry_output_format}
        '''
        result = self._values.get("geometry_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hybrid_table_lock_timeout(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait while trying to acquire row-level locks on a hybrid table, before timing out and aborting the statement.

        For more information, check `HYBRID_TABLE_LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#hybrid-table-lock-timeout>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#hybrid_table_lock_timeout CurrentAccount#hybrid_table_lock_timeout}
        '''
        result = self._values.get("hybrid_table_lock_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#id CurrentAccount#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_replication_size_limit_in_tb(self) -> typing.Optional[builtins.str]:
        '''Sets the maximum estimated size limit for the initial replication of a primary database to a secondary database (in TB).

        Set this parameter on any account that stores a secondary database. This size limit helps prevent accounts from accidentally incurring large database replication charges. To remove the size limit, set the value to 0.0. It is required to pass numbers with scale of at least 1 (e.g. 20.5, 32.25, 33.333, etc.). For more information, check `INITIAL_REPLICATION_SIZE_LIMIT_IN_TB docs <https://docs.snowflake.com/en/sql-reference/parameters#initial-replication-size-limit-in-tb>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#initial_replication_size_limit_in_tb CurrentAccount#initial_replication_size_limit_in_tb}
        '''
        result = self._values.get("initial_replication_size_limit_in_tb")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jdbc_treat_decimal_as_int(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how JDBC processes columns that have a scale of zero (0). For more information, check `JDBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-decimal-as-int>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_treat_decimal_as_int CurrentAccount#jdbc_treat_decimal_as_int}
        '''
        result = self._values.get("jdbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_treat_timestamp_ntz_as_utc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how JDBC processes TIMESTAMP_NTZ values (`more details <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_). For more information, check `JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-treat-timestamp-ntz-as-utc>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_treat_timestamp_ntz_as_utc CurrentAccount#jdbc_treat_timestamp_ntz_as_utc}
        '''
        result = self._values.get("jdbc_treat_timestamp_ntz_as_utc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jdbc_use_session_timezone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the JDBC Driver uses the time zone of the JVM or the time zone of the session (specified by the `TIMEZONE <https://docs.snowflake.com/en/sql-reference/parameters#label-timezone>`_ parameter) for the getDate(), getTime(), and getTimestamp() methods of the ResultSet class. For more information, check `JDBC_USE_SESSION_TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#jdbc-use-session-timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#jdbc_use_session_timezone CurrentAccount#jdbc_use_session_timezone}
        '''
        result = self._values.get("jdbc_use_session_timezone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def json_indent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of blank spaces to indent each new element in JSON output in the session.

        Also specifies whether to insert newline characters after each element. For more information, check `JSON_INDENT docs <https://docs.snowflake.com/en/sql-reference/parameters#json-indent>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#json_indent CurrentAccount#json_indent}
        '''
        result = self._values.get("json_indent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def js_treat_integer_as_bigint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how the Snowflake Node.js Driver processes numeric columns that have a scale of zero (0), for example INTEGER or NUMBER(p, 0). For more information, check `JS_TREAT_INTEGER_AS_BIGINT docs <https://docs.snowflake.com/en/sql-reference/parameters#js-treat-integer-as-bigint>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#js_treat_integer_as_bigint CurrentAccount#js_treat_integer_as_bigint}
        '''
        result = self._values.get("js_treat_integer_as_bigint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def listing_auto_fulfillment_replication_refresh_schedule(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Sets the time interval used to refresh the application package based data products to other regions.

        For more information, check `LISTING_AUTO_FULFILLMENT_REPLICATION_REFRESH_SCHEDULE docs <https://docs.snowflake.com/en/sql-reference/parameters#listing-auto-fulfillment-replication-refresh-schedule>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#listing_auto_fulfillment_replication_refresh_schedule CurrentAccount#listing_auto_fulfillment_replication_refresh_schedule}
        '''
        result = self._values.get("listing_auto_fulfillment_replication_refresh_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_timeout(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds to wait while trying to lock a resource, before timing out and aborting the statement.

        For more information, check `LOCK_TIMEOUT docs <https://docs.snowflake.com/en/sql-reference/parameters#lock-timeout>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#lock_timeout CurrentAccount#lock_timeout}
        '''
        result = self._values.get("lock_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the severity level of messages that should be ingested and made available in the active event table.

        Messages at the specified level (and at more severe levels) are ingested. For more information about log levels, see `Setting levels for logging, metrics, and tracing <https://docs.snowflake.com/en/developer-guide/logging-tracing/telemetry-levels>`_. Valid values are (case-insensitive): ``TRACE`` | ``DEBUG`` | ``INFO`` | ``WARN`` | ``ERROR`` | ``FATAL`` | ``OFF``. For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#log_level CurrentAccount#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrency_level(self) -> typing.Optional[jsii.Number]:
        '''Specifies the concurrency level for SQL statements (that is, queries and DML) executed by a warehouse (`more details <https://docs.snowflake.com/en/sql-reference/parameters#max-concurrency-level>`_). For more information, check `MAX_CONCURRENCY_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#max-concurrency-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#max_concurrency_level CurrentAccount#max_concurrency_level}
        '''
        result = self._values.get("max_concurrency_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_data_extension_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of days Snowflake can extend the data retention period for tables to prevent streams on the tables from becoming stale.

        By default, if the `DATA_RETENTION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters#data-retention-time-in-days>`_ setting for a source table is less than 14 days, and a stream has not been consumed, Snowflake temporarily extends this period to the stream’s offset, up to a maximum of 14 days, regardless of the `Snowflake Edition <https://docs.snowflake.com/en/user-guide/intro-editions>`_ for your account. The MAX_DATA_EXTENSION_TIME_IN_DAYS parameter enables you to limit this automatic extension period to control storage costs for data retention or for compliance reasons. For more information, check `MAX_DATA_EXTENSION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#max-data-extension-time-in-days>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#max_data_extension_time_in_days CurrentAccount#max_data_extension_time_in_days}
        '''
        result = self._values.get("max_data_extension_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_level(self) -> typing.Optional[builtins.str]:
        '''Controls how metrics data is ingested into the event table.

        For more information about metric levels, see `Setting levels for logging, metrics, and tracing <https://docs.snowflake.com/en/developer-guide/logging-tracing/telemetry-levels>`_. Valid values are (case-insensitive): ``ALL`` | ``NONE``. For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#metric_level CurrentAccount#metric_level}
        '''
        result = self._values.get("metric_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_data_retention_time_in_days(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of days for which Snowflake retains historical data for performing Time Travel actions (SELECT, CLONE, UNDROP) on an object.

        If a minimum number of days for data retention is set on an account, the data retention period for an object is determined by MAX(`DATA_RETENTION_TIME_IN_DAYS <https://docs.snowflake.com/en/sql-reference/parameters#label-data-retention-time-in-days>`_, MIN_DATA_RETENTION_TIME_IN_DAYS). For more information, check `MIN_DATA_RETENTION_TIME_IN_DAYS docs <https://docs.snowflake.com/en/sql-reference/parameters#min-data-retention-time-in-days>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#min_data_retention_time_in_days CurrentAccount#min_data_retention_time_in_days}
        '''
        result = self._values.get("min_data_retention_time_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def multi_statement_count(self) -> typing.Optional[jsii.Number]:
        '''Number of statements to execute when using the multi-statement capability. For more information, check `MULTI_STATEMENT_COUNT docs <https://docs.snowflake.com/en/sql-reference/parameters#multi-statement-count>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#multi_statement_count CurrentAccount#multi_statement_count}
        '''
        result = self._values.get("multi_statement_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the network policy to enforce for your account.

        Network policies enable restricting access to your account based on users’ IP address. For more details, see `Controlling network traffic with network policies <https://docs.snowflake.com/en/user-guide/network-policies>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. For more information, check `NETWORK_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#network-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#network_policy CurrentAccount#network_policy}
        '''
        result = self._values.get("network_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def noorder_sequence_as_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the ORDER or NOORDER property is set by default when you create a new sequence or add a new table column.

        The ORDER and NOORDER properties determine whether or not the values are generated for the sequence or auto-incremented column in `increasing or decreasing order <https://docs.snowflake.com/en/user-guide/querying-sequences.html#label-querying-sequences-increasing-values>`_. For more information, check `NOORDER_SEQUENCE_AS_DEFAULT docs <https://docs.snowflake.com/en/sql-reference/parameters#noorder-sequence-as-default>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#noorder_sequence_as_default CurrentAccount#noorder_sequence_as_default}
        '''
        result = self._values.get("noorder_sequence_as_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def oauth_add_privileged_roles_to_blocked_list(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles can be used as the primary role when creating a Snowflake session based on the access token from Snowflake’s authorization server.

        For more information, check `OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST docs <https://docs.snowflake.com/en/sql-reference/parameters#oauth-add-privileged-roles-to-blocked-list>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#oauth_add_privileged_roles_to_blocked_list CurrentAccount#oauth_add_privileged_roles_to_blocked_list}
        '''
        result = self._values.get("oauth_add_privileged_roles_to_blocked_list")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def odbc_treat_decimal_as_int(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies how ODBC processes columns that have a scale of zero (0). For more information, check `ODBC_TREAT_DECIMAL_AS_INT docs <https://docs.snowflake.com/en/sql-reference/parameters#odbc-treat-decimal-as-int>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#odbc_treat_decimal_as_int CurrentAccount#odbc_treat_decimal_as_int}
        '''
        result = self._values.get("odbc_treat_decimal_as_int")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def packages_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies `packages policy <https://docs.snowflake.com/en/developer-guide/udf/python/packages-policy>`_ for the current account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#packages_policy CurrentAccount#packages_policy}
        '''
        result = self._values.get("packages_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies `password policy <https://docs.snowflake.com/en/user-guide/password-authentication#label-using-password-policies>`_ for the current account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#password_policy CurrentAccount#password_policy}
        '''
        result = self._values.get("password_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def periodic_data_rekeying(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''It enables/disables re-encryption of table data with new keys on a yearly basis to provide additional levels of data protection (`more details <https://docs.snowflake.com/en/sql-reference/parameters#periodic-data-rekeying>`_). For more information, check `PERIODIC_DATA_REKEYING docs <https://docs.snowflake.com/en/sql-reference/parameters#periodic-data-rekeying>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#periodic_data_rekeying CurrentAccount#periodic_data_rekeying}
        '''
        result = self._values.get("periodic_data_rekeying")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pipe_execution_paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to pause a running pipe, primarily in preparation for transferring ownership of the pipe to a different role (`more details <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_). For more information, check `PIPE_EXECUTION_PAUSED docs <https://docs.snowflake.com/en/sql-reference/parameters#pipe-execution-paused>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#pipe_execution_paused CurrentAccount#pipe_execution_paused}
        '''
        result = self._values.get("pipe_execution_paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_unload_to_inline_url(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to prevent ad hoc data unload operations to external cloud storage locations (that is, `COPY INTO location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements that specify the cloud storage URL and access settings directly in the statement). For an example, see `Unloading data from a table directly to files in an external location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html#label-copy-into-location-ad-hoc>`_. For more information, check `PREVENT_UNLOAD_TO_INLINE_URL docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-inline-url>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#prevent_unload_to_inline_url CurrentAccount#prevent_unload_to_inline_url}
        '''
        result = self._values.get("prevent_unload_to_inline_url")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_unload_to_internal_stages(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to prevent data unload operations to internal (Snowflake) stages using `COPY INTO location <https://docs.snowflake.com/en/sql-reference/sql/copy-into-location>`_ statements. For more information, check `PREVENT_UNLOAD_TO_INTERNAL_STAGES docs <https://docs.snowflake.com/en/sql-reference/parameters#prevent-unload-to-internal-stages>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#prevent_unload_to_internal_stages CurrentAccount#prevent_unload_to_internal_stages}
        '''
        result = self._values.get("prevent_unload_to_internal_stages")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def python_profiler_modules(self) -> typing.Optional[builtins.str]:
        '''Specifies the list of Python modules to include in a report when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. For more information, check `PYTHON_PROFILER_MODULES docs <https://docs.snowflake.com/en/sql-reference/parameters#python-profiler-modules>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#python_profiler_modules CurrentAccount#python_profiler_modules}
        '''
        result = self._values.get("python_profiler_modules")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_profiler_target_stage(self) -> typing.Optional[builtins.str]:
        '''Specifies the fully-qualified name of the stage in which to save a report when `profiling Python handler code <https://docs.snowflake.com/en/developer-guide/stored-procedure/python/procedure-python-profiler>`_. For more information, check `PYTHON_PROFILER_TARGET_STAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#python-profiler-target-stage>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#python_profiler_target_stage CurrentAccount#python_profiler_target_stage}
        '''
        result = self._values.get("python_profiler_target_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_tag(self) -> typing.Optional[builtins.str]:
        '''Optional string that can be used to tag queries and other SQL statements executed within a session.

        The tags are displayed in the output of the `QUERY_HISTORY, QUERY_HISTORY_BY_* <https://docs.snowflake.com/en/sql-reference/functions/query_history>`_ functions. For more information, check `QUERY_TAG docs <https://docs.snowflake.com/en/sql-reference/parameters#query-tag>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#query_tag CurrentAccount#query_tag}
        '''
        result = self._values.get("query_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quoted_identifiers_ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether letters in double-quoted object identifiers are stored and resolved as uppercase letters.

        By default, Snowflake preserves the case of alphabetic characters when storing and resolving double-quoted identifiers (see `Identifier resolution <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing>`_). You can use this parameter in situations in which `third-party applications always use double quotes around identifiers <https://docs.snowflake.com/en/sql-reference/identifiers-syntax.html#label-identifier-casing-parameter>`_. For more information, check `QUOTED_IDENTIFIERS_IGNORE_CASE docs <https://docs.snowflake.com/en/sql-reference/parameters#quoted-identifiers-ignore-case>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#quoted_identifiers_ignore_case CurrentAccount#quoted_identifiers_ignore_case}
        '''
        result = self._values.get("quoted_identifiers_ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replace_invalid_characters(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for `Apache Iceberg™ tables <https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table>`_ that use an external catalog. For more information, check `REPLACE_INVALID_CHARACTERS docs <https://docs.snowflake.com/en/sql-reference/parameters#replace-invalid-characters>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#replace_invalid_characters CurrentAccount#replace_invalid_characters}
        '''
        result = self._values.get("replace_invalid_characters")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_storage_integration_for_stage_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to require a storage integration object as cloud credentials when creating a named external stage (using `CREATE STAGE <https://docs.snowflake.com/en/sql-reference/sql/create-stage>`_) to access a private cloud storage location. For more information, check `REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION docs <https://docs.snowflake.com/en/sql-reference/parameters#require-storage-integration-for-stage-creation>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#require_storage_integration_for_stage_creation CurrentAccount#require_storage_integration_for_stage_creation}
        '''
        result = self._values.get("require_storage_integration_for_stage_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_storage_integration_for_stage_operation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to require using a named external stage that references a storage integration object as cloud credentials when loading data from or unloading data to a private cloud storage location.

        For more information, check `REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION docs <https://docs.snowflake.com/en/sql-reference/parameters#require-storage-integration-for-stage-operation>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#require_storage_integration_for_stage_operation CurrentAccount#require_storage_integration_for_stage_operation}
        '''
        result = self._values.get("require_storage_integration_for_stage_operation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def resource_monitor(self) -> typing.Optional[builtins.str]:
        '''Parameter that specifies the name of the resource monitor used to control all virtual warehouses created in the account.

        External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#resource_monitor CurrentAccount#resource_monitor}
        '''
        result = self._values.get("resource_monitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rows_per_resultset(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of rows returned in a result set.

        A value of 0 specifies no maximum. For more information, check `ROWS_PER_RESULTSET docs <https://docs.snowflake.com/en/sql-reference/parameters#rows-per-resultset>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#rows_per_resultset CurrentAccount#rows_per_resultset}
        '''
        result = self._values.get("rows_per_resultset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3_stage_vpce_dns_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the DNS name of an Amazon S3 interface endpoint.

        Requests sent to the internal stage of an account via `AWS PrivateLink for Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html>`_ use this endpoint to connect. For more information, see `Accessing Internal stages with dedicated interface endpoints <https://docs.snowflake.com/en/user-guide/private-internal-stages-aws.html#label-aws-privatelink-internal-stage-network-isolation>`_. For more information, check `S3_STAGE_VPCE_DNS_NAME docs <https://docs.snowflake.com/en/sql-reference/parameters#s3-stage-vpce-dns-name>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#s3_stage_vpce_dns_name CurrentAccount#s3_stage_vpce_dns_name}
        '''
        result = self._values.get("s3_stage_vpce_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_identity_provider(self) -> typing.Optional[builtins.str]:
        '''Enables federated authentication. This deprecated parameter enables federated authentication (`more details <https://docs.snowflake.com/en/sql-reference/parameters#saml-identity-provider>`_). For more information, check `SAML_IDENTITY_PROVIDER docs <https://docs.snowflake.com/en/sql-reference/parameters#saml-identity-provider>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#saml_identity_provider CurrentAccount#saml_identity_provider}
        '''
        result = self._values.get("saml_identity_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_path(self) -> typing.Optional[builtins.str]:
        '''Specifies the path to search to resolve unqualified object names in queries.

        For more information, see `Name resolution in queries <https://docs.snowflake.com/en/sql-reference/name-resolution.html#label-object-name-resolution-search-path>`_. Comma-separated list of identifiers. An identifier can be a fully or partially qualified schema name. For more information, check `SEARCH_PATH docs <https://docs.snowflake.com/en/sql-reference/parameters#search-path>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#search_path CurrentAccount#search_path}
        '''
        result = self._values.get("search_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serverless_task_max_statement_size(self) -> typing.Optional[builtins.str]:
        '''Specifies the maximum allowed warehouse size for `Serverless tasks <https://docs.snowflake.com/en/user-guide/tasks-intro.html#label-tasks-compute-resources-serverless>`_. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `SERVERLESS_TASK_MAX_STATEMENT_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#serverless-task-max-statement-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#serverless_task_max_statement_size CurrentAccount#serverless_task_max_statement_size}
        '''
        result = self._values.get("serverless_task_max_statement_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serverless_task_min_statement_size(self) -> typing.Optional[builtins.str]:
        '''Specifies the minimum allowed warehouse size for `Serverless tasks <https://docs.snowflake.com/en/user-guide/tasks-intro.html#label-tasks-compute-resources-serverless>`_. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `SERVERLESS_TASK_MIN_STATEMENT_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#serverless-task-min-statement-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#serverless_task_min_statement_size CurrentAccount#serverless_task_min_statement_size}
        '''
        result = self._values.get("serverless_task_min_statement_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies `session policy <https://docs.snowflake.com/en/user-guide/session-policies-using>`_ for the current account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#session_policy CurrentAccount#session_policy}
        '''
        result = self._values.get("session_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def simulated_data_sharing_consumer(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of a consumer account to simulate for testing/validating shared data, particularly shared secure views.

        When this parameter is set in a session, shared views return rows as if executed in the specified consumer account rather than the provider account. For more information, check `SIMULATED_DATA_SHARING_CONSUMER docs <https://docs.snowflake.com/en/sql-reference/parameters#simulated-data-sharing-consumer>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#simulated_data_sharing_consumer CurrentAccount#simulated_data_sharing_consumer}
        '''
        result = self._values.get("simulated_data_sharing_consumer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sso_login_page(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This deprecated parameter disables preview mode for testing SSO (after enabling federated authentication) before rolling it out to users.

        For more information, check `SSO_LOGIN_PAGE docs <https://docs.snowflake.com/en/sql-reference/parameters#sso-login-page>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#sso_login_page CurrentAccount#sso_login_page}
        '''
        result = self._values.get("sso_login_page")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def statement_queued_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, a SQL statement (query, DDL, DML, etc.) remains queued for a warehouse before it is canceled by the system. This parameter can be used in conjunction with the `MAX_CONCURRENCY_LEVEL <https://docs.snowflake.com/en/sql-reference/parameters#label-max-concurrency-level>`_ parameter to ensure a warehouse is never backlogged. For more information, check `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-queued-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#statement_queued_timeout_in_seconds CurrentAccount#statement_queued_timeout_in_seconds}
        '''
        result = self._values.get("statement_queued_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def statement_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time, in seconds, after which a running SQL statement (query, DDL, DML, etc.) is canceled by the system. For more information, check `STATEMENT_TIMEOUT_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#statement_timeout_in_seconds CurrentAccount#statement_timeout_in_seconds}
        '''
        result = self._values.get("statement_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_serialization_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies the storage serialization policy for Snowflake-managed `Apache Iceberg™ tables <https://docs.snowflake.com/en/user-guide/tables-iceberg>`_. Valid values are (case-insensitive): ``COMPATIBLE`` | ``OPTIMIZED``. For more information, check `STORAGE_SERIALIZATION_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#storage-serialization-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#storage_serialization_policy CurrentAccount#storage_serialization_policy}
        '''
        result = self._values.get("storage_serialization_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strict_json_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This parameter specifies whether JSON output in a session is compatible with the general standard (as described by `http://json.org <http://json.org>`_). By design, Snowflake allows JSON input that contains non-standard values; however, these non-standard values might result in Snowflake outputting JSON that is incompatible with other platforms and languages. This parameter, when enabled, ensures that Snowflake outputs valid/compatible JSON. For more information, check `STRICT_JSON_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#strict-json-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#strict_json_output CurrentAccount#strict_json_output}
        '''
        result = self._values.get("strict_json_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suspend_task_after_num_failures(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of consecutive failed task runs after which the current task is suspended automatically.

        The default is 0 (no automatic suspension). For more information, check `SUSPEND_TASK_AFTER_NUM_FAILURES docs <https://docs.snowflake.com/en/sql-reference/parameters#suspend-task-after-num-failures>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#suspend_task_after_num_failures CurrentAccount#suspend_task_after_num_failures}
        '''
        result = self._values.get("suspend_task_after_num_failures")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_auto_retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of automatic task graph retry attempts.

        If any task graphs complete in a FAILED state, Snowflake can automatically retry the task graphs from the last task in the graph that failed. For more information, check `TASK_AUTO_RETRY_ATTEMPTS docs <https://docs.snowflake.com/en/sql-reference/parameters#task-auto-retry-attempts>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#task_auto_retry_attempts CurrentAccount#task_auto_retry_attempts}
        '''
        result = self._values.get("task_auto_retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported time format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of times stored in the system during the session). For more information, check `TIME_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#time_input_format CurrentAccount#time_input_format}
        '''
        result = self._values.get("time_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIME data type.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIME_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#time-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#time_output_format CurrentAccount#time_output_format}
        '''
        result = self._values.get("time_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CurrentAccountTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timeouts CurrentAccount#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CurrentAccountTimeouts"], result)

    @builtins.property
    def timestamp_day_is_always24_h(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the `DATEADD <https://docs.snowflake.com/en/sql-reference/functions/dateadd>`_ function (and its aliases) always consider a day to be exactly 24 hours for expressions that span multiple days. For more information, check `TIMESTAMP_DAY_IS_ALWAYS_24H docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-day-is-always-24h>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_day_is_always_24h CurrentAccount#timestamp_day_is_always_24h}
        '''
        result = self._values.get("timestamp_day_is_always24_h")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timestamp_input_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the input format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. Any valid, supported timestamp format or AUTO (AUTO specifies that Snowflake attempts to automatically detect the format of timestamps stored in the system during the session). For more information, check `TIMESTAMP_INPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-input-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_input_format CurrentAccount#timestamp_input_format}
        '''
        result = self._values.get("timestamp_input_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ltz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_LTZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_LTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ltz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_ltz_output_format CurrentAccount#timestamp_ltz_output_format}
        '''
        result = self._values.get("timestamp_ltz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_ntz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_NTZ data type. For more information, check `TIMESTAMP_NTZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-ntz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_ntz_output_format CurrentAccount#timestamp_ntz_output_format}
        '''
        result = self._values.get("timestamp_ntz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP data type alias.

        For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_output_format CurrentAccount#timestamp_output_format}
        '''
        result = self._values.get("timestamp_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_type_mapping(self) -> typing.Optional[builtins.str]:
        '''Specifies the TIMESTAMP_* variation that the TIMESTAMP data type alias maps to.

        Valid values are (case-insensitive): ``TIMESTAMP_LTZ`` | ``TIMESTAMP_NTZ`` | ``TIMESTAMP_TZ``. For more information, check `TIMESTAMP_TYPE_MAPPING docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-type-mapping>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_type_mapping CurrentAccount#timestamp_type_mapping}
        '''
        result = self._values.get("timestamp_type_mapping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp_tz_output_format(self) -> typing.Optional[builtins.str]:
        '''Specifies the display format for the TIMESTAMP_TZ data type.

        If no format is specified, defaults to `TIMESTAMP_OUTPUT_FORMAT <https://docs.snowflake.com/en/sql-reference/parameters#label-timestamp-output-format>`_. For more information, see `Date and time input and output formats <https://docs.snowflake.com/en/sql-reference/date-time-input-output>`_. For more information, check `TIMESTAMP_TZ_OUTPUT_FORMAT docs <https://docs.snowflake.com/en/sql-reference/parameters#timestamp-tz-output-format>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timestamp_tz_output_format CurrentAccount#timestamp_tz_output_format}
        '''
        result = self._values.get("timestamp_tz_output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone for the session.

        You can specify a `time zone name <https://data.iana.org/time-zones/tzdb-2021a/zone1970.tab>`_ or a `link name <https://data.iana.org/time-zones/tzdb-2021a/backward>`_ from release 2021a of the `IANA Time Zone Database <https://www.iana.org/time-zones>`_ (e.g. America/Los_Angeles, Europe/London, UTC, Etc/GMT, etc.). For more information, check `TIMEZONE docs <https://docs.snowflake.com/en/sql-reference/parameters#timezone>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#timezone CurrentAccount#timezone}
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Controls how trace events are ingested into the event table.

        For more information about trace levels, see `Setting trace level <https://docs.snowflake.com/en/developer-guide/logging-tracing/tracing-trace-level>`_. Valid values are (case-insensitive): ``ALWAYS`` | ``ON_EVENT`` | ``PROPAGATE`` | ``OFF``. For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#trace_level CurrentAccount#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transaction_abort_on_error(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies the action to perform when a statement issued within a non-autocommit transaction returns with an error.

        For more information, check `TRANSACTION_ABORT_ON_ERROR docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-abort-on-error>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#transaction_abort_on_error CurrentAccount#transaction_abort_on_error}
        '''
        result = self._values.get("transaction_abort_on_error")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transaction_default_isolation_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the isolation level for transactions in the user session.

        Valid values are (case-insensitive): ``READ COMMITTED``. For more information, check `TRANSACTION_DEFAULT_ISOLATION_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#transaction-default-isolation-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#transaction_default_isolation_level CurrentAccount#transaction_default_isolation_level}
        '''
        result = self._values.get("transaction_default_isolation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def two_digit_century_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the “century start” year for 2-digit years (i.e. the earliest year such dates can represent). This parameter prevents ambiguous dates when importing or converting data with the ``YY`` date format component (i.e. years represented as 2 digits). For more information, check `TWO_DIGIT_CENTURY_START docs <https://docs.snowflake.com/en/sql-reference/parameters#two-digit-century-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#two_digit_century_start CurrentAccount#two_digit_century_start}
        '''
        result = self._values.get("two_digit_century_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unsupported_ddl_action(self) -> typing.Optional[builtins.str]:
        '''Determines if an unsupported (i.e. non-default) value specified for a constraint property returns an error. For more information, check `UNSUPPORTED_DDL_ACTION docs <https://docs.snowflake.com/en/sql-reference/parameters#unsupported-ddl-action>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#unsupported_ddl_action CurrentAccount#unsupported_ddl_action}
        '''
        result = self._values.get("unsupported_ddl_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_cached_result(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to reuse persisted query results, if available, when a matching query is submitted.

        For more information, check `USE_CACHED_RESULT docs <https://docs.snowflake.com/en/sql-reference/parameters#use-cached-result>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#use_cached_result CurrentAccount#use_cached_result}
        '''
        result = self._values.get("use_cached_result")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def user_task_managed_initial_warehouse_size(self) -> typing.Optional[builtins.str]:
        '''Specifies the size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size.

        Once a task has successfully completed a few runs, Snowflake ignores this parameter setting. Valid values are (case-insensitive): ``XSMALL`` | ``X-SMALL`` | ``SMALL`` | ``MEDIUM`` | ``LARGE`` | ``XLARGE`` | ``X-LARGE`` | ``XXLARGE`` | ``X2LARGE`` | ``2X-LARGE`` | ``XXXLARGE`` | ``X3LARGE`` | ``3X-LARGE`` | ``X4LARGE`` | ``4X-LARGE`` | ``X5LARGE`` | ``5X-LARGE`` | ``X6LARGE`` | ``6X-LARGE``. For more information, check `USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-managed-initial-warehouse-size>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_managed_initial_warehouse_size CurrentAccount#user_task_managed_initial_warehouse_size}
        '''
        result = self._values.get("user_task_managed_initial_warehouse_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_task_minimum_trigger_interval_in_seconds(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''Minimum amount of time between Triggered Task executions in seconds For more information, check `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-minimum-trigger-interval-in-seconds>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_minimum_trigger_interval_in_seconds CurrentAccount#user_task_minimum_trigger_interval_in_seconds}
        '''
        result = self._values.get("user_task_minimum_trigger_interval_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def user_task_timeout_ms(self) -> typing.Optional[jsii.Number]:
        '''Specifies the time limit on a single run of the task before it times out (in milliseconds).

        For more information, check `USER_TASK_TIMEOUT_MS docs <https://docs.snowflake.com/en/sql-reference/parameters#user-task-timeout-ms>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#user_task_timeout_ms CurrentAccount#user_task_timeout_ms}
        '''
        result = self._values.get("user_task_timeout_ms")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_of_year_policy(self) -> typing.Optional[jsii.Number]:
        '''Specifies how the weeks in a given year are computed.

        ``0``: The semantics used are equivalent to the ISO semantics, in which a week belongs to a given year if at least 4 days of that week are in that year. ``1``: January 1 is included in the first week of the year and December 31 is included in the last week of the year. For more information, check `WEEK_OF_YEAR_POLICY docs <https://docs.snowflake.com/en/sql-reference/parameters#week-of-year-policy>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#week_of_year_policy CurrentAccount#week_of_year_policy}
        '''
        result = self._values.get("week_of_year_policy")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def week_start(self) -> typing.Optional[jsii.Number]:
        '''Specifies the first day of the week (used by week-related date functions).

        ``0``: Legacy Snowflake behavior is used (i.e. ISO-like semantics). ``1`` (Monday) to ``7`` (Sunday): All the week-related functions use weeks that start on the specified day of the week. For more information, check `WEEK_START docs <https://docs.snowflake.com/en/sql-reference/parameters#week-start>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#week_start CurrentAccount#week_start}
        '''
        result = self._values.get("week_start")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CurrentAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.currentAccount.CurrentAccountTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class CurrentAccountTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#create CurrentAccount#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#delete CurrentAccount#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#read CurrentAccount#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#update CurrentAccount#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447ebb75c5d2f45ca020d7fd6c7296d7919c51632008345c2ae7bf5558a46133)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#create CurrentAccount#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#delete CurrentAccount#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#read CurrentAccount#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/current_account#update CurrentAccount#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CurrentAccountTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CurrentAccountTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.currentAccount.CurrentAccountTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f1ab3f3d6ff9cc5e9476a6a39a0acf6d6c4703259e8ef2ead23a73015c2bade)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60528470a50b5a1dcf993d209d5443121f465a15a2496238afd9ca4b5fb049e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6b407a86f77579f53e5f177da952b8a34feaf3596796030196201a187360a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a75187fd38f80a99ace3b446eea22863c05d0e6ba1b20897dc842912b024c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e78614b99b865408e1a04efa0c8aa38fa7617a24994b3879c3e66407eb78226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CurrentAccountTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CurrentAccountTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CurrentAccountTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62ffa171b0c6da1d46d4f80cfe5d31288ddfcfcffbc3e04dbf7703ca3a06193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CurrentAccount",
    "CurrentAccountConfig",
    "CurrentAccountTimeouts",
    "CurrentAccountTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f7f566e7fa58e1c5c8bb6ae78cffb5d10b4382c9e69d7b4f44ed253bb80bd6e3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    active_python_profiler: typing.Optional[builtins.str] = None,
    allow_client_mfa_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    authentication_policy: typing.Optional[builtins.str] = None,
    autocommit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    base_location_prefix: typing.Optional[builtins.str] = None,
    binary_input_format: typing.Optional[builtins.str] = None,
    binary_output_format: typing.Optional[builtins.str] = None,
    catalog: typing.Optional[builtins.str] = None,
    catalog_sync: typing.Optional[builtins.str] = None,
    client_enable_log_info_statement_parameters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_encryption_key_size: typing.Optional[jsii.Number] = None,
    client_memory_limit: typing.Optional[jsii.Number] = None,
    client_metadata_request_use_connection_ctx: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_metadata_use_session_database: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_prefetch_threads: typing.Optional[jsii.Number] = None,
    client_result_chunk_size: typing.Optional[jsii.Number] = None,
    client_result_column_case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_session_keep_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_session_keep_alive_heartbeat_frequency: typing.Optional[jsii.Number] = None,
    client_timestamp_type_mapping: typing.Optional[builtins.str] = None,
    cortex_enabled_cross_region: typing.Optional[builtins.str] = None,
    cortex_models_allowlist: typing.Optional[builtins.str] = None,
    csv_timestamp_format: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    date_input_format: typing.Optional[builtins.str] = None,
    date_output_format: typing.Optional[builtins.str] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    default_notebook_compute_pool_cpu: typing.Optional[builtins.str] = None,
    default_notebook_compute_pool_gpu: typing.Optional[builtins.str] = None,
    default_null_ordering: typing.Optional[builtins.str] = None,
    default_streamlit_notebook_warehouse: typing.Optional[builtins.str] = None,
    disable_ui_download_button: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_user_privilege_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_automatic_sensitive_data_classification_log: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_egress_cost_optimizer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_identifier_first_login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_internal_stages_privatelink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_tri_secret_and_rekey_opt_out_for_image_repository: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unhandled_exceptions_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unredacted_secure_object_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce_network_rules_for_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_table: typing.Optional[builtins.str] = None,
    external_oauth_add_privileged_roles_to_blocked_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_volume: typing.Optional[builtins.str] = None,
    feature_policy: typing.Optional[builtins.str] = None,
    geography_output_format: typing.Optional[builtins.str] = None,
    geometry_output_format: typing.Optional[builtins.str] = None,
    hybrid_table_lock_timeout: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    initial_replication_size_limit_in_tb: typing.Optional[builtins.str] = None,
    jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_indent: typing.Optional[jsii.Number] = None,
    js_treat_integer_as_bigint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    listing_auto_fulfillment_replication_refresh_schedule: typing.Optional[builtins.str] = None,
    lock_timeout: typing.Optional[jsii.Number] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_concurrency_level: typing.Optional[jsii.Number] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    metric_level: typing.Optional[builtins.str] = None,
    min_data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    multi_statement_count: typing.Optional[jsii.Number] = None,
    network_policy: typing.Optional[builtins.str] = None,
    noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    oauth_add_privileged_roles_to_blocked_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    packages_policy: typing.Optional[builtins.str] = None,
    password_policy: typing.Optional[builtins.str] = None,
    periodic_data_rekeying: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pipe_execution_paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_unload_to_inline_url: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_unload_to_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    python_profiler_modules: typing.Optional[builtins.str] = None,
    python_profiler_target_stage: typing.Optional[builtins.str] = None,
    query_tag: typing.Optional[builtins.str] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_storage_integration_for_stage_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_storage_integration_for_stage_operation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_monitor: typing.Optional[builtins.str] = None,
    rows_per_resultset: typing.Optional[jsii.Number] = None,
    s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
    saml_identity_provider: typing.Optional[builtins.str] = None,
    search_path: typing.Optional[builtins.str] = None,
    serverless_task_max_statement_size: typing.Optional[builtins.str] = None,
    serverless_task_min_statement_size: typing.Optional[builtins.str] = None,
    session_policy: typing.Optional[builtins.str] = None,
    simulated_data_sharing_consumer: typing.Optional[builtins.str] = None,
    sso_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    storage_serialization_policy: typing.Optional[builtins.str] = None,
    strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
    task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
    time_input_format: typing.Optional[builtins.str] = None,
    time_output_format: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CurrentAccountTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8092f7b9c0214c6775bed7e05149e54603a0f64373a4674bb195b682c8145688(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2047342a26c301f150f888a22eb603d208c3bd63d8eb419d65c34f9f77f317(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba4c882ad6ae4d6c0e54fd76d884bdc8d31014238877552279fd269eeed39f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809cc4f9bc24b69f76716f3780159970245c4d74cf1490318c28d26ea0171906(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9df216d73b1647111e5fa878d3f7b0b3cb7d85c8a2eafdbf1c47e36aa5832e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eef508ddb3e2a728023cc8f890355294f74e24c9a17415c5664cc82813e122d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad0ad993cb38e5e548652a49207f68c295402b8e168f7491c609bce370bfddf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6393dd99353ec11fe21d60b1921d013fdfa1a71663de9b04d75d0e01295a2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d99850086dc114c04076f20fbd361a142d90b8e6089153652870ae3b155e788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa15d6cc073fc8e78263b1b9a708581ecbc68367bdad82f49a54a58904e7d579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cf7833a9cd2e1464db8c787e310cd1f88e3e38305695c5c8739a6b68eb7dfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc31abee3aeec07123a902ec39d9ad275c3a6c7750a1a437ef61295d04e951c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c70e6bdfac085993bc7970bea872c98db17c08601715f09b8547800c921846(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65107c569f5e8d5d853ee6a6bb92d0c3326cdd7f78aa0cd192307d3cd1ea3c65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac09a778a468581f2a11792a682337c75f6f3c90cde67ac814e696f672e2556(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c96809f48fcab87a3e210547221c47210389596cac96a67b330ad52e6ff537(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089c82fb1a132a3ce09cb1d5403db36669a029fce187e4ae44616ae835c2c575(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ccc61dcc80df55e84bd2d8cdbd3e3464e2b4ff3006a6679c7a24e40cf839bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6a5b9011604b225277c578f5c4e9b1e6043ddecd59468b915ada99bec41d0a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5500191a2f8492d871b1b73dc2e13f085dedbd561ec5f9f3be632d2b37d1f65(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3f7df5de185fc2c6571ac2555eec8598fe0f40bdb55ad0ed663d62445362e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2527c33b3147efd602219ce8249a448304cadefd800f84b4d332320bd6bf4a0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e86f908490016487c56a70dc6aaf0b1d912157c1190f3cea276a2be874a07e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25643de2c010d8eb1c20dccdeb86199ca7639b43322b8e451dec38275e334fb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e8b2adf229f9aa07b8c2439f15283797421a79c7045e53e0b97eb6d3921c91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7021fad4fe2c550e01d3272011046a700f6a208d772592c6d5844151549e128e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88540fe652d1aaea92a9edcfe9bb4baa6dbc6fbc045e886d8bcea0c0cf18f07d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef9adcfd62e0abcbb1bc43bb9c6286b3bf6e617c957ab3b4535658899101e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97565bbf19dd395e14278235645fa84e28812d0cceafaf98ddb00daefaa3a1c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ca359cfb0313c53b2f5a0d410e3ee0ece8afecbf6bc12c0d38da5365fe2d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1244bb183454057017fda99f9df330aacf20210c4cbb6fff90f439a8fc502ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a609f6c911a165949008370de3ced40d9446ab4ec8e58ce90d74cc1c24ab8d97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca19aadca7808e6c79b197cc95d4d3ace19f526004baa8b77acf03484b312d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d465fb726b539c22b047212d19b87b8c585b30bd93a91a4ac74336631d8844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c86c8822d0a5b43e291ef84a3bdbb4835f593cc0fc8f49feed0786ba333d34(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90484c9faea6debc29c6e919faaf5928b69e77cb11a9a77be30108cf9d7733d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953f099809403b6d05b194269ed8aa2fa91ec9907a9161fe14e1ddf59a1f9d56(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427967fba0933221c546a6c26e3a0796630df913949b952c28f4220d67ec6437(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814acad29b366dd1e17082e0e8f897e574b9e50b40424daca2a04b09d559b298(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293370260f12206a92011d498e1e6139afbbd5afe9f64781e7da850819a5ef58(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af248520e7a6fc02a2af14ab43105932580c57a9880cc454095b93a6c0ca4d97(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98790e56a9d2be95843d63e178943ea22c556f3b6b7786d2ba41490408b77c6b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1f8bf45a613b39467daf31b6d861d24850f04b82137881e5c64320aa37fcd4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d11a5ae3d39d05c57129c4421c1725a52aaf991acb82c56442b410d97e485ab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3aab39f5bdda9d0837673babed3a4ae0817688caa3c55b3301808921135045(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b181fdb1e72a623f95ca5a512a5877a19f1b1aeffe722809883470ab95f42e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a611a612a0b034275d961831b1a772393f7eb9af05d167c500b6b4b7c3da86a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740a2366cc5ca3d0ee388b50f0c667c23a08cb336bde5c90cf939dea62c3933b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f475575d21f9c5c540199c1275e200b2681032cda55184dfd781827e4a40a5a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a114ed5b6059f5a8b5f2f9d6cae0d2f98291613bb60cabac53ed1a703ff392f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6facb7f9e787436d00bbd20de95ef1d0d7042c8134c7000506f4e8c0948e670f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5629ef3e7c6b3bfbfbb09098800ae399d12ad0583e42de5e6e210df30909c345(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdaa01e9ada20536d88dd38de9432647b82f2b242e2a92853200cd7dc6032c81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0267c69ee565092154d6c47966b3172739ad12348cd689341873c6bf06bc306c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de228176e9a4e1f01631c98307d0df33646e11d1a291ea5836cc368430a4ee3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b19e8e107ab04584cc87e9fd6af754d4f994f4d4dbcec9910a9d1edfe0b607(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd771e9fa0f4d806cdb0e30e95355b2c71135728310fe1a2883bc4ec293a9178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed18a91a76853d5733faaa271478c73986b74892c002eb97642d068b10dd4e31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b5e3a824838c607eeff6176729ec8b39d19aadcd3e616f7390479945ac14ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3356453194f7657bc6be88f501c4ca8ce72249916012c347a270855d300bcfa5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1dc3bceaefedd72773724c5891a65f02d33601afd315b063bc376c8b3f41855(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b94c15ccd0c225e23149b48a942711d590f93bcc4ef5e86f5f189f3395f4a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bc214c9b3795213c478e7faa04f851608cb47ca70b038bdf3228d2f4b84a53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c49327d2c5a16b2fcf15bdd371a62d3eb4fb5dce2a1d54810279e017618c148(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a883fe9259a1f44a127aff1a2dd59b61a00a7f3b1257df16e36357caf992f614(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26062c6b10b8c0b769b73893a797b50dcdf2aa5b8af1b0bf523de88a59929615(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e9ab726258d4c2ea27cab555510d4a323f932ded4c9359b7db6095f74d0ac1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ed6b9cf62ce17f2cc3469ba861f4d8d4da5cdf4d48f7ad529f823f6befaf7c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bd888580f527a4416d153391097c0dc48fb19b5d5aa6fc1ea4d2435376d951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949ea780448ec6403c01b7c1a0c22fd81fd2623c4e37624f02b90f4d0cfeac6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc03a098bb663656d69de583d3a0047d83e321f00862ed55b4bff5c52f3f8a46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4c9dedb836473f5336b3850e25dbf122bba07d9a9b8957f712705b0fd4a9a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0c94cb5f139e4b6d20e53a7e8496bebd88975b3733874c6179a7510a7c0f5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35382c3ac5a3df76733472ddafcdf5205d420e18ee87d61b66b35ab1b5d9808f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f547f1c14ef82c60675e65995dbb00f20cc8907b9d1cb46ee7d7efa74914bf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b1796495fbcff84cb60240e12230a3d4d8e508d89dc2e94f2b15f4e9b80582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462c2e2e1b8f7cff68407f9c45c6c8798f3cdbd7a10c09672fdb3254a1088dac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052cdc2aac7e11f5eaa4fbca2f0b37d7b8c6f69767660069700c30277da0c0bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6ebfa9b0e605d6cb61b8cf0b60006654a51d68bde3ac47e788e1a23e6ca9f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e973e91e50a60009ff668b8f6a0a41427e8ae9c6ceaa75fab0cd83d1b3680ac3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca0d5bb142a3f8fef23acaa7e7e8df327029c060c2f6030d1f18ef3be9de365f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900a43ed635b85c00a9ee312a15b8e0b4f521955666eaa0f3aa9b9c1d8bc47a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8ce9c2e83e930374aa6234d2801cdce8002297e832a29da1129e881c1a0fe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9872a34ca6f14ab9219575ff77d3d97b28724237856f59e677ff8089d842febe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77d5917225c57e75b061c49007a02359d4c64591c383dceec5198b44c9223b7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf60506bbb105f40ccbf8f9b13125d8670a40b4c26b7e3f5257130bc49721ada(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83079e35b11e7e931b3f9c1687788d86133626ef84b541aaa62f280ba915e03c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e962dac0d86f28b6188ee8f40e335142b288ebe8136a5dd29f8e3e3b4e8b509(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8506aa69451a39a69fec2759bda49c6f9c670d723548ef0b968deb4a6c2a6362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0abe063aa5bdef91dc393768afa775541dbf8e1f4b70d5048ceea49abfed305(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060bdee7f0aecc9dba9675c975d6ad563d075f32cd2d8511929377ec68163907(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778b8732228f2f4396aae1fc9c0bcf25e314494bc6f0cebdf63a63a11492d6b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106bf81abdd7c21d99330ec722d9b77a02df3b8b5ce3d1a23cd424bb9a75c9ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5fb62a241a5254152b31a594cb662b37185d65571f2dae9fc39b73a1fd9eb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892ca3ae486d5bc8e72c5d6375429cdadd84c95eb7b73479a50cf4ac92700d93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092607976f1a149943e1da16e0052678ac1fc62a41a7899b80c0d00d6b613838(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aaadee6704f5d38efd0a0d63dbb1f06bac9e8af0dddfc8a0abe780d64c99dd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6151e5cb45fe56382744b393e30cc8e0f56b58cd704e4407befc978b8ddd5ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b257e21f06043cb9acd2d9731745f0117dd98999adf9141d4cd19ecb11c7d09(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9446e715566c10c86b28e136d0cd0022808b8e9f97800888a23140f08d1dba8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ed68c93da6cf73d962a5fde98837d7fa8c0f9a2fc61c71e41bfec3b75c820d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4f1fe4deb3803cd7436a28f2bc0573bfbbbc8d5a58a70fdf2160da93b1d459(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf011e3fa56ae23f584a2485871969c3af7835802fc339690ee05d50474df6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136fa345520af7040b0f006365a8ca1bdb02081de141515caad0953610e5d3ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bfe87797af8f1e867f295c9622ea81f46024992f83176266cd457c36fbaf26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff291df3ea4ce8dd455f6e41990d7e4d7420f36c86c29a99fbc7261e65bdf5df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee497298fa3dd542a629d6fa74aef162ed6ed3027859e2aeec054d7091f840e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4cb7357f75c5611fc67d89fecaff3c34a646d7bd6d6c2f8704bc1c2022301c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e819c9a6210eae033df8c71ab8cc45ca814124cb28ad3554ac1afc6256e5ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2070723d5135f6b9d18823e707b57a452fd950da868df5a8e992a80de6d06bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dc6a90c714d5f947876ccdcec9e5ac46b2f79777fb483a5a24793cf9c0a17f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2180a1bd0828eab82ef850481bbe62112db93e1babc02ed9441a0f3b34a199aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2056caf88f8bef0dd0b7976bc28e3e1f84c03b23fe151f8fcaa140c269cba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75183c46de8ed168c4177b3a3f4e8bad1e69dc3be3a177e4603534d13f4c4bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26d81116cbd83028d0dcbe613f94f27fc7c57105f5ebbc37a9cde763cbcf949(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7360f1a9047f428dd309831b1cbe6a86065b997196cd4ae7db3ef31d471f3c49(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e89dab914aa427f511d457bb58aa9228bbd5396efe06ced60255af0d38e3f77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc6e949a13ffb6764ffe85a72438f0e0856df1e4462c017289819cc0d5977b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06fd2f443b6df55ceb02862eba53bd95d93161ef1458903a88caf2be755b7cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1709f1aa9211a0f2931c324143a1fd545c18a63cfa1eeb5b960486c2668e30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2af3339643cef2ecaae334a5f2514d3ffba7f4d51ec53a9049d4752cf0fff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799045fe95d407effc22db8aff0dfaa85ac154f93099ff2f7afa76e1127c53f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ee7dea0ceb25bb3f278b7ab3675435b08d6fe702f41bd25a929456b7a855fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f7f99a630c5cd404967455190d8e3010fd39ba46424ec830e735e9fa355433(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fb4578ac1c61d8a3c465eb6ef1469c08ffa85a75fc30deb99fbab8fddeb3f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874092e4c779217cedf530a98d8b63a694bf8fad7ac9ff5d46fe8d69f55b1ca5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    abort_detached_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    active_python_profiler: typing.Optional[builtins.str] = None,
    allow_client_mfa_caching: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_id_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    authentication_policy: typing.Optional[builtins.str] = None,
    autocommit: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    base_location_prefix: typing.Optional[builtins.str] = None,
    binary_input_format: typing.Optional[builtins.str] = None,
    binary_output_format: typing.Optional[builtins.str] = None,
    catalog: typing.Optional[builtins.str] = None,
    catalog_sync: typing.Optional[builtins.str] = None,
    client_enable_log_info_statement_parameters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_encryption_key_size: typing.Optional[jsii.Number] = None,
    client_memory_limit: typing.Optional[jsii.Number] = None,
    client_metadata_request_use_connection_ctx: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_metadata_use_session_database: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_prefetch_threads: typing.Optional[jsii.Number] = None,
    client_result_chunk_size: typing.Optional[jsii.Number] = None,
    client_result_column_case_insensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_session_keep_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_session_keep_alive_heartbeat_frequency: typing.Optional[jsii.Number] = None,
    client_timestamp_type_mapping: typing.Optional[builtins.str] = None,
    cortex_enabled_cross_region: typing.Optional[builtins.str] = None,
    cortex_models_allowlist: typing.Optional[builtins.str] = None,
    csv_timestamp_format: typing.Optional[builtins.str] = None,
    data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    date_input_format: typing.Optional[builtins.str] = None,
    date_output_format: typing.Optional[builtins.str] = None,
    default_ddl_collation: typing.Optional[builtins.str] = None,
    default_notebook_compute_pool_cpu: typing.Optional[builtins.str] = None,
    default_notebook_compute_pool_gpu: typing.Optional[builtins.str] = None,
    default_null_ordering: typing.Optional[builtins.str] = None,
    default_streamlit_notebook_warehouse: typing.Optional[builtins.str] = None,
    disable_ui_download_button: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_user_privilege_grants: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_automatic_sensitive_data_classification_log: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_egress_cost_optimizer: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_identifier_first_login: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_internal_stages_privatelink: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_tri_secret_and_rekey_opt_out_for_image_repository: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_tri_secret_and_rekey_opt_out_for_spcs_block_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unhandled_exceptions_reporting: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unload_physical_type_optimization: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unredacted_query_syntax_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_unredacted_secure_object_error: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enforce_network_rules_for_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_merge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    error_on_nondeterministic_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_table: typing.Optional[builtins.str] = None,
    external_oauth_add_privileged_roles_to_blocked_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_volume: typing.Optional[builtins.str] = None,
    feature_policy: typing.Optional[builtins.str] = None,
    geography_output_format: typing.Optional[builtins.str] = None,
    geometry_output_format: typing.Optional[builtins.str] = None,
    hybrid_table_lock_timeout: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    initial_replication_size_limit_in_tb: typing.Optional[builtins.str] = None,
    jdbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_treat_timestamp_ntz_as_utc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jdbc_use_session_timezone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    json_indent: typing.Optional[jsii.Number] = None,
    js_treat_integer_as_bigint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    listing_auto_fulfillment_replication_refresh_schedule: typing.Optional[builtins.str] = None,
    lock_timeout: typing.Optional[jsii.Number] = None,
    log_level: typing.Optional[builtins.str] = None,
    max_concurrency_level: typing.Optional[jsii.Number] = None,
    max_data_extension_time_in_days: typing.Optional[jsii.Number] = None,
    metric_level: typing.Optional[builtins.str] = None,
    min_data_retention_time_in_days: typing.Optional[jsii.Number] = None,
    multi_statement_count: typing.Optional[jsii.Number] = None,
    network_policy: typing.Optional[builtins.str] = None,
    noorder_sequence_as_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    oauth_add_privileged_roles_to_blocked_list: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    odbc_treat_decimal_as_int: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    packages_policy: typing.Optional[builtins.str] = None,
    password_policy: typing.Optional[builtins.str] = None,
    periodic_data_rekeying: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pipe_execution_paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_unload_to_inline_url: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_unload_to_internal_stages: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    python_profiler_modules: typing.Optional[builtins.str] = None,
    python_profiler_target_stage: typing.Optional[builtins.str] = None,
    query_tag: typing.Optional[builtins.str] = None,
    quoted_identifiers_ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace_invalid_characters: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_storage_integration_for_stage_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_storage_integration_for_stage_operation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_monitor: typing.Optional[builtins.str] = None,
    rows_per_resultset: typing.Optional[jsii.Number] = None,
    s3_stage_vpce_dns_name: typing.Optional[builtins.str] = None,
    saml_identity_provider: typing.Optional[builtins.str] = None,
    search_path: typing.Optional[builtins.str] = None,
    serverless_task_max_statement_size: typing.Optional[builtins.str] = None,
    serverless_task_min_statement_size: typing.Optional[builtins.str] = None,
    session_policy: typing.Optional[builtins.str] = None,
    simulated_data_sharing_consumer: typing.Optional[builtins.str] = None,
    sso_login_page: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    statement_queued_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    statement_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    storage_serialization_policy: typing.Optional[builtins.str] = None,
    strict_json_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suspend_task_after_num_failures: typing.Optional[jsii.Number] = None,
    task_auto_retry_attempts: typing.Optional[jsii.Number] = None,
    time_input_format: typing.Optional[builtins.str] = None,
    time_output_format: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CurrentAccountTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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
    week_of_year_policy: typing.Optional[jsii.Number] = None,
    week_start: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447ebb75c5d2f45ca020d7fd6c7296d7919c51632008345c2ae7bf5558a46133(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1ab3f3d6ff9cc5e9476a6a39a0acf6d6c4703259e8ef2ead23a73015c2bade(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60528470a50b5a1dcf993d209d5443121f465a15a2496238afd9ca4b5fb049e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6b407a86f77579f53e5f177da952b8a34feaf3596796030196201a187360a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a75187fd38f80a99ace3b446eea22863c05d0e6ba1b20897dc842912b024c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e78614b99b865408e1a04efa0c8aa38fa7617a24994b3879c3e66407eb78226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62ffa171b0c6da1d46d4f80cfe5d31288ddfcfcffbc3e04dbf7703ca3a06193(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CurrentAccountTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
