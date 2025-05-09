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
from .. import outputs as _root_outputs

__all__ = [
    'GetPermissionResult',
    'AwaitableGetPermissionResult',
    'get_permission',
    'get_permission_output',
]

@pulumi.output_type
class GetPermissionResult:
    def __init__(__self__, arn=None, is_resource_type_default=None, permission_type=None, tags=None, version=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if is_resource_type_default and not isinstance(is_resource_type_default, bool):
            raise TypeError("Expected argument 'is_resource_type_default' to be a bool")
        pulumi.set(__self__, "is_resource_type_default", is_resource_type_default)
        if permission_type and not isinstance(permission_type, str):
            raise TypeError("Expected argument 'permission_type' to be a str")
        pulumi.set(__self__, "permission_type", permission_type)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def arn(self) -> Optional[builtins.str]:
        """
        The Amazon Resource Name (ARN) of the new permission.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="isResourceTypeDefault")
    def is_resource_type_default(self) -> Optional[builtins.bool]:
        """
        Set to true to use this as the default permission.
        """
        return pulumi.get(self, "is_resource_type_default")

    @property
    @pulumi.getter(name="permissionType")
    def permission_type(self) -> Optional[builtins.str]:
        """
        The type of managed permission. This can be one of the following values:

        - *AWS_MANAGED_PERMISSION* – AWS created and manages this managed permission. You can associate it with your resource shares, but you can't modify it.
        - *CUSTOMER_MANAGED_PERMISSION* – You, or another principal in your account created this managed permission. You can associate it with your resource shares and create new versions that have different permissions.
        """
        return pulumi.get(self, "permission_type")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        Specifies a list of one or more tag key and value pairs to attach to the permission.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def version(self) -> Optional[builtins.str]:
        """
        Version of the permission.
        """
        return pulumi.get(self, "version")


class AwaitableGetPermissionResult(GetPermissionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPermissionResult(
            arn=self.arn,
            is_resource_type_default=self.is_resource_type_default,
            permission_type=self.permission_type,
            tags=self.tags,
            version=self.version)


def get_permission(arn: Optional[builtins.str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPermissionResult:
    """
    Resource type definition for AWS::RAM::Permission


    :param builtins.str arn: The Amazon Resource Name (ARN) of the new permission.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ram:getPermission', __args__, opts=opts, typ=GetPermissionResult).value

    return AwaitableGetPermissionResult(
        arn=pulumi.get(__ret__, 'arn'),
        is_resource_type_default=pulumi.get(__ret__, 'is_resource_type_default'),
        permission_type=pulumi.get(__ret__, 'permission_type'),
        tags=pulumi.get(__ret__, 'tags'),
        version=pulumi.get(__ret__, 'version'))
def get_permission_output(arn: Optional[pulumi.Input[builtins.str]] = None,
                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPermissionResult]:
    """
    Resource type definition for AWS::RAM::Permission


    :param builtins.str arn: The Amazon Resource Name (ARN) of the new permission.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ram:getPermission', __args__, opts=opts, typ=GetPermissionResult)
    return __ret__.apply(lambda __response__: GetPermissionResult(
        arn=pulumi.get(__response__, 'arn'),
        is_resource_type_default=pulumi.get(__response__, 'is_resource_type_default'),
        permission_type=pulumi.get(__response__, 'permission_type'),
        tags=pulumi.get(__response__, 'tags'),
        version=pulumi.get(__response__, 'version')))
