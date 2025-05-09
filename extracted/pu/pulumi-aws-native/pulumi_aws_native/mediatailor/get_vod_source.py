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
from ._enums import *

__all__ = [
    'GetVodSourceResult',
    'AwaitableGetVodSourceResult',
    'get_vod_source',
    'get_vod_source_output',
]

@pulumi.output_type
class GetVodSourceResult:
    def __init__(__self__, arn=None, http_package_configurations=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if http_package_configurations and not isinstance(http_package_configurations, list):
            raise TypeError("Expected argument 'http_package_configurations' to be a list")
        pulumi.set(__self__, "http_package_configurations", http_package_configurations)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[builtins.str]:
        """
        <p>The ARN of the VOD source.</p>
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="httpPackageConfigurations")
    def http_package_configurations(self) -> Optional[Sequence['outputs.VodSourceHttpPackageConfiguration']]:
        """
        <p>A list of HTTP package configuration parameters for this VOD source.</p>
        """
        return pulumi.get(self, "http_package_configurations")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags to assign to the VOD source.
        """
        return pulumi.get(self, "tags")


class AwaitableGetVodSourceResult(GetVodSourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVodSourceResult(
            arn=self.arn,
            http_package_configurations=self.http_package_configurations,
            tags=self.tags)


def get_vod_source(source_location_name: Optional[builtins.str] = None,
                   vod_source_name: Optional[builtins.str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVodSourceResult:
    """
    Definition of AWS::MediaTailor::VodSource Resource Type


    :param builtins.str source_location_name: The name of the source location that the VOD source is associated with.
    :param builtins.str vod_source_name: The name of the VOD source.
    """
    __args__ = dict()
    __args__['sourceLocationName'] = source_location_name
    __args__['vodSourceName'] = vod_source_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:mediatailor:getVodSource', __args__, opts=opts, typ=GetVodSourceResult).value

    return AwaitableGetVodSourceResult(
        arn=pulumi.get(__ret__, 'arn'),
        http_package_configurations=pulumi.get(__ret__, 'http_package_configurations'),
        tags=pulumi.get(__ret__, 'tags'))
def get_vod_source_output(source_location_name: Optional[pulumi.Input[builtins.str]] = None,
                          vod_source_name: Optional[pulumi.Input[builtins.str]] = None,
                          opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetVodSourceResult]:
    """
    Definition of AWS::MediaTailor::VodSource Resource Type


    :param builtins.str source_location_name: The name of the source location that the VOD source is associated with.
    :param builtins.str vod_source_name: The name of the VOD source.
    """
    __args__ = dict()
    __args__['sourceLocationName'] = source_location_name
    __args__['vodSourceName'] = vod_source_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:mediatailor:getVodSource', __args__, opts=opts, typ=GetVodSourceResult)
    return __ret__.apply(lambda __response__: GetVodSourceResult(
        arn=pulumi.get(__response__, 'arn'),
        http_package_configurations=pulumi.get(__response__, 'http_package_configurations'),
        tags=pulumi.get(__response__, 'tags')))
