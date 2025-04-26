r'''
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![GitHub](https://img.shields.io/github/license/pepperize/cdk-apigateway-swagger-ui?style=flat-square)](https://github.com/pepperize/cdk-apigateway-swagger-ui/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@pepperize/cdk-apigateway-swagger-ui?style=flat-square)](https://www.npmjs.com/package/@pepperize/cdk-apigateway-swagger-ui)
[![PyPI](https://img.shields.io/pypi/v/pepperize.cdk-apigateway-swagger-ui?style=flat-square)](https://pypi.org/project/pepperize.cdk-apigateway-swagger-ui/)
[![Nuget](https://img.shields.io/nuget/v/Pepperize.CDK.ApigatewaySwaggerUi?style=flat-square)](https://www.nuget.org/packages/Pepperize.CDK.ApigatewaySwaggerUi/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.pepperize/cdk-apigateway-swagger-ui?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/pepperize/cdk-apigateway-swagger-ui/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/pepperize/cdk-apigateway-swagger-ui/release.yml?branch=main&label=release&style=flat-square)](https://github.com/pepperize/cdk-apigateway-swagger-ui/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/pepperize/cdk-apigateway-swagger-ui?sort=semver&style=flat-square)](https://github.com/pepperize/cdk-apigateway-swagger-ui/releases)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod&style=flat-square)](https://gitpod.io/#https://github.com/pepperize/cdk-apigateway-swagger-ui)

# CDK Apigateway SwaggerUI

Add SwaggerUI to your AWS Apigateway RestApi

![SwaggerUI Example](./images/swagger-ui-example.png)

## Install

### TypeScript

```shell
npm install @pepperize/cdk-apigateway-swagger-ui
```

or

```shell
yarn add @pepperize/cdk-apigateway-swagger-ui
```

### Python

```shell
pip install pepperize.cdk-apigateway-swagger-ui
```

### C# / .Net

```
dotnet add package Pepperize.CDK.ApigatewaySwaggerUi
```

### Java

```xml
<dependency>
  <groupId>com.pepperize</groupId>
  <artifactId>cdk-apigateway-swagger-ui</artifactId>
  <version>${cdkApigatewaySwaggerUi.version}</version>
</dependency>
```

## Usage

```python
import { Stack } from "aws-cdk-lib";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import { SwaggerUi } from "@pepperize/cdk-apigateway-swagger-ui";

const stack = new Stack();
const restApi = new apigateway.RestApi();

new SwaggerUi(stack, "SwaggerUI", { resource: restApi.root });
```

* Open your SwaggerUI: `https://<rest api id>.execute-api.<aws region>.amazonaws.com/<stage>/api-docs/swagger-ui.html`
* View your API docs: `https://<rest api id>.execute-api.<aws region>.amazonaws.com/<stage>/api-docs.json`
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

import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import constructs as _constructs_77d1e7e8


class SwaggerUi(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-apigateway-swagger-ui.SwaggerUi",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        resource: _aws_cdk_aws_apigateway_ceddda9d.IResource,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param resource: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01fc8d9e0f4362f8d3a52b21d10e71d1727720933ffd63ddf4da3316201a6c0d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SwaggerUiProps(resource=resource)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@pepperize/cdk-apigateway-swagger-ui.SwaggerUiProps",
    jsii_struct_bases=[],
    name_mapping={"resource": "resource"},
)
class SwaggerUiProps:
    def __init__(self, *, resource: _aws_cdk_aws_apigateway_ceddda9d.IResource) -> None:
        '''
        :param resource: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff009f16e03bb7a385c5165fe2cb9df68b952728b4366f05e6124282bc7d483f)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource": resource,
        }

    @builtins.property
    def resource(self) -> _aws_cdk_aws_apigateway_ceddda9d.IResource:
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.IResource, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SwaggerUiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SwaggerUi",
    "SwaggerUiProps",
]

publication.publish()

def _typecheckingstub__01fc8d9e0f4362f8d3a52b21d10e71d1727720933ffd63ddf4da3316201a6c0d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    resource: _aws_cdk_aws_apigateway_ceddda9d.IResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff009f16e03bb7a385c5165fe2cb9df68b952728b4366f05e6124282bc7d483f(
    *,
    resource: _aws_cdk_aws_apigateway_ceddda9d.IResource,
) -> None:
    """Type checking stubs"""
    pass
