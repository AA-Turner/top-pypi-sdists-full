r'''
# CDKTF prebuilt bindings for kreuzwerker/docker provider version 3.4.0

This repo builds and publishes the [Terraform docker provider](https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-docker](https://www.npmjs.com/package/@cdktf/provider-docker).

`npm install @cdktf/provider-docker`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-docker](https://pypi.org/project/cdktf-cdktf-provider-docker).

`pipenv install cdktf-cdktf-provider-docker`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Docker](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Docker).

`dotnet add package HashiCorp.Cdktf.Providers.Docker`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-docker](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-docker).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-docker</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-docker-go`](https://github.com/cdktf/cdktf-provider-docker-go) package.

`go get github.com/cdktf/cdktf-provider-docker-go/docker/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-docker-go/blob/main/docker/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-docker).

## Versioning

This project is explicitly not tracking the Terraform docker provider version 1:1. In fact, it always tracks `latest` of `~> 3.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform docker provider](https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0)
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
    "config",
    "container",
    "data_docker_image",
    "data_docker_logs",
    "data_docker_network",
    "data_docker_plugin",
    "data_docker_registry_image",
    "image",
    "network",
    "plugin",
    "provider",
    "registry_image",
    "secret",
    "service",
    "tag",
    "volume",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import config
from . import container
from . import data_docker_image
from . import data_docker_logs
from . import data_docker_network
from . import data_docker_plugin
from . import data_docker_registry_image
from . import image
from . import network
from . import plugin
from . import provider
from . import registry_image
from . import secret
from . import service
from . import tag
from . import volume
