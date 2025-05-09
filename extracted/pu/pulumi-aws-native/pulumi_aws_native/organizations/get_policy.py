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
    'GetPolicyResult',
    'AwaitableGetPolicyResult',
    'get_policy',
    'get_policy_output',
]

@pulumi.output_type
class GetPolicyResult:
    def __init__(__self__, arn=None, aws_managed=None, content=None, description=None, id=None, name=None, tags=None, target_ids=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if aws_managed and not isinstance(aws_managed, bool):
            raise TypeError("Expected argument 'aws_managed' to be a bool")
        pulumi.set(__self__, "aws_managed", aws_managed)
        if content and not isinstance(content, dict):
            raise TypeError("Expected argument 'content' to be a dict")
        pulumi.set(__self__, "content", content)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if target_ids and not isinstance(target_ids, list):
            raise TypeError("Expected argument 'target_ids' to be a list")
        pulumi.set(__self__, "target_ids", target_ids)

    @property
    @pulumi.getter
    def arn(self) -> Optional[builtins.str]:
        """
        ARN of the Policy
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsManaged")
    def aws_managed(self) -> Optional[builtins.bool]:
        """
        A boolean value that indicates whether the specified policy is an AWS managed policy. If true, then you can attach the policy to roots, OUs, or accounts, but you cannot edit it.
        """
        return pulumi.get(self, "aws_managed")

    @property
    @pulumi.getter
    def content(self) -> Optional[Any]:
        """
        The Policy text content. For AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::Organizations::Policy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter
    def description(self) -> Optional[builtins.str]:
        """
        Human readable description of the policy
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[builtins.str]:
        """
        Id of the Policy
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[builtins.str]:
        """
        Name of the Policy
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        A list of tags that you want to attach to the newly created policy. For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to null.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetIds")
    def target_ids(self) -> Optional[Sequence[builtins.str]]:
        """
        List of unique identifiers (IDs) of the root, OU, or account that you want to attach the policy to
        """
        return pulumi.get(self, "target_ids")


class AwaitableGetPolicyResult(GetPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyResult(
            arn=self.arn,
            aws_managed=self.aws_managed,
            content=self.content,
            description=self.description,
            id=self.id,
            name=self.name,
            tags=self.tags,
            target_ids=self.target_ids)


def get_policy(id: Optional[builtins.str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyResult:
    """
    Policies in AWS Organizations enable you to manage different features of the AWS accounts in your organization.  You can use policies when all features are enabled in your organization.


    :param builtins.str id: Id of the Policy
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:organizations:getPolicy', __args__, opts=opts, typ=GetPolicyResult).value

    return AwaitableGetPolicyResult(
        arn=pulumi.get(__ret__, 'arn'),
        aws_managed=pulumi.get(__ret__, 'aws_managed'),
        content=pulumi.get(__ret__, 'content'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'),
        target_ids=pulumi.get(__ret__, 'target_ids'))
def get_policy_output(id: Optional[pulumi.Input[builtins.str]] = None,
                      opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetPolicyResult]:
    """
    Policies in AWS Organizations enable you to manage different features of the AWS accounts in your organization.  You can use policies when all features are enabled in your organization.


    :param builtins.str id: Id of the Policy
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:organizations:getPolicy', __args__, opts=opts, typ=GetPolicyResult)
    return __ret__.apply(lambda __response__: GetPolicyResult(
        arn=pulumi.get(__response__, 'arn'),
        aws_managed=pulumi.get(__response__, 'aws_managed'),
        content=pulumi.get(__response__, 'content'),
        description=pulumi.get(__response__, 'description'),
        id=pulumi.get(__response__, 'id'),
        name=pulumi.get(__response__, 'name'),
        tags=pulumi.get(__response__, 'tags'),
        target_ids=pulumi.get(__response__, 'target_ids')))
