r'''
# CDKTF prebuilt bindings for integrations/github provider version 6.6.0

This repo builds and publishes the [Terraform github provider](https://registry.terraform.io/providers/integrations/github/6.6.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-github](https://www.npmjs.com/package/@cdktf/provider-github).

`npm install @cdktf/provider-github`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-github](https://pypi.org/project/cdktf-cdktf-provider-github).

`pipenv install cdktf-cdktf-provider-github`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Github](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Github).

`dotnet add package HashiCorp.Cdktf.Providers.Github`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-github](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-github).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-github</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-github-go`](https://github.com/cdktf/cdktf-provider-github-go) package.

`go get github.com/cdktf/cdktf-provider-github-go/github/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-github-go/blob/main/github/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-github).

## Versioning

This project is explicitly not tracking the Terraform github provider version 1:1. In fact, it always tracks `latest` of `~> 6.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform github provider](https://registry.terraform.io/providers/integrations/github/6.6.0)
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
    "actions_environment_secret",
    "actions_environment_variable",
    "actions_organization_oidc_subject_claim_customization_template",
    "actions_organization_permissions",
    "actions_organization_secret",
    "actions_organization_secret_repositories",
    "actions_organization_variable",
    "actions_repository_access_level",
    "actions_repository_oidc_subject_claim_customization_template",
    "actions_repository_permissions",
    "actions_runner_group",
    "actions_secret",
    "actions_variable",
    "app_installation_repositories",
    "app_installation_repository",
    "branch",
    "branch_default",
    "branch_protection",
    "branch_protection_v3",
    "codespaces_organization_secret",
    "codespaces_organization_secret_repositories",
    "codespaces_secret",
    "codespaces_user_secret",
    "data_github_actions_environment_secrets",
    "data_github_actions_environment_variables",
    "data_github_actions_organization_oidc_subject_claim_customization_template",
    "data_github_actions_organization_public_key",
    "data_github_actions_organization_registration_token",
    "data_github_actions_organization_secrets",
    "data_github_actions_organization_variables",
    "data_github_actions_public_key",
    "data_github_actions_registration_token",
    "data_github_actions_repository_oidc_subject_claim_customization_template",
    "data_github_actions_secrets",
    "data_github_actions_variables",
    "data_github_app",
    "data_github_app_token",
    "data_github_branch",
    "data_github_branch_protection_rules",
    "data_github_codespaces_organization_public_key",
    "data_github_codespaces_organization_secrets",
    "data_github_codespaces_public_key",
    "data_github_codespaces_secrets",
    "data_github_codespaces_user_public_key",
    "data_github_codespaces_user_secrets",
    "data_github_collaborators",
    "data_github_dependabot_organization_public_key",
    "data_github_dependabot_organization_secrets",
    "data_github_dependabot_public_key",
    "data_github_dependabot_secrets",
    "data_github_enterprise",
    "data_github_external_groups",
    "data_github_ip_ranges",
    "data_github_issue_labels",
    "data_github_membership",
    "data_github_organization",
    "data_github_organization_custom_role",
    "data_github_organization_external_identities",
    "data_github_organization_ip_allow_list",
    "data_github_organization_team_sync_groups",
    "data_github_organization_teams",
    "data_github_organization_webhooks",
    "data_github_ref",
    "data_github_release",
    "data_github_repositories",
    "data_github_repository",
    "data_github_repository_autolink_references",
    "data_github_repository_branches",
    "data_github_repository_custom_properties",
    "data_github_repository_deploy_keys",
    "data_github_repository_deployment_branch_policies",
    "data_github_repository_environments",
    "data_github_repository_file",
    "data_github_repository_milestone",
    "data_github_repository_pull_request",
    "data_github_repository_pull_requests",
    "data_github_repository_teams",
    "data_github_repository_webhooks",
    "data_github_rest_api",
    "data_github_ssh_keys",
    "data_github_team",
    "data_github_tree",
    "data_github_user",
    "data_github_user_external_identity",
    "data_github_users",
    "dependabot_organization_secret",
    "dependabot_organization_secret_repositories",
    "dependabot_secret",
    "emu_group_mapping",
    "enterprise_actions_permissions",
    "enterprise_actions_runner_group",
    "enterprise_organization",
    "issue",
    "issue_label",
    "issue_labels",
    "membership",
    "organization_block",
    "organization_custom_role",
    "organization_project",
    "organization_ruleset",
    "organization_security_manager",
    "organization_settings",
    "organization_webhook",
    "project_card",
    "project_column",
    "provider",
    "release",
    "repository",
    "repository_autolink_reference",
    "repository_collaborator",
    "repository_collaborators",
    "repository_custom_property",
    "repository_dependabot_security_updates",
    "repository_deploy_key",
    "repository_deployment_branch_policy",
    "repository_environment",
    "repository_environment_deployment_policy",
    "repository_file",
    "repository_milestone",
    "repository_project",
    "repository_pull_request",
    "repository_ruleset",
    "repository_topics",
    "repository_webhook",
    "team",
    "team_members",
    "team_membership",
    "team_repository",
    "team_settings",
    "team_sync_group_mapping",
    "user_gpg_key",
    "user_invitation_accepter",
    "user_ssh_key",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import actions_environment_secret
from . import actions_environment_variable
from . import actions_organization_oidc_subject_claim_customization_template
from . import actions_organization_permissions
from . import actions_organization_secret
from . import actions_organization_secret_repositories
from . import actions_organization_variable
from . import actions_repository_access_level
from . import actions_repository_oidc_subject_claim_customization_template
from . import actions_repository_permissions
from . import actions_runner_group
from . import actions_secret
from . import actions_variable
from . import app_installation_repositories
from . import app_installation_repository
from . import branch
from . import branch_default
from . import branch_protection
from . import branch_protection_v3
from . import codespaces_organization_secret
from . import codespaces_organization_secret_repositories
from . import codespaces_secret
from . import codespaces_user_secret
from . import data_github_actions_environment_secrets
from . import data_github_actions_environment_variables
from . import data_github_actions_organization_oidc_subject_claim_customization_template
from . import data_github_actions_organization_public_key
from . import data_github_actions_organization_registration_token
from . import data_github_actions_organization_secrets
from . import data_github_actions_organization_variables
from . import data_github_actions_public_key
from . import data_github_actions_registration_token
from . import data_github_actions_repository_oidc_subject_claim_customization_template
from . import data_github_actions_secrets
from . import data_github_actions_variables
from . import data_github_app
from . import data_github_app_token
from . import data_github_branch
from . import data_github_branch_protection_rules
from . import data_github_codespaces_organization_public_key
from . import data_github_codespaces_organization_secrets
from . import data_github_codespaces_public_key
from . import data_github_codespaces_secrets
from . import data_github_codespaces_user_public_key
from . import data_github_codespaces_user_secrets
from . import data_github_collaborators
from . import data_github_dependabot_organization_public_key
from . import data_github_dependabot_organization_secrets
from . import data_github_dependabot_public_key
from . import data_github_dependabot_secrets
from . import data_github_enterprise
from . import data_github_external_groups
from . import data_github_ip_ranges
from . import data_github_issue_labels
from . import data_github_membership
from . import data_github_organization
from . import data_github_organization_custom_role
from . import data_github_organization_external_identities
from . import data_github_organization_ip_allow_list
from . import data_github_organization_team_sync_groups
from . import data_github_organization_teams
from . import data_github_organization_webhooks
from . import data_github_ref
from . import data_github_release
from . import data_github_repositories
from . import data_github_repository
from . import data_github_repository_autolink_references
from . import data_github_repository_branches
from . import data_github_repository_custom_properties
from . import data_github_repository_deploy_keys
from . import data_github_repository_deployment_branch_policies
from . import data_github_repository_environments
from . import data_github_repository_file
from . import data_github_repository_milestone
from . import data_github_repository_pull_request
from . import data_github_repository_pull_requests
from . import data_github_repository_teams
from . import data_github_repository_webhooks
from . import data_github_rest_api
from . import data_github_ssh_keys
from . import data_github_team
from . import data_github_tree
from . import data_github_user
from . import data_github_user_external_identity
from . import data_github_users
from . import dependabot_organization_secret
from . import dependabot_organization_secret_repositories
from . import dependabot_secret
from . import emu_group_mapping
from . import enterprise_actions_permissions
from . import enterprise_actions_runner_group
from . import enterprise_organization
from . import issue
from . import issue_label
from . import issue_labels
from . import membership
from . import organization_block
from . import organization_custom_role
from . import organization_project
from . import organization_ruleset
from . import organization_security_manager
from . import organization_settings
from . import organization_webhook
from . import project_card
from . import project_column
from . import provider
from . import release
from . import repository
from . import repository_autolink_reference
from . import repository_collaborator
from . import repository_collaborators
from . import repository_custom_property
from . import repository_dependabot_security_updates
from . import repository_deploy_key
from . import repository_deployment_branch_policy
from . import repository_environment
from . import repository_environment_deployment_policy
from . import repository_file
from . import repository_milestone
from . import repository_project
from . import repository_pull_request
from . import repository_ruleset
from . import repository_topics
from . import repository_webhook
from . import team
from . import team_members
from . import team_membership
from . import team_repository
from . import team_settings
from . import team_sync_group_mapping
from . import user_gpg_key
from . import user_invitation_accepter
from . import user_ssh_key
