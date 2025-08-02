'''
[![NPM version](https://badge.fury.io/js/cdk-spot-one.svg)](https://badge.fury.io/js/cdk-spot-one)
[![PyPI version](https://badge.fury.io/py/cdk-spot-one.svg)](https://badge.fury.io/py/cdk-spot-one)
![Release](https://github.com/pahud/cdk-spot-one/workflows/Release/badge.svg)

# cdk-spot-one

One spot instance with EIP and defined duration. No interruption.

# Install

Use the npm dist tag to opt in CDKv1 or CDKv2:

```sh
// for CDKv2
npm install cdk-spot-one
or
npm install cdk-spot-one@latest

// for CDKv1
npm install cdk-spot-one@cdkv1
```

# Why

Sometimes we need an Amazon EC2 instance with static fixed IP for testing or development purpose for a duration of
time(probably hours). We need to make sure during this time, no interruption will occur and we don't want to pay
for on-demand rate. `cdk-spot-one` helps you reserve one single spot instance with pre-allocated or new
Elastic IP addresses(EIP) with defined `blockDuration`, during which time the spot instance will be secured with no spot interruption.

Behind the scene, `cdk-spot-one` provisions a spot fleet with capacity of single instance for you and it associates the EIP with this instance. The spot fleet is reserved as spot block with `blockDuration` from one hour up to six hours to ensure the high availability for your spot instance.

Multiple spot instances are possible by simply specifying the `targetCapacity` construct property, but we only associate the EIP with the first spot instance at this moment.

Enjoy your highly durable one spot instance with AWS CDK!

# Constructs

This library provides two major constructs:

## SpotInstance

* Create a spot instance **without** any fleet
* Does **NOT** support [Spot Block](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-requests.html#fixed-duration-spot-instances)
* Support `stop` or `hibernate` instance

Scenario: To leverage the `stop` or `hibernate` capabilities of the spot instance to persist the data in the ebs volume.

## SpotFleet

* Create a spot instance with a [Spot Fleet](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html)
* Support [Spot Block](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-requests.html#fixed-duration-spot-instances)
* Does **NOT** support `stop` or `hibernate` instance

Scenario: To ensure the availability with no disruption with defined period up to 6 hours.

# Sample

## SpotInstance

```python
import { SpotInstance, AmazonMachineImage } from 'cdk-spot-one';

// Default use Amazon Linux 2
new SpotInstance(stack, 'SpotInstance');


// Custom Id use Ubuntu 20.04 Arm64 Server.
new SpotInstance(stack, 'SpotInstanceUbuntu', {
      vpc,
      customAmiId: AmazonMachineImage.UBUNTU_20_04_ARM64.getImage(stack).imageId,
      defaultInstanceType: new InstanceType('t4g.medium'),
      keyName,
      blockDeviceMappings: [{ deviceName: '/dev/sda1', ebs: { volumeSize: 20 } }],
      additionalUserData: ['curl -fsSL https://get.docker.com -o get-docker.sh', 'sudo sh get-docker.sh'],
    });
```

## SpotFleet

```python
import { SpotFleet } from 'cdk-spot-one';

// create the first fleet for one hour and associate with our existing EIP
const fleet = new SpotFleet(stack, 'SpotFleet')

// configure the expiration after 1 hour
fleet.expireAfter(Duration.hours(1))


// create the 2nd fleet with single Gravition 2 instance for 6 hours and associate with new EIP
const fleet2 = new SpotFleet(stack, 'SpotFleet2', {
  blockDuration: BlockDuration.SIX_HOURS,
  eipAllocationId: 'eipalloc-0d1bc6d85895a5410',
  defaultInstanceType: new InstanceType('c6g.large'),
  vpc: fleet.vpc,
})
// configure the expiration after 6 hours
fleet2.expireAfter(Duration.hours(6))

// print the instanceId from each spot fleet
new CfnOutput(stack, 'SpotFleetInstanceId', { value: fleet.instanceId })
new CfnOutput(stack, 'SpotFleet2InstanceId', { value: fleet2.instanceId })
```

# Create spot instances without duration block

```python
const fleet = new SpotFleet(stack, 'SpotFleet', {
  blockDuration: BlockDuration.NONE,
})
```

NOTE: This kind of spot instance will be interrupted by AWS. However the fleet is using type [maintain](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html#spot-fleet-allocation-strategy), the fleet can be refulfilled.

# ARM64 and Graviton 2 support

`cdk-spot-one` selects the latest Amazon Linux 2 AMI for your `ARM64` instances. Simply select the instance types with the `defaultInstanceType` property and the `SpotFleet` will auto configure correct AMI for the instance.

```python
defaultInstanceType: new InstanceType('c6g.large')
```

# ECS Cluster support

See https://github.com/pahud/cdk-spot-one/issues/270#issuecomment-877152685

# Connect with Session Manager(recommended)

You may connect to the spot instance with [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html).

```sh
# make sure you have installed session-manager-plugin
$ session-manager-plugin
# start session
$ aws ssm start-session --target INSTANCE_ID
```

# Connect with EC2 SSH Connect

By default the `cdk-spot-one` does not bind any SSH public key for you on the instance. You are encouraged to use `ec2-instance-connect` to send your public key from local followed by one-time SSH connect.

For example:

```sh
pubkey="$HOME/.ssh/aws_2020_id_rsa.pub"
echo "sending public key to ${instanceId}"
aws ec2-instance-connect send-ssh-public-key --instance-id ${instanceId} --instance-os-user ec2-user \
--ssh-public-key file://${pubkey} --availability-zone ${az}
```

## npx ec2-connect INSTANCE_ID

To connect to the instance, run `npx ec2-connect` as below:

```sh
$ npx ec2-connect i-01f827ab9de7b93a9
```

or

```sh
$ npx ec2-connect i-01f827ab9de7b93a9 ~/.ssh/other_public_key_path
```

If you are using different SSH public key(default is ~/.ssh/id_rsa.pub)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


class AmazonMachineImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-spot-one.AmazonMachineImage",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromSsmParameter")
    @builtins.classmethod
    def from_ssm_parameter(
        cls,
        path: builtins.str,
    ) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        '''
        :param path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b96fcae70713cc804830a1868783ba5186ef848d49f8f4ee0494b271cf397eaf)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sinvoke(cls, "fromSsmParameter", [path]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX")
    def AMAZON_LINUX(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "AMAZON_LINUX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_LINUX_2")
    def AMAZON_LINUX_2(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "AMAZON_LINUX_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CENTOS_7")
    def CENTOS_7(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        '''CentOS product code from https://wiki.centos.org/Cloud/AWS.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "CENTOS_7"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CENTOS_8")
    def CENTOS_8(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "CENTOS_8"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_16_04_AMD64")
    def UBUNTU_16_04_AMD64(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "UBUNTU_16_04_AMD64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_16_04_ARM64")
    def UBUNTU_16_04_ARM64(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "UBUNTU_16_04_ARM64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_18_04_AMD64")
    def UBUNTU_18_04_AMD64(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "UBUNTU_18_04_AMD64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_18_04_ARM64")
    def UBUNTU_18_04_ARM64(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "UBUNTU_18_04_ARM64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_20_04_AMD64")
    def UBUNTU_20_04_AMD64(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "UBUNTU_20_04_AMD64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_20_04_ARM64")
    def UBUNTU_20_04_ARM64(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "UBUNTU_20_04_ARM64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_20_10_AMD64")
    def UBUNTU_20_10_AMD64(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "UBUNTU_20_10_AMD64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_20_10_ARM64")
    def UBUNTU_20_10_ARM64(cls) -> _aws_cdk_aws_ec2_ceddda9d.IMachineImage:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IMachineImage, jsii.sget(cls, "UBUNTU_20_10_ARM64"))


@jsii.enum(jsii_type="cdk-spot-one.BlockDuration")
class BlockDuration(enum.Enum):
    ONE_HOUR = "ONE_HOUR"
    TWO_HOURS = "TWO_HOURS"
    THREE_HOURS = "THREE_HOURS"
    FOUR_HOURS = "FOUR_HOURS"
    FIVE_HOURS = "FIVE_HOURS"
    SIX_HOURS = "SIX_HOURS"
    NONE = "NONE"


@jsii.interface(jsii_type="cdk-spot-one.ILaunchtemplate")
class ILaunchtemplate(typing_extensions.Protocol):
    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        '''
        :param spotfleet: -
        '''
        ...


class _ILaunchtemplateProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-spot-one.ILaunchtemplate"

    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        '''
        :param spotfleet: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a17739aff6cb47bb5f1cc30444aedbbfe369f9697978c076a2308761b65e7f)
            check_type(argname="argument spotfleet", value=spotfleet, expected_type=type_hints["spotfleet"])
        return typing.cast("SpotFleetLaunchTemplateConfig", jsii.invoke(self, "bind", [spotfleet]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILaunchtemplate).__jsii_proxy_class__ = lambda : _ILaunchtemplateProxy


@jsii.enum(jsii_type="cdk-spot-one.InstanceInterruptionBehavior")
class InstanceInterruptionBehavior(enum.Enum):
    HIBERNATE = "HIBERNATE"
    STOP = "STOP"
    TERMINATE = "TERMINATE"


@jsii.implements(ILaunchtemplate)
class LaunchTemplate(metaclass=jsii.JSIIMeta, jsii_type="cdk-spot-one.LaunchTemplate"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        '''
        :param spotfleet: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab13ed4a78ec523cb8eb543eda35c8d88200ff938a6a7fe946cd7c73c0910a33)
            check_type(argname="argument spotfleet", value=spotfleet, expected_type=type_hints["spotfleet"])
        return typing.cast("SpotFleetLaunchTemplateConfig", jsii.invoke(self, "bind", [spotfleet]))


@jsii.data_type(
    jsii_type="cdk-spot-one.LaunchTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "block_device_mappings": "blockDeviceMappings",
        "default_instance_type": "defaultInstanceType",
        "iam_instance_profile": "iamInstanceProfile",
        "image_id": "imageId",
        "instance_market_options": "instanceMarketOptions",
        "key_name": "keyName",
        "security_group": "securityGroup",
        "user_data": "userData",
    },
)
class LaunchTemplateProps:
    def __init__(
        self,
        *,
        block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        iam_instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        image_id: typing.Optional[builtins.str] = None,
        instance_market_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.InstanceMarketOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    ) -> None:
        '''
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param default_instance_type: 
        :param iam_instance_profile: 
        :param image_id: 
        :param instance_market_options: 
        :param key_name: 
        :param security_group: 
        :param user_data: 
        '''
        if isinstance(instance_market_options, dict):
            instance_market_options = _aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.InstanceMarketOptionsProperty(**instance_market_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759b429fb83bcf2652a939c36d250b2bd7e1733f11180b4a30cc4ecc14af472c)
            check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
            check_type(argname="argument default_instance_type", value=default_instance_type, expected_type=type_hints["default_instance_type"])
            check_type(argname="argument iam_instance_profile", value=iam_instance_profile, expected_type=type_hints["iam_instance_profile"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument instance_market_options", value=instance_market_options, expected_type=type_hints["instance_market_options"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if default_instance_type is not None:
            self._values["default_instance_type"] = default_instance_type
        if iam_instance_profile is not None:
            self._values["iam_instance_profile"] = iam_instance_profile
        if image_id is not None:
            self._values["image_id"] = image_id
        if instance_market_options is not None:
            self._values["instance_market_options"] = instance_market_options
        if key_name is not None:
            self._values["key_name"] = key_name
        if security_group is not None:
            self._values["security_group"] = security_group
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty]]:
        '''blockDeviceMappings for config instance.

        :default: - from ami config.
        '''
        result = self._values.get("block_device_mappings")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty]], result)

    @builtins.property
    def default_instance_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        result = self._values.get("default_instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def iam_instance_profile(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile]:
        result = self._values.get("iam_instance_profile")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_market_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.InstanceMarketOptionsProperty]:
        result = self._values.get("instance_market_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.InstanceMarketOptionsProperty], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def user_data(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData]:
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LaunchTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LaunchTemplateResource(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-spot-one.LaunchTemplateResource",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        iam_instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        image_id: typing.Optional[builtins.str] = None,
        instance_market_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.InstanceMarketOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param default_instance_type: 
        :param iam_instance_profile: 
        :param image_id: 
        :param instance_market_options: 
        :param key_name: 
        :param security_group: 
        :param user_data: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bcd9862d3c9cd6ee0b8f560ac41947c0170a5a0c1e4032545f00fcd33671e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LaunchTemplateProps(
            block_device_mappings=block_device_mappings,
            default_instance_type=default_instance_type,
            iam_instance_profile=iam_instance_profile,
            image_id=image_id,
            instance_market_options=instance_market_options,
            key_name=key_name,
            security_group=security_group,
            user_data=user_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="defaultInstanceType")
    def default_instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, jsii.get(self, "defaultInstanceType"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate, jsii.get(self, "resource"))


@jsii.enum(jsii_type="cdk-spot-one.NodeType")
class NodeType(enum.Enum):
    '''Whether the worker nodes should support GPU or just standard instances.'''

    STANDARD = "STANDARD"
    '''Standard instances.'''
    GPU = "GPU"
    '''GPU instances.'''
    INFERENTIA = "INFERENTIA"
    '''Inferentia instances.'''
    ARM = "ARM"
    '''ARM instances.'''


@jsii.data_type(
    jsii_type="cdk-spot-one.SpotFleetLaunchTemplateConfig",
    jsii_struct_bases=[],
    name_mapping={"launch_template": "launchTemplate", "spotfleet": "spotfleet"},
)
class SpotFleetLaunchTemplateConfig:
    def __init__(
        self,
        *,
        launch_template: ILaunchtemplate,
        spotfleet: "SpotFleet",
    ) -> None:
        '''
        :param launch_template: 
        :param spotfleet: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffae7b2d15f14683fd96349764281eea8e2619837bab1c0f79bc019e4e27af44)
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument spotfleet", value=spotfleet, expected_type=type_hints["spotfleet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "launch_template": launch_template,
            "spotfleet": spotfleet,
        }

    @builtins.property
    def launch_template(self) -> ILaunchtemplate:
        result = self._values.get("launch_template")
        assert result is not None, "Required property 'launch_template' is missing"
        return typing.cast(ILaunchtemplate, result)

    @builtins.property
    def spotfleet(self) -> "SpotFleet":
        result = self._values.get("spotfleet")
        assert result is not None, "Required property 'spotfleet' is missing"
        return typing.cast("SpotFleet", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotFleetLaunchTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpotOne(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-spot-one.SpotOne",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        assign_eip: typing.Optional[builtins.bool] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param assign_eip: Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined. Default: true
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param ebs_volume_size: default EBS volume size for the spot instance. Default: 60;
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_profile: instance profile for the resource. Default: - create a new one
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a26dc5b61be007df8d828c7c38f20abe5ccdfcd3569da27060c1b7ffbc292f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SpotOneProps(
            additional_user_data=additional_user_data,
            assign_eip=assign_eip,
            custom_ami_id=custom_ami_id,
            default_instance_type=default_instance_type,
            ebs_volume_size=ebs_volume_size,
            eip_allocation_id=eip_allocation_id,
            instance_interruption_behavior=instance_interruption_behavior,
            instance_profile=instance_profile,
            instance_role=instance_role,
            key_name=key_name,
            security_group=security_group,
            target_capacity=target_capacity,
            vpc=vpc,
            vpc_subnet=vpc_subnet,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="associateEip")
    def _associate_eip(
        self,
        *,
        additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        assign_eip: typing.Optional[builtins.bool] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param assign_eip: Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined. Default: true
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param ebs_volume_size: default EBS volume size for the spot instance. Default: 60;
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_profile: instance profile for the resource. Default: - create a new one
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        '''
        props = SpotOneProps(
            additional_user_data=additional_user_data,
            assign_eip=assign_eip,
            custom_ami_id=custom_ami_id,
            default_instance_type=default_instance_type,
            ebs_volume_size=ebs_volume_size,
            eip_allocation_id=eip_allocation_id,
            instance_interruption_behavior=instance_interruption_behavior,
            instance_profile=instance_profile,
            instance_role=instance_role,
            key_name=key_name,
            security_group=security_group,
            target_capacity=target_capacity,
            vpc=vpc,
            vpc_subnet=vpc_subnet,
        )

        return typing.cast(None, jsii.invoke(self, "associateEip", [props]))

    @jsii.member(jsii_name="createInstanceProfile")
    def _create_instance_profile(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> _aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile:
        '''
        :param role: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57717a069b78acb0f31e14c07d7ca67c7814cad03d88bea04493ce6591978955)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile, jsii.invoke(self, "createInstanceProfile", [role]))

    @jsii.member(jsii_name="createInstanceRole")
    def _create_instance_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createInstanceRole", []))

    @jsii.member(jsii_name="createSecurityGroup")
    def _create_security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.SecurityGroup:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SecurityGroup, jsii.invoke(self, "createSecurityGroup", []))

    @builtins.property
    @jsii.member(jsii_name="defaultInstanceType")
    def default_instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, jsii.get(self, "defaultInstanceType"))

    @builtins.property
    @jsii.member(jsii_name="defaultSecurityGroup")
    def default_security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The default security group of the instance, which only allows TCP 22 SSH ingress rule.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "defaultSecurityGroup"))

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.UserData, jsii.get(self, "userData"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceType"))

    @builtins.property
    @jsii.member(jsii_name="instanceProfile")
    def _instance_profile(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile]:
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile], jsii.get(self, "instanceProfile"))

    @_instance_profile.setter
    def _instance_profile(
        self,
        value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096c67a39b13998b5201b09edc1fa1718e7257df17777f9b99422a44d8781138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceProfile", value)

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def _instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "instanceRole"))

    @_instance_role.setter
    def _instance_role(
        self,
        value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4ca358b50a7c9836fae6a322d56f85089cad135a64ef9eea3c2d7053c9e363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceRole", value)


class _SpotOneProxy(SpotOne):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, SpotOne).__jsii_proxy_class__ = lambda : _SpotOneProxy


