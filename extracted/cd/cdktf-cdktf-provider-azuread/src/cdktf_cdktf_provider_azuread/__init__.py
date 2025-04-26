r'''
# CDKTF prebuilt bindings for hashicorp/azuread provider version 3.3.0

This repo builds and publishes the [Terraform azuread provider](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-azuread](https://www.npmjs.com/package/@cdktf/provider-azuread).

`npm install @cdktf/provider-azuread`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-azuread](https://pypi.org/project/cdktf-cdktf-provider-azuread).

`pipenv install cdktf-cdktf-provider-azuread`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Azuread](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Azuread).

`dotnet add package HashiCorp.Cdktf.Providers.Azuread`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-azuread](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-azuread).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-azuread</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-azuread-go`](https://github.com/cdktf/cdktf-provider-azuread-go) package.

`go get github.com/cdktf/cdktf-provider-azuread-go/azuread/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-azuread-go/blob/main/azuread/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-azuread).

## Versioning

This project is explicitly not tracking the Terraform azuread provider version 1:1. In fact, it always tracks `latest` of `~> 3.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform azuread provider](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0)
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
    "access_package",
    "access_package_assignment_policy",
    "access_package_catalog",
    "access_package_catalog_role_assignment",
    "access_package_resource_catalog_association",
    "access_package_resource_package_association",
    "administrative_unit",
    "administrative_unit_member",
    "administrative_unit_role_member",
    "app_role_assignment",
    "application",
    "application_api_access",
    "application_app_role",
    "application_certificate",
    "application_fallback_public_client",
    "application_federated_identity_credential",
    "application_from_template",
    "application_identifier_uri",
    "application_known_clients",
    "application_optional_claims",
    "application_owner",
    "application_password",
    "application_permission_scope",
    "application_pre_authorized",
    "application_redirect_uris",
    "application_registration",
    "authentication_strength_policy",
    "claims_mapping_policy",
    "conditional_access_policy",
    "custom_directory_role",
    "data_azuread_access_package",
    "data_azuread_access_package_catalog",
    "data_azuread_access_package_catalog_role",
    "data_azuread_administrative_unit",
    "data_azuread_application",
    "data_azuread_application_published_app_ids",
    "data_azuread_application_template",
    "data_azuread_client_config",
    "data_azuread_directory_object",
    "data_azuread_directory_role_templates",
    "data_azuread_directory_roles",
    "data_azuread_domains",
    "data_azuread_group",
    "data_azuread_group_role_management_policy",
    "data_azuread_groups",
    "data_azuread_named_location",
    "data_azuread_service_principal",
    "data_azuread_service_principals",
    "data_azuread_user",
    "data_azuread_users",
    "directory_role",
    "directory_role_assignment",
    "directory_role_eligibility_schedule_request",
    "directory_role_member",
    "group",
    "group_member",
    "group_role_management_policy",
    "group_without_members",
    "invitation",
    "named_location",
    "privileged_access_group_assignment_schedule",
    "privileged_access_group_eligibility_schedule",
    "provider",
    "service_principal",
    "service_principal_certificate",
    "service_principal_claims_mapping_policy_assignment",
    "service_principal_delegated_permission_grant",
    "service_principal_password",
    "service_principal_token_signing_certificate",
    "synchronization_job",
    "synchronization_job_provision_on_demand",
    "synchronization_secret",
    "user",
    "user_flow_attribute",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import access_package
from . import access_package_assignment_policy
from . import access_package_catalog
from . import access_package_catalog_role_assignment
from . import access_package_resource_catalog_association
from . import access_package_resource_package_association
from . import administrative_unit
from . import administrative_unit_member
from . import administrative_unit_role_member
from . import app_role_assignment
from . import application
from . import application_api_access
from . import application_app_role
from . import application_certificate
from . import application_fallback_public_client
from . import application_federated_identity_credential
from . import application_from_template
from . import application_identifier_uri
from . import application_known_clients
from . import application_optional_claims
from . import application_owner
from . import application_password
from . import application_permission_scope
from . import application_pre_authorized
from . import application_redirect_uris
from . import application_registration
from . import authentication_strength_policy
from . import claims_mapping_policy
from . import conditional_access_policy
from . import custom_directory_role
from . import data_azuread_access_package
from . import data_azuread_access_package_catalog
from . import data_azuread_access_package_catalog_role
from . import data_azuread_administrative_unit
from . import data_azuread_application
from . import data_azuread_application_published_app_ids
from . import data_azuread_application_template
from . import data_azuread_client_config
from . import data_azuread_directory_object
from . import data_azuread_directory_role_templates
from . import data_azuread_directory_roles
from . import data_azuread_domains
from . import data_azuread_group
from . import data_azuread_group_role_management_policy
from . import data_azuread_groups
from . import data_azuread_named_location
from . import data_azuread_service_principal
from . import data_azuread_service_principals
from . import data_azuread_user
from . import data_azuread_users
from . import directory_role
from . import directory_role_assignment
from . import directory_role_eligibility_schedule_request
from . import directory_role_member
from . import group
from . import group_member
from . import group_role_management_policy
from . import group_without_members
from . import invitation
from . import named_location
from . import privileged_access_group_assignment_schedule
from . import privileged_access_group_eligibility_schedule
from . import provider
from . import service_principal
from . import service_principal_certificate
from . import service_principal_claims_mapping_policy_assignment
from . import service_principal_delegated_permission_grant
from . import service_principal_password
from . import service_principal_token_signing_certificate
from . import synchronization_job
from . import synchronization_job_provision_on_demand
from . import synchronization_secret
from . import user
from . import user_flow_attribute
