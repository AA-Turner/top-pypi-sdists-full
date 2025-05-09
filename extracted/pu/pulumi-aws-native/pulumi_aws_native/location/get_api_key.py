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
from .. import outputs as _root_outputs

__all__ = [
    'GetApiKeyResult',
    'AwaitableGetApiKeyResult',
    'get_api_key',
    'get_api_key_output',
]

@pulumi.output_type
class GetApiKeyResult:
    def __init__(__self__, arn=None, create_time=None, description=None, expire_time=None, key_arn=None, restrictions=None, tags=None, update_time=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if expire_time and not isinstance(expire_time, str):
            raise TypeError("Expected argument 'expire_time' to be a str")
        pulumi.set(__self__, "expire_time", expire_time)
        if key_arn and not isinstance(key_arn, str):
            raise TypeError("Expected argument 'key_arn' to be a str")
        pulumi.set(__self__, "key_arn", key_arn)
        if restrictions and not isinstance(restrictions, dict):
            raise TypeError("Expected argument 'restrictions' to be a dict")
        pulumi.set(__self__, "restrictions", restrictions)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter
    def arn(self) -> Optional[builtins.str]:
        """
        The Amazon Resource Name (ARN) for the resource. Used when you need to specify a resource across all AWS .
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[builtins.str]:
        """
        The timestamp for when the API key resource was created in ISO 8601 format: YYYY-MM-DDThh:mm:ss.sssZ.
        """
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[builtins.str]:
        """
        Updates the description for the API key resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> Optional[builtins.str]:
        """
        The optional timestamp for when the API key resource will expire in [ISO 8601 format](https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html) .
        """
        return pulumi.get(self, "expire_time")

    @property
    @pulumi.getter(name="keyArn")
    def key_arn(self) -> Optional[builtins.str]:
        """
        The Amazon Resource Name (ARN) for the API key resource. Used when you need to specify a resource across all AWS .
        """
        return pulumi.get(self, "key_arn")

    @property
    @pulumi.getter
    def restrictions(self) -> Optional['outputs.ApiKeyRestrictions']:
        """
        The API key restrictions for the API key resource.
        """
        return pulumi.get(self, "restrictions")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[builtins.str]:
        """
        The timestamp for when the API key resource was last updated in ISO 8601 format: `YYYY-MM-DDThh:mm:ss.sssZ` .
        """
        return pulumi.get(self, "update_time")


class AwaitableGetApiKeyResult(GetApiKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApiKeyResult(
            arn=self.arn,
            create_time=self.create_time,
            description=self.description,
            expire_time=self.expire_time,
            key_arn=self.key_arn,
            restrictions=self.restrictions,
            tags=self.tags,
            update_time=self.update_time)


def get_api_key(key_name: Optional[builtins.str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApiKeyResult:
    """
    Definition of AWS::Location::APIKey Resource Type


    :param builtins.str key_name: A custom name for the API key resource.
           
           Requirements:
           
           - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
           - Must be a unique API key name.
           - No spaces allowed. For example, `ExampleAPIKey` .
    """
    __args__ = dict()
    __args__['keyName'] = key_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:location:getApiKey', __args__, opts=opts, typ=GetApiKeyResult).value

    return AwaitableGetApiKeyResult(
        arn=pulumi.get(__ret__, 'arn'),
        create_time=pulumi.get(__ret__, 'create_time'),
        description=pulumi.get(__ret__, 'description'),
        expire_time=pulumi.get(__ret__, 'expire_time'),
        key_arn=pulumi.get(__ret__, 'key_arn'),
        restrictions=pulumi.get(__ret__, 'restrictions'),
        tags=pulumi.get(__ret__, 'tags'),
        update_time=pulumi.get(__ret__, 'update_time'))
def get_api_key_output(key_name: Optional[pulumi.Input[builtins.str]] = None,
                       opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetApiKeyResult]:
    """
    Definition of AWS::Location::APIKey Resource Type


    :param builtins.str key_name: A custom name for the API key resource.
           
           Requirements:
           
           - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
           - Must be a unique API key name.
           - No spaces allowed. For example, `ExampleAPIKey` .
    """
    __args__ = dict()
    __args__['keyName'] = key_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:location:getApiKey', __args__, opts=opts, typ=GetApiKeyResult)
    return __ret__.apply(lambda __response__: GetApiKeyResult(
        arn=pulumi.get(__response__, 'arn'),
        create_time=pulumi.get(__response__, 'create_time'),
        description=pulumi.get(__response__, 'description'),
        expire_time=pulumi.get(__response__, 'expire_time'),
        key_arn=pulumi.get(__response__, 'key_arn'),
        restrictions=pulumi.get(__response__, 'restrictions'),
        tags=pulumi.get(__response__, 'tags'),
        update_time=pulumi.get(__response__, 'update_time')))
