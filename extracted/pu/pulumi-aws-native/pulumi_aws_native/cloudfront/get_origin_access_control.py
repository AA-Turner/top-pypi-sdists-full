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
from . import outputs

__all__ = [
    'GetOriginAccessControlResult',
    'AwaitableGetOriginAccessControlResult',
    'get_origin_access_control',
    'get_origin_access_control_output',
]

@pulumi.output_type
class GetOriginAccessControlResult:
    def __init__(__self__, id=None, origin_access_control_config=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if origin_access_control_config and not isinstance(origin_access_control_config, dict):
            raise TypeError("Expected argument 'origin_access_control_config' to be a dict")
        pulumi.set(__self__, "origin_access_control_config", origin_access_control_config)

    @property
    @pulumi.getter
    def id(self) -> Optional[builtins.str]:
        """
        The unique identifier of the origin access control.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="originAccessControlConfig")
    def origin_access_control_config(self) -> Optional['outputs.OriginAccessControlConfig']:
        """
        The origin access control.
        """
        return pulumi.get(self, "origin_access_control_config")


class AwaitableGetOriginAccessControlResult(GetOriginAccessControlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOriginAccessControlResult(
            id=self.id,
            origin_access_control_config=self.origin_access_control_config)


def get_origin_access_control(id: Optional[builtins.str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOriginAccessControlResult:
    """
    Creates a new origin access control in CloudFront. After you create an origin access control, you can add it to an origin in a CloudFront distribution so that CloudFront sends authenticated (signed) requests to the origin.
     This makes it possible to block public access to the origin, allowing viewers (users) to access the origin's content only through CloudFront.
     For more information about using a CloudFront origin access control, see [Restricting access to an origin](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-origin.html) in the *Amazon CloudFront Developer Guide*.


    :param builtins.str id: The unique identifier of the origin access control.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudfront:getOriginAccessControl', __args__, opts=opts, typ=GetOriginAccessControlResult).value

    return AwaitableGetOriginAccessControlResult(
        id=pulumi.get(__ret__, 'id'),
        origin_access_control_config=pulumi.get(__ret__, 'origin_access_control_config'))
def get_origin_access_control_output(id: Optional[pulumi.Input[builtins.str]] = None,
                                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetOriginAccessControlResult]:
    """
    Creates a new origin access control in CloudFront. After you create an origin access control, you can add it to an origin in a CloudFront distribution so that CloudFront sends authenticated (signed) requests to the origin.
     This makes it possible to block public access to the origin, allowing viewers (users) to access the origin's content only through CloudFront.
     For more information about using a CloudFront origin access control, see [Restricting access to an origin](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-origin.html) in the *Amazon CloudFront Developer Guide*.


    :param builtins.str id: The unique identifier of the origin access control.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cloudfront:getOriginAccessControl', __args__, opts=opts, typ=GetOriginAccessControlResult)
    return __ret__.apply(lambda __response__: GetOriginAccessControlResult(
        id=pulumi.get(__response__, 'id'),
        origin_access_control_config=pulumi.get(__response__, 'origin_access_control_config')))
