r'''
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![GitHub](https://img.shields.io/github/license/pepperize/cdk-terraform-state-backend?style=flat-square)](https://github.com/pepperize/cdk-terraform-state-backend/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@pepperize/cdk-terraform-state-backend?style=flat-square)](https://www.npmjs.com/package/@pepperize/cdk-terraform-state-backend)
[![PyPI](https://img.shields.io/pypi/v/pepperize.cdk-terraform-state-backend?style=flat-square)](https://pypi.org/project/pepperize.cdk-terraform-state-backend/)
[![Nuget](https://img.shields.io/nuget/v/Pepperize.CDK.TerraformStateBackend?style=flat-square)](https://www.nuget.org/packages/Pepperize.CDK.TerraformStateBackend/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.pepperize/cdk-terraform-state-backend?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/pepperize/cdk-terraform-state-backend/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/pepperize/cdk-terraform-state-backend/release.yml?banch=main&label=release&style=flat-square)](https://github.com/pepperize/cdk-terraform-state-backend/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/pepperize/cdk-terraform-state-backend?sort=semver&style=flat-square)](https://github.com/pepperize/cdk-terraform-state-backend/releases)

# AWS CDK Terraform state backend

This project provides a CDK construct bootstrapping an AWS account with a S3 Bucket and a DynamoDB table as [Terraform state backend](https://www.terraform.io/docs/language/settings/backends/s3.html).

Terraform doesn't come shipped with a cli command bootstrapping the account for [State Storage and Locking](https://www.terraform.io/docs/language/state/backends.html)
like [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/cli.html#cli-bootstrap) provides with `cdk bootstrap`.
While bootstrapping the AWS Organization and Accounts this construct may be used to create:

* S3 Bucket with blocked public access, versioned, encrypted by SSE-S3
* DynamoDB Table with pay per request, continuous backups using point-in-time recovery, encrypted by AWS owned key
* IAM Policy with read/write access to the created S3 Bucket and DynamoDB Table

See [API.md](https://github.com/pepperize/cdk-terraform-state-backend/blob/main/API.md)

## Install

### TypeScript

```shell
npm install @pepperize/cdk-terraform-state-backend
```

or

```shell
yarn add @pepperize/cdk-terraform-state-backend
```

### Python

```shell
pip install pepperize.cdk-terraform-state-backend
```

### C# / .Net

```
dotnet add package Pepperize.CDK.TerraformStateBackend
```

### Java

```xml
<dependency>
  <groupId>com.pepperize</groupId>
  <artifactId>cdk-terraform-state-backend</artifactId>
  <version>${cdkTerraformStateBackend.version}</version>
</dependency>
```

## Example

```python
import { App, Stack } from "aws-cdk-lib";
import { TerraformStateBackend } from "@pepperize/cdk-terraform-state-backend";

const app = new App();
const stack = new Stack(app, "stack", {
  env: {
    account: "123456789012",
    region: "us-east-1",
  },
});

// When
new TerraformStateBackend(stack, "TerraformStateBackend", {
  bucketName: "terraform-state-backend",
  tableName: "terraform-state-backend",
});
```

```hcl
terraform {
  backend "s3" {
    bucket = "terraform-state-backend-123456789012-us-east-1"
    dynamodb_table = "terraform-state-backend-123456789012"
    key = "path/to/my/key"
    region = "us-east-1"
  }
}
```

See [Terraform S3 Example Configuration](https://www.terraform.io/docs/language/settings/backends/s3.html#example-configuration)
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

import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class TerraformStateBackend(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-terraform-state-backend.TerraformStateBackend",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: 
        :param policy_name: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5d9ea79fbdf82b9c5457ace185ccd4d5fb90582a7733f44f532ccc11e08978)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TerraformStateBackendProps(
            bucket_name=bucket_name, policy_name=policy_name, table_name=table_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> _aws_cdk_aws_iam_ceddda9d.IPolicy:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPolicy, jsii.get(self, "policy"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> _aws_cdk_aws_dynamodb_ceddda9d.ITable:
        return typing.cast(_aws_cdk_aws_dynamodb_ceddda9d.ITable, jsii.get(self, "table"))


@jsii.data_type(
    jsii_type="@pepperize/cdk-terraform-state-backend.TerraformStateBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "policy_name": "policyName",
        "table_name": "tableName",
    },
)
class TerraformStateBackendProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_name: 
        :param policy_name: 
        :param table_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1346563d896365ac4e6ae76af129662631de126bf78153d23b83e432a302a93f)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformStateBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TerraformStateBackend",
    "TerraformStateBackendProps",
]

publication.publish()

def _typecheckingstub__fa5d9ea79fbdf82b9c5457ace185ccd4d5fb90582a7733f44f532ccc11e08978(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1346563d896365ac4e6ae76af129662631de126bf78153d23b83e432a302a93f(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
