# coding=utf-8
# *** WARNING: this file was generated by pulumi-language-python. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import builtins
import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities

__all__ = [
    'GetVpcCidrBlockResult',
    'AwaitableGetVpcCidrBlockResult',
    'get_vpc_cidr_block',
    'get_vpc_cidr_block_output',
]

@pulumi.output_type
class GetVpcCidrBlockResult:
    def __init__(__self__, id=None, ip_source=None, ipv6_address_attribute=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_source and not isinstance(ip_source, str):
            raise TypeError("Expected argument 'ip_source' to be a str")
        pulumi.set(__self__, "ip_source", ip_source)
        if ipv6_address_attribute and not isinstance(ipv6_address_attribute, str):
            raise TypeError("Expected argument 'ipv6_address_attribute' to be a str")
        pulumi.set(__self__, "ipv6_address_attribute", ipv6_address_attribute)

    @property
    @pulumi.getter
    def id(self) -> Optional[builtins.str]:
        """
        The Id of the VPC associated CIDR Block.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipSource")
    def ip_source(self) -> Optional[builtins.str]:
        """
        The IP Source of an IPv6 VPC CIDR Block.
        """
        return pulumi.get(self, "ip_source")

    @property
    @pulumi.getter(name="ipv6AddressAttribute")
    def ipv6_address_attribute(self) -> Optional[builtins.str]:
        """
        The value denoting whether an IPv6 VPC CIDR Block is public or private.
        """
        return pulumi.get(self, "ipv6_address_attribute")


class AwaitableGetVpcCidrBlockResult(GetVpcCidrBlockResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcCidrBlockResult(
            id=self.id,
            ip_source=self.ip_source,
            ipv6_address_attribute=self.ipv6_address_attribute)


def get_vpc_cidr_block(id: Optional[builtins.str] = None,
                       vpc_id: Optional[builtins.str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcCidrBlockResult:
    """
    Resource Type definition for AWS::EC2::VPCCidrBlock


    :param builtins.str id: The Id of the VPC associated CIDR Block.
    :param builtins.str vpc_id: The ID of the VPC.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['vpcId'] = vpc_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getVpcCidrBlock', __args__, opts=opts, typ=GetVpcCidrBlockResult).value

    return AwaitableGetVpcCidrBlockResult(
        id=pulumi.get(__ret__, 'id'),
        ip_source=pulumi.get(__ret__, 'ip_source'),
        ipv6_address_attribute=pulumi.get(__ret__, 'ipv6_address_attribute'))
def get_vpc_cidr_block_output(id: Optional[pulumi.Input[builtins.str]] = None,
                              vpc_id: Optional[pulumi.Input[builtins.str]] = None,
                              opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetVpcCidrBlockResult]:
    """
    Resource Type definition for AWS::EC2::VPCCidrBlock


    :param builtins.str id: The Id of the VPC associated CIDR Block.
    :param builtins.str vpc_id: The ID of the VPC.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['vpcId'] = vpc_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getVpcCidrBlock', __args__, opts=opts, typ=GetVpcCidrBlockResult)
    return __ret__.apply(lambda __response__: GetVpcCidrBlockResult(
        id=pulumi.get(__response__, 'id'),
        ip_source=pulumi.get(__response__, 'ip_source'),
        ipv6_address_attribute=pulumi.get(__response__, 'ipv6_address_attribute')))
