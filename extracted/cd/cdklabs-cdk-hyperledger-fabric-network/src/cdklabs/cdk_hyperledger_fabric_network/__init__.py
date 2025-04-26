r'''
# Hyperledger Fabric on Amazon Managed Blockchain

[![license](https://img.shields.io/github/license/cdklabs/cdk-hyperledger-fabric-network?color=green)](https://opensource.org/licenses/MIT)
[![release](https://img.shields.io/github/v/release/cdklabs/cdk-hyperledger-fabric-network?color=green)](https://github.com/cdklabs/cdk-hyperledger-fabric-network/releases)
[![npm:version](https://img.shields.io/npm/v/@cdklabs/cdk-hyperledger-fabric-network?color=blue)](https://www.npmjs.com/package/@cdklabs/cdk-hyperledger-fabric-network)
[![PyPi:version](https://img.shields.io/pypi/v/cdklabs.cdk-hyperledger-fabric-network?color=blue)](https://pypi.org/project/cdklabs.cdk-hyperledger-fabric-network/)
[![Maven:version](https://img.shields.io/maven-central/v/io.github.cdklabs/cdk-hyperledger-fabric-network?color=blue&label=maven)](https://central.sonatype.dev/artifact/io.github.cdklabs/cdk-hyperledger-fabric-network/0.8.147)
[![NuGet:version](https://img.shields.io/nuget/v/Cdklabs.CdkHyperledgerFabricNetwork?color=blue)](https://www.nuget.org/packages/Cdklabs.CdkHyperledgerFabricNetwork)

This repository contains a CDK construct to deploy a Hyperledger Fabric network
running on Amazon Managed Blockchain. It builds out a member and its nodes, a VPC
and associated endpoint to access them, and a set of users enrolled on the network.

The following functionality is planned for future releases:

* Create channels on nodes
* Instantiate chaincode on nodes

## Installation

Note that this construct requires [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_install).

#### JavaScript

```bash
npm install --save @cdklabs/cdk-hyperledger-fabric-network
```

#### Python

```bash
pip3 install cdklabs.cdk-hyperledger-fabric-network
```

#### Java

Add the following to `pom.xml`:

```xml
<dependency>
  <groupId>io.github.cdklabs</groupId>
  <artifactId>cdk-hyperledger-fabric-network</artifactId>
</dependency>
```

#### .NET

```bash
dotnet add package Cdklabs.CdkHyperledgerFabricNetwork
```

## Usage

A minimally complete deployment is shown below. By default, a standard network
will be created running Hyperledger Fabric 1.4 with a single `bc.t3.small` node.

```python
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { HyperledgerFabricNetwork } from '@cdklabs/cdk-hyperledger-fabric-network';

class MyStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);
    new HyperledgerFabricNetwork(this, 'Example', {
      networkName: 'MyNetwork',
      memberName: 'MyMember',
    });
  }
}
```

The equivalent Python code is as follows:

```python
from aws_cdk import Stack
from cdklabs.cdk_hyperledger_fabric_network import HyperledgerFabricNetwork

class MyStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        HyperledgerFabricNetwork(
            self, 'Example',
            network_name='MyNetwork',
            member_name='MyMember',
        )
```

The following is a more complex instantiation illustrating some of the options available.

```python
new HyperledgerFabricNetwork(this, 'Example', {
  networkName: 'MyNetwork',
  networkDescription: 'This is my Hyperledger Fabric network',
  memberName: 'MyMember',
  networkDescription: 'This is my Hyperledger Fabric member',
  frameworkVersion: hyperledger.FrameworkVersion.VERSION_1_2,
  proposalDurationInHours: 48,
  thresholdPercentage: 75,
  nodes: [
    {
      availabilityZone: 'us-east-1a',
      instanceType: hyperledger.InstanceType.STANDARD5_LARGE,
    },
    {
      availabilityZone: 'us-east-1b',
      instanceType: hyperledger.InstanceType.STANDARD5_LARGE,
    },
  ],
  users: [
    { userId: 'AppUser1', affilitation: 'MyMember' },
    { userId: 'AppUser2', affilitation: 'MyMember.department1' },
  ],
});
```

See the [API Documentation](API.md) for details on all available input and output parameters.

## References

* [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
* [Amazon Managed Blockchain](https://aws.amazon.com/managed-blockchain/)
* [Hyperledger Fabric](https://hyperledger-fabric.readthedocs.io/)
* [Node Fabric SDK](https://hyperledger.github.io/fabric-sdk-node/release-1.4/index.html)
* [Fabric Chaincode Node](https://hyperledger.github.io/fabric-chaincode-node/)

## Contributing

Pull requests are welcomed. Please review the [Contributing Guidelines](CONTRIBUTING.md)
and the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## Authors

* Jud Neer (judneer@amazon.com)
* Vignesh Rajasingh (vrajasin@amazon.com)

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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.custom_resources as _aws_cdk_custom_resources_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@cdklabs/cdk-hyperledger-fabric-network.FrameworkVersion")
class FrameworkVersion(enum.Enum):
    '''Define which Hyperledger Fabric framework to use.'''

    VERSION_1_2 = "VERSION_1_2"
    VERSION_1_4 = "VERSION_1_4"
    VERSION_2_2 = "VERSION_2_2"


class HyperledgerFabricClient(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-hyperledger-fabric-network.HyperledgerFabricClient",
):
    '''Creates a VPC and endpoint that allows Hyperledger Fabric client to interact with the Hyperledger Fabric endpoints that Amazon Managed Blockchain exposes for the member and network resources.'''

    def __init__(
        self,
        scope: "HyperledgerFabricNetwork",
        id: builtins.str,
        *,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: Client VPC to create the endpoints. If not provided, VPC will be created with the default properties (CIDR-``10.0.0.0/16`` and subnets of type ``PRIVATE_ISOLATED``)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154d415e43d85e79ab77897d337126adb7e3863def6e54ea460292a8d8ed8ab3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HyperledgerFabricClientProps(vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The client VPC that has endpoint to access the Amazon Managed Blockchain.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="vpcEndpoint")
    def vpc_endpoint(self) -> _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpoint:
        '''Managed Blockchain network VPC endpoint.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpoint, jsii.get(self, "vpcEndpoint"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-hyperledger-fabric-network.HyperledgerFabricClientProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class HyperledgerFabricClientProps:
    def __init__(
        self,
        *,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''Construct properties for ``HyperledgerFabricVpc``.

        :param vpc: Client VPC to create the endpoints. If not provided, VPC will be created with the default properties (CIDR-``10.0.0.0/16`` and subnets of type ``PRIVATE_ISOLATED``)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85f32d6b24ec882e649285cfecfe6489e6c84dfc692b1823fb92058be9fe7629)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''Client VPC to create the endpoints.

        If not provided,
        VPC will be created with the default properties
        (CIDR-``10.0.0.0/16`` and subnets of type ``PRIVATE_ISOLATED``)
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HyperledgerFabricClientProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HyperledgerFabricNetwork(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-hyperledger-fabric-network.HyperledgerFabricNetwork",
):
    '''Creates a Hyperledger Fabric network on Amazon Managed Blockchain.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        member_name: builtins.str,
        network_name: builtins.str,
        client: typing.Optional[typing.Union[HyperledgerFabricClientProps, typing.Dict[builtins.str, typing.Any]]] = None,
        enable_ca_logging: typing.Optional[builtins.bool] = None,
        enroll_admin: typing.Optional[builtins.bool] = None,
        framework_version: typing.Optional[FrameworkVersion] = None,
        member_description: typing.Optional[builtins.str] = None,
        network_description: typing.Optional[builtins.str] = None,
        network_edition: typing.Optional["NetworkEdition"] = None,
        nodes: typing.Optional[typing.Sequence[typing.Union["HyperledgerFabricNodeProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
        threshold_comparator: typing.Optional["ThresholdComparator"] = None,
        threshold_percentage: typing.Optional[jsii.Number] = None,
        users: typing.Optional[typing.Sequence[typing.Union["HyperledgerFabricUserProps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param member_name: Managed Blockchain member name.
        :param network_name: Managed Blockchain network name.
        :param client: The Client network to interact with the Hyperledger Fabric network. Default: - Client network with Default properties (CIDR-``10.0.0.0/16`` and subnets of type ``PRIVATE_ISOLATED``)
        :param enable_ca_logging: The configuration to enable or disable certificate authority logging. Default: - true
        :param enroll_admin: Configuration to enable/disable enrollment of admin user. Default: - true
        :param framework_version: Hyperledger Fabric framework version. Default: - FrameworkVersion.VERSION_1_4
        :param member_description: Managed Blockchain member description. Default: - Set to match member name
        :param network_description: Managed Blockchain network description. Default: - Set to match network name
        :param network_edition: Managed Blockchain network edition. Default: - NetworkEdition.STANDARD
        :param nodes: List of nodes to create on the network. Default: - One node with default configuration
        :param proposal_duration_in_hours: The duration from the time that a proposal is created until it expires. Default: - 24 hours
        :param threshold_comparator: Determines whether the yes votes must be greater than the threshold percentage or must be greater than or equal to the threhold percentage to be approved. Default: - GREATER_THAN
        :param threshold_percentage: The percentage of votes among all members that must be yes for a proposal to be approved. Default: - 50 percent
        :param users: List of users to register with Fabric CA Note: enrollAdmin property has to be enabled for registering users.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1d5370f935b3b70349960b0af6ca6d69e5b9f4c34a6350d1987a218105bc1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HyperledgerFabricNetworkProps(
            member_name=member_name,
            network_name=network_name,
            client=client,
            enable_ca_logging=enable_ca_logging,
            enroll_admin=enroll_admin,
            framework_version=framework_version,
            member_description=member_description,
            network_description=network_description,
            network_edition=network_edition,
            nodes=nodes,
            proposal_duration_in_hours=proposal_duration_in_hours,
            threshold_comparator=threshold_comparator,
            threshold_percentage=threshold_percentage,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="adminPasswordSecret")
    def admin_password_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''Secret ARN for the Hyperledger Fabric admin password.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "adminPasswordSecret"))

    @builtins.property
    @jsii.member(jsii_name="adminPrivateKeySecret")
    def admin_private_key_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''Secret for Hyperledger Fabric admin private key.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "adminPrivateKeySecret"))

    @builtins.property
    @jsii.member(jsii_name="adminSignedCertSecret")
    def admin_signed_cert_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''Secret for Hyperledger Fabric admin signed certificate.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "adminSignedCertSecret"))

    @builtins.property
    @jsii.member(jsii_name="caEndpoint")
    def ca_endpoint(self) -> builtins.str:
        '''Managed Blockchain member CA endpoint.'''
        return typing.cast(builtins.str, jsii.get(self, "caEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="client")
    def client(self) -> HyperledgerFabricClient:
        '''The client network to interact with the Hyperledger Fabric network.'''
        return typing.cast(HyperledgerFabricClient, jsii.get(self, "client"))

    @builtins.property
    @jsii.member(jsii_name="enableCaLogging")
    def enable_ca_logging(self) -> builtins.bool:
        '''The configuration to enable or disable certificate authority logging.'''
        return typing.cast(builtins.bool, jsii.get(self, "enableCaLogging"))

    @builtins.property
    @jsii.member(jsii_name="enrollAdmin")
    def enroll_admin(self) -> builtins.bool:
        '''Configuration to enable/disable admin user enrollment.'''
        return typing.cast(builtins.bool, jsii.get(self, "enrollAdmin"))

    @builtins.property
    @jsii.member(jsii_name="frameworkVersion")
    def framework_version(self) -> FrameworkVersion:
        '''Hyperledger Fabric framework version.'''
        return typing.cast(FrameworkVersion, jsii.get(self, "frameworkVersion"))

    @builtins.property
    @jsii.member(jsii_name="memberDescription")
    def member_description(self) -> builtins.str:
        '''Managed Blockchain member description.'''
        return typing.cast(builtins.str, jsii.get(self, "memberDescription"))

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(self) -> builtins.str:
        '''Managed Blockchain member identifier generated on construction.'''
        return typing.cast(builtins.str, jsii.get(self, "memberId"))

    @builtins.property
    @jsii.member(jsii_name="memberName")
    def member_name(self) -> builtins.str:
        '''Managed Blockchain member name.'''
        return typing.cast(builtins.str, jsii.get(self, "memberName"))

    @builtins.property
    @jsii.member(jsii_name="networkDescription")
    def network_description(self) -> builtins.str:
        '''Managed Blockchain network description.'''
        return typing.cast(builtins.str, jsii.get(self, "networkDescription"))

    @builtins.property
    @jsii.member(jsii_name="networkEdition")
    def network_edition(self) -> "NetworkEdition":
        '''Managed Blockchain network edition.'''
        return typing.cast("NetworkEdition", jsii.get(self, "networkEdition"))

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        '''Managed Blockchain network identifier generated on construction.'''
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @builtins.property
    @jsii.member(jsii_name="networkName")
    def network_name(self) -> builtins.str:
        '''Managed Blockchain network name.'''
        return typing.cast(builtins.str, jsii.get(self, "networkName"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.List["HyperledgerFabricNode"]:
        '''List of nodes created in the network.'''
        return typing.cast(typing.List["HyperledgerFabricNode"], jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="ordererEndpoint")
    def orderer_endpoint(self) -> builtins.str:
        '''Managed Blockchain network ordering service endpoint.'''
        return typing.cast(builtins.str, jsii.get(self, "ordererEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="proposalDurationInHours")
    def proposal_duration_in_hours(self) -> jsii.Number:
        '''The duration from the time that a proposal is created until it expires.'''
        return typing.cast(jsii.Number, jsii.get(self, "proposalDurationInHours"))

    @builtins.property
    @jsii.member(jsii_name="thresholdComparator")
    def threshold_comparator(self) -> "ThresholdComparator":
        '''Determines whether the yes votes must be greater than the threshold percentage or must be greater than or equal to the threhold percentage to be approved.'''
        return typing.cast("ThresholdComparator", jsii.get(self, "thresholdComparator"))

    @builtins.property
    @jsii.member(jsii_name="thresholdPercentage")
    def threshold_percentage(self) -> jsii.Number:
        '''The percentage of votes among all members that must be yes for a proposal to be approved.'''
        return typing.cast(jsii.Number, jsii.get(self, "thresholdPercentage"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List["HyperledgerFabricUser"]:
        '''List of users registered with CA.'''
        return typing.cast(typing.List["HyperledgerFabricUser"], jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointServiceName")
    def vpc_endpoint_service_name(self) -> builtins.str:
        '''Managed Blockchain network VPC endpoint service name.'''
        return typing.cast(builtins.str, jsii.get(self, "vpcEndpointServiceName"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-hyperledger-fabric-network.HyperledgerFabricNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "member_name": "memberName",
        "network_name": "networkName",
        "client": "client",
        "enable_ca_logging": "enableCaLogging",
        "enroll_admin": "enrollAdmin",
        "framework_version": "frameworkVersion",
        "member_description": "memberDescription",
        "network_description": "networkDescription",
        "network_edition": "networkEdition",
        "nodes": "nodes",
        "proposal_duration_in_hours": "proposalDurationInHours",
        "threshold_comparator": "thresholdComparator",
        "threshold_percentage": "thresholdPercentage",
        "users": "users",
    },
)
class HyperledgerFabricNetworkProps:
    def __init__(
        self,
        *,
        member_name: builtins.str,
        network_name: builtins.str,
        client: typing.Optional[typing.Union[HyperledgerFabricClientProps, typing.Dict[builtins.str, typing.Any]]] = None,
        enable_ca_logging: typing.Optional[builtins.bool] = None,
        enroll_admin: typing.Optional[builtins.bool] = None,
        framework_version: typing.Optional[FrameworkVersion] = None,
        member_description: typing.Optional[builtins.str] = None,
        network_description: typing.Optional[builtins.str] = None,
        network_edition: typing.Optional["NetworkEdition"] = None,
        nodes: typing.Optional[typing.Sequence[typing.Union["HyperledgerFabricNodeProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
        threshold_comparator: typing.Optional["ThresholdComparator"] = None,
        threshold_percentage: typing.Optional[jsii.Number] = None,
        users: typing.Optional[typing.Sequence[typing.Union["HyperledgerFabricUserProps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Construct properties for ``HyperledgerFabricNetwork``.

        :param member_name: Managed Blockchain member name.
        :param network_name: Managed Blockchain network name.
        :param client: The Client network to interact with the Hyperledger Fabric network. Default: - Client network with Default properties (CIDR-``10.0.0.0/16`` and subnets of type ``PRIVATE_ISOLATED``)
        :param enable_ca_logging: The configuration to enable or disable certificate authority logging. Default: - true
        :param enroll_admin: Configuration to enable/disable enrollment of admin user. Default: - true
        :param framework_version: Hyperledger Fabric framework version. Default: - FrameworkVersion.VERSION_1_4
        :param member_description: Managed Blockchain member description. Default: - Set to match member name
        :param network_description: Managed Blockchain network description. Default: - Set to match network name
        :param network_edition: Managed Blockchain network edition. Default: - NetworkEdition.STANDARD
        :param nodes: List of nodes to create on the network. Default: - One node with default configuration
        :param proposal_duration_in_hours: The duration from the time that a proposal is created until it expires. Default: - 24 hours
        :param threshold_comparator: Determines whether the yes votes must be greater than the threshold percentage or must be greater than or equal to the threhold percentage to be approved. Default: - GREATER_THAN
        :param threshold_percentage: The percentage of votes among all members that must be yes for a proposal to be approved. Default: - 50 percent
        :param users: List of users to register with Fabric CA Note: enrollAdmin property has to be enabled for registering users.
        '''
        if isinstance(client, dict):
            client = HyperledgerFabricClientProps(**client)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb03cc45eb5a09d534d69a98734d9a4df6f050b76ee233d74973c6bb52e04a3d)
            check_type(argname="argument member_name", value=member_name, expected_type=type_hints["member_name"])
            check_type(argname="argument network_name", value=network_name, expected_type=type_hints["network_name"])
            check_type(argname="argument client", value=client, expected_type=type_hints["client"])
            check_type(argname="argument enable_ca_logging", value=enable_ca_logging, expected_type=type_hints["enable_ca_logging"])
            check_type(argname="argument enroll_admin", value=enroll_admin, expected_type=type_hints["enroll_admin"])
            check_type(argname="argument framework_version", value=framework_version, expected_type=type_hints["framework_version"])
            check_type(argname="argument member_description", value=member_description, expected_type=type_hints["member_description"])
            check_type(argname="argument network_description", value=network_description, expected_type=type_hints["network_description"])
            check_type(argname="argument network_edition", value=network_edition, expected_type=type_hints["network_edition"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument proposal_duration_in_hours", value=proposal_duration_in_hours, expected_type=type_hints["proposal_duration_in_hours"])
            check_type(argname="argument threshold_comparator", value=threshold_comparator, expected_type=type_hints["threshold_comparator"])
            check_type(argname="argument threshold_percentage", value=threshold_percentage, expected_type=type_hints["threshold_percentage"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "member_name": member_name,
            "network_name": network_name,
        }
        if client is not None:
            self._values["client"] = client
        if enable_ca_logging is not None:
            self._values["enable_ca_logging"] = enable_ca_logging
        if enroll_admin is not None:
            self._values["enroll_admin"] = enroll_admin
        if framework_version is not None:
            self._values["framework_version"] = framework_version
        if member_description is not None:
            self._values["member_description"] = member_description
        if network_description is not None:
            self._values["network_description"] = network_description
        if network_edition is not None:
            self._values["network_edition"] = network_edition
        if nodes is not None:
            self._values["nodes"] = nodes
        if proposal_duration_in_hours is not None:
            self._values["proposal_duration_in_hours"] = proposal_duration_in_hours
        if threshold_comparator is not None:
            self._values["threshold_comparator"] = threshold_comparator
        if threshold_percentage is not None:
            self._values["threshold_percentage"] = threshold_percentage
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def member_name(self) -> builtins.str:
        '''Managed Blockchain member name.'''
        result = self._values.get("member_name")
        assert result is not None, "Required property 'member_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_name(self) -> builtins.str:
        '''Managed Blockchain network name.'''
        result = self._values.get("network_name")
        assert result is not None, "Required property 'network_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client(self) -> typing.Optional[HyperledgerFabricClientProps]:
        '''The Client network to interact with the Hyperledger Fabric network.

        :default:

        - Client network with Default properties
        (CIDR-``10.0.0.0/16`` and subnets of type ``PRIVATE_ISOLATED``)
        '''
        result = self._values.get("client")
        return typing.cast(typing.Optional[HyperledgerFabricClientProps], result)

    @builtins.property
    def enable_ca_logging(self) -> typing.Optional[builtins.bool]:
        '''The configuration to enable or disable certificate authority logging.

        :default: - true
        '''
        result = self._values.get("enable_ca_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enroll_admin(self) -> typing.Optional[builtins.bool]:
        '''Configuration to enable/disable enrollment of admin user.

        :default: - true
        '''
        result = self._values.get("enroll_admin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def framework_version(self) -> typing.Optional[FrameworkVersion]:
        '''Hyperledger Fabric framework version.

        :default: - FrameworkVersion.VERSION_1_4
        '''
        result = self._values.get("framework_version")
        return typing.cast(typing.Optional[FrameworkVersion], result)

    @builtins.property
    def member_description(self) -> typing.Optional[builtins.str]:
        '''Managed Blockchain member description.

        :default: - Set to match member name
        '''
        result = self._values.get("member_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_description(self) -> typing.Optional[builtins.str]:
        '''Managed Blockchain network description.

        :default: - Set to match network name
        '''
        result = self._values.get("network_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_edition(self) -> typing.Optional["NetworkEdition"]:
        '''Managed Blockchain network edition.

        :default: - NetworkEdition.STANDARD
        '''
        result = self._values.get("network_edition")
        return typing.cast(typing.Optional["NetworkEdition"], result)

    @builtins.property
    def nodes(self) -> typing.Optional[typing.List["HyperledgerFabricNodeProps"]]:
        '''List of nodes to create on the network.

        :default: - One node with default configuration
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.List["HyperledgerFabricNodeProps"]], result)

    @builtins.property
    def proposal_duration_in_hours(self) -> typing.Optional[jsii.Number]:
        '''The duration from the time that a proposal is created until it expires.

        :default: - 24 hours
        '''
        result = self._values.get("proposal_duration_in_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_comparator(self) -> typing.Optional["ThresholdComparator"]:
        '''Determines whether the yes votes must be greater than the threshold percentage or must be greater than or equal to the threhold percentage to be approved.

        :default: - GREATER_THAN
        '''
        result = self._values.get("threshold_comparator")
        return typing.cast(typing.Optional["ThresholdComparator"], result)

    @builtins.property
    def threshold_percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of votes among all members that must be yes for a proposal to be approved.

        :default: - 50 percent
        '''
        result = self._values.get("threshold_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List["HyperledgerFabricUserProps"]]:
        '''List of users to register with Fabric CA Note: enrollAdmin property has to be enabled for registering users.'''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List["HyperledgerFabricUserProps"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HyperledgerFabricNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HyperledgerFabricNode(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-hyperledger-fabric-network.HyperledgerFabricNode",
):
    '''Creates a Hyperledger Fabric node on an Amazon Managed Blockchain network.'''

    def __init__(
        self,
        scope: HyperledgerFabricNetwork,
        id: builtins.str,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        enable_chaincode_logging: typing.Optional[builtins.bool] = None,
        enable_node_logging: typing.Optional[builtins.bool] = None,
        instance_type: typing.Optional["InstanceType"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zone: The Availability Zone in which the node will be created. Default: - The first AZ in the region
        :param enable_chaincode_logging: The configuration to enable or disable chaincode logging. Default: - true
        :param enable_node_logging: The configuration to enable or disable node logging. Default: - true
        :param instance_type: The Amazon Managed Blockchain instance type for the node. Default: - BURSTABLE3_SMALL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7995f832618c77cb04cb68e6714f94e1250a43519f0a71560329886f71ebd00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HyperledgerFabricNodeProps(
            availability_zone=availability_zone,
            enable_chaincode_logging=enable_chaincode_logging,
            enable_node_logging=enable_node_logging,
            instance_type=instance_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="constructNodes")
    @builtins.classmethod
    def construct_nodes(
        cls,
        scope: HyperledgerFabricNetwork,
        node_props: typing.Optional[typing.Sequence[typing.Union["HyperledgerFabricNodeProps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> typing.List["HyperledgerFabricNode"]:
        '''Build out a list of HyperledgerFabricNode constructs given a list of input property objects;

        additionally checks to ensure node count is supported given the network type

        :param scope: -
        :param node_props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b797c6e583410cc99ceddaa6905a221c7b2f75be172755d0f9c3937d02f7c362)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument node_props", value=node_props, expected_type=type_hints["node_props"])
        return typing.cast(typing.List["HyperledgerFabricNode"], jsii.sinvoke(cls, "constructNodes", [scope, node_props]))

    @jsii.member(jsii_name="configureLogging")
    def configure_logging(
        self,
        sdk_call_policy: _aws_cdk_custom_resources_ceddda9d.AwsCustomResourcePolicy,
    ) -> None:
        '''Configure logging for the node via SDK call;

        this function
        should be merged back into the constructor once the race condition is solved

        :param sdk_call_policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7d3fa3a460e574be75d2f37ca3d6ee5c9738c12ea5a8ac614f022f7eb93ac6)
            check_type(argname="argument sdk_call_policy", value=sdk_call_policy, expected_type=type_hints["sdk_call_policy"])
        return typing.cast(None, jsii.invoke(self, "configureLogging", [sdk_call_policy]))

    @jsii.member(jsii_name="fetchData")
    def fetch_data(
        self,
        data_sdk_call_policy: _aws_cdk_custom_resources_ceddda9d.AwsCustomResourcePolicy,
    ) -> None:
        '''Populate the output properties that must be fetched via SDK call;

        this function
        should be merged back into the constructor once the race condition is solved

        :param data_sdk_call_policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ecd06245a395ae577811c9b59204dc29d172cef60b6f94e0a2605aa666b484)
            check_type(argname="argument data_sdk_call_policy", value=data_sdk_call_policy, expected_type=type_hints["data_sdk_call_policy"])
        return typing.cast(None, jsii.invoke(self, "fetchData", [data_sdk_call_policy]))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        '''The Availability Zone in which the node exists.'''
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="enableChaincodeLogging")
    def enable_chaincode_logging(self) -> builtins.bool:
        '''The configuration to enable or disable chaincode logging.'''
        return typing.cast(builtins.bool, jsii.get(self, "enableChaincodeLogging"))

    @builtins.property
    @jsii.member(jsii_name="enableNodeLogging")
    def enable_node_logging(self) -> builtins.bool:
        '''The configuration to enable or disable node logging.'''
        return typing.cast(builtins.bool, jsii.get(self, "enableNodeLogging"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> "InstanceType":
        '''The Amazon Managed Blockchain instance type for the node.'''
        return typing.cast("InstanceType", jsii.get(self, "instanceType"))

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(self) -> builtins.str:
        '''Managed Blockchain member identifier.'''
        return typing.cast(builtins.str, jsii.get(self, "memberId"))

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        '''Managed Blockchain network identifier.'''
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @builtins.property
    @jsii.member(jsii_name="nodeId")
    def node_id(self) -> builtins.str:
        '''Managed Blockchain node identifier generated on construction.'''
        return typing.cast(builtins.str, jsii.get(self, "nodeId"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdee31785b54c48b4fa9169ec6277422cd4c131918f0a90bc652151f2f7fc452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventEndpoint")
    def event_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventEndpoint"))

    @event_endpoint.setter
    def event_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb35119bfaae75c607a8fdd3192990f4f0d0c432181500f8ffa70f35fb44c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventEndpoint", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdklabs/cdk-hyperledger-fabric-network.HyperledgerFabricNodeProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "enable_chaincode_logging": "enableChaincodeLogging",
        "enable_node_logging": "enableNodeLogging",
        "instance_type": "instanceType",
    },
)
class HyperledgerFabricNodeProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        enable_chaincode_logging: typing.Optional[builtins.bool] = None,
        enable_node_logging: typing.Optional[builtins.bool] = None,
        instance_type: typing.Optional["InstanceType"] = None,
    ) -> None:
        '''Construct properties for ``HyperledgerFabricNode``.

        :param availability_zone: The Availability Zone in which the node will be created. Default: - The first AZ in the region
        :param enable_chaincode_logging: The configuration to enable or disable chaincode logging. Default: - true
        :param enable_node_logging: The configuration to enable or disable node logging. Default: - true
        :param instance_type: The Amazon Managed Blockchain instance type for the node. Default: - BURSTABLE3_SMALL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be11b2c72ea8ac0ec37f21ab913b040d96305b807ed21989fdb865fa3811d545)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument enable_chaincode_logging", value=enable_chaincode_logging, expected_type=type_hints["enable_chaincode_logging"])
            check_type(argname="argument enable_node_logging", value=enable_node_logging, expected_type=type_hints["enable_node_logging"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if enable_chaincode_logging is not None:
            self._values["enable_chaincode_logging"] = enable_chaincode_logging
        if enable_node_logging is not None:
            self._values["enable_node_logging"] = enable_node_logging
        if instance_type is not None:
            self._values["instance_type"] = instance_type

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone in which the node will be created.

        :default: - The first AZ in the region
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_chaincode_logging(self) -> typing.Optional[builtins.bool]:
        '''The configuration to enable or disable chaincode logging.

        :default: - true
        '''
        result = self._values.get("enable_chaincode_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_node_logging(self) -> typing.Optional[builtins.bool]:
        '''The configuration to enable or disable node logging.

        :default: - true
        '''
        result = self._values.get("enable_node_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_type(self) -> typing.Optional["InstanceType"]:
        '''The Amazon Managed Blockchain instance type for the node.

        :default: - BURSTABLE3_SMALL
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["InstanceType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HyperledgerFabricNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HyperledgerFabricUser(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-hyperledger-fabric-network.HyperledgerFabricUser",
):
    '''Creates custom resources to register and enroll users identities with the CA using the fabric-ca-client SDK.'''

    def __init__(
        self,
        scope: HyperledgerFabricNetwork,
        id: builtins.str,
        *,
        affilitation: builtins.str,
        user_id: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param affilitation: User's affiliation to the member. Should be hierarchical with member name as root(``MemberName.Dept1``).
        :param user_id: User ID to register with CA.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb2143be061442e099e630c3417f6f56e7955da98e6cea5a3851dc6af9affe0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HyperledgerFabricUserProps(affilitation=affilitation, user_id=user_id)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="affiliation")
    def affiliation(self) -> builtins.str:
        '''User's affiliation to the member.'''
        return typing.cast(builtins.str, jsii.get(self, "affiliation"))

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        '''User ID registered with CA.'''
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property
    @jsii.member(jsii_name="userPrivateKeySecret")
    def user_private_key_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''Secret for user private key.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "userPrivateKeySecret"))

    @builtins.property
    @jsii.member(jsii_name="userSignedCertSecret")
    def user_signed_cert_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''Secret for user signed certificate.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "userSignedCertSecret"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-hyperledger-fabric-network.HyperledgerFabricUserProps",
    jsii_struct_bases=[],
    name_mapping={"affilitation": "affilitation", "user_id": "userId"},
)
class HyperledgerFabricUserProps:
    def __init__(self, *, affilitation: builtins.str, user_id: builtins.str) -> None:
        '''Construct properties for ``HyperledgerFabricUser``.

        :param affilitation: User's affiliation to the member. Should be hierarchical with member name as root(``MemberName.Dept1``).
        :param user_id: User ID to register with CA.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a912d2eb440428f1d791054b0d66ffe03e4d879ba1df147d1dd3d9fb1f8bc32d)
            check_type(argname="argument affilitation", value=affilitation, expected_type=type_hints["affilitation"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "affilitation": affilitation,
            "user_id": user_id,
        }

    @builtins.property
    def affilitation(self) -> builtins.str:
        '''User's affiliation to the member.

        Should be hierarchical with member name as root(``MemberName.Dept1``).
        '''
        result = self._values.get("affilitation")
        assert result is not None, "Required property 'affilitation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''User ID to register with CA.'''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HyperledgerFabricUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/cdk-hyperledger-fabric-network.InstanceType")
class InstanceType(enum.Enum):
    '''Supported instance types for Managed Blockchain nodes.'''

    BURSTABLE3_SMALL = "BURSTABLE3_SMALL"
    BURSTABLE3_MEDIUM = "BURSTABLE3_MEDIUM"
    BURSTABLE3_LARGE = "BURSTABLE3_LARGE"
    BURSTABLE3_XLARGE = "BURSTABLE3_XLARGE"
    STANDARD5_LARGE = "STANDARD5_LARGE"
    STANDARD5_XLARGE = "STANDARD5_XLARGE"
    STANDARD5_XLARGE2 = "STANDARD5_XLARGE2"
    STANDARD5_XLARGE4 = "STANDARD5_XLARGE4"
    COMPUTE5_LARGE = "COMPUTE5_LARGE"
    COMPUTE5_XLARGE = "COMPUTE5_XLARGE"
    COMPUTE5_XLARGE2 = "COMPUTE5_XLARGE2"
    COMPUTE5_XLARGE4 = "COMPUTE5_XLARGE4"


@jsii.enum(jsii_type="@cdklabs/cdk-hyperledger-fabric-network.NetworkEdition")
class NetworkEdition(enum.Enum):
    '''Starter networks are cheaper, but are limited to 2 nodes that can only be from a subset of types (see node.ts for the list).'''

    STARTER = "STARTER"
    STANDARD = "STANDARD"


@jsii.enum(jsii_type="@cdklabs/cdk-hyperledger-fabric-network.ThresholdComparator")
class ThresholdComparator(enum.Enum):
    '''Constants to define ties in voting for new members.'''

    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUAL_TO = "GREATER_THAN_OR_EQUAL_TO"


__all__ = [
    "FrameworkVersion",
    "HyperledgerFabricClient",
    "HyperledgerFabricClientProps",
    "HyperledgerFabricNetwork",
    "HyperledgerFabricNetworkProps",
    "HyperledgerFabricNode",
    "HyperledgerFabricNodeProps",
    "HyperledgerFabricUser",
    "HyperledgerFabricUserProps",
    "InstanceType",
    "NetworkEdition",
    "ThresholdComparator",
]

publication.publish()

def _typecheckingstub__154d415e43d85e79ab77897d337126adb7e3863def6e54ea460292a8d8ed8ab3(
    scope: HyperledgerFabricNetwork,
    id: builtins.str,
    *,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f32d6b24ec882e649285cfecfe6489e6c84dfc692b1823fb92058be9fe7629(
    *,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1d5370f935b3b70349960b0af6ca6d69e5b9f4c34a6350d1987a218105bc1e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    member_name: builtins.str,
    network_name: builtins.str,
    client: typing.Optional[typing.Union[HyperledgerFabricClientProps, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_ca_logging: typing.Optional[builtins.bool] = None,
    enroll_admin: typing.Optional[builtins.bool] = None,
    framework_version: typing.Optional[FrameworkVersion] = None,
    member_description: typing.Optional[builtins.str] = None,
    network_description: typing.Optional[builtins.str] = None,
    network_edition: typing.Optional[NetworkEdition] = None,
    nodes: typing.Optional[typing.Sequence[typing.Union[HyperledgerFabricNodeProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
    threshold_comparator: typing.Optional[ThresholdComparator] = None,
    threshold_percentage: typing.Optional[jsii.Number] = None,
    users: typing.Optional[typing.Sequence[typing.Union[HyperledgerFabricUserProps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb03cc45eb5a09d534d69a98734d9a4df6f050b76ee233d74973c6bb52e04a3d(
    *,
    member_name: builtins.str,
    network_name: builtins.str,
    client: typing.Optional[typing.Union[HyperledgerFabricClientProps, typing.Dict[builtins.str, typing.Any]]] = None,
    enable_ca_logging: typing.Optional[builtins.bool] = None,
    enroll_admin: typing.Optional[builtins.bool] = None,
    framework_version: typing.Optional[FrameworkVersion] = None,
    member_description: typing.Optional[builtins.str] = None,
    network_description: typing.Optional[builtins.str] = None,
    network_edition: typing.Optional[NetworkEdition] = None,
    nodes: typing.Optional[typing.Sequence[typing.Union[HyperledgerFabricNodeProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
    threshold_comparator: typing.Optional[ThresholdComparator] = None,
    threshold_percentage: typing.Optional[jsii.Number] = None,
    users: typing.Optional[typing.Sequence[typing.Union[HyperledgerFabricUserProps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7995f832618c77cb04cb68e6714f94e1250a43519f0a71560329886f71ebd00(
    scope: HyperledgerFabricNetwork,
    id: builtins.str,
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    enable_chaincode_logging: typing.Optional[builtins.bool] = None,
    enable_node_logging: typing.Optional[builtins.bool] = None,
    instance_type: typing.Optional[InstanceType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b797c6e583410cc99ceddaa6905a221c7b2f75be172755d0f9c3937d02f7c362(
    scope: HyperledgerFabricNetwork,
    node_props: typing.Optional[typing.Sequence[typing.Union[HyperledgerFabricNodeProps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7d3fa3a460e574be75d2f37ca3d6ee5c9738c12ea5a8ac614f022f7eb93ac6(
    sdk_call_policy: _aws_cdk_custom_resources_ceddda9d.AwsCustomResourcePolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ecd06245a395ae577811c9b59204dc29d172cef60b6f94e0a2605aa666b484(
    data_sdk_call_policy: _aws_cdk_custom_resources_ceddda9d.AwsCustomResourcePolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdee31785b54c48b4fa9169ec6277422cd4c131918f0a90bc652151f2f7fc452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb35119bfaae75c607a8fdd3192990f4f0d0c432181500f8ffa70f35fb44c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be11b2c72ea8ac0ec37f21ab913b040d96305b807ed21989fdb865fa3811d545(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    enable_chaincode_logging: typing.Optional[builtins.bool] = None,
    enable_node_logging: typing.Optional[builtins.bool] = None,
    instance_type: typing.Optional[InstanceType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb2143be061442e099e630c3417f6f56e7955da98e6cea5a3851dc6af9affe0(
    scope: HyperledgerFabricNetwork,
    id: builtins.str,
    *,
    affilitation: builtins.str,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a912d2eb440428f1d791054b0d66ffe03e4d879ba1df147d1dd3d9fb1f8bc32d(
    *,
    affilitation: builtins.str,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