@jsii.data_type(
    jsii_type="cdk-spot-one.SpotOneProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_user_data": "additionalUserData",
        "assign_eip": "assignEip",
        "custom_ami_id": "customAmiId",
        "default_instance_type": "defaultInstanceType",
        "ebs_volume_size": "ebsVolumeSize",
        "eip_allocation_id": "eipAllocationId",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "instance_profile": "instanceProfile",
        "instance_role": "instanceRole",
        "key_name": "keyName",
        "security_group": "securityGroup",
        "target_capacity": "targetCapacity",
        "vpc": "vpc",
        "vpc_subnet": "vpcSubnet",
    },
)
class SpotOneProps:
    def __init__(
        self,
        *,
        additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        assign_eip: typing.Optional[builtins.bool] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param assign_eip: Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined. Default: true
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param ebs_volume_size: default EBS volume size for the spot instance. Default: 60;
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_profile: instance profile for the resource. Default: - create a new one
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        '''
        if isinstance(vpc_subnet, dict):
            vpc_subnet = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnet)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52a24783e47934efddfa0ac5714ea66b189584c30fbdd4239bf1f671f91c519)
            check_type(argname="argument additional_user_data", value=additional_user_data, expected_type=type_hints["additional_user_data"])
            check_type(argname="argument assign_eip", value=assign_eip, expected_type=type_hints["assign_eip"])
            check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
            check_type(argname="argument default_instance_type", value=default_instance_type, expected_type=type_hints["default_instance_type"])
            check_type(argname="argument ebs_volume_size", value=ebs_volume_size, expected_type=type_hints["ebs_volume_size"])
            check_type(argname="argument eip_allocation_id", value=eip_allocation_id, expected_type=type_hints["eip_allocation_id"])
            check_type(argname="argument instance_interruption_behavior", value=instance_interruption_behavior, expected_type=type_hints["instance_interruption_behavior"])
            check_type(argname="argument instance_profile", value=instance_profile, expected_type=type_hints["instance_profile"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument target_capacity", value=target_capacity, expected_type=type_hints["target_capacity"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnet", value=vpc_subnet, expected_type=type_hints["vpc_subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_user_data is not None:
            self._values["additional_user_data"] = additional_user_data
        if assign_eip is not None:
            self._values["assign_eip"] = assign_eip
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if default_instance_type is not None:
            self._values["default_instance_type"] = default_instance_type
        if ebs_volume_size is not None:
            self._values["ebs_volume_size"] = ebs_volume_size
        if eip_allocation_id is not None:
            self._values["eip_allocation_id"] = eip_allocation_id
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_profile is not None:
            self._values["instance_profile"] = instance_profile
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if key_name is not None:
            self._values["key_name"] = key_name
        if security_group is not None:
            self._values["security_group"] = security_group
        if target_capacity is not None:
            self._values["target_capacity"] = target_capacity
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet

    @builtins.property
    def additional_user_data(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional commands for user data.

        :default: - no additional user data
        '''
        result = self._values.get("additional_user_data")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assign_eip(self) -> typing.Optional[builtins.bool]:
        '''Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined.

        :default: true
        '''
        result = self._values.get("assign_eip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        '''custom AMI ID.

        :default: - The latest Amaozn Linux 2 AMI ID
        '''
        result = self._values.get("custom_ami_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''default EC2 instance type.

        :default: - t3.large
        '''
        result = self._values.get("default_instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def ebs_volume_size(self) -> typing.Optional[jsii.Number]:
        '''default EBS volume size for the spot instance.

        :default: 60;
        '''
        result = self._values.get("ebs_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def eip_allocation_id(self) -> typing.Optional[builtins.str]:
        '''Allocation ID for your existing Elastic IP Address.

        :defalt: new EIP and its association will be created for the first instance in this spot fleet
        '''
        result = self._values.get("eip_allocation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional[InstanceInterruptionBehavior]:
        '''The behavior when a Spot Instance is interrupted.

        :default: - InstanceInterruptionBehavior.TERMINATE
        '''
        result = self._values.get("instance_interruption_behavior")
        return typing.cast(typing.Optional[InstanceInterruptionBehavior], result)

    @builtins.property
    def instance_profile(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile]:
        '''instance profile for the resource.

        :default: - create a new one
        '''
        result = self._values.get("instance_profile")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''IAM role for the spot instance.'''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''SSH key name.

        :default: - no ssh key will be assigned
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]:
        '''Security group for the spot fleet.

        :default: - allows TCP 22 SSH ingress rule
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup], result)

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        '''number of the target capacity.

        :default: - 1
        '''
        result = self._values.get("target_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC for the spot fleet.

        :default: - new VPC will be created
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC subnet for the spot fleet.

        :default: - public subnet
        '''
        result = self._values.get("vpc_subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotOneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcProvider(
    _aws_cdk_ceddda9d.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-spot-one.VpcProvider",
):
    def __init__(
        self,
        scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        id: typing.Optional[builtins.str] = None,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Creates a new stack.

        :param scope: Parent of this stack, usually an ``App`` or a ``Stage``, but could be any construct.
        :param id: The construct ID of this stack. If ``stackName`` is not explicitly defined, this id (and any parent IDs) will be used to determine the physical ID of the stack.
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aaeda9d6b54e2895822babee76c88ad0329142c535101526027c33e3fd61d7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.StackProps(
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(
        cls,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb11883b5bc26050a41c4df4fdeba25b038be92163f0a70cc4a2efe29771c7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.sinvoke(cls, "getOrCreate", [scope]))


@jsii.data_type(
    jsii_type="cdk-spot-one.BaseSpotFleetProps",
    jsii_struct_bases=[SpotOneProps],
    name_mapping={
        "additional_user_data": "additionalUserData",
        "assign_eip": "assignEip",
        "custom_ami_id": "customAmiId",
        "default_instance_type": "defaultInstanceType",
        "ebs_volume_size": "ebsVolumeSize",
        "eip_allocation_id": "eipAllocationId",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "instance_profile": "instanceProfile",
        "instance_role": "instanceRole",
        "key_name": "keyName",
        "security_group": "securityGroup",
        "target_capacity": "targetCapacity",
        "vpc": "vpc",
        "vpc_subnet": "vpcSubnet",
        "block_device_mappings": "blockDeviceMappings",
        "block_duration": "blockDuration",
        "terminate_instances_with_expiration": "terminateInstancesWithExpiration",
        "valid_from": "validFrom",
        "valid_until": "validUntil",
    },
)
class BaseSpotFleetProps(SpotOneProps):
    def __init__(
        self,
        *,
        additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        assign_eip: typing.Optional[builtins.bool] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        block_duration: typing.Optional[BlockDuration] = None,
        terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
        valid_from: typing.Optional[builtins.str] = None,
        valid_until: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param assign_eip: Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined. Default: true
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param ebs_volume_size: default EBS volume size for the spot instance. Default: 60;
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_profile: instance profile for the resource. Default: - create a new one
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param block_duration: reservce the spot instance as spot block with defined duration. Default: - BlockDuration.ONE_HOUR
        :param terminate_instances_with_expiration: terminate the instance when the allocation is expired. Default: - true
        :param valid_from: the time when the spot fleet allocation starts. Default: - no expiration
        :param valid_until: the time when the spot fleet allocation expires. Default: - no expiration
        '''
        if isinstance(vpc_subnet, dict):
            vpc_subnet = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnet)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a105d8564c89659e1305ead2964e9fb84833bba7cd56bfed8c8314bd869167da)
            check_type(argname="argument additional_user_data", value=additional_user_data, expected_type=type_hints["additional_user_data"])
            check_type(argname="argument assign_eip", value=assign_eip, expected_type=type_hints["assign_eip"])
            check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
            check_type(argname="argument default_instance_type", value=default_instance_type, expected_type=type_hints["default_instance_type"])
            check_type(argname="argument ebs_volume_size", value=ebs_volume_size, expected_type=type_hints["ebs_volume_size"])
            check_type(argname="argument eip_allocation_id", value=eip_allocation_id, expected_type=type_hints["eip_allocation_id"])
            check_type(argname="argument instance_interruption_behavior", value=instance_interruption_behavior, expected_type=type_hints["instance_interruption_behavior"])
            check_type(argname="argument instance_profile", value=instance_profile, expected_type=type_hints["instance_profile"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument target_capacity", value=target_capacity, expected_type=type_hints["target_capacity"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnet", value=vpc_subnet, expected_type=type_hints["vpc_subnet"])
            check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
            check_type(argname="argument block_duration", value=block_duration, expected_type=type_hints["block_duration"])
            check_type(argname="argument terminate_instances_with_expiration", value=terminate_instances_with_expiration, expected_type=type_hints["terminate_instances_with_expiration"])
            check_type(argname="argument valid_from", value=valid_from, expected_type=type_hints["valid_from"])
            check_type(argname="argument valid_until", value=valid_until, expected_type=type_hints["valid_until"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_user_data is not None:
            self._values["additional_user_data"] = additional_user_data
        if assign_eip is not None:
            self._values["assign_eip"] = assign_eip
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if default_instance_type is not None:
            self._values["default_instance_type"] = default_instance_type
        if ebs_volume_size is not None:
            self._values["ebs_volume_size"] = ebs_volume_size
        if eip_allocation_id is not None:
            self._values["eip_allocation_id"] = eip_allocation_id
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_profile is not None:
            self._values["instance_profile"] = instance_profile
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if key_name is not None:
            self._values["key_name"] = key_name
        if security_group is not None:
            self._values["security_group"] = security_group
        if target_capacity is not None:
            self._values["target_capacity"] = target_capacity
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if block_duration is not None:
            self._values["block_duration"] = block_duration
        if terminate_instances_with_expiration is not None:
            self._values["terminate_instances_with_expiration"] = terminate_instances_with_expiration
        if valid_from is not None:
            self._values["valid_from"] = valid_from
        if valid_until is not None:
            self._values["valid_until"] = valid_until

    @builtins.property
    def additional_user_data(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional commands for user data.

        :default: - no additional user data
        '''
        result = self._values.get("additional_user_data")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assign_eip(self) -> typing.Optional[builtins.bool]:
        '''Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined.

        :default: true
        '''
        result = self._values.get("assign_eip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        '''custom AMI ID.

        :default: - The latest Amaozn Linux 2 AMI ID
        '''
        result = self._values.get("custom_ami_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''default EC2 instance type.

        :default: - t3.large
        '''
        result = self._values.get("default_instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def ebs_volume_size(self) -> typing.Optional[jsii.Number]:
        '''default EBS volume size for the spot instance.

        :default: 60;
        '''
        result = self._values.get("ebs_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def eip_allocation_id(self) -> typing.Optional[builtins.str]:
        '''Allocation ID for your existing Elastic IP Address.

        :defalt: new EIP and its association will be created for the first instance in this spot fleet
        '''
        result = self._values.get("eip_allocation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional[InstanceInterruptionBehavior]:
        '''The behavior when a Spot Instance is interrupted.

        :default: - InstanceInterruptionBehavior.TERMINATE
        '''
        result = self._values.get("instance_interruption_behavior")
        return typing.cast(typing.Optional[InstanceInterruptionBehavior], result)

    @builtins.property
    def instance_profile(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile]:
        '''instance profile for the resource.

        :default: - create a new one
        '''
        result = self._values.get("instance_profile")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''IAM role for the spot instance.'''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''SSH key name.

        :default: - no ssh key will be assigned
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]:
        '''Security group for the spot fleet.

        :default: - allows TCP 22 SSH ingress rule
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup], result)

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        '''number of the target capacity.

        :default: - 1
        '''
        result = self._values.get("target_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC for the spot fleet.

        :default: - new VPC will be created
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC subnet for the spot fleet.

        :default: - public subnet
        '''
        result = self._values.get("vpc_subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty]]:
        '''blockDeviceMappings for config instance.

        :default: - from ami config.
        '''
        result = self._values.get("block_device_mappings")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty]], result)

    @builtins.property
    def block_duration(self) -> typing.Optional[BlockDuration]:
        '''reservce the spot instance as spot block with defined duration.

        :default: - BlockDuration.ONE_HOUR
        '''
        result = self._values.get("block_duration")
        return typing.cast(typing.Optional[BlockDuration], result)

    @builtins.property
    def terminate_instances_with_expiration(self) -> typing.Optional[builtins.bool]:
        '''terminate the instance when the allocation is expired.

        :default: - true
        '''
        result = self._values.get("terminate_instances_with_expiration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def valid_from(self) -> typing.Optional[builtins.str]:
        '''the time when the spot fleet allocation starts.

        :default: - no expiration
        '''
        result = self._values.get("valid_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def valid_until(self) -> typing.Optional[builtins.str]:
        '''the time when the spot fleet allocation expires.

        :default: - no expiration
        '''
        result = self._values.get("valid_until")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseSpotFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpotFleet(SpotOne, metaclass=jsii.JSIIMeta, jsii_type="cdk-spot-one.SpotFleet"):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_only: typing.Optional[builtins.bool] = None,
        launch_template: typing.Optional[ILaunchtemplate] = None,
        block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        block_duration: typing.Optional[BlockDuration] = None,
        terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
        valid_from: typing.Optional[builtins.str] = None,
        valid_until: typing.Optional[builtins.str] = None,
        additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        assign_eip: typing.Optional[builtins.bool] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_only: Whether to create spot instance only instead of a fleet. Default: false;
        :param launch_template: Launch template for the spot fleet.
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param block_duration: reservce the spot instance as spot block with defined duration. Default: - BlockDuration.ONE_HOUR
        :param terminate_instances_with_expiration: terminate the instance when the allocation is expired. Default: - true
        :param valid_from: the time when the spot fleet allocation starts. Default: - no expiration
        :param valid_until: the time when the spot fleet allocation expires. Default: - no expiration
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param assign_eip: Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined. Default: true
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param ebs_volume_size: default EBS volume size for the spot instance. Default: 60;
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_profile: instance profile for the resource. Default: - create a new one
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d458e5027f67519ec07e37707891074920db9d67309ed0f82cf13c69eec98e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SpotFleetProps(
            instance_only=instance_only,
            launch_template=launch_template,
            block_device_mappings=block_device_mappings,
            block_duration=block_duration,
            terminate_instances_with_expiration=terminate_instances_with_expiration,
            valid_from=valid_from,
            valid_until=valid_until,
            additional_user_data=additional_user_data,
            assign_eip=assign_eip,
            custom_ami_id=custom_ami_id,
            default_instance_type=default_instance_type,
            ebs_volume_size=ebs_volume_size,
            eip_allocation_id=eip_allocation_id,
            instance_interruption_behavior=instance_interruption_behavior,
            instance_profile=instance_profile,
            instance_role=instance_role,
            key_name=key_name,
            security_group=security_group,
            target_capacity=target_capacity,
            vpc=vpc,
            vpc_subnet=vpc_subnet,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="expireAfter")
    def expire_after(self, duration: _aws_cdk_ceddda9d.Duration) -> None:
        '''
        :param duration: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06f1885da2ec77d6c2f7a3f48b82f0cf225b6276d51c9e828a7a13bae29d94d)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        return typing.cast(None, jsii.invoke(self, "expireAfter", [duration]))

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> ILaunchtemplate:
        return typing.cast(ILaunchtemplate, jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="spotFleetId")
    def spot_fleet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spotFleetId"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''the first instance id in this fleet.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="instanceInterruptionBehavior")
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional[InstanceInterruptionBehavior]:
        '''The behavior when a Spot Instance is interrupted.

        :default: terminate
        '''
        return typing.cast(typing.Optional[InstanceInterruptionBehavior], jsii.get(self, "instanceInterruptionBehavior"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''instance type of the first instance in this fleet.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceType"))

    @builtins.property
    @jsii.member(jsii_name="spotFleetRequestId")
    def spot_fleet_request_id(self) -> typing.Optional[builtins.str]:
        '''SpotFleetRequestId for this spot fleet.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "spotFleetRequestId"))

    @builtins.property
    @jsii.member(jsii_name="targetCapacity")
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetCapacity"))


@jsii.data_type(
    jsii_type="cdk-spot-one.SpotFleetProps",
    jsii_struct_bases=[BaseSpotFleetProps],
    name_mapping={
        "additional_user_data": "additionalUserData",
        "assign_eip": "assignEip",
        "custom_ami_id": "customAmiId",
        "default_instance_type": "defaultInstanceType",
        "ebs_volume_size": "ebsVolumeSize",
        "eip_allocation_id": "eipAllocationId",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "instance_profile": "instanceProfile",
        "instance_role": "instanceRole",
        "key_name": "keyName",
        "security_group": "securityGroup",
        "target_capacity": "targetCapacity",
        "vpc": "vpc",
        "vpc_subnet": "vpcSubnet",
        "block_device_mappings": "blockDeviceMappings",
        "block_duration": "blockDuration",
        "terminate_instances_with_expiration": "terminateInstancesWithExpiration",
        "valid_from": "validFrom",
        "valid_until": "validUntil",
        "instance_only": "instanceOnly",
        "launch_template": "launchTemplate",
    },
)
class SpotFleetProps(BaseSpotFleetProps):
    def __init__(
        self,
        *,
        additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        assign_eip: typing.Optional[builtins.bool] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        block_duration: typing.Optional[BlockDuration] = None,
        terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
        valid_from: typing.Optional[builtins.str] = None,
        valid_until: typing.Optional[builtins.str] = None,
        instance_only: typing.Optional[builtins.bool] = None,
        launch_template: typing.Optional[ILaunchtemplate] = None,
    ) -> None:
        '''
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param assign_eip: Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined. Default: true
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param ebs_volume_size: default EBS volume size for the spot instance. Default: 60;
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_profile: instance profile for the resource. Default: - create a new one
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param block_duration: reservce the spot instance as spot block with defined duration. Default: - BlockDuration.ONE_HOUR
        :param terminate_instances_with_expiration: terminate the instance when the allocation is expired. Default: - true
        :param valid_from: the time when the spot fleet allocation starts. Default: - no expiration
        :param valid_until: the time when the spot fleet allocation expires. Default: - no expiration
        :param instance_only: Whether to create spot instance only instead of a fleet. Default: false;
        :param launch_template: Launch template for the spot fleet.
        '''
        if isinstance(vpc_subnet, dict):
            vpc_subnet = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnet)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439a84c60aa1f25ed6ae1340cf8d297d93c49bc052fd75a145f5c03ed8e12c87)
            check_type(argname="argument additional_user_data", value=additional_user_data, expected_type=type_hints["additional_user_data"])
            check_type(argname="argument assign_eip", value=assign_eip, expected_type=type_hints["assign_eip"])
            check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
            check_type(argname="argument default_instance_type", value=default_instance_type, expected_type=type_hints["default_instance_type"])
            check_type(argname="argument ebs_volume_size", value=ebs_volume_size, expected_type=type_hints["ebs_volume_size"])
            check_type(argname="argument eip_allocation_id", value=eip_allocation_id, expected_type=type_hints["eip_allocation_id"])
            check_type(argname="argument instance_interruption_behavior", value=instance_interruption_behavior, expected_type=type_hints["instance_interruption_behavior"])
            check_type(argname="argument instance_profile", value=instance_profile, expected_type=type_hints["instance_profile"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument target_capacity", value=target_capacity, expected_type=type_hints["target_capacity"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnet", value=vpc_subnet, expected_type=type_hints["vpc_subnet"])
            check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
            check_type(argname="argument block_duration", value=block_duration, expected_type=type_hints["block_duration"])
            check_type(argname="argument terminate_instances_with_expiration", value=terminate_instances_with_expiration, expected_type=type_hints["terminate_instances_with_expiration"])
            check_type(argname="argument valid_from", value=valid_from, expected_type=type_hints["valid_from"])
            check_type(argname="argument valid_until", value=valid_until, expected_type=type_hints["valid_until"])
            check_type(argname="argument instance_only", value=instance_only, expected_type=type_hints["instance_only"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_user_data is not None:
            self._values["additional_user_data"] = additional_user_data
        if assign_eip is not None:
            self._values["assign_eip"] = assign_eip
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if default_instance_type is not None:
            self._values["default_instance_type"] = default_instance_type
        if ebs_volume_size is not None:
            self._values["ebs_volume_size"] = ebs_volume_size
        if eip_allocation_id is not None:
            self._values["eip_allocation_id"] = eip_allocation_id
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_profile is not None:
            self._values["instance_profile"] = instance_profile
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if key_name is not None:
            self._values["key_name"] = key_name
        if security_group is not None:
            self._values["security_group"] = security_group
        if target_capacity is not None:
            self._values["target_capacity"] = target_capacity
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if block_duration is not None:
            self._values["block_duration"] = block_duration
        if terminate_instances_with_expiration is not None:
            self._values["terminate_instances_with_expiration"] = terminate_instances_with_expiration
        if valid_from is not None:
            self._values["valid_from"] = valid_from
        if valid_until is not None:
            self._values["valid_until"] = valid_until
        if instance_only is not None:
            self._values["instance_only"] = instance_only
        if launch_template is not None:
            self._values["launch_template"] = launch_template

    @builtins.property
    def additional_user_data(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional commands for user data.

        :default: - no additional user data
        '''
        result = self._values.get("additional_user_data")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assign_eip(self) -> typing.Optional[builtins.bool]:
        '''Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined.

        :default: true
        '''
        result = self._values.get("assign_eip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        '''custom AMI ID.

        :default: - The latest Amaozn Linux 2 AMI ID
        '''
        result = self._values.get("custom_ami_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''default EC2 instance type.

        :default: - t3.large
        '''
        result = self._values.get("default_instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def ebs_volume_size(self) -> typing.Optional[jsii.Number]:
        '''default EBS volume size for the spot instance.

        :default: 60;
        '''
        result = self._values.get("ebs_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def eip_allocation_id(self) -> typing.Optional[builtins.str]:
        '''Allocation ID for your existing Elastic IP Address.

        :defalt: new EIP and its association will be created for the first instance in this spot fleet
        '''
        result = self._values.get("eip_allocation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional[InstanceInterruptionBehavior]:
        '''The behavior when a Spot Instance is interrupted.

        :default: - InstanceInterruptionBehavior.TERMINATE
        '''
        result = self._values.get("instance_interruption_behavior")
        return typing.cast(typing.Optional[InstanceInterruptionBehavior], result)

    @builtins.property
    def instance_profile(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile]:
        '''instance profile for the resource.

        :default: - create a new one
        '''
        result = self._values.get("instance_profile")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''IAM role for the spot instance.'''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''SSH key name.

        :default: - no ssh key will be assigned
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]:
        '''Security group for the spot fleet.

        :default: - allows TCP 22 SSH ingress rule
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup], result)

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        '''number of the target capacity.

        :default: - 1
        '''
        result = self._values.get("target_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC for the spot fleet.

        :default: - new VPC will be created
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC subnet for the spot fleet.

        :default: - public subnet
        '''
        result = self._values.get("vpc_subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty]]:
        '''blockDeviceMappings for config instance.

        :default: - from ami config.
        '''
        result = self._values.get("block_device_mappings")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty]], result)

    @builtins.property
    def block_duration(self) -> typing.Optional[BlockDuration]:
        '''reservce the spot instance as spot block with defined duration.

        :default: - BlockDuration.ONE_HOUR
        '''
        result = self._values.get("block_duration")
        return typing.cast(typing.Optional[BlockDuration], result)

    @builtins.property
    def terminate_instances_with_expiration(self) -> typing.Optional[builtins.bool]:
        '''terminate the instance when the allocation is expired.

        :default: - true
        '''
        result = self._values.get("terminate_instances_with_expiration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def valid_from(self) -> typing.Optional[builtins.str]:
        '''the time when the spot fleet allocation starts.

        :default: - no expiration
        '''
        result = self._values.get("valid_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def valid_until(self) -> typing.Optional[builtins.str]:
        '''the time when the spot fleet allocation expires.

        :default: - no expiration
        '''
        result = self._values.get("valid_until")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_only(self) -> typing.Optional[builtins.bool]:
        '''Whether to create spot instance only instead of a fleet.

        :default: false;
        '''
        result = self._values.get("instance_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def launch_template(self) -> typing.Optional[ILaunchtemplate]:
        '''Launch template for the spot fleet.'''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional[ILaunchtemplate], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpotInstance(
    SpotOne,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-spot-one.SpotInstance",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        assign_eip: typing.Optional[builtins.bool] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param assign_eip: Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined. Default: true
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param ebs_volume_size: default EBS volume size for the spot instance. Default: 60;
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_profile: instance profile for the resource. Default: - create a new one
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187cb0ee5367d5bba846e3c5a35a89980bbf90e4781e5e2ebfa2f884eef117be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SpotInstanceProps(
            block_device_mappings=block_device_mappings,
            additional_user_data=additional_user_data,
            assign_eip=assign_eip,
            custom_ami_id=custom_ami_id,
            default_instance_type=default_instance_type,
            ebs_volume_size=ebs_volume_size,
            eip_allocation_id=eip_allocation_id,
            instance_interruption_behavior=instance_interruption_behavior,
            instance_profile=instance_profile,
            instance_role=instance_role,
            key_name=key_name,
            security_group=security_group,
            target_capacity=target_capacity,
            vpc=vpc,
            vpc_subnet=vpc_subnet,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceType"))


@jsii.data_type(
    jsii_type="cdk-spot-one.SpotInstanceProps",
    jsii_struct_bases=[SpotOneProps],
    name_mapping={
        "additional_user_data": "additionalUserData",
        "assign_eip": "assignEip",
        "custom_ami_id": "customAmiId",
        "default_instance_type": "defaultInstanceType",
        "ebs_volume_size": "ebsVolumeSize",
        "eip_allocation_id": "eipAllocationId",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "instance_profile": "instanceProfile",
        "instance_role": "instanceRole",
        "key_name": "keyName",
        "security_group": "securityGroup",
        "target_capacity": "targetCapacity",
        "vpc": "vpc",
        "vpc_subnet": "vpcSubnet",
        "block_device_mappings": "blockDeviceMappings",
    },
)
class SpotInstanceProps(SpotOneProps):
    def __init__(
        self,
        *,
        additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
        assign_eip: typing.Optional[builtins.bool] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param assign_eip: Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined. Default: true
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param ebs_volume_size: default EBS volume size for the spot instance. Default: 60;
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_profile: instance profile for the resource. Default: - create a new one
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        '''
        if isinstance(vpc_subnet, dict):
            vpc_subnet = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnet)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd4781df98e5f2f8383b9dbcf7ff65be947f1e85f01066ea2f0a2027a966391)
            check_type(argname="argument additional_user_data", value=additional_user_data, expected_type=type_hints["additional_user_data"])
            check_type(argname="argument assign_eip", value=assign_eip, expected_type=type_hints["assign_eip"])
            check_type(argname="argument custom_ami_id", value=custom_ami_id, expected_type=type_hints["custom_ami_id"])
            check_type(argname="argument default_instance_type", value=default_instance_type, expected_type=type_hints["default_instance_type"])
            check_type(argname="argument ebs_volume_size", value=ebs_volume_size, expected_type=type_hints["ebs_volume_size"])
            check_type(argname="argument eip_allocation_id", value=eip_allocation_id, expected_type=type_hints["eip_allocation_id"])
            check_type(argname="argument instance_interruption_behavior", value=instance_interruption_behavior, expected_type=type_hints["instance_interruption_behavior"])
            check_type(argname="argument instance_profile", value=instance_profile, expected_type=type_hints["instance_profile"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument target_capacity", value=target_capacity, expected_type=type_hints["target_capacity"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnet", value=vpc_subnet, expected_type=type_hints["vpc_subnet"])
            check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_user_data is not None:
            self._values["additional_user_data"] = additional_user_data
        if assign_eip is not None:
            self._values["assign_eip"] = assign_eip
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if default_instance_type is not None:
            self._values["default_instance_type"] = default_instance_type
        if ebs_volume_size is not None:
            self._values["ebs_volume_size"] = ebs_volume_size
        if eip_allocation_id is not None:
            self._values["eip_allocation_id"] = eip_allocation_id
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_profile is not None:
            self._values["instance_profile"] = instance_profile
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if key_name is not None:
            self._values["key_name"] = key_name
        if security_group is not None:
            self._values["security_group"] = security_group
        if target_capacity is not None:
            self._values["target_capacity"] = target_capacity
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings

    @builtins.property
    def additional_user_data(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional commands for user data.

        :default: - no additional user data
        '''
        result = self._values.get("additional_user_data")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assign_eip(self) -> typing.Optional[builtins.bool]:
        '''Auto assign a new EIP on this instance if ``eipAllocationId`` is not defined.

        :default: true
        '''
        result = self._values.get("assign_eip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        '''custom AMI ID.

        :default: - The latest Amaozn Linux 2 AMI ID
        '''
        result = self._values.get("custom_ami_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''default EC2 instance type.

        :default: - t3.large
        '''
        result = self._values.get("default_instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def ebs_volume_size(self) -> typing.Optional[jsii.Number]:
        '''default EBS volume size for the spot instance.

        :default: 60;
        '''
        result = self._values.get("ebs_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def eip_allocation_id(self) -> typing.Optional[builtins.str]:
        '''Allocation ID for your existing Elastic IP Address.

        :defalt: new EIP and its association will be created for the first instance in this spot fleet
        '''
        result = self._values.get("eip_allocation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional[InstanceInterruptionBehavior]:
        '''The behavior when a Spot Instance is interrupted.

        :default: - InstanceInterruptionBehavior.TERMINATE
        '''
        result = self._values.get("instance_interruption_behavior")
        return typing.cast(typing.Optional[InstanceInterruptionBehavior], result)

    @builtins.property
    def instance_profile(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile]:
        '''instance profile for the resource.

        :default: - create a new one
        '''
        result = self._values.get("instance_profile")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''IAM role for the spot instance.'''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''SSH key name.

        :default: - no ssh key will be assigned
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]:
        '''Security group for the spot fleet.

        :default: - allows TCP 22 SSH ingress rule
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup], result)

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        '''number of the target capacity.

        :default: - 1
        '''
        result = self._values.get("target_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC for the spot fleet.

        :default: - new VPC will be created
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''VPC subnet for the spot fleet.

        :default: - public subnet
        '''
        result = self._values.get("vpc_subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty]]:
        '''blockDeviceMappings for config instance.

        :default: - from ami config.
        '''
        result = self._values.get("block_device_mappings")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AmazonMachineImage",
    "BaseSpotFleetProps",
    "BlockDuration",
    "ILaunchtemplate",
    "InstanceInterruptionBehavior",
    "LaunchTemplate",
    "LaunchTemplateProps",
    "LaunchTemplateResource",
    "NodeType",
    "SpotFleet",
    "SpotFleetLaunchTemplateConfig",
    "SpotFleetProps",
    "SpotInstance",
    "SpotInstanceProps",
    "SpotOne",
    "SpotOneProps",
    "VpcProvider",
]

publication.publish()

def _typecheckingstub__b96fcae70713cc804830a1868783ba5186ef848d49f8f4ee0494b271cf397eaf(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a17739aff6cb47bb5f1cc30444aedbbfe369f9697978c076a2308761b65e7f(
    spotfleet: SpotFleet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab13ed4a78ec523cb8eb543eda35c8d88200ff938a6a7fe946cd7c73c0910a33(
    spotfleet: SpotFleet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759b429fb83bcf2652a939c36d250b2bd7e1733f11180b4a30cc4ecc14af472c(
    *,
    block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    iam_instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    image_id: typing.Optional[builtins.str] = None,
    instance_market_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.InstanceMarketOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bcd9862d3c9cd6ee0b8f560ac41947c0170a5a0c1e4032545f00fcd33671e8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    iam_instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    image_id: typing.Optional[builtins.str] = None,
    instance_market_options: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.InstanceMarketOptionsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    user_data: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.UserData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffae7b2d15f14683fd96349764281eea8e2619837bab1c0f79bc019e4e27af44(
    *,
    launch_template: ILaunchtemplate,
    spotfleet: SpotFleet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a26dc5b61be007df8d828c7c38f20abe5ccdfcd3569da27060c1b7ffbc292f7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    assign_eip: typing.Optional[builtins.bool] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    eip_allocation_id: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57717a069b78acb0f31e14c07d7ca67c7814cad03d88bea04493ce6591978955(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096c67a39b13998b5201b09edc1fa1718e7257df17777f9b99422a44d8781138(
    value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4ca358b50a7c9836fae6a322d56f85089cad135a64ef9eea3c2d7053c9e363(
    value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52a24783e47934efddfa0ac5714ea66b189584c30fbdd4239bf1f671f91c519(
    *,
    additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    assign_eip: typing.Optional[builtins.bool] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    eip_allocation_id: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aaeda9d6b54e2895822babee76c88ad0329142c535101526027c33e3fd61d7f(
    scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    id: typing.Optional[builtins.str] = None,
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb11883b5bc26050a41c4df4fdeba25b038be92163f0a70cc4a2efe29771c7d(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a105d8564c89659e1305ead2964e9fb84833bba7cd56bfed8c8314bd869167da(
    *,
    additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    assign_eip: typing.Optional[builtins.bool] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    eip_allocation_id: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    block_duration: typing.Optional[BlockDuration] = None,
    terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
    valid_from: typing.Optional[builtins.str] = None,
    valid_until: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d458e5027f67519ec07e37707891074920db9d67309ed0f82cf13c69eec98e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_only: typing.Optional[builtins.bool] = None,
    launch_template: typing.Optional[ILaunchtemplate] = None,
    block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    block_duration: typing.Optional[BlockDuration] = None,
    terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
    valid_from: typing.Optional[builtins.str] = None,
    valid_until: typing.Optional[builtins.str] = None,
    additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    assign_eip: typing.Optional[builtins.bool] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    eip_allocation_id: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06f1885da2ec77d6c2f7a3f48b82f0cf225b6276d51c9e828a7a13bae29d94d(
    duration: _aws_cdk_ceddda9d.Duration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439a84c60aa1f25ed6ae1340cf8d297d93c49bc052fd75a145f5c03ed8e12c87(
    *,
    additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    assign_eip: typing.Optional[builtins.bool] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    eip_allocation_id: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    block_duration: typing.Optional[BlockDuration] = None,
    terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
    valid_from: typing.Optional[builtins.str] = None,
    valid_until: typing.Optional[builtins.str] = None,
    instance_only: typing.Optional[builtins.bool] = None,
    launch_template: typing.Optional[ILaunchtemplate] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187cb0ee5367d5bba846e3c5a35a89980bbf90e4781e5e2ebfa2f884eef117be(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    assign_eip: typing.Optional[builtins.bool] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    eip_allocation_id: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd4781df98e5f2f8383b9dbcf7ff65be947f1e85f01066ea2f0a2027a966391(
    *,
    additional_user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    assign_eip: typing.Optional[builtins.bool] = None,
    custom_ami_id: typing.Optional[builtins.str] = None,
    default_instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    eip_allocation_id: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    instance_profile: typing.Optional[_aws_cdk_aws_iam_ceddda9d.CfnInstanceProfile] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    key_name: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup] = None,
    target_capacity: typing.Optional[jsii.Number] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    block_device_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
