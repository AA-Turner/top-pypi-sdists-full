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
from ._enums import *

__all__ = [
    'GetAppResult',
    'AwaitableGetAppResult',
    'get_app',
    'get_app_output',
]

@pulumi.output_type
class GetAppResult:
    def __init__(__self__, app_arn=None):
        if app_arn and not isinstance(app_arn, str):
            raise TypeError("Expected argument 'app_arn' to be a str")
        pulumi.set(__self__, "app_arn", app_arn)

    @property
    @pulumi.getter(name="appArn")
    def app_arn(self) -> Optional[builtins.str]:
        """
        The Amazon Resource Name (ARN) of the app.
        """
        return pulumi.get(self, "app_arn")


class AwaitableGetAppResult(GetAppResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAppResult(
            app_arn=self.app_arn)


def get_app(app_name: Optional[builtins.str] = None,
            app_type: Optional['AppType'] = None,
            domain_id: Optional[builtins.str] = None,
            user_profile_name: Optional[builtins.str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAppResult:
    """
    Resource Type definition for AWS::SageMaker::App


    :param builtins.str app_name: The name of the app.
    :param 'AppType' app_type: The type of app.
    :param builtins.str domain_id: The domain ID.
    :param builtins.str user_profile_name: The user profile name.
    """
    __args__ = dict()
    __args__['appName'] = app_name
    __args__['appType'] = app_type
    __args__['domainId'] = domain_id
    __args__['userProfileName'] = user_profile_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:sagemaker:getApp', __args__, opts=opts, typ=GetAppResult).value

    return AwaitableGetAppResult(
        app_arn=pulumi.get(__ret__, 'app_arn'))
def get_app_output(app_name: Optional[pulumi.Input[builtins.str]] = None,
                   app_type: Optional[pulumi.Input['AppType']] = None,
                   domain_id: Optional[pulumi.Input[builtins.str]] = None,
                   user_profile_name: Optional[pulumi.Input[builtins.str]] = None,
                   opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetAppResult]:
    """
    Resource Type definition for AWS::SageMaker::App


    :param builtins.str app_name: The name of the app.
    :param 'AppType' app_type: The type of app.
    :param builtins.str domain_id: The domain ID.
    :param builtins.str user_profile_name: The user profile name.
    """
    __args__ = dict()
    __args__['appName'] = app_name
    __args__['appType'] = app_type
    __args__['domainId'] = domain_id
    __args__['userProfileName'] = user_profile_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:sagemaker:getApp', __args__, opts=opts, typ=GetAppResult)
    return __ret__.apply(lambda __response__: GetAppResult(
        app_arn=pulumi.get(__response__, 'app_arn')))
