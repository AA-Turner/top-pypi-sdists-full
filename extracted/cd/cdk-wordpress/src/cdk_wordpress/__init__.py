r'''
# cdk-wordpress

[![NPM version](https://badge.fury.io/js/cdk-wordpress.svg)](https://www.npmjs.com/package/cdk-wordpress)
[![PyPI version](https://badge.fury.io/py/cdk-wordpress.svg)](https://pypi.org/project/cdk-wordpress)
![Release](https://github.com/clarencetw/cdk-wordpress/workflows/Release/badge.svg)

![npm](https://img.shields.io/npm/dt/cdk-wordpress?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-wordpress?label=pypi&color=blue)

A CDK construct library to deploy WordPress

## How do use

Install your package manager:

```sh
yarn add cdk-wordpress
```

### TypeScript Sample

```python
import { WordPress } from "cdk-wordpress";

const wordpress = new WordPress(stack, "WordPressEcs");

// Get WordPress endpoint
new CfnOutput(stack, "Endpoint", { value: wordpress.endpoint });
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
cdk destroy
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_7896c08f
import aws_cdk.aws_rds as _aws_cdk_aws_rds_9543e6d5
import aws_cdk.core as _aws_cdk_core_f4b25747


class WordPress(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-wordpress.WordPress",
):
    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Cluster] = None,
        rds_instance: typing.Optional[_aws_cdk_aws_rds_9543e6d5.DatabaseInstance] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: The WordPress cluster.
        :param rds_instance: The WordPress RDS.
        :param vpc: The WordPress VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7cc402012ef89de5a356e24d3136be850bd259f7c51b04db67faad69c2a8f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WordPressProps(cluster=cluster, rds_instance=rds_instance, vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))


@jsii.data_type(
    jsii_type="cdk-wordpress.WordPressProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster", "rds_instance": "rdsInstance", "vpc": "vpc"},
)
class WordPressProps:
    def __init__(
        self,
        *,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Cluster] = None,
        rds_instance: typing.Optional[_aws_cdk_aws_rds_9543e6d5.DatabaseInstance] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''The interface for all wordpress.

        :param cluster: The WordPress cluster.
        :param rds_instance: The WordPress RDS.
        :param vpc: The WordPress VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a36a6d5e121b2c4302e35a3331fcaea9704cc1646448e94ff2271cf03a5d49)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument rds_instance", value=rds_instance, expected_type=type_hints["rds_instance"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster is not None:
            self._values["cluster"] = cluster
        if rds_instance is not None:
            self._values["rds_instance"] = rds_instance
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.Cluster]:
        '''The WordPress cluster.'''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.Cluster], result)

    @builtins.property
    def rds_instance(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_9543e6d5.DatabaseInstance]:
        '''The WordPress RDS.'''
        result = self._values.get("rds_instance")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_9543e6d5.DatabaseInstance], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The WordPress VPC.'''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WordPressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "WordPress",
    "WordPressProps",
]

publication.publish()

def _typecheckingstub__db7cc402012ef89de5a356e24d3136be850bd259f7c51b04db67faad69c2a8f9(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Cluster] = None,
    rds_instance: typing.Optional[_aws_cdk_aws_rds_9543e6d5.DatabaseInstance] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a36a6d5e121b2c4302e35a3331fcaea9704cc1646448e94ff2271cf03a5d49(
    *,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Cluster] = None,
    rds_instance: typing.Optional[_aws_cdk_aws_rds_9543e6d5.DatabaseInstance] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass
