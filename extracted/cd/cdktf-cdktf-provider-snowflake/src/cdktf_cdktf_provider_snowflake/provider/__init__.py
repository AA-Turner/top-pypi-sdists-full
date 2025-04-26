r'''
# `provider`

Refer to the Terraform Registry for docs: [`snowflake`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs).
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


class SnowflakeProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.provider.SnowflakeProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs snowflake}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_name: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        authenticator: typing.Optional[builtins.str] = None,
        client_ip: typing.Optional[builtins.str] = None,
        client_request_mfa_token: typing.Optional[builtins.str] = None,
        client_store_temporary_credential: typing.Optional[builtins.str] = None,
        client_timeout: typing.Optional[jsii.Number] = None,
        disable_console_login: typing.Optional[builtins.str] = None,
        disable_query_context_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_telemetry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        driver_tracing: typing.Optional[builtins.str] = None,
        external_browser_timeout: typing.Optional[jsii.Number] = None,
        host: typing.Optional[builtins.str] = None,
        include_retry_reason: typing.Optional[builtins.str] = None,
        insecure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jwt_client_timeout: typing.Optional[jsii.Number] = None,
        jwt_expire_timeout: typing.Optional[jsii.Number] = None,
        keep_session_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        login_timeout: typing.Optional[jsii.Number] = None,
        max_retry_count: typing.Optional[jsii.Number] = None,
        ocsp_fail_open: typing.Optional[builtins.str] = None,
        okta_url: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        passcode: typing.Optional[builtins.str] = None,
        passcode_in_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preview_features_enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_key: typing.Optional[builtins.str] = None,
        private_key_passphrase: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        request_timeout: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        skip_toml_file_permission_verification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tmp_directory_path: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        token_accessor: typing.Optional[typing.Union["SnowflakeProviderTokenAccessor", typing.Dict[builtins.str, typing.Any]]] = None,
        user: typing.Optional[builtins.str] = None,
        validate_default_parameters: typing.Optional[builtins.str] = None,
        warehouse: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs snowflake} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_name: Specifies your Snowflake account name assigned by Snowflake. For information about account identifiers, see the `Snowflake documentation <https://docs.snowflake.com/en/user-guide/admin-account-identifier#account-name>`_. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_ACCOUNT_NAME`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#account_name SnowflakeProvider#account_name}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#alias SnowflakeProvider#alias}
        :param authenticator: Specifies the `authentication type <https://pkg.go.dev/github.com/snowflakedb/gosnowflake#AuthType>`_ to use when connecting to Snowflake. Valid options are: ``SNOWFLAKE`` | ``OAUTH`` | ``EXTERNALBROWSER`` | ``OKTA`` | ``SNOWFLAKE_JWT`` | ``TOKENACCESSOR`` | ``USERNAMEPASSWORDMFA``. Can also be sourced from the ``SNOWFLAKE_AUTHENTICATOR`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#authenticator SnowflakeProvider#authenticator}
        :param client_ip: IP address for network checks. Can also be sourced from the ``SNOWFLAKE_CLIENT_IP`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_ip SnowflakeProvider#client_ip}
        :param client_request_mfa_token: When true the MFA token is cached in the credential manager. True by default in Windows/OSX. False for Linux. Can also be sourced from the ``SNOWFLAKE_CLIENT_REQUEST_MFA_TOKEN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_request_mfa_token SnowflakeProvider#client_request_mfa_token}
        :param client_store_temporary_credential: When true the ID token is cached in the credential manager. True by default in Windows/OSX. False for Linux. Can also be sourced from the ``SNOWFLAKE_CLIENT_STORE_TEMPORARY_CREDENTIAL`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_store_temporary_credential SnowflakeProvider#client_store_temporary_credential}
        :param client_timeout: The timeout in seconds for the client to complete the authentication. Can also be sourced from the ``SNOWFLAKE_CLIENT_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_timeout SnowflakeProvider#client_timeout}
        :param disable_console_login: Indicates whether console login should be disabled in the driver. Can also be sourced from the ``SNOWFLAKE_DISABLE_CONSOLE_LOGIN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_console_login SnowflakeProvider#disable_console_login}
        :param disable_query_context_cache: Disables HTAP query context cache in the driver. Can also be sourced from the ``SNOWFLAKE_DISABLE_QUERY_CONTEXT_CACHE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_query_context_cache SnowflakeProvider#disable_query_context_cache}
        :param disable_telemetry: Disables telemetry in the driver. Can also be sourced from the ``DISABLE_TELEMETRY`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_telemetry SnowflakeProvider#disable_telemetry}
        :param driver_tracing: Specifies the logging level to be used by the driver. Valid options are: ``trace`` | ``debug`` | ``info`` | ``print`` | ``warning`` | ``error`` | ``fatal`` | ``panic``. Can also be sourced from the ``SNOWFLAKE_DRIVER_TRACING`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#driver_tracing SnowflakeProvider#driver_tracing}
        :param external_browser_timeout: The timeout in seconds for the external browser to complete the authentication. Can also be sourced from the ``SNOWFLAKE_EXTERNAL_BROWSER_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#external_browser_timeout SnowflakeProvider#external_browser_timeout}
        :param host: Specifies a custom host value used by the driver for privatelink connections. Can also be sourced from the ``SNOWFLAKE_HOST`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#host SnowflakeProvider#host}
        :param include_retry_reason: Should retried request contain retry reason. Can also be sourced from the ``SNOWFLAKE_INCLUDE_RETRY_REASON`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#include_retry_reason SnowflakeProvider#include_retry_reason}
        :param insecure_mode: If true, bypass the Online Certificate Status Protocol (OCSP) certificate revocation check. IMPORTANT: Change the default value for testing or emergency situations only. Can also be sourced from the ``SNOWFLAKE_INSECURE_MODE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#insecure_mode SnowflakeProvider#insecure_mode}
        :param jwt_client_timeout: The timeout in seconds for the JWT client to complete the authentication. Can also be sourced from the ``SNOWFLAKE_JWT_CLIENT_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#jwt_client_timeout SnowflakeProvider#jwt_client_timeout}
        :param jwt_expire_timeout: JWT expire after timeout in seconds. Can also be sourced from the ``SNOWFLAKE_JWT_EXPIRE_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#jwt_expire_timeout SnowflakeProvider#jwt_expire_timeout}
        :param keep_session_alive: Enables the session to persist even after the connection is closed. Can also be sourced from the ``SNOWFLAKE_KEEP_SESSION_ALIVE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#keep_session_alive SnowflakeProvider#keep_session_alive}
        :param login_timeout: Login retry timeout in seconds EXCLUDING network roundtrip and read out http response. Can also be sourced from the ``SNOWFLAKE_LOGIN_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#login_timeout SnowflakeProvider#login_timeout}
        :param max_retry_count: Specifies how many times non-periodic HTTP request can be retried by the driver. Can also be sourced from the ``SNOWFLAKE_MAX_RETRY_COUNT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#max_retry_count SnowflakeProvider#max_retry_count}
        :param ocsp_fail_open: True represents OCSP fail open mode. False represents OCSP fail closed mode. Fail open true by default. Can also be sourced from the ``SNOWFLAKE_OCSP_FAIL_OPEN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#ocsp_fail_open SnowflakeProvider#ocsp_fail_open}
        :param okta_url: The URL of the Okta server. e.g. https://example.okta.com. Okta URL host needs to to have a suffix ``okta.com``. Read more in Snowflake `docs <https://docs.snowflake.com/en/user-guide/oauth-okta>`_. Can also be sourced from the ``SNOWFLAKE_OKTA_URL`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#okta_url SnowflakeProvider#okta_url}
        :param organization_name: Specifies your Snowflake organization name assigned by Snowflake. For information about account identifiers, see the `Snowflake documentation <https://docs.snowflake.com/en/user-guide/admin-account-identifier#organization-name>`_. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_ORGANIZATION_NAME`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#organization_name SnowflakeProvider#organization_name}
        :param params: Sets other connection (i.e. session) parameters. `Parameters <https://docs.snowflake.com/en/sql-reference/parameters>`_. This field can not be set with environmental variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#params SnowflakeProvider#params}
        :param passcode: Specifies the passcode provided by Duo when using multi-factor authentication (MFA) for login. Can also be sourced from the ``SNOWFLAKE_PASSCODE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#passcode SnowflakeProvider#passcode}
        :param passcode_in_password: False by default. Set to true if the MFA passcode is embedded to the configured password. Can also be sourced from the ``SNOWFLAKE_PASSCODE_IN_PASSWORD`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#passcode_in_password SnowflakeProvider#passcode_in_password}
        :param password: Password for user + password auth. Cannot be used with ``private_key`` and ``private_key_passphrase``. Can also be sourced from the ``SNOWFLAKE_PASSWORD`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#password SnowflakeProvider#password}
        :param port: Specifies a custom port value used by the driver for privatelink connections. Can also be sourced from the ``SNOWFLAKE_PORT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#port SnowflakeProvider#port}
        :param preview_features_enabled: A list of preview features that are handled by the provider. See `preview features list <https://github.com/Snowflake-Labs/terraform-provider-snowflake/blob/main/v1-preparations/LIST_OF_PREVIEW_FEATURES_FOR_V1.md>`_. Preview features may have breaking changes in future releases, even without raising the major version. This field can not be set with environmental variables. Valid options are: ``snowflake_current_account_datasource`` | ``snowflake_account_authentication_policy_attachment_resource`` | ``snowflake_account_password_policy_attachment_resource`` | ``snowflake_alert_resource`` | ``snowflake_alerts_datasource`` | ``snowflake_api_integration_resource`` | ``snowflake_authentication_policy_resource`` | ``snowflake_cortex_search_service_resource`` | ``snowflake_cortex_search_services_datasource`` | ``snowflake_database_datasource`` | ``snowflake_database_role_datasource`` | ``snowflake_dynamic_table_resource`` | ``snowflake_dynamic_tables_datasource`` | ``snowflake_external_function_resource`` | ``snowflake_external_functions_datasource`` | ``snowflake_external_table_resource`` | ``snowflake_external_tables_datasource`` | ``snowflake_external_volume_resource`` | ``snowflake_failover_group_resource`` | ``snowflake_failover_groups_datasource`` | ``snowflake_file_format_resource`` | ``snowflake_file_formats_datasource`` | ``snowflake_function_java_resource`` | ``snowflake_function_javascript_resource`` | ``snowflake_function_python_resource`` | ``snowflake_function_scala_resource`` | ``snowflake_function_sql_resource`` | ``snowflake_functions_datasource`` | ``snowflake_managed_account_resource`` | ``snowflake_materialized_view_resource`` | ``snowflake_materialized_views_datasource`` | ``snowflake_network_policy_attachment_resource`` | ``snowflake_network_rule_resource`` | ``snowflake_email_notification_integration_resource`` | ``snowflake_notification_integration_resource`` | ``snowflake_object_parameter_resource`` | ``snowflake_password_policy_resource`` | ``snowflake_pipe_resource`` | ``snowflake_pipes_datasource`` | ``snowflake_current_role_datasource`` | ``snowflake_sequence_resource`` | ``snowflake_sequences_datasource`` | ``snowflake_share_resource`` | ``snowflake_shares_datasource`` | ``snowflake_parameters_datasource`` | ``snowflake_procedure_java_resource`` | ``snowflake_procedure_javascript_resource`` | ``snowflake_procedure_python_resource`` | ``snowflake_procedure_scala_resource`` | ``snowflake_procedure_sql_resource`` | ``snowflake_procedures_datasource`` | ``snowflake_stage_resource`` | ``snowflake_stages_datasource`` | ``snowflake_storage_integration_resource`` | ``snowflake_storage_integrations_datasource`` | ``snowflake_system_generate_scim_access_token_datasource`` | ``snowflake_system_get_aws_sns_iam_policy_datasource`` | ``snowflake_system_get_privatelink_config_datasource`` | ``snowflake_system_get_snowflake_platform_info_datasource`` | ``snowflake_table_column_masking_policy_application_resource`` | ``snowflake_table_constraint_resource`` | ``snowflake_table_resource`` | ``snowflake_tables_datasource`` | ``snowflake_user_authentication_policy_attachment_resource`` | ``snowflake_user_public_keys_resource`` | ``snowflake_user_password_policy_attachment_resource``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#preview_features_enabled SnowflakeProvider#preview_features_enabled}
        :param private_key: Private Key for username+private-key auth. Cannot be used with ``password``. Can also be sourced from the ``SNOWFLAKE_PRIVATE_KEY`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#private_key SnowflakeProvider#private_key}
        :param private_key_passphrase: Supports the encryption ciphers aes-128-cbc, aes-128-gcm, aes-192-cbc, aes-192-gcm, aes-256-cbc, aes-256-gcm, and des-ede3-cbc. Can also be sourced from the ``SNOWFLAKE_PRIVATE_KEY_PASSPHRASE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#private_key_passphrase SnowflakeProvider#private_key_passphrase}
        :param profile: Sets the profile to read from ~/.snowflake/config file. Can also be sourced from the ``SNOWFLAKE_PROFILE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#profile SnowflakeProvider#profile}
        :param protocol: A protocol used in the connection. Valid options are: ``http`` | ``https``. Can also be sourced from the ``SNOWFLAKE_PROTOCOL`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#protocol SnowflakeProvider#protocol}
        :param request_timeout: request retry timeout in seconds EXCLUDING network roundtrip and read out http response. Can also be sourced from the ``SNOWFLAKE_REQUEST_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#request_timeout SnowflakeProvider#request_timeout}
        :param role: Specifies the role to use by default for accessing Snowflake objects in the client session. Can also be sourced from the ``SNOWFLAKE_ROLE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#role SnowflakeProvider#role}
        :param skip_toml_file_permission_verification: True by default. Skips TOML configuration file permission verification. This flag has no effect on Windows systems, as the permissions are not checked on this platform. We recommend setting this to ``false`` and setting the proper privileges - see `the section below <#order-precedence>`_. Can also be sourced from the ``SNOWFLAKE_SKIP_TOML_FILE_PERMISSION_VERIFICATION`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#skip_toml_file_permission_verification SnowflakeProvider#skip_toml_file_permission_verification}
        :param tmp_directory_path: Sets temporary directory used by the driver for operations like encrypting, compressing etc. Can also be sourced from the ``SNOWFLAKE_TMP_DIRECTORY_PATH`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#tmp_directory_path SnowflakeProvider#tmp_directory_path}
        :param token: Token to use for OAuth and other forms of token based auth. Can also be sourced from the ``SNOWFLAKE_TOKEN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#token SnowflakeProvider#token}
        :param token_accessor: token_accessor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#token_accessor SnowflakeProvider#token_accessor}
        :param user: Username. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_USER`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#user SnowflakeProvider#user}
        :param validate_default_parameters: True by default. If false, disables the validation checks for Database, Schema, Warehouse and Role at the time a connection is established. Can also be sourced from the ``SNOWFLAKE_VALIDATE_DEFAULT_PARAMETERS`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#validate_default_parameters SnowflakeProvider#validate_default_parameters}
        :param warehouse: Specifies the virtual warehouse to use by default for queries, loading, etc. in the client session. Can also be sourced from the ``SNOWFLAKE_WAREHOUSE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#warehouse SnowflakeProvider#warehouse}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dffb8c16f0bdbd356b60ba75b76332c0fa5872a9b67c09d939ada39e30798782)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = SnowflakeProviderConfig(
            account_name=account_name,
            alias=alias,
            authenticator=authenticator,
            client_ip=client_ip,
            client_request_mfa_token=client_request_mfa_token,
            client_store_temporary_credential=client_store_temporary_credential,
            client_timeout=client_timeout,
            disable_console_login=disable_console_login,
            disable_query_context_cache=disable_query_context_cache,
            disable_telemetry=disable_telemetry,
            driver_tracing=driver_tracing,
            external_browser_timeout=external_browser_timeout,
            host=host,
            include_retry_reason=include_retry_reason,
            insecure_mode=insecure_mode,
            jwt_client_timeout=jwt_client_timeout,
            jwt_expire_timeout=jwt_expire_timeout,
            keep_session_alive=keep_session_alive,
            login_timeout=login_timeout,
            max_retry_count=max_retry_count,
            ocsp_fail_open=ocsp_fail_open,
            okta_url=okta_url,
            organization_name=organization_name,
            params=params,
            passcode=passcode,
            passcode_in_password=passcode_in_password,
            password=password,
            port=port,
            preview_features_enabled=preview_features_enabled,
            private_key=private_key,
            private_key_passphrase=private_key_passphrase,
            profile=profile,
            protocol=protocol,
            request_timeout=request_timeout,
            role=role,
            skip_toml_file_permission_verification=skip_toml_file_permission_verification,
            tmp_directory_path=tmp_directory_path,
            token=token,
            token_accessor=token_accessor,
            user=user,
            validate_default_parameters=validate_default_parameters,
            warehouse=warehouse,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a SnowflakeProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SnowflakeProvider to import.
        :param import_from_id: The id of the existing SnowflakeProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SnowflakeProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a3a5ee41e1141e62bec029bdb8709bf3cc38a98cb6c277789fc640ecc924d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAccountName")
    def reset_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountName", []))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetAuthenticator")
    def reset_authenticator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticator", []))

    @jsii.member(jsii_name="resetClientIp")
    def reset_client_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientIp", []))

    @jsii.member(jsii_name="resetClientRequestMfaToken")
    def reset_client_request_mfa_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientRequestMfaToken", []))

    @jsii.member(jsii_name="resetClientStoreTemporaryCredential")
    def reset_client_store_temporary_credential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientStoreTemporaryCredential", []))

    @jsii.member(jsii_name="resetClientTimeout")
    def reset_client_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTimeout", []))

    @jsii.member(jsii_name="resetDisableConsoleLogin")
    def reset_disable_console_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableConsoleLogin", []))

    @jsii.member(jsii_name="resetDisableQueryContextCache")
    def reset_disable_query_context_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableQueryContextCache", []))

    @jsii.member(jsii_name="resetDisableTelemetry")
    def reset_disable_telemetry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableTelemetry", []))

    @jsii.member(jsii_name="resetDriverTracing")
    def reset_driver_tracing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverTracing", []))

    @jsii.member(jsii_name="resetExternalBrowserTimeout")
    def reset_external_browser_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalBrowserTimeout", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetIncludeRetryReason")
    def reset_include_retry_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRetryReason", []))

    @jsii.member(jsii_name="resetInsecureMode")
    def reset_insecure_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureMode", []))

    @jsii.member(jsii_name="resetJwtClientTimeout")
    def reset_jwt_client_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtClientTimeout", []))

    @jsii.member(jsii_name="resetJwtExpireTimeout")
    def reset_jwt_expire_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtExpireTimeout", []))

    @jsii.member(jsii_name="resetKeepSessionAlive")
    def reset_keep_session_alive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepSessionAlive", []))

    @jsii.member(jsii_name="resetLoginTimeout")
    def reset_login_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginTimeout", []))

    @jsii.member(jsii_name="resetMaxRetryCount")
    def reset_max_retry_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetryCount", []))

    @jsii.member(jsii_name="resetOcspFailOpen")
    def reset_ocsp_fail_open(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcspFailOpen", []))

    @jsii.member(jsii_name="resetOktaUrl")
    def reset_okta_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOktaUrl", []))

    @jsii.member(jsii_name="resetOrganizationName")
    def reset_organization_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationName", []))

    @jsii.member(jsii_name="resetParams")
    def reset_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParams", []))

    @jsii.member(jsii_name="resetPasscode")
    def reset_passcode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasscode", []))

    @jsii.member(jsii_name="resetPasscodeInPassword")
    def reset_passcode_in_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasscodeInPassword", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPreviewFeaturesEnabled")
    def reset_preview_features_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreviewFeaturesEnabled", []))

    @jsii.member(jsii_name="resetPrivateKey")
    def reset_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKey", []))

    @jsii.member(jsii_name="resetPrivateKeyPassphrase")
    def reset_private_key_passphrase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKeyPassphrase", []))

    @jsii.member(jsii_name="resetProfile")
    def reset_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfile", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRequestTimeout")
    def reset_request_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestTimeout", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @jsii.member(jsii_name="resetSkipTomlFilePermissionVerification")
    def reset_skip_toml_file_permission_verification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipTomlFilePermissionVerification", []))

    @jsii.member(jsii_name="resetTmpDirectoryPath")
    def reset_tmp_directory_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTmpDirectoryPath", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetTokenAccessor")
    def reset_token_accessor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenAccessor", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @jsii.member(jsii_name="resetValidateDefaultParameters")
    def reset_validate_default_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateDefaultParameters", []))

    @jsii.member(jsii_name="resetWarehouse")
    def reset_warehouse(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarehouse", []))

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
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticatorInput")
    def authenticator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticatorInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIpInput")
    def client_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIpInput"))

    @builtins.property
    @jsii.member(jsii_name="clientRequestMfaTokenInput")
    def client_request_mfa_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientRequestMfaTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="clientStoreTemporaryCredentialInput")
    def client_store_temporary_credential_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientStoreTemporaryCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTimeoutInput")
    def client_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="disableConsoleLoginInput")
    def disable_console_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "disableConsoleLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="disableQueryContextCacheInput")
    def disable_query_context_cache_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableQueryContextCacheInput"))

    @builtins.property
    @jsii.member(jsii_name="disableTelemetryInput")
    def disable_telemetry_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableTelemetryInput"))

    @builtins.property
    @jsii.member(jsii_name="driverTracingInput")
    def driver_tracing_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverTracingInput"))

    @builtins.property
    @jsii.member(jsii_name="externalBrowserTimeoutInput")
    def external_browser_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalBrowserTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="includeRetryReasonInput")
    def include_retry_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeRetryReasonInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureModeInput")
    def insecure_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureModeInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtClientTimeoutInput")
    def jwt_client_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jwtClientTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtExpireTimeoutInput")
    def jwt_expire_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jwtExpireTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="keepSessionAliveInput")
    def keep_session_alive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepSessionAliveInput"))

    @builtins.property
    @jsii.member(jsii_name="loginTimeoutInput")
    def login_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "loginTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetryCountInput")
    def max_retry_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetryCountInput"))

    @builtins.property
    @jsii.member(jsii_name="ocspFailOpenInput")
    def ocsp_fail_open_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ocspFailOpenInput"))

    @builtins.property
    @jsii.member(jsii_name="oktaUrlInput")
    def okta_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oktaUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationNameInput")
    def organization_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="paramsInput")
    def params_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "paramsInput"))

    @builtins.property
    @jsii.member(jsii_name="passcodeInPasswordInput")
    def passcode_in_password_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passcodeInPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="passcodeInput")
    def passcode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passcodeInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="previewFeaturesEnabledInput")
    def preview_features_enabled_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "previewFeaturesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyPassphraseInput")
    def private_key_passphrase_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyPassphraseInput"))

    @builtins.property
    @jsii.member(jsii_name="profileInput")
    def profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profileInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="requestTimeoutInput")
    def request_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="skipTomlFilePermissionVerificationInput")
    def skip_toml_file_permission_verification_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipTomlFilePermissionVerificationInput"))

    @builtins.property
    @jsii.member(jsii_name="tmpDirectoryPathInput")
    def tmp_directory_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tmpDirectoryPathInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenAccessorInput")
    def token_accessor_input(self) -> typing.Optional["SnowflakeProviderTokenAccessor"]:
        return typing.cast(typing.Optional["SnowflakeProviderTokenAccessor"], jsii.get(self, "tokenAccessorInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="validateDefaultParametersInput")
    def validate_default_parameters_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validateDefaultParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="warehouseInput")
    def warehouse_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5315d56ee30ee609fed8a7384053e2d89e64d147c3e39d4a64e7ee8f9da71c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cdc7cd12d304b2eddd5316af316d83f132ecae360404d6176a8e6a997e8dc2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticator")
    def authenticator(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticator"))

    @authenticator.setter
    def authenticator(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6d6a40d1a5605a9094439f3d2d1e57d143ffa3c2083b130937df91f19b35b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientIp")
    def client_ip(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIp"))

    @client_ip.setter
    def client_ip(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370f87780241c7b2653971c27701eed45e4fc0fea1e1c19909bf4822f9a35139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientRequestMfaToken")
    def client_request_mfa_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientRequestMfaToken"))

    @client_request_mfa_token.setter
    def client_request_mfa_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f642b106f9ead7f93ccfef26461a60434d7ce40769a4318d6de7980d579723d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientRequestMfaToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientStoreTemporaryCredential")
    def client_store_temporary_credential(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientStoreTemporaryCredential"))

    @client_store_temporary_credential.setter
    def client_store_temporary_credential(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6586aace401480ef0ce4ab53207770ca079b6a438409c516fcce530b59649f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientStoreTemporaryCredential", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientTimeout")
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "clientTimeout"))

    @client_timeout.setter
    def client_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818f5069d0221466e050c5c53b6b1e3eaaac0d5a53109481e4ead46297f0b141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableConsoleLogin")
    def disable_console_login(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "disableConsoleLogin"))

    @disable_console_login.setter
    def disable_console_login(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f30878256d65fb4fbff323db95be390c5bb75dc6485dcce1f99b94352cb2923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableConsoleLogin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableQueryContextCache")
    def disable_query_context_cache(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableQueryContextCache"))

    @disable_query_context_cache.setter
    def disable_query_context_cache(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abcf60fa4330b65affc6db33362afcc184ad771a4fafb37665309283f9986ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableQueryContextCache", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableTelemetry")
    def disable_telemetry(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableTelemetry"))

    @disable_telemetry.setter
    def disable_telemetry(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269dfbf8bd7e9687bd9093ed943acb915d1e33d5f2a1d222d2ebe73340152dd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTelemetry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverTracing")
    def driver_tracing(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverTracing"))

    @driver_tracing.setter
    def driver_tracing(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e803321f9dec6856addb562eb977c838137e88d82837d8f7697c4ab9a728c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverTracing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalBrowserTimeout")
    def external_browser_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalBrowserTimeout"))

    @external_browser_timeout.setter
    def external_browser_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be356c932dd3785d09f2c4a5c787d88fcbbb1846738765a3ac6f6118bf230c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalBrowserTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "host"))

    @host.setter
    def host(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25df655b6fdfcfce4cc80d4c7d317296ba4b1b1e6a48e51e051a48b933da7a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeRetryReason")
    def include_retry_reason(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeRetryReason"))

    @include_retry_reason.setter
    def include_retry_reason(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2721eb9275edb4164b9ec378522a486b2f6dc36b44bd5279ea361763413992c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeRetryReason", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="insecureMode")
    def insecure_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureMode"))

    @insecure_mode.setter
    def insecure_mode(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0b770f66297cf03ca54574462492185fa522c242f96b03b32317dc69d38166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtClientTimeout")
    def jwt_client_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jwtClientTimeout"))

    @jwt_client_timeout.setter
    def jwt_client_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c2273f5de1a2697d59b298ef8372bd657956bd24ac15953410953c6bc5e48e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtClientTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtExpireTimeout")
    def jwt_expire_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "jwtExpireTimeout"))

    @jwt_expire_timeout.setter
    def jwt_expire_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e006c8754a599103a5f7c5d6363a2fd8f44dbc569d9882eab0fe73527000b263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtExpireTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepSessionAlive")
    def keep_session_alive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepSessionAlive"))

    @keep_session_alive.setter
    def keep_session_alive(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87491bfb7b1ecfe9103c8dddaf7734ff39eb830fb1a351d40dc0f7c1adb4d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepSessionAlive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginTimeout")
    def login_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "loginTimeout"))

    @login_timeout.setter
    def login_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e932bf3dd2379e89075f4162cb5bc10d1da873452b7e84361af61777412cd1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetryCount")
    def max_retry_count(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetryCount"))

    @max_retry_count.setter
    def max_retry_count(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36d2e0b2b382201abb6a86d0fe2d7485162112389b92ff28ef96259e1ccffea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetryCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ocspFailOpen")
    def ocsp_fail_open(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ocspFailOpen"))

    @ocsp_fail_open.setter
    def ocsp_fail_open(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5794c009d8765aa8f769a80e9753aabe08dc725863ff7b18eab0341eed543c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ocspFailOpen", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oktaUrl")
    def okta_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oktaUrl"))

    @okta_url.setter
    def okta_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2acb8cea3c2b00df9129f4f3b5786e34b302b4fbbe61119d57006a7804f3f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oktaUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationName")
    def organization_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationName"))

    @organization_name.setter
    def organization_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed43f438fe4a19bb28b8430f1c8bb2fd059736a0f6aed32c603c6be4724cad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="params")
    def params(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "params"))

    @params.setter
    def params(
        self,
        value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5079b47ba384ea5e3aaafe6322f07c7068ea187e00a883751b397324ec04b6c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "params", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passcode")
    def passcode(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passcode"))

    @passcode.setter
    def passcode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8aeb67752ef65d8786754b2e094e8334d801727dcb831c2a6d6bbbd59c0c6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passcode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passcodeInPassword")
    def passcode_in_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passcodeInPassword"))

    @passcode_in_password.setter
    def passcode_in_password(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d285d39d0d7dfff15a4462be9b03f6e0824d61185275e2de835935b4db1d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passcodeInPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4647c5ce21749b9912e9bb483866a4fe9decad7840786080279fac4bf9b9881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ab59f5493ec686723d4a013bc5f681695f8805e1a21d0e2961ffb9ba96bb2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="previewFeaturesEnabled")
    def preview_features_enabled(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "previewFeaturesEnabled"))

    @preview_features_enabled.setter
    def preview_features_enabled(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12651490b7406e943ebdd65ee6414415ba2a4f63379177d5a569694f8682242b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previewFeaturesEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174acb5ca0c2f03f2c07759d01042240477d689ab50d9a3e5014d671f7072072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKeyPassphrase")
    def private_key_passphrase(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyPassphrase"))

    @private_key_passphrase.setter
    def private_key_passphrase(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e45747860bace19eea01fe56764a0071fb76645a7df1767604942c712bc7fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKeyPassphrase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="profile")
    def profile(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "profile"))

    @profile.setter
    def profile(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2890938b1cd71ed7815000e422a912b7b3d54903511d4f7b45712b5a30212795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272d3205644fbaa065eff9f5ac6d27774f4829ae96c327fd974c31e2c14d17ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestTimeout")
    def request_timeout(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requestTimeout"))

    @request_timeout.setter
    def request_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee0543502fab097af52ebd9c81a19791d58a795a589dead81d2ddb4e53710eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "role"))

    @role.setter
    def role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c825aa96baa5ca037e135d9294ae15fc9d5395c87a9275884dd82a5edd2ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipTomlFilePermissionVerification")
    def skip_toml_file_permission_verification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipTomlFilePermissionVerification"))

    @skip_toml_file_permission_verification.setter
    def skip_toml_file_permission_verification(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731655dfe45c6700235008005df19215e75be3265c5dc630398af6efc1f8d115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipTomlFilePermissionVerification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tmpDirectoryPath")
    def tmp_directory_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tmpDirectoryPath"))

    @tmp_directory_path.setter
    def tmp_directory_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86326f4f72d6311c173383f98855bddd97933cfde8d7b692da0f5c02423b0a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tmpDirectoryPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40535fefad35c2491bb2aa60c6522f5cd80fc0876e21c80deb2f684e33cf2380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenAccessor")
    def token_accessor(self) -> typing.Optional["SnowflakeProviderTokenAccessor"]:
        return typing.cast(typing.Optional["SnowflakeProviderTokenAccessor"], jsii.get(self, "tokenAccessor"))

    @token_accessor.setter
    def token_accessor(
        self,
        value: typing.Optional["SnowflakeProviderTokenAccessor"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b86051ecb7af168b4414164285a52653116c6c1fd66e45e577d5e94b071fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenAccessor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "user"))

    @user.setter
    def user(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc30eb22eb05f35288fb4961dd14be1e1fe9101084acdde298c42009214db961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateDefaultParameters")
    def validate_default_parameters(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validateDefaultParameters"))

    @validate_default_parameters.setter
    def validate_default_parameters(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43646ed314e4eea24bb621b967fbe094538e70a124a4c7cc36c518a3834ac02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateDefaultParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouse")
    def warehouse(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouse"))

    @warehouse.setter
    def warehouse(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d86a20638ec60e4335171ba31cc595ce61cbb7fbb325816de15f3387860facb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouse", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.provider.SnowflakeProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "account_name": "accountName",
        "alias": "alias",
        "authenticator": "authenticator",
        "client_ip": "clientIp",
        "client_request_mfa_token": "clientRequestMfaToken",
        "client_store_temporary_credential": "clientStoreTemporaryCredential",
        "client_timeout": "clientTimeout",
        "disable_console_login": "disableConsoleLogin",
        "disable_query_context_cache": "disableQueryContextCache",
        "disable_telemetry": "disableTelemetry",
        "driver_tracing": "driverTracing",
        "external_browser_timeout": "externalBrowserTimeout",
        "host": "host",
        "include_retry_reason": "includeRetryReason",
        "insecure_mode": "insecureMode",
        "jwt_client_timeout": "jwtClientTimeout",
        "jwt_expire_timeout": "jwtExpireTimeout",
        "keep_session_alive": "keepSessionAlive",
        "login_timeout": "loginTimeout",
        "max_retry_count": "maxRetryCount",
        "ocsp_fail_open": "ocspFailOpen",
        "okta_url": "oktaUrl",
        "organization_name": "organizationName",
        "params": "params",
        "passcode": "passcode",
        "passcode_in_password": "passcodeInPassword",
        "password": "password",
        "port": "port",
        "preview_features_enabled": "previewFeaturesEnabled",
        "private_key": "privateKey",
        "private_key_passphrase": "privateKeyPassphrase",
        "profile": "profile",
        "protocol": "protocol",
        "request_timeout": "requestTimeout",
        "role": "role",
        "skip_toml_file_permission_verification": "skipTomlFilePermissionVerification",
        "tmp_directory_path": "tmpDirectoryPath",
        "token": "token",
        "token_accessor": "tokenAccessor",
        "user": "user",
        "validate_default_parameters": "validateDefaultParameters",
        "warehouse": "warehouse",
    },
)
class SnowflakeProviderConfig:
    def __init__(
        self,
        *,
        account_name: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        authenticator: typing.Optional[builtins.str] = None,
        client_ip: typing.Optional[builtins.str] = None,
        client_request_mfa_token: typing.Optional[builtins.str] = None,
        client_store_temporary_credential: typing.Optional[builtins.str] = None,
        client_timeout: typing.Optional[jsii.Number] = None,
        disable_console_login: typing.Optional[builtins.str] = None,
        disable_query_context_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_telemetry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        driver_tracing: typing.Optional[builtins.str] = None,
        external_browser_timeout: typing.Optional[jsii.Number] = None,
        host: typing.Optional[builtins.str] = None,
        include_retry_reason: typing.Optional[builtins.str] = None,
        insecure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jwt_client_timeout: typing.Optional[jsii.Number] = None,
        jwt_expire_timeout: typing.Optional[jsii.Number] = None,
        keep_session_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        login_timeout: typing.Optional[jsii.Number] = None,
        max_retry_count: typing.Optional[jsii.Number] = None,
        ocsp_fail_open: typing.Optional[builtins.str] = None,
        okta_url: typing.Optional[builtins.str] = None,
        organization_name: typing.Optional[builtins.str] = None,
        params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        passcode: typing.Optional[builtins.str] = None,
        passcode_in_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preview_features_enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_key: typing.Optional[builtins.str] = None,
        private_key_passphrase: typing.Optional[builtins.str] = None,
        profile: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        request_timeout: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        skip_toml_file_permission_verification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tmp_directory_path: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        token_accessor: typing.Optional[typing.Union["SnowflakeProviderTokenAccessor", typing.Dict[builtins.str, typing.Any]]] = None,
        user: typing.Optional[builtins.str] = None,
        validate_default_parameters: typing.Optional[builtins.str] = None,
        warehouse: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Specifies your Snowflake account name assigned by Snowflake. For information about account identifiers, see the `Snowflake documentation <https://docs.snowflake.com/en/user-guide/admin-account-identifier#account-name>`_. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_ACCOUNT_NAME`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#account_name SnowflakeProvider#account_name}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#alias SnowflakeProvider#alias}
        :param authenticator: Specifies the `authentication type <https://pkg.go.dev/github.com/snowflakedb/gosnowflake#AuthType>`_ to use when connecting to Snowflake. Valid options are: ``SNOWFLAKE`` | ``OAUTH`` | ``EXTERNALBROWSER`` | ``OKTA`` | ``SNOWFLAKE_JWT`` | ``TOKENACCESSOR`` | ``USERNAMEPASSWORDMFA``. Can also be sourced from the ``SNOWFLAKE_AUTHENTICATOR`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#authenticator SnowflakeProvider#authenticator}
        :param client_ip: IP address for network checks. Can also be sourced from the ``SNOWFLAKE_CLIENT_IP`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_ip SnowflakeProvider#client_ip}
        :param client_request_mfa_token: When true the MFA token is cached in the credential manager. True by default in Windows/OSX. False for Linux. Can also be sourced from the ``SNOWFLAKE_CLIENT_REQUEST_MFA_TOKEN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_request_mfa_token SnowflakeProvider#client_request_mfa_token}
        :param client_store_temporary_credential: When true the ID token is cached in the credential manager. True by default in Windows/OSX. False for Linux. Can also be sourced from the ``SNOWFLAKE_CLIENT_STORE_TEMPORARY_CREDENTIAL`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_store_temporary_credential SnowflakeProvider#client_store_temporary_credential}
        :param client_timeout: The timeout in seconds for the client to complete the authentication. Can also be sourced from the ``SNOWFLAKE_CLIENT_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_timeout SnowflakeProvider#client_timeout}
        :param disable_console_login: Indicates whether console login should be disabled in the driver. Can also be sourced from the ``SNOWFLAKE_DISABLE_CONSOLE_LOGIN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_console_login SnowflakeProvider#disable_console_login}
        :param disable_query_context_cache: Disables HTAP query context cache in the driver. Can also be sourced from the ``SNOWFLAKE_DISABLE_QUERY_CONTEXT_CACHE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_query_context_cache SnowflakeProvider#disable_query_context_cache}
        :param disable_telemetry: Disables telemetry in the driver. Can also be sourced from the ``DISABLE_TELEMETRY`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_telemetry SnowflakeProvider#disable_telemetry}
        :param driver_tracing: Specifies the logging level to be used by the driver. Valid options are: ``trace`` | ``debug`` | ``info`` | ``print`` | ``warning`` | ``error`` | ``fatal`` | ``panic``. Can also be sourced from the ``SNOWFLAKE_DRIVER_TRACING`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#driver_tracing SnowflakeProvider#driver_tracing}
        :param external_browser_timeout: The timeout in seconds for the external browser to complete the authentication. Can also be sourced from the ``SNOWFLAKE_EXTERNAL_BROWSER_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#external_browser_timeout SnowflakeProvider#external_browser_timeout}
        :param host: Specifies a custom host value used by the driver for privatelink connections. Can also be sourced from the ``SNOWFLAKE_HOST`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#host SnowflakeProvider#host}
        :param include_retry_reason: Should retried request contain retry reason. Can also be sourced from the ``SNOWFLAKE_INCLUDE_RETRY_REASON`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#include_retry_reason SnowflakeProvider#include_retry_reason}
        :param insecure_mode: If true, bypass the Online Certificate Status Protocol (OCSP) certificate revocation check. IMPORTANT: Change the default value for testing or emergency situations only. Can also be sourced from the ``SNOWFLAKE_INSECURE_MODE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#insecure_mode SnowflakeProvider#insecure_mode}
        :param jwt_client_timeout: The timeout in seconds for the JWT client to complete the authentication. Can also be sourced from the ``SNOWFLAKE_JWT_CLIENT_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#jwt_client_timeout SnowflakeProvider#jwt_client_timeout}
        :param jwt_expire_timeout: JWT expire after timeout in seconds. Can also be sourced from the ``SNOWFLAKE_JWT_EXPIRE_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#jwt_expire_timeout SnowflakeProvider#jwt_expire_timeout}
        :param keep_session_alive: Enables the session to persist even after the connection is closed. Can also be sourced from the ``SNOWFLAKE_KEEP_SESSION_ALIVE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#keep_session_alive SnowflakeProvider#keep_session_alive}
        :param login_timeout: Login retry timeout in seconds EXCLUDING network roundtrip and read out http response. Can also be sourced from the ``SNOWFLAKE_LOGIN_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#login_timeout SnowflakeProvider#login_timeout}
        :param max_retry_count: Specifies how many times non-periodic HTTP request can be retried by the driver. Can also be sourced from the ``SNOWFLAKE_MAX_RETRY_COUNT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#max_retry_count SnowflakeProvider#max_retry_count}
        :param ocsp_fail_open: True represents OCSP fail open mode. False represents OCSP fail closed mode. Fail open true by default. Can also be sourced from the ``SNOWFLAKE_OCSP_FAIL_OPEN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#ocsp_fail_open SnowflakeProvider#ocsp_fail_open}
        :param okta_url: The URL of the Okta server. e.g. https://example.okta.com. Okta URL host needs to to have a suffix ``okta.com``. Read more in Snowflake `docs <https://docs.snowflake.com/en/user-guide/oauth-okta>`_. Can also be sourced from the ``SNOWFLAKE_OKTA_URL`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#okta_url SnowflakeProvider#okta_url}
        :param organization_name: Specifies your Snowflake organization name assigned by Snowflake. For information about account identifiers, see the `Snowflake documentation <https://docs.snowflake.com/en/user-guide/admin-account-identifier#organization-name>`_. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_ORGANIZATION_NAME`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#organization_name SnowflakeProvider#organization_name}
        :param params: Sets other connection (i.e. session) parameters. `Parameters <https://docs.snowflake.com/en/sql-reference/parameters>`_. This field can not be set with environmental variables. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#params SnowflakeProvider#params}
        :param passcode: Specifies the passcode provided by Duo when using multi-factor authentication (MFA) for login. Can also be sourced from the ``SNOWFLAKE_PASSCODE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#passcode SnowflakeProvider#passcode}
        :param passcode_in_password: False by default. Set to true if the MFA passcode is embedded to the configured password. Can also be sourced from the ``SNOWFLAKE_PASSCODE_IN_PASSWORD`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#passcode_in_password SnowflakeProvider#passcode_in_password}
        :param password: Password for user + password auth. Cannot be used with ``private_key`` and ``private_key_passphrase``. Can also be sourced from the ``SNOWFLAKE_PASSWORD`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#password SnowflakeProvider#password}
        :param port: Specifies a custom port value used by the driver for privatelink connections. Can also be sourced from the ``SNOWFLAKE_PORT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#port SnowflakeProvider#port}
        :param preview_features_enabled: A list of preview features that are handled by the provider. See `preview features list <https://github.com/Snowflake-Labs/terraform-provider-snowflake/blob/main/v1-preparations/LIST_OF_PREVIEW_FEATURES_FOR_V1.md>`_. Preview features may have breaking changes in future releases, even without raising the major version. This field can not be set with environmental variables. Valid options are: ``snowflake_current_account_datasource`` | ``snowflake_account_authentication_policy_attachment_resource`` | ``snowflake_account_password_policy_attachment_resource`` | ``snowflake_alert_resource`` | ``snowflake_alerts_datasource`` | ``snowflake_api_integration_resource`` | ``snowflake_authentication_policy_resource`` | ``snowflake_cortex_search_service_resource`` | ``snowflake_cortex_search_services_datasource`` | ``snowflake_database_datasource`` | ``snowflake_database_role_datasource`` | ``snowflake_dynamic_table_resource`` | ``snowflake_dynamic_tables_datasource`` | ``snowflake_external_function_resource`` | ``snowflake_external_functions_datasource`` | ``snowflake_external_table_resource`` | ``snowflake_external_tables_datasource`` | ``snowflake_external_volume_resource`` | ``snowflake_failover_group_resource`` | ``snowflake_failover_groups_datasource`` | ``snowflake_file_format_resource`` | ``snowflake_file_formats_datasource`` | ``snowflake_function_java_resource`` | ``snowflake_function_javascript_resource`` | ``snowflake_function_python_resource`` | ``snowflake_function_scala_resource`` | ``snowflake_function_sql_resource`` | ``snowflake_functions_datasource`` | ``snowflake_managed_account_resource`` | ``snowflake_materialized_view_resource`` | ``snowflake_materialized_views_datasource`` | ``snowflake_network_policy_attachment_resource`` | ``snowflake_network_rule_resource`` | ``snowflake_email_notification_integration_resource`` | ``snowflake_notification_integration_resource`` | ``snowflake_object_parameter_resource`` | ``snowflake_password_policy_resource`` | ``snowflake_pipe_resource`` | ``snowflake_pipes_datasource`` | ``snowflake_current_role_datasource`` | ``snowflake_sequence_resource`` | ``snowflake_sequences_datasource`` | ``snowflake_share_resource`` | ``snowflake_shares_datasource`` | ``snowflake_parameters_datasource`` | ``snowflake_procedure_java_resource`` | ``snowflake_procedure_javascript_resource`` | ``snowflake_procedure_python_resource`` | ``snowflake_procedure_scala_resource`` | ``snowflake_procedure_sql_resource`` | ``snowflake_procedures_datasource`` | ``snowflake_stage_resource`` | ``snowflake_stages_datasource`` | ``snowflake_storage_integration_resource`` | ``snowflake_storage_integrations_datasource`` | ``snowflake_system_generate_scim_access_token_datasource`` | ``snowflake_system_get_aws_sns_iam_policy_datasource`` | ``snowflake_system_get_privatelink_config_datasource`` | ``snowflake_system_get_snowflake_platform_info_datasource`` | ``snowflake_table_column_masking_policy_application_resource`` | ``snowflake_table_constraint_resource`` | ``snowflake_table_resource`` | ``snowflake_tables_datasource`` | ``snowflake_user_authentication_policy_attachment_resource`` | ``snowflake_user_public_keys_resource`` | ``snowflake_user_password_policy_attachment_resource``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#preview_features_enabled SnowflakeProvider#preview_features_enabled}
        :param private_key: Private Key for username+private-key auth. Cannot be used with ``password``. Can also be sourced from the ``SNOWFLAKE_PRIVATE_KEY`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#private_key SnowflakeProvider#private_key}
        :param private_key_passphrase: Supports the encryption ciphers aes-128-cbc, aes-128-gcm, aes-192-cbc, aes-192-gcm, aes-256-cbc, aes-256-gcm, and des-ede3-cbc. Can also be sourced from the ``SNOWFLAKE_PRIVATE_KEY_PASSPHRASE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#private_key_passphrase SnowflakeProvider#private_key_passphrase}
        :param profile: Sets the profile to read from ~/.snowflake/config file. Can also be sourced from the ``SNOWFLAKE_PROFILE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#profile SnowflakeProvider#profile}
        :param protocol: A protocol used in the connection. Valid options are: ``http`` | ``https``. Can also be sourced from the ``SNOWFLAKE_PROTOCOL`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#protocol SnowflakeProvider#protocol}
        :param request_timeout: request retry timeout in seconds EXCLUDING network roundtrip and read out http response. Can also be sourced from the ``SNOWFLAKE_REQUEST_TIMEOUT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#request_timeout SnowflakeProvider#request_timeout}
        :param role: Specifies the role to use by default for accessing Snowflake objects in the client session. Can also be sourced from the ``SNOWFLAKE_ROLE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#role SnowflakeProvider#role}
        :param skip_toml_file_permission_verification: True by default. Skips TOML configuration file permission verification. This flag has no effect on Windows systems, as the permissions are not checked on this platform. We recommend setting this to ``false`` and setting the proper privileges - see `the section below <#order-precedence>`_. Can also be sourced from the ``SNOWFLAKE_SKIP_TOML_FILE_PERMISSION_VERIFICATION`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#skip_toml_file_permission_verification SnowflakeProvider#skip_toml_file_permission_verification}
        :param tmp_directory_path: Sets temporary directory used by the driver for operations like encrypting, compressing etc. Can also be sourced from the ``SNOWFLAKE_TMP_DIRECTORY_PATH`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#tmp_directory_path SnowflakeProvider#tmp_directory_path}
        :param token: Token to use for OAuth and other forms of token based auth. Can also be sourced from the ``SNOWFLAKE_TOKEN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#token SnowflakeProvider#token}
        :param token_accessor: token_accessor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#token_accessor SnowflakeProvider#token_accessor}
        :param user: Username. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_USER`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#user SnowflakeProvider#user}
        :param validate_default_parameters: True by default. If false, disables the validation checks for Database, Schema, Warehouse and Role at the time a connection is established. Can also be sourced from the ``SNOWFLAKE_VALIDATE_DEFAULT_PARAMETERS`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#validate_default_parameters SnowflakeProvider#validate_default_parameters}
        :param warehouse: Specifies the virtual warehouse to use by default for queries, loading, etc. in the client session. Can also be sourced from the ``SNOWFLAKE_WAREHOUSE`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#warehouse SnowflakeProvider#warehouse}
        '''
        if isinstance(token_accessor, dict):
            token_accessor = SnowflakeProviderTokenAccessor(**token_accessor)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84bb0483800dda7e061db008e0e400dcb834624a9f09076e86185fce1a232ed)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument authenticator", value=authenticator, expected_type=type_hints["authenticator"])
            check_type(argname="argument client_ip", value=client_ip, expected_type=type_hints["client_ip"])
            check_type(argname="argument client_request_mfa_token", value=client_request_mfa_token, expected_type=type_hints["client_request_mfa_token"])
            check_type(argname="argument client_store_temporary_credential", value=client_store_temporary_credential, expected_type=type_hints["client_store_temporary_credential"])
            check_type(argname="argument client_timeout", value=client_timeout, expected_type=type_hints["client_timeout"])
            check_type(argname="argument disable_console_login", value=disable_console_login, expected_type=type_hints["disable_console_login"])
            check_type(argname="argument disable_query_context_cache", value=disable_query_context_cache, expected_type=type_hints["disable_query_context_cache"])
            check_type(argname="argument disable_telemetry", value=disable_telemetry, expected_type=type_hints["disable_telemetry"])
            check_type(argname="argument driver_tracing", value=driver_tracing, expected_type=type_hints["driver_tracing"])
            check_type(argname="argument external_browser_timeout", value=external_browser_timeout, expected_type=type_hints["external_browser_timeout"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument include_retry_reason", value=include_retry_reason, expected_type=type_hints["include_retry_reason"])
            check_type(argname="argument insecure_mode", value=insecure_mode, expected_type=type_hints["insecure_mode"])
            check_type(argname="argument jwt_client_timeout", value=jwt_client_timeout, expected_type=type_hints["jwt_client_timeout"])
            check_type(argname="argument jwt_expire_timeout", value=jwt_expire_timeout, expected_type=type_hints["jwt_expire_timeout"])
            check_type(argname="argument keep_session_alive", value=keep_session_alive, expected_type=type_hints["keep_session_alive"])
            check_type(argname="argument login_timeout", value=login_timeout, expected_type=type_hints["login_timeout"])
            check_type(argname="argument max_retry_count", value=max_retry_count, expected_type=type_hints["max_retry_count"])
            check_type(argname="argument ocsp_fail_open", value=ocsp_fail_open, expected_type=type_hints["ocsp_fail_open"])
            check_type(argname="argument okta_url", value=okta_url, expected_type=type_hints["okta_url"])
            check_type(argname="argument organization_name", value=organization_name, expected_type=type_hints["organization_name"])
            check_type(argname="argument params", value=params, expected_type=type_hints["params"])
            check_type(argname="argument passcode", value=passcode, expected_type=type_hints["passcode"])
            check_type(argname="argument passcode_in_password", value=passcode_in_password, expected_type=type_hints["passcode_in_password"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preview_features_enabled", value=preview_features_enabled, expected_type=type_hints["preview_features_enabled"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument private_key_passphrase", value=private_key_passphrase, expected_type=type_hints["private_key_passphrase"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument request_timeout", value=request_timeout, expected_type=type_hints["request_timeout"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument skip_toml_file_permission_verification", value=skip_toml_file_permission_verification, expected_type=type_hints["skip_toml_file_permission_verification"])
            check_type(argname="argument tmp_directory_path", value=tmp_directory_path, expected_type=type_hints["tmp_directory_path"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument token_accessor", value=token_accessor, expected_type=type_hints["token_accessor"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument validate_default_parameters", value=validate_default_parameters, expected_type=type_hints["validate_default_parameters"])
            check_type(argname="argument warehouse", value=warehouse, expected_type=type_hints["warehouse"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_name is not None:
            self._values["account_name"] = account_name
        if alias is not None:
            self._values["alias"] = alias
        if authenticator is not None:
            self._values["authenticator"] = authenticator
        if client_ip is not None:
            self._values["client_ip"] = client_ip
        if client_request_mfa_token is not None:
            self._values["client_request_mfa_token"] = client_request_mfa_token
        if client_store_temporary_credential is not None:
            self._values["client_store_temporary_credential"] = client_store_temporary_credential
        if client_timeout is not None:
            self._values["client_timeout"] = client_timeout
        if disable_console_login is not None:
            self._values["disable_console_login"] = disable_console_login
        if disable_query_context_cache is not None:
            self._values["disable_query_context_cache"] = disable_query_context_cache
        if disable_telemetry is not None:
            self._values["disable_telemetry"] = disable_telemetry
        if driver_tracing is not None:
            self._values["driver_tracing"] = driver_tracing
        if external_browser_timeout is not None:
            self._values["external_browser_timeout"] = external_browser_timeout
        if host is not None:
            self._values["host"] = host
        if include_retry_reason is not None:
            self._values["include_retry_reason"] = include_retry_reason
        if insecure_mode is not None:
            self._values["insecure_mode"] = insecure_mode
        if jwt_client_timeout is not None:
            self._values["jwt_client_timeout"] = jwt_client_timeout
        if jwt_expire_timeout is not None:
            self._values["jwt_expire_timeout"] = jwt_expire_timeout
        if keep_session_alive is not None:
            self._values["keep_session_alive"] = keep_session_alive
        if login_timeout is not None:
            self._values["login_timeout"] = login_timeout
        if max_retry_count is not None:
            self._values["max_retry_count"] = max_retry_count
        if ocsp_fail_open is not None:
            self._values["ocsp_fail_open"] = ocsp_fail_open
        if okta_url is not None:
            self._values["okta_url"] = okta_url
        if organization_name is not None:
            self._values["organization_name"] = organization_name
        if params is not None:
            self._values["params"] = params
        if passcode is not None:
            self._values["passcode"] = passcode
        if passcode_in_password is not None:
            self._values["passcode_in_password"] = passcode_in_password
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if preview_features_enabled is not None:
            self._values["preview_features_enabled"] = preview_features_enabled
        if private_key is not None:
            self._values["private_key"] = private_key
        if private_key_passphrase is not None:
            self._values["private_key_passphrase"] = private_key_passphrase
        if profile is not None:
            self._values["profile"] = profile
        if protocol is not None:
            self._values["protocol"] = protocol
        if request_timeout is not None:
            self._values["request_timeout"] = request_timeout
        if role is not None:
            self._values["role"] = role
        if skip_toml_file_permission_verification is not None:
            self._values["skip_toml_file_permission_verification"] = skip_toml_file_permission_verification
        if tmp_directory_path is not None:
            self._values["tmp_directory_path"] = tmp_directory_path
        if token is not None:
            self._values["token"] = token
        if token_accessor is not None:
            self._values["token_accessor"] = token_accessor
        if user is not None:
            self._values["user"] = user
        if validate_default_parameters is not None:
            self._values["validate_default_parameters"] = validate_default_parameters
        if warehouse is not None:
            self._values["warehouse"] = warehouse

    @builtins.property
    def account_name(self) -> typing.Optional[builtins.str]:
        '''Specifies your Snowflake account name assigned by Snowflake.

        For information about account identifiers, see the `Snowflake documentation <https://docs.snowflake.com/en/user-guide/admin-account-identifier#account-name>`_. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_ACCOUNT_NAME`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#account_name SnowflakeProvider#account_name}
        '''
        result = self._values.get("account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#alias SnowflakeProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authenticator(self) -> typing.Optional[builtins.str]:
        '''Specifies the `authentication type <https://pkg.go.dev/github.com/snowflakedb/gosnowflake#AuthType>`_ to use when connecting to Snowflake. Valid options are: ``SNOWFLAKE`` | ``OAUTH`` | ``EXTERNALBROWSER`` | ``OKTA`` | ``SNOWFLAKE_JWT`` | ``TOKENACCESSOR`` | ``USERNAMEPASSWORDMFA``. Can also be sourced from the ``SNOWFLAKE_AUTHENTICATOR`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#authenticator SnowflakeProvider#authenticator}
        '''
        result = self._values.get("authenticator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_ip(self) -> typing.Optional[builtins.str]:
        '''IP address for network checks. Can also be sourced from the ``SNOWFLAKE_CLIENT_IP`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_ip SnowflakeProvider#client_ip}
        '''
        result = self._values.get("client_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_request_mfa_token(self) -> typing.Optional[builtins.str]:
        '''When true the MFA token is cached in the credential manager.

        True by default in Windows/OSX. False for Linux. Can also be sourced from the ``SNOWFLAKE_CLIENT_REQUEST_MFA_TOKEN`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_request_mfa_token SnowflakeProvider#client_request_mfa_token}
        '''
        result = self._values.get("client_request_mfa_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_store_temporary_credential(self) -> typing.Optional[builtins.str]:
        '''When true the ID token is cached in the credential manager.

        True by default in Windows/OSX. False for Linux. Can also be sourced from the ``SNOWFLAKE_CLIENT_STORE_TEMPORARY_CREDENTIAL`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_store_temporary_credential SnowflakeProvider#client_store_temporary_credential}
        '''
        result = self._values.get("client_store_temporary_credential")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout in seconds for the client to complete the authentication.

        Can also be sourced from the ``SNOWFLAKE_CLIENT_TIMEOUT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_timeout SnowflakeProvider#client_timeout}
        '''
        result = self._values.get("client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disable_console_login(self) -> typing.Optional[builtins.str]:
        '''Indicates whether console login should be disabled in the driver. Can also be sourced from the ``SNOWFLAKE_DISABLE_CONSOLE_LOGIN`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_console_login SnowflakeProvider#disable_console_login}
        '''
        result = self._values.get("disable_console_login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_query_context_cache(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables HTAP query context cache in the driver. Can also be sourced from the ``SNOWFLAKE_DISABLE_QUERY_CONTEXT_CACHE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_query_context_cache SnowflakeProvider#disable_query_context_cache}
        '''
        result = self._values.get("disable_query_context_cache")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_telemetry(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables telemetry in the driver. Can also be sourced from the ``DISABLE_TELEMETRY`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#disable_telemetry SnowflakeProvider#disable_telemetry}
        '''
        result = self._values.get("disable_telemetry")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def driver_tracing(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level to be used by the driver.

        Valid options are: ``trace`` | ``debug`` | ``info`` | ``print`` | ``warning`` | ``error`` | ``fatal`` | ``panic``. Can also be sourced from the ``SNOWFLAKE_DRIVER_TRACING`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#driver_tracing SnowflakeProvider#driver_tracing}
        '''
        result = self._values.get("driver_tracing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_browser_timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout in seconds for the external browser to complete the authentication.

        Can also be sourced from the ``SNOWFLAKE_EXTERNAL_BROWSER_TIMEOUT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#external_browser_timeout SnowflakeProvider#external_browser_timeout}
        '''
        result = self._values.get("external_browser_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Specifies a custom host value used by the driver for privatelink connections.

        Can also be sourced from the ``SNOWFLAKE_HOST`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#host SnowflakeProvider#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_retry_reason(self) -> typing.Optional[builtins.str]:
        '''Should retried request contain retry reason. Can also be sourced from the ``SNOWFLAKE_INCLUDE_RETRY_REASON`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#include_retry_reason SnowflakeProvider#include_retry_reason}
        '''
        result = self._values.get("include_retry_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, bypass the Online Certificate Status Protocol (OCSP) certificate revocation check.

        IMPORTANT: Change the default value for testing or emergency situations only. Can also be sourced from the ``SNOWFLAKE_INSECURE_MODE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#insecure_mode SnowflakeProvider#insecure_mode}
        '''
        result = self._values.get("insecure_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jwt_client_timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout in seconds for the JWT client to complete the authentication.

        Can also be sourced from the ``SNOWFLAKE_JWT_CLIENT_TIMEOUT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#jwt_client_timeout SnowflakeProvider#jwt_client_timeout}
        '''
        result = self._values.get("jwt_client_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def jwt_expire_timeout(self) -> typing.Optional[jsii.Number]:
        '''JWT expire after timeout in seconds. Can also be sourced from the ``SNOWFLAKE_JWT_EXPIRE_TIMEOUT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#jwt_expire_timeout SnowflakeProvider#jwt_expire_timeout}
        '''
        result = self._values.get("jwt_expire_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def keep_session_alive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the session to persist even after the connection is closed.

        Can also be sourced from the ``SNOWFLAKE_KEEP_SESSION_ALIVE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#keep_session_alive SnowflakeProvider#keep_session_alive}
        '''
        result = self._values.get("keep_session_alive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def login_timeout(self) -> typing.Optional[jsii.Number]:
        '''Login retry timeout in seconds EXCLUDING network roundtrip and read out http response.

        Can also be sourced from the ``SNOWFLAKE_LOGIN_TIMEOUT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#login_timeout SnowflakeProvider#login_timeout}
        '''
        result = self._values.get("login_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retry_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies how many times non-periodic HTTP request can be retried by the driver.

        Can also be sourced from the ``SNOWFLAKE_MAX_RETRY_COUNT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#max_retry_count SnowflakeProvider#max_retry_count}
        '''
        result = self._values.get("max_retry_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ocsp_fail_open(self) -> typing.Optional[builtins.str]:
        '''True represents OCSP fail open mode.

        False represents OCSP fail closed mode. Fail open true by default. Can also be sourced from the ``SNOWFLAKE_OCSP_FAIL_OPEN`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#ocsp_fail_open SnowflakeProvider#ocsp_fail_open}
        '''
        result = self._values.get("ocsp_fail_open")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def okta_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the Okta server.

        e.g. https://example.okta.com. Okta URL host needs to to have a suffix ``okta.com``. Read more in Snowflake `docs <https://docs.snowflake.com/en/user-guide/oauth-okta>`_. Can also be sourced from the ``SNOWFLAKE_OKTA_URL`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#okta_url SnowflakeProvider#okta_url}
        '''
        result = self._values.get("okta_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_name(self) -> typing.Optional[builtins.str]:
        '''Specifies your Snowflake organization name assigned by Snowflake.

        For information about account identifiers, see the `Snowflake documentation <https://docs.snowflake.com/en/user-guide/admin-account-identifier#organization-name>`_. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_ORGANIZATION_NAME`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#organization_name SnowflakeProvider#organization_name}
        '''
        result = self._values.get("organization_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def params(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sets other connection (i.e. session) parameters. `Parameters <https://docs.snowflake.com/en/sql-reference/parameters>`_. This field can not be set with environmental variables.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#params SnowflakeProvider#params}
        '''
        result = self._values.get("params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def passcode(self) -> typing.Optional[builtins.str]:
        '''Specifies the passcode provided by Duo when using multi-factor authentication (MFA) for login.

        Can also be sourced from the ``SNOWFLAKE_PASSCODE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#passcode SnowflakeProvider#passcode}
        '''
        result = self._values.get("passcode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def passcode_in_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''False by default.

        Set to true if the MFA passcode is embedded to the configured password. Can also be sourced from the ``SNOWFLAKE_PASSCODE_IN_PASSWORD`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#passcode_in_password SnowflakeProvider#passcode_in_password}
        '''
        result = self._values.get("passcode_in_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for user + password auth.

        Cannot be used with ``private_key`` and ``private_key_passphrase``. Can also be sourced from the ``SNOWFLAKE_PASSWORD`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#password SnowflakeProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Specifies a custom port value used by the driver for privatelink connections.

        Can also be sourced from the ``SNOWFLAKE_PORT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#port SnowflakeProvider#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preview_features_enabled(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of preview features that are handled by the provider.

        See `preview features list <https://github.com/Snowflake-Labs/terraform-provider-snowflake/blob/main/v1-preparations/LIST_OF_PREVIEW_FEATURES_FOR_V1.md>`_. Preview features may have breaking changes in future releases, even without raising the major version. This field can not be set with environmental variables. Valid options are: ``snowflake_current_account_datasource`` | ``snowflake_account_authentication_policy_attachment_resource`` | ``snowflake_account_password_policy_attachment_resource`` | ``snowflake_alert_resource`` | ``snowflake_alerts_datasource`` | ``snowflake_api_integration_resource`` | ``snowflake_authentication_policy_resource`` | ``snowflake_cortex_search_service_resource`` | ``snowflake_cortex_search_services_datasource`` | ``snowflake_database_datasource`` | ``snowflake_database_role_datasource`` | ``snowflake_dynamic_table_resource`` | ``snowflake_dynamic_tables_datasource`` | ``snowflake_external_function_resource`` | ``snowflake_external_functions_datasource`` | ``snowflake_external_table_resource`` | ``snowflake_external_tables_datasource`` | ``snowflake_external_volume_resource`` | ``snowflake_failover_group_resource`` | ``snowflake_failover_groups_datasource`` | ``snowflake_file_format_resource`` | ``snowflake_file_formats_datasource`` | ``snowflake_function_java_resource`` | ``snowflake_function_javascript_resource`` | ``snowflake_function_python_resource`` | ``snowflake_function_scala_resource`` | ``snowflake_function_sql_resource`` | ``snowflake_functions_datasource`` | ``snowflake_managed_account_resource`` | ``snowflake_materialized_view_resource`` | ``snowflake_materialized_views_datasource`` | ``snowflake_network_policy_attachment_resource`` | ``snowflake_network_rule_resource`` | ``snowflake_email_notification_integration_resource`` | ``snowflake_notification_integration_resource`` | ``snowflake_object_parameter_resource`` | ``snowflake_password_policy_resource`` | ``snowflake_pipe_resource`` | ``snowflake_pipes_datasource`` | ``snowflake_current_role_datasource`` | ``snowflake_sequence_resource`` | ``snowflake_sequences_datasource`` | ``snowflake_share_resource`` | ``snowflake_shares_datasource`` | ``snowflake_parameters_datasource`` | ``snowflake_procedure_java_resource`` | ``snowflake_procedure_javascript_resource`` | ``snowflake_procedure_python_resource`` | ``snowflake_procedure_scala_resource`` | ``snowflake_procedure_sql_resource`` | ``snowflake_procedures_datasource`` | ``snowflake_stage_resource`` | ``snowflake_stages_datasource`` | ``snowflake_storage_integration_resource`` | ``snowflake_storage_integrations_datasource`` | ``snowflake_system_generate_scim_access_token_datasource`` | ``snowflake_system_get_aws_sns_iam_policy_datasource`` | ``snowflake_system_get_privatelink_config_datasource`` | ``snowflake_system_get_snowflake_platform_info_datasource`` | ``snowflake_table_column_masking_policy_application_resource`` | ``snowflake_table_constraint_resource`` | ``snowflake_table_resource`` | ``snowflake_tables_datasource`` | ``snowflake_user_authentication_policy_attachment_resource`` | ``snowflake_user_public_keys_resource`` | ``snowflake_user_password_policy_attachment_resource``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#preview_features_enabled SnowflakeProvider#preview_features_enabled}
        '''
        result = self._values.get("preview_features_enabled")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''Private Key for username+private-key auth. Cannot be used with ``password``. Can also be sourced from the ``SNOWFLAKE_PRIVATE_KEY`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#private_key SnowflakeProvider#private_key}
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_passphrase(self) -> typing.Optional[builtins.str]:
        '''Supports the encryption ciphers aes-128-cbc, aes-128-gcm, aes-192-cbc, aes-192-gcm, aes-256-cbc, aes-256-gcm, and des-ede3-cbc.

        Can also be sourced from the ``SNOWFLAKE_PRIVATE_KEY_PASSPHRASE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#private_key_passphrase SnowflakeProvider#private_key_passphrase}
        '''
        result = self._values.get("private_key_passphrase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Sets the profile to read from ~/.snowflake/config file. Can also be sourced from the ``SNOWFLAKE_PROFILE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#profile SnowflakeProvider#profile}
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''A protocol used in the connection.

        Valid options are: ``http`` | ``https``. Can also be sourced from the ``SNOWFLAKE_PROTOCOL`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#protocol SnowflakeProvider#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_timeout(self) -> typing.Optional[jsii.Number]:
        '''request retry timeout in seconds EXCLUDING network roundtrip and read out http response.

        Can also be sourced from the ``SNOWFLAKE_REQUEST_TIMEOUT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#request_timeout SnowflakeProvider#request_timeout}
        '''
        result = self._values.get("request_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''Specifies the role to use by default for accessing Snowflake objects in the client session.

        Can also be sourced from the ``SNOWFLAKE_ROLE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#role SnowflakeProvider#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_toml_file_permission_verification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True by default.

        Skips TOML configuration file permission verification. This flag has no effect on Windows systems, as the permissions are not checked on this platform. We recommend setting this to ``false`` and setting the proper privileges - see `the section below <#order-precedence>`_. Can also be sourced from the ``SNOWFLAKE_SKIP_TOML_FILE_PERMISSION_VERIFICATION`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#skip_toml_file_permission_verification SnowflakeProvider#skip_toml_file_permission_verification}
        '''
        result = self._values.get("skip_toml_file_permission_verification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tmp_directory_path(self) -> typing.Optional[builtins.str]:
        '''Sets temporary directory used by the driver for operations like encrypting, compressing etc.

        Can also be sourced from the ``SNOWFLAKE_TMP_DIRECTORY_PATH`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#tmp_directory_path SnowflakeProvider#tmp_directory_path}
        '''
        result = self._values.get("tmp_directory_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Token to use for OAuth and other forms of token based auth.

        Can also be sourced from the ``SNOWFLAKE_TOKEN`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#token SnowflakeProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_accessor(self) -> typing.Optional["SnowflakeProviderTokenAccessor"]:
        '''token_accessor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#token_accessor SnowflakeProvider#token_accessor}
        '''
        result = self._values.get("token_accessor")
        return typing.cast(typing.Optional["SnowflakeProviderTokenAccessor"], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''Username. Required unless using ``profile``. Can also be sourced from the ``SNOWFLAKE_USER`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#user SnowflakeProvider#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_default_parameters(self) -> typing.Optional[builtins.str]:
        '''True by default.

        If false, disables the validation checks for Database, Schema, Warehouse and Role at the time a connection is established. Can also be sourced from the ``SNOWFLAKE_VALIDATE_DEFAULT_PARAMETERS`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#validate_default_parameters SnowflakeProvider#validate_default_parameters}
        '''
        result = self._values.get("validate_default_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warehouse(self) -> typing.Optional[builtins.str]:
        '''Specifies the virtual warehouse to use by default for queries, loading, etc.

        in the client session. Can also be sourced from the ``SNOWFLAKE_WAREHOUSE`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#warehouse SnowflakeProvider#warehouse}
        '''
        result = self._values.get("warehouse")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnowflakeProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.provider.SnowflakeProviderTokenAccessor",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "redirect_uri": "redirectUri",
        "refresh_token": "refreshToken",
        "token_endpoint": "tokenEndpoint",
    },
)
class SnowflakeProviderTokenAccessor:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
        redirect_uri: builtins.str,
        refresh_token: builtins.str,
        token_endpoint: builtins.str,
    ) -> None:
        '''
        :param client_id: The client ID for the OAuth provider when using a refresh token to renew access token. Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_CLIENT_ID`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_id SnowflakeProvider#client_id}
        :param client_secret: The client secret for the OAuth provider when using a refresh token to renew access token. Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_CLIENT_SECRET`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_secret SnowflakeProvider#client_secret}
        :param redirect_uri: The redirect URI for the OAuth provider when using a refresh token to renew access token. Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_REDIRECT_URI`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#redirect_uri SnowflakeProvider#redirect_uri}
        :param refresh_token: The refresh token for the OAuth provider when using a refresh token to renew access token. Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_REFRESH_TOKEN`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#refresh_token SnowflakeProvider#refresh_token}
        :param token_endpoint: The token endpoint for the OAuth provider e.g. https://{yourDomain}/oauth/token when using a refresh token to renew access token. Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_TOKEN_ENDPOINT`` environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#token_endpoint SnowflakeProvider#token_endpoint}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1128816df89d2a749b0e5810c787caadc6cc459628345c3c8a737c1565945960)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
            check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
            check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "refresh_token": refresh_token,
            "token_endpoint": token_endpoint,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID for the OAuth provider when using a refresh token to renew access token.

        Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_CLIENT_ID`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_id SnowflakeProvider#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''The client secret for the OAuth provider when using a refresh token to renew access token.

        Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_CLIENT_SECRET`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#client_secret SnowflakeProvider#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def redirect_uri(self) -> builtins.str:
        '''The redirect URI for the OAuth provider when using a refresh token to renew access token.

        Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_REDIRECT_URI`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#redirect_uri SnowflakeProvider#redirect_uri}
        '''
        result = self._values.get("redirect_uri")
        assert result is not None, "Required property 'redirect_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def refresh_token(self) -> builtins.str:
        '''The refresh token for the OAuth provider when using a refresh token to renew access token.

        Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_REFRESH_TOKEN`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#refresh_token SnowflakeProvider#refresh_token}
        '''
        result = self._values.get("refresh_token")
        assert result is not None, "Required property 'refresh_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        '''The token endpoint for the OAuth provider e.g. https://{yourDomain}/oauth/token when using a refresh token to renew access token. Can also be sourced from the ``SNOWFLAKE_TOKEN_ACCESSOR_TOKEN_ENDPOINT`` environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs#token_endpoint SnowflakeProvider#token_endpoint}
        '''
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnowflakeProviderTokenAccessor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SnowflakeProvider",
    "SnowflakeProviderConfig",
    "SnowflakeProviderTokenAccessor",
]

publication.publish()

def _typecheckingstub__dffb8c16f0bdbd356b60ba75b76332c0fa5872a9b67c09d939ada39e30798782(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_name: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    authenticator: typing.Optional[builtins.str] = None,
    client_ip: typing.Optional[builtins.str] = None,
    client_request_mfa_token: typing.Optional[builtins.str] = None,
    client_store_temporary_credential: typing.Optional[builtins.str] = None,
    client_timeout: typing.Optional[jsii.Number] = None,
    disable_console_login: typing.Optional[builtins.str] = None,
    disable_query_context_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_telemetry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    driver_tracing: typing.Optional[builtins.str] = None,
    external_browser_timeout: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    include_retry_reason: typing.Optional[builtins.str] = None,
    insecure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jwt_client_timeout: typing.Optional[jsii.Number] = None,
    jwt_expire_timeout: typing.Optional[jsii.Number] = None,
    keep_session_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    login_timeout: typing.Optional[jsii.Number] = None,
    max_retry_count: typing.Optional[jsii.Number] = None,
    ocsp_fail_open: typing.Optional[builtins.str] = None,
    okta_url: typing.Optional[builtins.str] = None,
    organization_name: typing.Optional[builtins.str] = None,
    params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    passcode: typing.Optional[builtins.str] = None,
    passcode_in_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    preview_features_enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_key: typing.Optional[builtins.str] = None,
    private_key_passphrase: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    request_timeout: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    skip_toml_file_permission_verification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tmp_directory_path: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    token_accessor: typing.Optional[typing.Union[SnowflakeProviderTokenAccessor, typing.Dict[builtins.str, typing.Any]]] = None,
    user: typing.Optional[builtins.str] = None,
    validate_default_parameters: typing.Optional[builtins.str] = None,
    warehouse: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a3a5ee41e1141e62bec029bdb8709bf3cc38a98cb6c277789fc640ecc924d2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5315d56ee30ee609fed8a7384053e2d89e64d147c3e39d4a64e7ee8f9da71c5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cdc7cd12d304b2eddd5316af316d83f132ecae360404d6176a8e6a997e8dc2e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6d6a40d1a5605a9094439f3d2d1e57d143ffa3c2083b130937df91f19b35b4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370f87780241c7b2653971c27701eed45e4fc0fea1e1c19909bf4822f9a35139(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f642b106f9ead7f93ccfef26461a60434d7ce40769a4318d6de7980d579723d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6586aace401480ef0ce4ab53207770ca079b6a438409c516fcce530b59649f36(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818f5069d0221466e050c5c53b6b1e3eaaac0d5a53109481e4ead46297f0b141(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f30878256d65fb4fbff323db95be390c5bb75dc6485dcce1f99b94352cb2923(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abcf60fa4330b65affc6db33362afcc184ad771a4fafb37665309283f9986ed(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269dfbf8bd7e9687bd9093ed943acb915d1e33d5f2a1d222d2ebe73340152dd5(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e803321f9dec6856addb562eb977c838137e88d82837d8f7697c4ab9a728c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be356c932dd3785d09f2c4a5c787d88fcbbb1846738765a3ac6f6118bf230c45(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25df655b6fdfcfce4cc80d4c7d317296ba4b1b1e6a48e51e051a48b933da7a96(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2721eb9275edb4164b9ec378522a486b2f6dc36b44bd5279ea361763413992c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0b770f66297cf03ca54574462492185fa522c242f96b03b32317dc69d38166(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c2273f5de1a2697d59b298ef8372bd657956bd24ac15953410953c6bc5e48e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e006c8754a599103a5f7c5d6363a2fd8f44dbc569d9882eab0fe73527000b263(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87491bfb7b1ecfe9103c8dddaf7734ff39eb830fb1a351d40dc0f7c1adb4d2b(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e932bf3dd2379e89075f4162cb5bc10d1da873452b7e84361af61777412cd1fc(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36d2e0b2b382201abb6a86d0fe2d7485162112389b92ff28ef96259e1ccffea(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5794c009d8765aa8f769a80e9753aabe08dc725863ff7b18eab0341eed543c64(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2acb8cea3c2b00df9129f4f3b5786e34b302b4fbbe61119d57006a7804f3f1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed43f438fe4a19bb28b8430f1c8bb2fd059736a0f6aed32c603c6be4724cad2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5079b47ba384ea5e3aaafe6322f07c7068ea187e00a883751b397324ec04b6c8(
    value: typing.Optional[typing.Mapping[builtins.str, builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8aeb67752ef65d8786754b2e094e8334d801727dcb831c2a6d6bbbd59c0c6ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d285d39d0d7dfff15a4462be9b03f6e0824d61185275e2de835935b4db1d4d(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4647c5ce21749b9912e9bb483866a4fe9decad7840786080279fac4bf9b9881(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ab59f5493ec686723d4a013bc5f681695f8805e1a21d0e2961ffb9ba96bb2a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12651490b7406e943ebdd65ee6414415ba2a4f63379177d5a569694f8682242b(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174acb5ca0c2f03f2c07759d01042240477d689ab50d9a3e5014d671f7072072(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e45747860bace19eea01fe56764a0071fb76645a7df1767604942c712bc7fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2890938b1cd71ed7815000e422a912b7b3d54903511d4f7b45712b5a30212795(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272d3205644fbaa065eff9f5ac6d27774f4829ae96c327fd974c31e2c14d17ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee0543502fab097af52ebd9c81a19791d58a795a589dead81d2ddb4e53710eab(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c825aa96baa5ca037e135d9294ae15fc9d5395c87a9275884dd82a5edd2ce8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731655dfe45c6700235008005df19215e75be3265c5dc630398af6efc1f8d115(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86326f4f72d6311c173383f98855bddd97933cfde8d7b692da0f5c02423b0a33(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40535fefad35c2491bb2aa60c6522f5cd80fc0876e21c80deb2f684e33cf2380(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b86051ecb7af168b4414164285a52653116c6c1fd66e45e577d5e94b071fe5(
    value: typing.Optional[SnowflakeProviderTokenAccessor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc30eb22eb05f35288fb4961dd14be1e1fe9101084acdde298c42009214db961(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43646ed314e4eea24bb621b967fbe094538e70a124a4c7cc36c518a3834ac02(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d86a20638ec60e4335171ba31cc595ce61cbb7fbb325816de15f3387860facb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84bb0483800dda7e061db008e0e400dcb834624a9f09076e86185fce1a232ed(
    *,
    account_name: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    authenticator: typing.Optional[builtins.str] = None,
    client_ip: typing.Optional[builtins.str] = None,
    client_request_mfa_token: typing.Optional[builtins.str] = None,
    client_store_temporary_credential: typing.Optional[builtins.str] = None,
    client_timeout: typing.Optional[jsii.Number] = None,
    disable_console_login: typing.Optional[builtins.str] = None,
    disable_query_context_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_telemetry: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    driver_tracing: typing.Optional[builtins.str] = None,
    external_browser_timeout: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    include_retry_reason: typing.Optional[builtins.str] = None,
    insecure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jwt_client_timeout: typing.Optional[jsii.Number] = None,
    jwt_expire_timeout: typing.Optional[jsii.Number] = None,
    keep_session_alive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    login_timeout: typing.Optional[jsii.Number] = None,
    max_retry_count: typing.Optional[jsii.Number] = None,
    ocsp_fail_open: typing.Optional[builtins.str] = None,
    okta_url: typing.Optional[builtins.str] = None,
    organization_name: typing.Optional[builtins.str] = None,
    params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    passcode: typing.Optional[builtins.str] = None,
    passcode_in_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    preview_features_enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_key: typing.Optional[builtins.str] = None,
    private_key_passphrase: typing.Optional[builtins.str] = None,
    profile: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    request_timeout: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    skip_toml_file_permission_verification: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tmp_directory_path: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    token_accessor: typing.Optional[typing.Union[SnowflakeProviderTokenAccessor, typing.Dict[builtins.str, typing.Any]]] = None,
    user: typing.Optional[builtins.str] = None,
    validate_default_parameters: typing.Optional[builtins.str] = None,
    warehouse: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1128816df89d2a749b0e5810c787caadc6cc459628345c3c8a737c1565945960(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
    redirect_uri: builtins.str,
    refresh_token: builtins.str,
    token_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
