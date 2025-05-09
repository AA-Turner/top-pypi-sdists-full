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
    'GetLaunchTemplateResult',
    'AwaitableGetLaunchTemplateResult',
    'get_launch_template',
    'get_launch_template_output',
]

@pulumi.output_type
class GetLaunchTemplateResult:
    def __init__(__self__, default_version_number=None, latest_version_number=None, launch_template_id=None):
        if default_version_number and not isinstance(default_version_number, str):
            raise TypeError("Expected argument 'default_version_number' to be a str")
        pulumi.set(__self__, "default_version_number", default_version_number)
        if latest_version_number and not isinstance(latest_version_number, str):
            raise TypeError("Expected argument 'latest_version_number' to be a str")
        pulumi.set(__self__, "latest_version_number", latest_version_number)
        if launch_template_id and not isinstance(launch_template_id, str):
            raise TypeError("Expected argument 'launch_template_id' to be a str")
        pulumi.set(__self__, "launch_template_id", launch_template_id)

    @property
    @pulumi.getter(name="defaultVersionNumber")
    def default_version_number(self) -> Optional[builtins.str]:
        """
        The default version of the launch template, such as 2.

        The default version of a launch template cannot be specified in AWS CloudFormation . The default version can be set in the Amazon EC2 console or by using the `modify-launch-template` AWS CLI command.
        """
        return pulumi.get(self, "default_version_number")

    @property
    @pulumi.getter(name="latestVersionNumber")
    def latest_version_number(self) -> Optional[builtins.str]:
        """
        The latest version of the launch template, such as `5` .
        """
        return pulumi.get(self, "latest_version_number")

    @property
    @pulumi.getter(name="launchTemplateId")
    def launch_template_id(self) -> Optional[builtins.str]:
        """
        The ID of the launch template.
        """
        return pulumi.get(self, "launch_template_id")


class AwaitableGetLaunchTemplateResult(GetLaunchTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLaunchTemplateResult(
            default_version_number=self.default_version_number,
            latest_version_number=self.latest_version_number,
            launch_template_id=self.launch_template_id)


def get_launch_template(launch_template_id: Optional[builtins.str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLaunchTemplateResult:
    """
    Specifies the properties for creating a launch template.
     The minimum required properties for specifying a launch template are as follows:
      +  You must specify at least one property for the launch template data.
      +  You can optionally specify a name for the launch template. If you do not specify a name, CFN creates a name for you.

     A launch template can contain some or all of the configuration information to launch an instance. When you launch an instance using a launch template, instance properties that are not specified in the launch template use default values, except the ``ImageId`` property, which has no default value. If you do not specify an AMI ID for the launch template ``ImageId`` property, you must specify an AMI ID for the instance ``ImageId`` property.
     For more information, see [Launch an instance from a launch template](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html) in the *Amazon EC2 User Guide*.


    :param builtins.str launch_template_id: The ID of the launch template.
    """
    __args__ = dict()
    __args__['launchTemplateId'] = launch_template_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getLaunchTemplate', __args__, opts=opts, typ=GetLaunchTemplateResult).value

    return AwaitableGetLaunchTemplateResult(
        default_version_number=pulumi.get(__ret__, 'default_version_number'),
        latest_version_number=pulumi.get(__ret__, 'latest_version_number'),
        launch_template_id=pulumi.get(__ret__, 'launch_template_id'))
def get_launch_template_output(launch_template_id: Optional[pulumi.Input[builtins.str]] = None,
                               opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetLaunchTemplateResult]:
    """
    Specifies the properties for creating a launch template.
     The minimum required properties for specifying a launch template are as follows:
      +  You must specify at least one property for the launch template data.
      +  You can optionally specify a name for the launch template. If you do not specify a name, CFN creates a name for you.

     A launch template can contain some or all of the configuration information to launch an instance. When you launch an instance using a launch template, instance properties that are not specified in the launch template use default values, except the ``ImageId`` property, which has no default value. If you do not specify an AMI ID for the launch template ``ImageId`` property, you must specify an AMI ID for the instance ``ImageId`` property.
     For more information, see [Launch an instance from a launch template](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html) in the *Amazon EC2 User Guide*.


    :param builtins.str launch_template_id: The ID of the launch template.
    """
    __args__ = dict()
    __args__['launchTemplateId'] = launch_template_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ec2:getLaunchTemplate', __args__, opts=opts, typ=GetLaunchTemplateResult)
    return __ret__.apply(lambda __response__: GetLaunchTemplateResult(
        default_version_number=pulumi.get(__response__, 'default_version_number'),
        latest_version_number=pulumi.get(__response__, 'latest_version_number'),
        launch_template_id=pulumi.get(__response__, 'launch_template_id')))
