r'''
# AWS Lambda Layer with curl

[![NPM version](https://badge.fury.io/js/cdk-lambda-layer-curl.svg)](https://badge.fury.io/js/cdk-lambda-layer-curl)
[![PyPI version](https://badge.fury.io/py/cdk-lambda-layer-curl.svg)](https://badge.fury.io/py/cdk-lambda-layer-curl)
![Release](https://github.com/clarencetw/cdk-lambda-layer-curl/workflows/release/badge.svg)
[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/clarencetw/cdk-lambda-layer-curl)

Usage:

```python
// CurlLayer bundles the curl in a lambda layer
import { CurlLayer } from 'cdk-lambda-layer-curl';

declare const fn: lambda.Function;
fn.addLayers(new CurlLayer(this, 'CurlLayer'));
```

```python
import { CurlLayer } from 'cdk-lambda-layer-curl'
import * as lambda from 'aws-cdk-lib/aws-lambda'

new lambda.Function(this, 'MyLambda', {
  code: lambda.Code.fromAsset(path.join(__dirname, 'my-lambda-handler')),
  handler: 'index.main',
  runtime: lambda.Runtime.PYTHON_3_9,
  layers: [new CurlLayer(this, 'CurlLayer')]
});
```
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

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class CurlLayer(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-layer-curl.CurlLayer",
):
    '''An AWS Lambda layer that includes the curl.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6ac3f7b211cb260c976aa26ddff6970c25c928d63a470c513c0179ac044aad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


__all__ = [
    "CurlLayer",
]

publication.publish()

def _typecheckingstub__8b6ac3f7b211cb260c976aa26ddff6970c25c928d63a470c513c0179ac044aad(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
