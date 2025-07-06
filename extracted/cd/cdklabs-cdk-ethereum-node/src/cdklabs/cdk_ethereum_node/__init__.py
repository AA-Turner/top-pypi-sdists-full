r'''
# Ethereum on Amazon Managed Blockchain

[![license](https://img.shields.io/github/license/cdklabs/cdk-ethereum-node?color=green)](https://opensource.org/licenses/MIT)
[![release](https://img.shields.io/github/v/release/cdklabs/cdk-ethereum-node?color=green)](https://github.com/cdklabs/cdk-ethereum-node/releases)
[![npm:version](https://img.shields.io/npm/v/@cdklabs/cdk-ethereum-node?color=blue)](https://www.npmjs.com/package/@cdklabs/cdk-ethereum-node)
[![PyPi:version](https://img.shields.io/pypi/v/cdklabs.cdk-ethereum-node?color=blue)](https://pypi.org/project/cdklabs.cdk-ethereum-node/)
[![Maven:version](https://img.shields.io/maven-central/v/io.github.cdklabs/cdk-ethereum-node?color=blue&label=maven)](https://central.sonatype.dev/artifact/io.github.cdklabs/cdk-ethereum-node/0.0.61)
[![NuGet:version](https://img.shields.io/nuget/v/Cdklabs.CdkEthereumNode?color=blue)](https://www.nuget.org/packages/Cdklabs.CdkEthereumNode)

This repository contains a CDK construct to deploy an Ethereum node running
on Amazon Managed Blockchain. The following networks are supported:

* Mainnet (default)
* Testnet: Goerli
* Testnet: Rinkeby
* Testnet: Ropsten

## Installation

Note that this construct requires [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_install).

#### JavaScript

```bash
npm install --save @cdklabs/cdk-ethereum-node
```

#### Python

```bash
pip3 install cdklabs.cdk-ethereum-node
```

#### Java

Add the following to `pom.xml`:

```xml
<dependency>
  <groupId>io.github.cdklabs</groupId>
  <artifactId>cdk-ethereum-node</artifactId>
</dependency>
```

#### .NET

```bash
dotnet add package Cdklabs.CdkEthereumNode
```

## Usage

A minimally complete deployment is shown below. By default,
a `bc.t3.large` node will be created on the Ethereum Mainnet.

```python
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { EthereumNode, Network, InstanceType } from '@cdklabs/cdk-ethereum-node';

export class MyStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);
    new EthereumNode(this, 'Example');
  }
}
```

The equivalent Python code is as follows:

```python
from aws_cdk import Stack
from cdklabs.cdk_ethereum_node import EthereumNode

class MyStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        EthereumNode(self, 'Example')
```

The following is a more complex instantiation illustrating some of the node configuration options available.

```python
new EthereumNode(this, 'Example', {
  network: Network.ROPSTEN,
  availabilityZone: 'us-east-1b',
  instanceType: InstanceType.BURSTABLE3_LARGE,
});
```

See the [API Documentation](API.md) for details on all available input and output parameters.

## References

* [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
* [Amazon Managed Blockchain](https://aws.amazon.com/managed-blockchain/)
* [Ethereum](https://ethereum.org/en/developers/docs/)

## Contributing

Pull requests are welcomed. Please review the [Contributing Guidelines](CONTRIBUTING.md)
and the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## Authors

* Trinity Key (trinikey@amazon.com)
* Marc Gozali (gozalim@amazon.com)

## License

This project is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.
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

import constructs as _constructs_77d1e7e8


class EthereumNode(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-ethereum-node.EthereumNode",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional["InstanceType"] = None,
        network: typing.Optional["Network"] = None,
    ) -> None:
        '''Creates an Ethereum public network node on an Amazon Managed Blockchain network.

        :param scope: -
        :param id: -
        :param availability_zone: The Availability Zone in which the node will be created. Default: - us-east-1a
        :param instance_type: The Amazon Managed Blockchain instance type for the Ethereum node. Default: - BURSTABLE3_LARGE
        :param network: The Ethereum Network in which the node will be created. Default: - The default network selected is Mainnet network
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883df649ac5a6816d0717ff3c03dc2f6619322f14f88e09746a5e1f7a51ae784)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EthereumNodeProps(
            availability_zone=availability_zone,
            instance_type=instance_type,
            network=network,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        '''The Availability Zone in which the node exists.'''
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> "InstanceType":
        '''The Amazon Managed Blockchain instance type for the node.'''
        return typing.cast("InstanceType", jsii.get(self, "instanceType"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "Network":
        '''Managed Blockchain Ethereum network identifier.'''
        return typing.cast("Network", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        '''The Region in which the node exists.'''
        return typing.cast(builtins.str, jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-ethereum-node.EthereumNodeProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "instance_type": "instanceType",
        "network": "network",
    },
)
class EthereumNodeProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional["InstanceType"] = None,
        network: typing.Optional["Network"] = None,
    ) -> None:
        '''Construct properties for ``EthereumNode``.

        :param availability_zone: The Availability Zone in which the node will be created. Default: - us-east-1a
        :param instance_type: The Amazon Managed Blockchain instance type for the Ethereum node. Default: - BURSTABLE3_LARGE
        :param network: The Ethereum Network in which the node will be created. Default: - The default network selected is Mainnet network
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54eb351435528770e30b6b2276685c6b5a38ac83dbc65c2a99e116b97c8c64ba)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if network is not None:
            self._values["network"] = network

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone in which the node will be created.

        :default: - us-east-1a
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional["InstanceType"]:
        '''The Amazon Managed Blockchain instance type for the Ethereum node.

        :default: - BURSTABLE3_LARGE
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["InstanceType"], result)

    @builtins.property
    def network(self) -> typing.Optional["Network"]:
        '''The Ethereum Network in which the node will be created.

        :default: - The default network selected is Mainnet network
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["Network"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EthereumNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/cdk-ethereum-node.InstanceType")
class InstanceType(enum.Enum):
    '''Supported instance types for Managed Blockchain nodes.'''

    BURSTABLE3_XLARGE = "BURSTABLE3_XLARGE"
    STANDARD5_XLARGE = "STANDARD5_XLARGE"
    STANDARD5_XLARGE2 = "STANDARD5_XLARGE2"
    STANDARD5_XLARGE4 = "STANDARD5_XLARGE4"
    COMPUTE5_XLARGE2 = "COMPUTE5_XLARGE2"
    COMPUTE5_XLARGE4 = "COMPUTE5_XLARGE4"


@jsii.enum(jsii_type="@cdklabs/cdk-ethereum-node.Network")
class Network(enum.Enum):
    '''Supported Ethereum networks for Managed Blockchain nodes.'''

    MAINNET = "MAINNET"
    GOERLI = "GOERLI"
    RINKEBY = "RINKEBY"
    ROPSTEN = "ROPSTEN"


__all__ = [
    "EthereumNode",
    "EthereumNodeProps",
    "InstanceType",
    "Network",
]

publication.publish()

def _typecheckingstub__883df649ac5a6816d0717ff3c03dc2f6619322f14f88e09746a5e1f7a51ae784(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[InstanceType] = None,
    network: typing.Optional[Network] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54eb351435528770e30b6b2276685c6b5a38ac83dbc65c2a99e116b97c8c64ba(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[InstanceType] = None,
    network: typing.Optional[Network] = None,
) -> None:
    """Type checking stubs"""
    pass
