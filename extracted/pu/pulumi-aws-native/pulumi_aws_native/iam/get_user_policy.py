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
    'GetUserPolicyResult',
    'AwaitableGetUserPolicyResult',
    'get_user_policy',
    'get_user_policy_output',
]

@pulumi.output_type
class GetUserPolicyResult:
    def __init__(__self__, policy_document=None):
        if policy_document and not isinstance(policy_document, dict):
            raise TypeError("Expected argument 'policy_document' to be a dict")
        pulumi.set(__self__, "policy_document", policy_document)

    @property
    @pulumi.getter(name="policyDocument")
    def policy_document(self) -> Optional[Any]:
        """
        The policy document.
         You must provide policies in JSON format in IAM. However, for CFN templates formatted in YAML, you can provide the policy in JSON or YAML format. CFN always converts a YAML policy to JSON format before submitting it to IAM.
         The [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex) used to validate this parameter is a string of characters consisting of the following:
          +  Any printable ASCII character ranging from the space character (``\\u0020``) through the end of the ASCII character range
          +  The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF``)
          +  The special characters tab (``\\u0009``), line feed (``\\u000A``), and carriage return (``\\u000D``)

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::IAM::UserPolicy` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "policy_document")


class AwaitableGetUserPolicyResult(GetUserPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserPolicyResult(
            policy_document=self.policy_document)


def get_user_policy(policy_name: Optional[builtins.str] = None,
                    user_name: Optional[builtins.str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserPolicyResult:
    """
    Adds or updates an inline policy document that is embedded in the specified IAM user.
     An IAM user can also have a managed policy attached to it. To attach a managed policy to a user, use [AWS::IAM::User](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html). To create a new managed policy, use [AWS::IAM::ManagedPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html). For information about policies, see [Managed policies and inline policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *IAM User Guide*.
     For information about the maximum number of inline policies that you can embed in a user, see [IAM and quotas](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html) in the *IAM User Guide*.


    :param builtins.str policy_name: The name of the policy document.
            This parameter allows (through its [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex)) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
    :param builtins.str user_name: The name of the user to associate the policy with.
            This parameter allows (through its [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex)) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
    """
    __args__ = dict()
    __args__['policyName'] = policy_name
    __args__['userName'] = user_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:iam:getUserPolicy', __args__, opts=opts, typ=GetUserPolicyResult).value

    return AwaitableGetUserPolicyResult(
        policy_document=pulumi.get(__ret__, 'policy_document'))
def get_user_policy_output(policy_name: Optional[pulumi.Input[builtins.str]] = None,
                           user_name: Optional[pulumi.Input[builtins.str]] = None,
                           opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetUserPolicyResult]:
    """
    Adds or updates an inline policy document that is embedded in the specified IAM user.
     An IAM user can also have a managed policy attached to it. To attach a managed policy to a user, use [AWS::IAM::User](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html). To create a new managed policy, use [AWS::IAM::ManagedPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html). For information about policies, see [Managed policies and inline policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html) in the *IAM User Guide*.
     For information about the maximum number of inline policies that you can embed in a user, see [IAM and quotas](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html) in the *IAM User Guide*.


    :param builtins.str policy_name: The name of the policy document.
            This parameter allows (through its [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex)) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
    :param builtins.str user_name: The name of the user to associate the policy with.
            This parameter allows (through its [regex pattern](https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex)) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
    """
    __args__ = dict()
    __args__['policyName'] = policy_name
    __args__['userName'] = user_name
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:iam:getUserPolicy', __args__, opts=opts, typ=GetUserPolicyResult)
    return __ret__.apply(lambda __response__: GetUserPolicyResult(
        policy_document=pulumi.get(__response__, 'policy_document')))
