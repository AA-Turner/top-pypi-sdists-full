r'''
# CDK fck-nat

A CDK construct for deploying NAT Instances using [fck-nat](https://github.com/AndrewGuenther/fck-nat). The (f)easible (c)ost (k)onfigurable NAT!

* Overpaying for AWS Managed NAT Gateways? fck-nat.
* Want to use NAT instances and stay up-to-date with the latest security patches? fck-nat.
* Want to reuse your Bastion hosts as a NAT? fck-nat.

fck-nat offers a ready-to-use ARM and x86 based AMIs built on Amazon Linux 2023 which can support up to 5Gbps NAT traffic
on a t4g.nano instance. How does that compare to a Managed NAT Gateway?

Hourly rates:

* Managed NAT Gateway hourly: $0.045
* t4g.nano hourly: $0.0042

Per GB rates:

* Managed NAT Gateway per GB: $0.045
* fck-nat per GB: $0.00

Sitting idle, fck-nat costs 10% of a Managed NAT Gateway. In practice, the savings are even greater.

*"But what about AWS' NAT Instance AMI?"*

The official AWS supported NAT Instance AMI hasn't been updates since 2018, is still running Amazon Linux 1 which is
now EOL, and has no ARM support, meaning it can't be deployed on EC2's most cost effective instance types. fck-nat.

*"When would I want to use a Managed NAT Gateway instead of fck-nat?"*

AWS limits outgoing internet bandwidth on EC2 instances to 5Gbps. This means that the highest bandwidth that fck-nat
can support is 5Gbps. This is enough to cover a very broad set of use cases, but if you need additional bandwidth,
you should use Managed NAT Gateway. If AWS were to lift the limit on internet egress bandwidth from EC2, you could
cost-effectively operate fck-nat at speeds up to 25Gbps, but you wouldn't need Managed NAT Gateway then would you?
fck-nat.

Read more about EC2 bandwidth limits here: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-network-bandwidth.html
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

import aws_cdk.aws_autoscaling as _aws_cdk_aws_autoscaling_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d


@jsii.data_type(
    jsii_type="cdk-fck-nat.FckNatInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "asg_update_policy": "asgUpdatePolicy",
        "cloud_watch_config_param": "cloudWatchConfigParam",
        "eip_pool": "eipPool",
        "enable_cloud_watch": "enableCloudWatch",
        "enable_ssm": "enableSsm",
        "key_name": "keyName",
        "key_pair": "keyPair",
        "machine_image": "machineImage",
        "security_group": "securityGroup",
        "user_data": "userData",
    },
)
class FckNatInstanceProps:
    def __init__(
        self,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        asg_update_policy: typing.Optional[_aws_cdk_aws_autoscaling_ceddda9d.UpdatePolicy] = None,
        cloud_watch_config_param: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        eip_pool: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_cloud_watch: typing.Optional[builtins.bool] = None,
        enable_ssm: typing.Optional[builtins.bool] = None,
        key_name: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for a fck-nat instance.

        :param instance_type: Instance type of the fck-nat instance.
        :param asg_update_policy: Configures the auto-scaling group update policy for the fck-nat instances. This will update the existing instance and new instances with the latest ASG configuration. See: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_autoscaling.UpdatePolicy.html Default: - No update policy is applied.
        :param cloud_watch_config_param: Optionally override the base Cloudwatch metric configuration found at https://fck-nat.dev/develop/features/#metrics. If you wish to override the default parameter name, the default configuration contents are stored on the ``FckNatInstanceProvider.DEFAULT_CLOUDWATCH_CONFIG`` constant Default: - If Cloudwatch metrics are enabled, a default configuration will be used.
        :param eip_pool: A list of EIP allocation IDs which can be attached to NAT instances. The number of allocations supplied must be greater than or equal to the number of egress subnets in your VPC.
        :param enable_cloud_watch: Add necessary role permissions and configuration for supplementary CloudWatch metrics. ENABLING THIS FEATURE WILL INCUR ADDITIONAL COSTS! See https://fck-nat.dev/develop/features/#metrics for more details. Default: - Additional Cloudwatch metrics are disabled
        :param enable_ssm: Add necessary role permissions for SSM automatically. Default: - SSM is enabled
        :param key_name: (deprecated) Name of SSH keypair to grant access to instance. Setting this value will not automatically update security groups, that must be done separately. Default: - No SSH access will be possible.
        :param key_pair: SSH keypair to attach to instances. Setting this value will not automatically update security groups, that must be done separately. Default: - No SSH access will be possible.
        :param machine_image: The machine image (AMI) to use. By default, will do an AMI lookup for the latest fck-nat instance image. If you have a specific AMI ID you want to use, pass a ``GenericLinuxImage``. For example:: FckNatInstanceProvider({ instanceType: new ec2.InstanceType('t3.micro'), machineImage: new LookupMachineImage({ name: 'fck-nat-al2023-*-arm64-ebs', owners: ['568608671756'], }) }) Default: - Latest fck-nat instance image
        :param security_group: Security Group for fck-nat instances. Default: - A new security group will be created
        :param user_data: Optionally add commands to the user data of the instance. Default: - No additional user commands are added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4557b0164d909dd1470d454a4f5d57f3ed9a34033b627565f2c5265d5d68c85)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument asg_update_policy", value=asg_update_policy, expected_type=type_hints["asg_update_policy"])
            check_type(argname="argument cloud_watch_config_param", value=cloud_watch_config_param, expected_type=type_hints["cloud_watch_config_param"])
            check_type(argname="argument eip_pool", value=eip_pool, expected_type=type_hints["eip_pool"])
            check_type(argname="argument enable_cloud_watch", value=enable_cloud_watch, expected_type=type_hints["enable_cloud_watch"])
            check_type(argname="argument enable_ssm", value=enable_ssm, expected_type=type_hints["enable_ssm"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
        }
        if asg_update_policy is not None:
            self._values["asg_update_policy"] = asg_update_policy
        if cloud_watch_config_param is not None:
            self._values["cloud_watch_config_param"] = cloud_watch_config_param
        if eip_pool is not None:
            self._values["eip_pool"] = eip_pool
        if enable_cloud_watch is not None:
            self._values["enable_cloud_watch"] = enable_cloud_watch
        if enable_ssm is not None:
            self._values["enable_ssm"] = enable_ssm
        if key_name is not None:
            self._values["key_name"] = key_name
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if security_group is not None:
            self._values["security_group"] = security_group
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        '''Instance type of the fck-nat instance.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, result)

    @builtins.property
    def asg_update_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_autoscaling_ceddda9d.UpdatePolicy]:
        '''Configures the auto-scaling group update policy for the fck-nat instances.

        This will update the existing instance and new instances with the latest ASG configuration.
        See: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_autoscaling.UpdatePolicy.html

        :default: - No update policy is applied.
        '''
        result = self._values.get("asg_update_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_autoscaling_ceddda9d.UpdatePolicy], result)

    @builtins.property
    def cloud_watch_config_param(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter]:
        '''Optionally override the base Cloudwatch metric configuration found at https://fck-nat.dev/develop/features/#metrics.

        If you wish to override the default parameter name, the default configuration contents are stored on the
        ``FckNatInstanceProvider.DEFAULT_CLOUDWATCH_CONFIG`` constant

        :default: - If Cloudwatch metrics are enabled, a default configuration will be used.
        '''
        result = self._values.get("cloud_watch_config_param")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter], result)

    @builtins.property
    def eip_pool(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EIP allocation IDs which can be attached to NAT instances.

        The number of allocations supplied must be
        greater than or equal to the number of egress subnets in your VPC.
        '''
        result = self._values.get("eip_pool")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_cloud_watch(self) -> typing.Optional[builtins.bool]:
        '''Add necessary role permissions and configuration for supplementary CloudWatch metrics.

        ENABLING THIS FEATURE WILL
        INCUR ADDITIONAL COSTS! See https://fck-nat.dev/develop/features/#metrics for more details.

        :default: - Additional Cloudwatch metrics are disabled
        '''
        result = self._values.get("enable_cloud_watch")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_ssm(self) -> typing.Optional[builtins.bool]:
        '''Add necessary role permissions for SSM automatically.

        :default: - SSM is enabled
        '''
        result = self._values.get("enable_ssm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of SSH keypair to grant access to instance.

        Setting this value will not automatically update security groups,
        that must be done separately.

        :default: - No SSH access will be possible.

        :deprecated: - CDK has deprecated the ``keyName`` parameter, use ``keyPair`` instead.

        :stability: deprecated
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair]:
        '''SSH keypair to attach to instances.

        Setting this value will not automatically update security groups, that must be
        done separately.

        :default: - No SSH access will be possible.
        '''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair], result)

    @builtins.property
    def machine_image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''The machine image (AMI) to use.

        By default, will do an AMI lookup for the latest fck-nat instance image.

        If you have a specific AMI ID you want to use, pass a ``GenericLinuxImage``. For example::

           FckNatInstanceProvider({
             instanceType: new ec2.InstanceType('t3.micro'),
             machineImage: new LookupMachineImage({
               name: 'fck-nat-al2023-*-arm64-ebs',
               owners: ['568608671756'],
             })
           })

        :default: - Latest fck-nat instance image
        '''
        result = self._values.get("machine_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Group for fck-nat instances.

        :default: - A new security group will be created
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def user_data(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optionally add commands to the user data of the instance.

        :default: - No additional user commands are added.
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FckNatInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IConnectable)
class FckNatInstanceProvider(
    _aws_cdk_aws_ec2_ceddda9d.NatProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-fck-nat.FckNatInstanceProvider",
):
    def __init__(
        self,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        asg_update_policy: typing.Optional[_aws_cdk_aws_autoscaling_ceddda9d.UpdatePolicy] = None,
        cloud_watch_config_param: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
        eip_pool: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_cloud_watch: typing.Optional[builtins.bool] = None,
        enable_ssm: typing.Optional[builtins.bool] = None,
        key_name: typing.Optional[builtins.str] = None,
        key_pair: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instance_type: Instance type of the fck-nat instance.
        :param asg_update_policy: Configures the auto-scaling group update policy for the fck-nat instances. This will update the existing instance and new instances with the latest ASG configuration. See: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_autoscaling.UpdatePolicy.html Default: - No update policy is applied.
        :param cloud_watch_config_param: Optionally override the base Cloudwatch metric configuration found at https://fck-nat.dev/develop/features/#metrics. If you wish to override the default parameter name, the default configuration contents are stored on the ``FckNatInstanceProvider.DEFAULT_CLOUDWATCH_CONFIG`` constant Default: - If Cloudwatch metrics are enabled, a default configuration will be used.
        :param eip_pool: A list of EIP allocation IDs which can be attached to NAT instances. The number of allocations supplied must be greater than or equal to the number of egress subnets in your VPC.
        :param enable_cloud_watch: Add necessary role permissions and configuration for supplementary CloudWatch metrics. ENABLING THIS FEATURE WILL INCUR ADDITIONAL COSTS! See https://fck-nat.dev/develop/features/#metrics for more details. Default: - Additional Cloudwatch metrics are disabled
        :param enable_ssm: Add necessary role permissions for SSM automatically. Default: - SSM is enabled
        :param key_name: (deprecated) Name of SSH keypair to grant access to instance. Setting this value will not automatically update security groups, that must be done separately. Default: - No SSH access will be possible.
        :param key_pair: SSH keypair to attach to instances. Setting this value will not automatically update security groups, that must be done separately. Default: - No SSH access will be possible.
        :param machine_image: The machine image (AMI) to use. By default, will do an AMI lookup for the latest fck-nat instance image. If you have a specific AMI ID you want to use, pass a ``GenericLinuxImage``. For example:: FckNatInstanceProvider({ instanceType: new ec2.InstanceType('t3.micro'), machineImage: new LookupMachineImage({ name: 'fck-nat-al2023-*-arm64-ebs', owners: ['568608671756'], }) }) Default: - Latest fck-nat instance image
        :param security_group: Security Group for fck-nat instances. Default: - A new security group will be created
        :param user_data: Optionally add commands to the user data of the instance. Default: - No additional user commands are added.
        '''
        props = FckNatInstanceProps(
            instance_type=instance_type,
            asg_update_policy=asg_update_policy,
            cloud_watch_config_param=cloud_watch_config_param,
            eip_pool=eip_pool,
            enable_cloud_watch=enable_cloud_watch,
            enable_ssm=enable_ssm,
            key_name=key_name,
            key_pair=key_pair,
            machine_image=machine_image,
            security_group=security_group,
            user_data=user_data,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="configureNat")
    def configure_nat(
        self,
        *,
        nat_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
        private_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> None:
        '''Called by the VPC to configure NAT.

        Don't call this directly, the VPC will call it automatically.

        :param nat_subnets: The public subnets where the NAT providers need to be placed.
        :param private_subnets: The private subnets that need to route through the NAT providers. There may be more private subnets than public subnets with NAT providers.
        :param vpc: The VPC we're configuring NAT for.
        '''
        options = _aws_cdk_aws_ec2_ceddda9d.ConfigureNatOptions(
            nat_subnets=nat_subnets, private_subnets=private_subnets, vpc=vpc
        )

        return typing.cast(None, jsii.invoke(self, "configureNat", [options]))

    @jsii.member(jsii_name="configureSubnet")
    def configure_subnet(self, subnet: _aws_cdk_aws_ec2_ceddda9d.PrivateSubnet) -> None:
        '''Configures subnet with the gateway.

        Don't call this directly, the VPC will call it automatically.

        :param subnet: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2530e48e0fe57e3382c88c654d9132a4425b047a1cbece5fb1b57592d62710ba)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        return typing.cast(None, jsii.invoke(self, "configureSubnet", [subnet]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMI_NAME")
    def AMI_NAME(cls) -> builtins.str:
        '''The AMI name used internally when calling ``LookupMachineImage``.

        Can be referenced if you wish to do AMI lookups
        externally.
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "AMI_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMI_OWNER")
    def AMI_OWNER(cls) -> builtins.str:
        '''The AMI owner used internally when calling ``LookupMachineImage``.

        Can be referenced if you wish to do AMI lookups
        externally.
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "AMI_OWNER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_CLOUDWATCH_CONFIG")
    def DEFAULT_CLOUDWATCH_CONFIG(cls) -> typing.Any:
        '''The default CloudWatch config used when additional CloudWatch metric reporting is enabled.'''
        return typing.cast(typing.Any, jsii.sget(cls, "DEFAULT_CLOUDWATCH_CONFIG"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(
        self,
    ) -> typing.List[_aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup]:
        '''The ASGs (Auto Scaling Groups) managing the NAT instances.

        These can be retrieved to get metrics and
        '''
        return typing.cast(typing.List[_aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup], jsii.get(self, "autoScalingGroups"))

    @builtins.property
    @jsii.member(jsii_name="configuredGateways")
    def configured_gateways(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.GatewayConfig]:
        '''Return list of gateways spawned by the provider.'''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.GatewayConfig], jsii.get(self, "configuredGateways"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''Manage the Security Groups associated with the NAT instances.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''The instance role attached with the NAT instances.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The Security Group associated with the NAT instances.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))


__all__ = [
    "FckNatInstanceProps",
    "FckNatInstanceProvider",
]

publication.publish()

def _typecheckingstub__c4557b0164d909dd1470d454a4f5d57f3ed9a34033b627565f2c5265d5d68c85(
    *,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    asg_update_policy: typing.Optional[_aws_cdk_aws_autoscaling_ceddda9d.UpdatePolicy] = None,
    cloud_watch_config_param: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.IStringParameter] = None,
    eip_pool: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_cloud_watch: typing.Optional[builtins.bool] = None,
    enable_ssm: typing.Optional[builtins.bool] = None,
    key_name: typing.Optional[builtins.str] = None,
    key_pair: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IKeyPair] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    user_data: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2530e48e0fe57e3382c88c654d9132a4425b047a1cbece5fb1b57592d62710ba(
    subnet: _aws_cdk_aws_ec2_ceddda9d.PrivateSubnet,
) -> None:
    """Type checking stubs"""
    pass
