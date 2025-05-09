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
from ._enums import *

__all__ = [
    'GetDistributionConfigurationResult',
    'AwaitableGetDistributionConfigurationResult',
    'get_distribution_configuration',
    'get_distribution_configuration_output',
]

@pulumi.output_type
class GetDistributionConfigurationResult:
    def __init__(__self__, arn=None, description=None, distributions=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if distributions and not isinstance(distributions, list):
            raise TypeError("Expected argument 'distributions' to be a list")
        pulumi.set(__self__, "distributions", distributions)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[builtins.str]:
        """
        The Amazon Resource Name (ARN) of the distribution configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[builtins.str]:
        """
        The description of the distribution configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def distributions(self) -> Optional[Sequence['outputs.DistributionConfigurationDistribution']]:
        """
        The distributions of the distribution configuration.
        """
        return pulumi.get(self, "distributions")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, builtins.str]]:
        """
        The tags associated with the component.
        """
        return pulumi.get(self, "tags")


class AwaitableGetDistributionConfigurationResult(GetDistributionConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDistributionConfigurationResult(
            arn=self.arn,
            description=self.description,
            distributions=self.distributions,
            tags=self.tags)


def get_distribution_configuration(arn: Optional[builtins.str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDistributionConfigurationResult:
    """
    Resource schema for AWS::ImageBuilder::DistributionConfiguration


    :param builtins.str arn: The Amazon Resource Name (ARN) of the distribution configuration.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:imagebuilder:getDistributionConfiguration', __args__, opts=opts, typ=GetDistributionConfigurationResult).value

    return AwaitableGetDistributionConfigurationResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        distributions=pulumi.get(__ret__, 'distributions'),
        tags=pulumi.get(__ret__, 'tags'))
def get_distribution_configuration_output(arn: Optional[pulumi.Input[builtins.str]] = None,
                                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetDistributionConfigurationResult]:
    """
    Resource schema for AWS::ImageBuilder::DistributionConfiguration


    :param builtins.str arn: The Amazon Resource Name (ARN) of the distribution configuration.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:imagebuilder:getDistributionConfiguration', __args__, opts=opts, typ=GetDistributionConfigurationResult)
    return __ret__.apply(lambda __response__: GetDistributionConfigurationResult(
        arn=pulumi.get(__response__, 'arn'),
        description=pulumi.get(__response__, 'description'),
        distributions=pulumi.get(__response__, 'distributions'),
        tags=pulumi.get(__response__, 'tags')))
