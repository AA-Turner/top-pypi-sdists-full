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
    'GetStreamResult',
    'AwaitableGetStreamResult',
    'get_stream',
    'get_stream_output',
]

@pulumi.output_type
class GetStreamResult:
    def __init__(__self__, arn=None, desired_shard_level_metrics=None, retention_period_hours=None, shard_count=None, stream_encryption=None, stream_mode_details=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if desired_shard_level_metrics and not isinstance(desired_shard_level_metrics, list):
            raise TypeError("Expected argument 'desired_shard_level_metrics' to be a list")
        pulumi.set(__self__, "desired_shard_level_metrics", desired_shard_level_metrics)
        if retention_period_hours and not isinstance(retention_period_hours, int):
            raise TypeError("Expected argument 'retention_period_hours' to be a int")
        pulumi.set(__self__, "retention_period_hours", retention_period_hours)
        if shard_count and not isinstance(shard_count, int):
            raise TypeError("Expected argument 'shard_count' to be a int")
        pulumi.set(__self__, "shard_count", shard_count)
        if stream_encryption and not isinstance(stream_encryption, dict):
            raise TypeError("Expected argument 'stream_encryption' to be a dict")
        pulumi.set(__self__, "stream_encryption", stream_encryption)
        if stream_mode_details and not isinstance(stream_mode_details, dict):
            raise TypeError("Expected argument 'stream_mode_details' to be a dict")
        pulumi.set(__self__, "stream_mode_details", stream_mode_details)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[builtins.str]:
        """
        The Amazon resource name (ARN) of the Kinesis stream
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="desiredShardLevelMetrics")
    def desired_shard_level_metrics(self) -> Optional[Sequence['StreamEnhancedMetric']]:
        """
        The final list of shard-level metrics
        """
        return pulumi.get(self, "desired_shard_level_metrics")

    @property
    @pulumi.getter(name="retentionPeriodHours")
    def retention_period_hours(self) -> Optional[builtins.int]:
        """
        The number of hours for the data records that are stored in shards to remain accessible.
        """
        return pulumi.get(self, "retention_period_hours")

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> Optional[builtins.int]:
        """
        The number of shards that the stream uses. Required when StreamMode = PROVISIONED is passed.
        """
        return pulumi.get(self, "shard_count")

    @property
    @pulumi.getter(name="streamEncryption")
    def stream_encryption(self) -> Optional['outputs.StreamEncryption']:
        """
        When specified, enables or updates server-side encryption using an AWS KMS key for a specified stream.
        """
        return pulumi.get(self, "stream_encryption")

    @property
    @pulumi.getter(name="streamModeDetails")
    def stream_mode_details(self) -> Optional['outputs.StreamModeDetails']:
        """
        The mode in which the stream is running.
        """
        return pulumi.get(self, "stream_mode_details")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        An arbitrary set of tags (key–value pairs) to associate with the Kinesis stream.
        """
        return pulumi.get(self, "tags")


class AwaitableGetStreamResult(GetStreamResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStreamResult(
            arn=self.arn,
            desired_shard_level_metrics=self.desired_shard_level_metrics,
            retention_period_hours=self.retention_period_hours,
            shard_count=self.shard_count,
            stream_encryption=self.stream_encryption,
            stream_mode_details=self.stream_mode_details,
            tags=self.tags)


def get_stream(name: Optional[builtins.str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStreamResult:
    """
    Resource Type definition for AWS::Kinesis::Stream


    :param builtins.str name: The name of the Kinesis stream.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kinesis:getStream', __args__, opts=opts, typ=GetStreamResult).value

    return AwaitableGetStreamResult(
        arn=pulumi.get(__ret__, 'arn'),
        desired_shard_level_metrics=pulumi.get(__ret__, 'desired_shard_level_metrics'),
        retention_period_hours=pulumi.get(__ret__, 'retention_period_hours'),
        shard_count=pulumi.get(__ret__, 'shard_count'),
        stream_encryption=pulumi.get(__ret__, 'stream_encryption'),
        stream_mode_details=pulumi.get(__ret__, 'stream_mode_details'),
        tags=pulumi.get(__ret__, 'tags'))
def get_stream_output(name: Optional[pulumi.Input[builtins.str]] = None,
                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetStreamResult]:
    """
    Resource Type definition for AWS::Kinesis::Stream


    :param builtins.str name: The name of the Kinesis stream.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:kinesis:getStream', __args__, opts=opts, typ=GetStreamResult)
    return __ret__.apply(lambda __response__: GetStreamResult(
        arn=pulumi.get(__response__, 'arn'),
        desired_shard_level_metrics=pulumi.get(__response__, 'desired_shard_level_metrics'),
        retention_period_hours=pulumi.get(__response__, 'retention_period_hours'),
        shard_count=pulumi.get(__response__, 'shard_count'),
        stream_encryption=pulumi.get(__response__, 'stream_encryption'),
        stream_mode_details=pulumi.get(__response__, 'stream_mode_details'),
        tags=pulumi.get(__response__, 'tags')))
