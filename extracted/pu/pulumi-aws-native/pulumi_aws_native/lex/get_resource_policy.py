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
    'GetResourcePolicyResult',
    'AwaitableGetResourcePolicyResult',
    'get_resource_policy',
    'get_resource_policy_output',
]

@pulumi.output_type
class GetResourcePolicyResult:
    def __init__(__self__, id=None, policy=None, resource_arn=None, revision_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy and not isinstance(policy, dict):
            raise TypeError("Expected argument 'policy' to be a dict")
        pulumi.set(__self__, "policy", policy)
        if resource_arn and not isinstance(resource_arn, str):
            raise TypeError("Expected argument 'resource_arn' to be a str")
        pulumi.set(__self__, "resource_arn", resource_arn)
        if revision_id and not isinstance(revision_id, str):
            raise TypeError("Expected argument 'revision_id' to be a str")
        pulumi.set(__self__, "revision_id", revision_id)

    @property
    @pulumi.getter
    def id(self) -> Optional[builtins.str]:
        """
        The identifier of the resource policy.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def policy(self) -> Optional['outputs.ResourcePolicyPolicy']:
        """
        A resource policy to add to the resource. The policy is a JSON structure that contains one or more statements that define the policy. The policy must follow IAM syntax. If the policy isn't valid, Amazon Lex returns a validation exception.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> Optional[builtins.str]:
        """
        The Amazon Resource Name (ARN) of the bot or bot alias that the resource policy is attached to.
        """
        return pulumi.get(self, "resource_arn")

    @property
    @pulumi.getter(name="revisionId")
    def revision_id(self) -> Optional[builtins.str]:
        """
        Specifies the current revision of a resource policy.
        """
        return pulumi.get(self, "revision_id")


class AwaitableGetResourcePolicyResult(GetResourcePolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourcePolicyResult(
            id=self.id,
            policy=self.policy,
            resource_arn=self.resource_arn,
            revision_id=self.revision_id)


def get_resource_policy(id: Optional[builtins.str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourcePolicyResult:
    """
    A resource policy with specified policy statements that attaches to a Lex bot or bot alias.


    :param builtins.str id: The identifier of the resource policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:lex:getResourcePolicy', __args__, opts=opts, typ=GetResourcePolicyResult).value

    return AwaitableGetResourcePolicyResult(
        id=pulumi.get(__ret__, 'id'),
        policy=pulumi.get(__ret__, 'policy'),
        resource_arn=pulumi.get(__ret__, 'resource_arn'),
        revision_id=pulumi.get(__ret__, 'revision_id'))
def get_resource_policy_output(id: Optional[pulumi.Input[builtins.str]] = None,
                               opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetResourcePolicyResult]:
    """
    A resource policy with specified policy statements that attaches to a Lex bot or bot alias.


    :param builtins.str id: The identifier of the resource policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:lex:getResourcePolicy', __args__, opts=opts, typ=GetResourcePolicyResult)
    return __ret__.apply(lambda __response__: GetResourcePolicyResult(
        id=pulumi.get(__response__, 'id'),
        policy=pulumi.get(__response__, 'policy'),
        resource_arn=pulumi.get(__response__, 'resource_arn'),
        revision_id=pulumi.get(__response__, 'revision_id')))
