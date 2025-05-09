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
    'GetTopicResult',
    'AwaitableGetTopicResult',
    'get_topic',
    'get_topic_output',
]

@pulumi.output_type
class GetTopicResult:
    def __init__(__self__, archive_policy=None, content_based_deduplication=None, data_protection_policy=None, delivery_status_logging=None, display_name=None, fifo_throughput_scope=None, kms_master_key_id=None, signature_version=None, subscription=None, tags=None, topic_arn=None, tracing_config=None):
        if archive_policy and not isinstance(archive_policy, dict):
            raise TypeError("Expected argument 'archive_policy' to be a dict")
        pulumi.set(__self__, "archive_policy", archive_policy)
        if content_based_deduplication and not isinstance(content_based_deduplication, bool):
            raise TypeError("Expected argument 'content_based_deduplication' to be a bool")
        pulumi.set(__self__, "content_based_deduplication", content_based_deduplication)
        if data_protection_policy and not isinstance(data_protection_policy, dict):
            raise TypeError("Expected argument 'data_protection_policy' to be a dict")
        pulumi.set(__self__, "data_protection_policy", data_protection_policy)
        if delivery_status_logging and not isinstance(delivery_status_logging, list):
            raise TypeError("Expected argument 'delivery_status_logging' to be a list")
        pulumi.set(__self__, "delivery_status_logging", delivery_status_logging)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if fifo_throughput_scope and not isinstance(fifo_throughput_scope, str):
            raise TypeError("Expected argument 'fifo_throughput_scope' to be a str")
        pulumi.set(__self__, "fifo_throughput_scope", fifo_throughput_scope)
        if kms_master_key_id and not isinstance(kms_master_key_id, str):
            raise TypeError("Expected argument 'kms_master_key_id' to be a str")
        pulumi.set(__self__, "kms_master_key_id", kms_master_key_id)
        if signature_version and not isinstance(signature_version, str):
            raise TypeError("Expected argument 'signature_version' to be a str")
        pulumi.set(__self__, "signature_version", signature_version)
        if subscription and not isinstance(subscription, list):
            raise TypeError("Expected argument 'subscription' to be a list")
        pulumi.set(__self__, "subscription", subscription)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if topic_arn and not isinstance(topic_arn, str):
            raise TypeError("Expected argument 'topic_arn' to be a str")
        pulumi.set(__self__, "topic_arn", topic_arn)
        if tracing_config and not isinstance(tracing_config, str):
            raise TypeError("Expected argument 'tracing_config' to be a str")
        pulumi.set(__self__, "tracing_config", tracing_config)

    @property
    @pulumi.getter(name="archivePolicy")
    def archive_policy(self) -> Optional[Any]:
        """
        The archive policy determines the number of days SNS retains messages. You can set a retention period from 1 to 365 days.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::SNS::Topic` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "archive_policy")

    @property
    @pulumi.getter(name="contentBasedDeduplication")
    def content_based_deduplication(self) -> Optional[builtins.bool]:
        """
        Enables content-based deduplication for FIFO topics.
          +  By default, ``ContentBasedDeduplication`` is set to ``false``. If you create a FIFO topic and this attribute is ``false``, you must specify a value for the ``MessageDeduplicationId`` parameter for the [Publish](https://docs.aws.amazon.com/sns/latest/api/API_Publish.html) action. 
          +  When you set ``ContentBasedDeduplication`` to ``true``, SNS uses a SHA-256 hash to generate the ``MessageDeduplicationId`` using the body of the message (but not the attributes of the message).
         (Optional) To override the generated value, you can specify a value for the the ``MessageDeduplicationId`` parameter for the ``Publish`` action.
        """
        return pulumi.get(self, "content_based_deduplication")

    @property
    @pulumi.getter(name="dataProtectionPolicy")
    def data_protection_policy(self) -> Optional[Any]:
        """
        The body of the policy document you want to use for this topic.
         You can only add one policy per topic.
         The policy must be in JSON string format.
         Length Constraints: Maximum length of 30,720.

        Search the [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/) for `AWS::SNS::Topic` for more information about the expected schema for this property.
        """
        return pulumi.get(self, "data_protection_policy")

    @property
    @pulumi.getter(name="deliveryStatusLogging")
    def delivery_status_logging(self) -> Optional[Sequence['outputs.TopicLoggingConfig']]:
        """
        The ``DeliveryStatusLogging`` configuration enables you to log the delivery status of messages sent from your Amazon SNS topic to subscribed endpoints with the following supported delivery protocols:
          +  HTTP 
          +  Amazon Kinesis Data Firehose
          +   AWS Lambda
          +  Platform application endpoint
          +  Amazon Simple Queue Service
          
         Once configured, log entries are sent to Amazon CloudWatch Logs.
        """
        return pulumi.get(self, "delivery_status_logging")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[builtins.str]:
        """
        The display name to use for an SNS topic with SMS subscriptions. The display name must be maximum 100 characters long, including hyphens (-), underscores (_), spaces, and tabs.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="fifoThroughputScope")
    def fifo_throughput_scope(self) -> Optional[builtins.str]:
        """
        Specifies the throughput quota and deduplication behavior to apply for the FIFO topic. Valid values are `Topic` or `MessageGroup` .
        """
        return pulumi.get(self, "fifo_throughput_scope")

    @property
    @pulumi.getter(name="kmsMasterKeyId")
    def kms_master_key_id(self) -> Optional[builtins.str]:
        """
        The ID of an AWS managed customer master key (CMK) for SNS or a custom CMK. For more information, see [Key terms](https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html#sse-key-terms). For more examples, see ``KeyId`` in the *API Reference*.
         This property applies only to [server-side-encryption](https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html).
        """
        return pulumi.get(self, "kms_master_key_id")

    @property
    @pulumi.getter(name="signatureVersion")
    def signature_version(self) -> Optional[builtins.str]:
        """
        The signature version corresponds to the hashing algorithm used while creating the signature of the notifications, subscription confirmations, or unsubscribe confirmation messages sent by Amazon SNS. By default, ``SignatureVersion`` is set to ``1``.
        """
        return pulumi.get(self, "signature_version")

    @property
    @pulumi.getter
    def subscription(self) -> Optional[Sequence['outputs.TopicSubscription']]:
        """
        The SNS subscriptions (endpoints) for this topic.
          If you specify the ``Subscription`` property in the ``AWS::SNS::Topic`` resource and it creates an associated subscription resource, the associated subscription is not deleted when the ``AWS::SNS::Topic`` resource is deleted.
        """
        return pulumi.get(self, "subscription")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['_root_outputs.Tag']]:
        """
        The list of tags to add to a new topic.
          To be able to tag a topic on creation, you must have the ``sns:CreateTopic`` and ``sns:TagResource`` permissions.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="topicArn")
    def topic_arn(self) -> Optional[builtins.str]:
        """
        Returns the ARN of an Amazon SNS topic.
        """
        return pulumi.get(self, "topic_arn")

    @property
    @pulumi.getter(name="tracingConfig")
    def tracing_config(self) -> Optional[builtins.str]:
        """
        Tracing mode of an SNS topic. By default ``TracingConfig`` is set to ``PassThrough``, and the topic passes through the tracing header it receives from an SNS publisher to its subscriptions. If set to ``Active``, SNS will vend X-Ray segment data to topic owner account if the sampled flag in the tracing header is true.
        """
        return pulumi.get(self, "tracing_config")


class AwaitableGetTopicResult(GetTopicResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTopicResult(
            archive_policy=self.archive_policy,
            content_based_deduplication=self.content_based_deduplication,
            data_protection_policy=self.data_protection_policy,
            delivery_status_logging=self.delivery_status_logging,
            display_name=self.display_name,
            fifo_throughput_scope=self.fifo_throughput_scope,
            kms_master_key_id=self.kms_master_key_id,
            signature_version=self.signature_version,
            subscription=self.subscription,
            tags=self.tags,
            topic_arn=self.topic_arn,
            tracing_config=self.tracing_config)


def get_topic(topic_arn: Optional[builtins.str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTopicResult:
    """
    The ``AWS::SNS::Topic`` resource creates a topic to which notifications can be published.
      One account can create a maximum of 100,000 standard topics and 1,000 FIFO topics. For more information, see [endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/sns.html) in the *General Reference*.
       The structure of ``AUTHPARAMS`` depends on the .signature of the API request. For more information, see [Examples of the complete Signature Version 4 signing process](https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html) in the *General Reference*.


    :param builtins.str topic_arn: Returns the ARN of an Amazon SNS topic.
    """
    __args__ = dict()
    __args__['topicArn'] = topic_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:sns:getTopic', __args__, opts=opts, typ=GetTopicResult).value

    return AwaitableGetTopicResult(
        archive_policy=pulumi.get(__ret__, 'archive_policy'),
        content_based_deduplication=pulumi.get(__ret__, 'content_based_deduplication'),
        data_protection_policy=pulumi.get(__ret__, 'data_protection_policy'),
        delivery_status_logging=pulumi.get(__ret__, 'delivery_status_logging'),
        display_name=pulumi.get(__ret__, 'display_name'),
        fifo_throughput_scope=pulumi.get(__ret__, 'fifo_throughput_scope'),
        kms_master_key_id=pulumi.get(__ret__, 'kms_master_key_id'),
        signature_version=pulumi.get(__ret__, 'signature_version'),
        subscription=pulumi.get(__ret__, 'subscription'),
        tags=pulumi.get(__ret__, 'tags'),
        topic_arn=pulumi.get(__ret__, 'topic_arn'),
        tracing_config=pulumi.get(__ret__, 'tracing_config'))
def get_topic_output(topic_arn: Optional[pulumi.Input[builtins.str]] = None,
                     opts: Optional[Union[pulumi.InvokeOptions, pulumi.InvokeOutputOptions]] = None) -> pulumi.Output[GetTopicResult]:
    """
    The ``AWS::SNS::Topic`` resource creates a topic to which notifications can be published.
      One account can create a maximum of 100,000 standard topics and 1,000 FIFO topics. For more information, see [endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/sns.html) in the *General Reference*.
       The structure of ``AUTHPARAMS`` depends on the .signature of the API request. For more information, see [Examples of the complete Signature Version 4 signing process](https://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html) in the *General Reference*.


    :param builtins.str topic_arn: Returns the ARN of an Amazon SNS topic.
    """
    __args__ = dict()
    __args__['topicArn'] = topic_arn
    opts = pulumi.InvokeOutputOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('aws-native:sns:getTopic', __args__, opts=opts, typ=GetTopicResult)
    return __ret__.apply(lambda __response__: GetTopicResult(
        archive_policy=pulumi.get(__response__, 'archive_policy'),
        content_based_deduplication=pulumi.get(__response__, 'content_based_deduplication'),
        data_protection_policy=pulumi.get(__response__, 'data_protection_policy'),
        delivery_status_logging=pulumi.get(__response__, 'delivery_status_logging'),
        display_name=pulumi.get(__response__, 'display_name'),
        fifo_throughput_scope=pulumi.get(__response__, 'fifo_throughput_scope'),
        kms_master_key_id=pulumi.get(__response__, 'kms_master_key_id'),
        signature_version=pulumi.get(__response__, 'signature_version'),
        subscription=pulumi.get(__response__, 'subscription'),
        tags=pulumi.get(__response__, 'tags'),
        topic_arn=pulumi.get(__response__, 'topic_arn'),
        tracing_config=pulumi.get(__response__, 'tracing_config')))
