r'''
# CDKTF prebuilt bindings for newrelic/newrelic provider version 3.69.1

This repo builds and publishes the [Terraform newrelic provider](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-newrelic](https://www.npmjs.com/package/@cdktf/provider-newrelic).

`npm install @cdktf/provider-newrelic`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-newrelic](https://pypi.org/project/cdktf-cdktf-provider-newrelic).

`pipenv install cdktf-cdktf-provider-newrelic`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Newrelic](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Newrelic).

`dotnet add package HashiCorp.Cdktf.Providers.Newrelic`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-newrelic](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-newrelic).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-newrelic</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-newrelic-go`](https://github.com/cdktf/cdktf-provider-newrelic-go) package.

`go get github.com/cdktf/cdktf-provider-newrelic-go/newrelic/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-newrelic-go/blob/main/newrelic/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-newrelic).

## Versioning

This project is explicitly not tracking the Terraform newrelic provider version 1:1. In fact, it always tracks `latest` of `~> 3.7` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform newrelic provider](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1)
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
    "account_management",
    "alert_channel",
    "alert_condition",
    "alert_muting_rule",
    "alert_policy",
    "alert_policy_channel",
    "api_access_key",
    "application_settings",
    "browser_application",
    "cloud_aws_govcloud_integrations",
    "cloud_aws_govcloud_link_account",
    "cloud_aws_integrations",
    "cloud_aws_link_account",
    "cloud_azure_integrations",
    "cloud_azure_link_account",
    "cloud_gcp_integrations",
    "cloud_gcp_link_account",
    "data_newrelic_account",
    "data_newrelic_alert_channel",
    "data_newrelic_alert_policy",
    "data_newrelic_application",
    "data_newrelic_authentication_domain",
    "data_newrelic_cloud_account",
    "data_newrelic_entity",
    "data_newrelic_group",
    "data_newrelic_key_transaction",
    "data_newrelic_notification_destination",
    "data_newrelic_obfuscation_expression",
    "data_newrelic_service_level_alert_helper",
    "data_newrelic_synthetics_private_location",
    "data_newrelic_synthetics_secure_credential",
    "data_newrelic_test_grok_pattern",
    "data_newrelic_user",
    "data_partition_rule",
    "entity_tags",
    "events_to_metrics_rule",
    "group",
    "infra_alert_condition",
    "insights_event",
    "key_transaction",
    "log_parsing_rule",
    "monitor_downtime",
    "notification_channel",
    "notification_destination",
    "nrql_alert_condition",
    "nrql_drop_rule",
    "obfuscation_expression",
    "obfuscation_rule",
    "one_dashboard",
    "one_dashboard_json",
    "one_dashboard_raw",
    "pipeline_cloud_rule",
    "provider",
    "service_level",
    "synthetics_alert_condition",
    "synthetics_broken_links_monitor",
    "synthetics_cert_check_monitor",
    "synthetics_monitor",
    "synthetics_multilocation_alert_condition",
    "synthetics_private_location",
    "synthetics_script_monitor",
    "synthetics_secure_credential",
    "synthetics_step_monitor",
    "user",
    "workflow",
    "workload",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import account_management
from . import alert_channel
from . import alert_condition
from . import alert_muting_rule
from . import alert_policy
from . import alert_policy_channel
from . import api_access_key
from . import application_settings
from . import browser_application
from . import cloud_aws_govcloud_integrations
from . import cloud_aws_govcloud_link_account
from . import cloud_aws_integrations
from . import cloud_aws_link_account
from . import cloud_azure_integrations
from . import cloud_azure_link_account
from . import cloud_gcp_integrations
from . import cloud_gcp_link_account
from . import data_newrelic_account
from . import data_newrelic_alert_channel
from . import data_newrelic_alert_policy
from . import data_newrelic_application
from . import data_newrelic_authentication_domain
from . import data_newrelic_cloud_account
from . import data_newrelic_entity
from . import data_newrelic_group
from . import data_newrelic_key_transaction
from . import data_newrelic_notification_destination
from . import data_newrelic_obfuscation_expression
from . import data_newrelic_service_level_alert_helper
from . import data_newrelic_synthetics_private_location
from . import data_newrelic_synthetics_secure_credential
from . import data_newrelic_test_grok_pattern
from . import data_newrelic_user
from . import data_partition_rule
from . import entity_tags
from . import events_to_metrics_rule
from . import group
from . import infra_alert_condition
from . import insights_event
from . import key_transaction
from . import log_parsing_rule
from . import monitor_downtime
from . import notification_channel
from . import notification_destination
from . import nrql_alert_condition
from . import nrql_drop_rule
from . import obfuscation_expression
from . import obfuscation_rule
from . import one_dashboard
from . import one_dashboard_json
from . import one_dashboard_raw
from . import pipeline_cloud_rule
from . import provider
from . import service_level
from . import synthetics_alert_condition
from . import synthetics_broken_links_monitor
from . import synthetics_cert_check_monitor
from . import synthetics_monitor
from . import synthetics_multilocation_alert_condition
from . import synthetics_private_location
from . import synthetics_script_monitor
from . import synthetics_secure_credential
from . import synthetics_step_monitor
from . import user
from . import workflow
from . import workload
