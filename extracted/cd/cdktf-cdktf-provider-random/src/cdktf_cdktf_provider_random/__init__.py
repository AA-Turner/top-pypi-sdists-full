r'''
# CDKTF prebuilt bindings for hashicorp/random provider version 3.7.2

HashiCorp made the decision to stop publishing new versions of prebuilt [Terraform random provider](https://registry.terraform.io/providers/hashicorp/random/3.7.2) bindings for [CDK for Terraform](https://cdk.tf) on December 10, 2025. As such, this repository has been archived and is no longer supported in any way by HashiCorp. Previously-published versions of this prebuilt provider will still continue to be available on their respective package managers (e.g. npm, PyPi, Maven, NuGet), but these will not be compatible with new releases of `cdktf` past `0.21.0` and are no longer eligible for commercial support.

As a reminder, you can continue to use the `hashicorp/random` provider in your CDK for Terraform (CDKTF) projects, even with newer versions of CDKTF, but you will need to generate the bindings locally. The easiest way to do so is to use the [`provider add` command](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands#provider-add), optionally with the `--force-local` flag enabled:

`cdktf provider add hashicorp/random --force-local`

For more information and additional examples, check out our documentation on [generating provider bindings manually](https://cdk.tf/imports).

## Deprecated Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-random](https://www.npmjs.com/package/@cdktf/provider-random).

`npm install @cdktf/provider-random`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-random](https://pypi.org/project/cdktf-cdktf-provider-random).

`pipenv install cdktf-cdktf-provider-random`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Random](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Random).

`dotnet add package HashiCorp.Cdktf.Providers.Random`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-random](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-random).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-random</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-random-go`](https://github.com/cdktf/cdktf-provider-random-go) package.

`go get github.com/cdktf/cdktf-provider-random-go/random/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-random-go/blob/main/random/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-random).
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
    "bytes",
    "id",
    "integer",
    "password",
    "pet",
    "provider",
    "shuffle",
    "string_resource",
    "uuid",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import bytes
from . import id
from . import integer
from . import password
from . import pet
from . import provider
from . import shuffle
from . import string_resource
from . import uuid
