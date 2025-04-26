r'''
# CDKTF prebuilt bindings for cyrilgdn/postgresql provider version 1.25.0

This repo builds and publishes the [Terraform postgresql provider](https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-postgresql](https://www.npmjs.com/package/@cdktf/provider-postgresql).

`npm install @cdktf/provider-postgresql`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-postgresql](https://pypi.org/project/cdktf-cdktf-provider-postgresql).

`pipenv install cdktf-cdktf-provider-postgresql`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Postgresql](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Postgresql).

`dotnet add package HashiCorp.Cdktf.Providers.Postgresql`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-postgresql](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-postgresql).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-postgresql</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-postgresql-go`](https://github.com/cdktf/cdktf-provider-postgresql-go) package.

`go get github.com/cdktf/cdktf-provider-postgresql-go/postgresql/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-postgresql-go/blob/main/postgresql/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-postgresql).

## Versioning

This project is explicitly not tracking the Terraform postgresql provider version 1:1. In fact, it always tracks `latest` of `~> 1.14` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform postgresql provider](https://registry.terraform.io/providers/cyrilgdn/postgresql/1.25.0)
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
    "data_postgresql_schemas",
    "data_postgresql_sequences",
    "data_postgresql_tables",
    "database",
    "default_privileges",
    "extension",
    "function_resource",
    "grant",
    "grant_role",
    "physical_replication_slot",
    "provider",
    "publication",
    "replication_slot",
    "role",
    "schema",
    "security_label",
    "server",
    "subscription",
    "user_mapping",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import data_postgresql_schemas
from . import data_postgresql_sequences
from . import data_postgresql_tables
from . import database
from . import default_privileges
from . import extension
from . import function_resource
from . import grant
from . import grant_role
from . import physical_replication_slot
from . import provider
from . import publication
from . import replication_slot
from . import role
from . import schema
from . import security_label
from . import server
from . import subscription
from . import user_mapping
