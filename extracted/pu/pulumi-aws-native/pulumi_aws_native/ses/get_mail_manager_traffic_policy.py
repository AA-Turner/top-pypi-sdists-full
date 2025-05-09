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
    'GetMailManagerTrafficPolicyResult',
    'AwaitableGetMailManagerTrafficPolicyResult',
    'get_mail_manager_traffic_policy',
    'get_mail_manager_traffic_policy_output',
]

@pulumi.output_type
class GetMailManagerTrafficPolicyResult:
    def __init__(__self__, default_action=None, max_message_size_bytes=None, policy_statements=None, tags=None, traffic_policy_arn=None, traffic_policy_id=None, traffic_policy_name=None):
        if default_action and not isinstance(default_action, str):
            raise TypeError("Expected argument 'default_action' to be a str")
        pulumi.set(__self__, "default_action", default_action)
        if max_message_size_bytes and not isinstance(max_message_size_bytes, float):
            raise TypeError("Expected argument 'max_message_size_bytes' to be a float")
        pulumi.set(__self__, "max_message_size_bytes", max_message_size_bytes)
        if policy_statements and not isinstance(policy_statements, list):
            raise TypeError("Expected argument 'policy_statements' to be a list")
        pulumi.set(__self__, "policy_statements", policy_statements)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if traffic_policy_arn and not isinstance(traffic_policy_arn, str):
            raise TypeError("Expected argument 'traffic_policy_arn' to be a str")
        pulumi.set(__self__, "traffic_policy_arn", traffic_policy_arn)
        if traffic_policy_id and not isinstance(traffic_policy_id, str):
            raise TypeError("Expected argument 'traffic_policy_id' to be a str")
        pulumi.set(__self__, "traffic_policy_id", traffic_policy_id)
        if traffic_policy_name and not isinstance(traffic_policy_name, str):
            raise TypeError("Expected argument 'traffic_policy_name' to be a str")
        pulumi.set(__self__, "traffic_policy_name", traffic_policy_name)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> Optional['MailManagerTrafficPolicyAcceptAction']:
        """
        Default action instructs the traﬃc policy to either Allow or Deny (block) messages that fall outside of (or not addressed by) the conditions of your policy statements
        """
        return pulumi.get(self, "default_action")

    @property
    @pulumi.getter(name="maxMessageSizeBytes")
    def max_message_size_bytes(self) -> Optional[builtins.float]:
        """
        The maximum message size in bytes of email which is allowed in by this traffic policy—anything larger will be blocked.
        """
        return pulumi.get(self, "max_message_size_bytes")

    @property
    @pulumi.getter(name="policyStatements")
    def policy_statements(self) -> Optional[Sequence['outputs.MailManagerTrafficPolicyPolicyStatement']]:
        """
        Conditional statements for filtering email traffic.
        """
        return pulumi.get(self, "policy_statements")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The tags used to organize, track, or control access for the resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="trafficPolicyArn")
    def traffic_policy_arn(self) -> Optional[builtins.str]:
        """
        The Amazon Resource Name (ARN) of the traffic policy resource.
        """
        return pulumi.get(self, "traffic_policy_arn")

    @property
    @pulumi.getter(name="trafficPolicyId")
    def traffic_policy_id(self) -> Optional[builtins.str]:
        """
        The identifier of the traffic policy resource.
        """
        return pulumi.get(self, "traffic_policy_id")

    @property
    @pulumi.getter(name="trafficPolicyName")
    def traffic_policy_name(self) -> Optional[builtins.str]:
        """
        The name of the policy.

        The policy name cannot exceed 64 characters and can only include alphanumeric characters, dashes, and underscores.
        """
        return pulumi.get(self, "traffic_policy_name")


class AwaitableGetMailManagerTrafficPolicyResult(GetMailManagerTrafficPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMailManagerTrafficPolicyResult(
            default_action=self.default_action,
            max_message_size_bytes=self.max_message_size_bytes,
            policy_statements=self.policy_statements,
            tags=self.tags,
            traffic_policy_arn=self.traffic_policy_arn,
            traffic_policy_id=self.traffic_policy_id,
            traffic_policy_name=self.traffic_policy_name)


def get_mail_manager_traffic_policy(traffic_policy_id: Optional[builtins.str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMailManagerTrafficPolicyResult:
    """
    Definition of AWS::SES::MailManagerTrafficPolicy Resource Type


    :param builtins.str traffic_policy_id: The identifier of the traffic policy resource.
    """
    __args__ = dict()
    __args__['trafficPolicyId'] = traffic_policy_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ses:getMailManagerTrafficPolicy', __args__, opts=opts, typ=GetMailManagerTrafficPolicyResult).value

    return AwaitableGetMailManagerTrafficPolicyResult(
        default_action=pulumi.get(__ret__, 'default_action'),
        max_message_size_bytes=pulumi.get(__ret__, 'max_message_size_bytes'),
        policy_statements=pulumi.get(__ret__, 'policy_statements'),
        tags=pulumi.get(__ret__, 'tags'),
        traffic_policy_arn=pulumi.get(__ret__, 'traffic_policy_arn'),
        traffic_policy_id=pulumi.get(__ret__, 'traffic_policy_id'),
        traffic_policy_name=pulumi.get(__ret__, 'traffic_policy_name'))
def get_mail_manager_traffic_policy_output(traffic_policy_id: Optional[pulumi.Input[builtins.str]] = None,
                                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetMailManagerTrafficPolicyResult]:
    """
    Definition of AWS::SES::MailManagerTrafficPolicy Resource Type


    :param builtins.str traffic_policy_id: The identifier of the traffic policy resource.
    """
    __args__ = dict()
    __args__['trafficPolicyId'] = traffic_policy_id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:ses:getMailManagerTrafficPolicy', __args__, opts=opts, typ=GetMailManagerTrafficPolicyResult)
    return __ret__.apply(lambda __response__: GetMailManagerTrafficPolicyResult(
        default_action=pulumi.get(__response__, 'default_action'),
        max_message_size_bytes=pulumi.get(__response__, 'max_message_size_bytes'),
        policy_statements=pulumi.get(__response__, 'policy_statements'),
        tags=pulumi.get(__response__, 'tags'),
        traffic_policy_arn=pulumi.get(__response__, 'traffic_policy_arn'),
        traffic_policy_id=pulumi.get(__response__, 'traffic_policy_id'),
        traffic_policy_name=pulumi.get(__response__, 'traffic_policy_name')))
