r'''
# CDKTF prebuilt bindings for Snowflake-Labs/snowflake provider version 1.0.5

This repo builds and publishes the [Terraform snowflake provider](https://registry.terraform.io/providers/Snowflake-Labs/snowflake/1.0.5/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-snowflake](https://www.npmjs.com/package/@cdktf/provider-snowflake).

`npm install @cdktf/provider-snowflake`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-snowflake](https://pypi.org/project/cdktf-cdktf-provider-snowflake).

`pipenv install cdktf-cdktf-provider-snowflake`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Snowflake](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Snowflake).

`dotnet add package HashiCorp.Cdktf.Providers.Snowflake`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-snowflake](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-snowflake).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-snowflake</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-snowflake-go`](https://github.com/cdktf/cdktf-provider-snowflake-go) package.

`go get github.com/cdktf/cdktf-provider-snowflake-go/snowflake/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-snowflake-go/blob/main/snowflake/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-snowflake).

## Versioning

This project is explicitly not tracking the Terraform snowflake provider version 1:1. In fact, it always tracks `latest` of ` ~> 1.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform snowflake provider](https://registry.terraform.io/providers/Snowflake-Labs/snowflake/1.0.5)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
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

from ._jsii import *

__all__ = [
    "account",
    "account_authentication_policy_attachment",
    "account_parameter",
    "account_password_policy_attachment",
    "account_role",
    "alert",
    "api_authentication_integration_with_authorization_code_grant",
    "api_authentication_integration_with_client_credentials",
    "api_authentication_integration_with_jwt_bearer",
    "api_integration",
    "authentication_policy",
    "cortex_search_service",
    "data_snowflake_account_roles",
    "data_snowflake_accounts",
    "data_snowflake_alerts",
    "data_snowflake_connections",
    "data_snowflake_cortex_search_services",
    "data_snowflake_current_account",
    "data_snowflake_current_role",
    "data_snowflake_database",
    "data_snowflake_database_role",
    "data_snowflake_database_roles",
    "data_snowflake_databases",
    "data_snowflake_dynamic_tables",
    "data_snowflake_external_functions",
    "data_snowflake_external_tables",
    "data_snowflake_failover_groups",
    "data_snowflake_file_formats",
    "data_snowflake_functions",
    "data_snowflake_grants",
    "data_snowflake_masking_policies",
    "data_snowflake_materialized_views",
    "data_snowflake_network_policies",
    "data_snowflake_parameters",
    "data_snowflake_pipes",
    "data_snowflake_procedures",
    "data_snowflake_resource_monitors",
    "data_snowflake_row_access_policies",
    "data_snowflake_schemas",
    "data_snowflake_secrets",
    "data_snowflake_security_integrations",
    "data_snowflake_sequences",
    "data_snowflake_shares",
    "data_snowflake_stages",
    "data_snowflake_storage_integrations",
    "data_snowflake_streamlits",
    "data_snowflake_streams",
    "data_snowflake_system_generate_scim_access_token",
    "data_snowflake_system_get_aws_sns_iam_policy",
    "data_snowflake_system_get_privatelink_config",
    "data_snowflake_system_get_snowflake_platform_info",
    "data_snowflake_tables",
    "data_snowflake_tags",
    "data_snowflake_tasks",
    "data_snowflake_users",
    "data_snowflake_views",
    "data_snowflake_warehouses",
    "database",
    "database_role",
    "dynamic_table",
    "email_notification_integration",
    "execute",
    "external_function",
    "external_oauth_integration",
    "external_table",
    "external_volume",
    "failover_group",
    "file_format",
    "function_java",
    "function_javascript",
    "function_python",
    "function_scala",
    "function_sql",
    "grant_account_role",
    "grant_application_role",
    "grant_database_role",
    "grant_ownership",
    "grant_privileges_to_account_role",
    "grant_privileges_to_database_role",
    "grant_privileges_to_share",
    "legacy_service_user",
    "managed_account",
    "masking_policy",
    "materialized_view",
    "network_policy",
    "network_policy_attachment",
    "network_rule",
    "notification_integration",
    "oauth_integration_for_custom_clients",
    "oauth_integration_for_partner_applications",
    "object_parameter",
    "password_policy",
    "pipe",
    "primary_connection",
    "procedure_java",
    "procedure_javascript",
    "procedure_python",
    "procedure_scala",
    "procedure_sql",
    "provider",
    "resource_monitor",
    "row_access_policy",
    "saml2_integration",
    "schema",
    "scim_integration",
    "secondary_connection",
    "secondary_database",
    "secret_with_authorization_code_grant",
    "secret_with_basic_authentication",
    "secret_with_client_credentials",
    "secret_with_generic_string",
    "sequence",
    "service_user",
    "share",
    "shared_database",
    "stage",
    "storage_integration",
    "stream_on_directory_table",
    "stream_on_external_table",
    "stream_on_table",
    "stream_on_view",
    "streamlit",
    "table",
    "table_column_masking_policy_application",
    "table_constraint",
    "tag",
    "tag_association",
    "task",
    "user",
    "user_authentication_policy_attachment",
    "user_password_policy_attachment",
    "user_public_keys",
    "view",
    "warehouse",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import account
from . import account_authentication_policy_attachment
from . import account_parameter
from . import account_password_policy_attachment
from . import account_role
from . import alert
from . import api_authentication_integration_with_authorization_code_grant
from . import api_authentication_integration_with_client_credentials
from . import api_authentication_integration_with_jwt_bearer
from . import api_integration
from . import authentication_policy
from . import cortex_search_service
from . import data_snowflake_account_roles
from . import data_snowflake_accounts
from . import data_snowflake_alerts
from . import data_snowflake_connections
from . import data_snowflake_cortex_search_services
from . import data_snowflake_current_account
from . import data_snowflake_current_role
from . import data_snowflake_database
from . import data_snowflake_database_role
from . import data_snowflake_database_roles
from . import data_snowflake_databases
from . import data_snowflake_dynamic_tables
from . import data_snowflake_external_functions
from . import data_snowflake_external_tables
from . import data_snowflake_failover_groups
from . import data_snowflake_file_formats
from . import data_snowflake_functions
from . import data_snowflake_grants
from . import data_snowflake_masking_policies
from . import data_snowflake_materialized_views
from . import data_snowflake_network_policies
from . import data_snowflake_parameters
from . import data_snowflake_pipes
from . import data_snowflake_procedures
from . import data_snowflake_resource_monitors
from . import data_snowflake_row_access_policies
from . import data_snowflake_schemas
from . import data_snowflake_secrets
from . import data_snowflake_security_integrations
from . import data_snowflake_sequences
from . import data_snowflake_shares
from . import data_snowflake_stages
from . import data_snowflake_storage_integrations
from . import data_snowflake_streamlits
from . import data_snowflake_streams
from . import data_snowflake_system_generate_scim_access_token
from . import data_snowflake_system_get_aws_sns_iam_policy
from . import data_snowflake_system_get_privatelink_config
from . import data_snowflake_system_get_snowflake_platform_info
from . import data_snowflake_tables
from . import data_snowflake_tags
from . import data_snowflake_tasks
from . import data_snowflake_users
from . import data_snowflake_views
from . import data_snowflake_warehouses
from . import database
from . import database_role
from . import dynamic_table
from . import email_notification_integration
from . import execute
from . import external_function
from . import external_oauth_integration
from . import external_table
from . import external_volume
from . import failover_group
from . import file_format
from . import function_java
from . import function_javascript
from . import function_python
from . import function_scala
from . import function_sql
from . import grant_account_role
from . import grant_application_role
from . import grant_database_role
from . import grant_ownership
from . import grant_privileges_to_account_role
from . import grant_privileges_to_database_role
from . import grant_privileges_to_share
from . import legacy_service_user
from . import managed_account
from . import masking_policy
from . import materialized_view
from . import network_policy
from . import network_policy_attachment
from . import network_rule
from . import notification_integration
from . import oauth_integration_for_custom_clients
from . import oauth_integration_for_partner_applications
from . import object_parameter
from . import password_policy
from . import pipe
from . import primary_connection
from . import procedure_java
from . import procedure_javascript
from . import procedure_python
from . import procedure_scala
from . import procedure_sql
from . import provider
from . import resource_monitor
from . import row_access_policy
from . import saml2_integration
from . import schema
from . import scim_integration
from . import secondary_connection
from . import secondary_database
from . import secret_with_authorization_code_grant
from . import secret_with_basic_authentication
from . import secret_with_client_credentials
from . import secret_with_generic_string
from . import sequence
from . import service_user
from . import share
from . import shared_database
from . import stage
from . import storage_integration
from . import stream_on_directory_table
from . import stream_on_external_table
from . import stream_on_table
from . import stream_on_view
from . import streamlit
from . import table
from . import table_column_masking_policy_application
from . import table_constraint
from . import tag
from . import tag_association
from . import task
from . import user
from . import user_authentication_policy_attachment
from . import user_password_policy_attachment
from . import user_public_keys
from . import view
from . import warehouse
