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
    'GetPublicKeyResult',
    'AwaitableGetPublicKeyResult',
    'get_public_key',
    'get_public_key_output',
]

@pulumi.output_type
class GetPublicKeyResult:
    def __init__(__self__, created_time=None, id=None, public_key_config=None):
        if created_time and not isinstance(created_time, str):
            raise TypeError("Expected argument 'created_time' to be a str")
        pulumi.set(__self__, "created_time", created_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if public_key_config and not isinstance(public_key_config, dict):
            raise TypeError("Expected argument 'public_key_config' to be a dict")
        pulumi.set(__self__, "public_key_config", public_key_config)

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[builtins.str]:
        """
        The date and time when the public key was uploaded.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter
    def id(self) -> Optional[builtins.str]:
        """
        The identifier of the public key.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="publicKeyConfig")
    def public_key_config(self) -> Optional['outputs.PublicKeyConfig']:
        """
        Configuration information about a public key that you can use with [signed URLs and signed cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html), or with [field-level encryption](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/field-level-encryption.html).
        """
        return pulumi.get(self, "public_key_config")


class AwaitableGetPublicKeyResult(GetPublicKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPublicKeyResult(
            created_time=self.created_time,
            id=self.id,
            public_key_config=self.public_key_config)


def get_public_key(id: Optional[builtins.str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPublicKeyResult:
    """
    A public key that you can use with [signed URLs and signed cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html), or with [field-level encryption](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/field-level-encryption.html).


    :param builtins.str id: The identifier of the public key.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:cloudfront:getPublicKey', __args__, opts=opts, typ=GetPublicKeyResult).value

    return AwaitableGetPublicKeyResult(
        created_time=pulumi.get(__ret__, 'created_time'),
        id=pulumi.get(__ret__, 'id'),
        public_key_config=pulumi.get(__ret__, 'public_key_config'))
def get_public_key_output(id: Optional[pulumi.Input[builtins.str]] = None,
                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPublicKeyResult]:
    """
    A public key that you can use with [signed URLs and signed cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html), or with [field-level encryption](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/field-level-encryption.html).


    :param builtins.str id: The identifier of the public key.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:cloudfront:getPublicKey', __args__, opts=opts, typ=GetPublicKeyResult)
    return __ret__.apply(lambda __response__: GetPublicKeyResult(
        created_time=pulumi.get(__response__, 'created_time'),
        id=pulumi.get(__response__, 'id'),
        public_key_config=pulumi.get(__response__, 'public_key_config')))
