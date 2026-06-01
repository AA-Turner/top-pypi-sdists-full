'''
# S3 Bucket Notifications Destinations

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module includes integration classes for using Topics, Queues or Lambdas
as S3 Notification Destinations.

## Examples

The following example shows how to send a notification to an SNS
topic when an object is created in an S3 bucket:

```python
import aws_cdk.aws_sns as sns


bucket = s3.Bucket(self, "Bucket")
topic = sns.Topic(self, "Topic")

bucket.add_event_notification(s3.EventType.OBJECT_CREATED_PUT, s3n.SnsDestination(topic))
```

The following example shows how to send a notification to an SQS queue
when an object is created in an S3 bucket:

```python
import aws_cdk.aws_sqs as sqs


bucket = s3.Bucket(self, "Bucket")
queue = sqs.Queue(self, "Queue")

bucket.add_event_notification(s3.EventType.OBJECT_CREATED_PUT, s3n.SqsDestination(queue))
```

The following example shows how to send a notification to a Lambda function when an object is created in an S3 bucket:

```python
import aws_cdk.aws_lambda as lambda_


bucket = s3.Bucket(self, "Bucket")
fn = lambda_.Function(self, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
)

bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(fn))
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.aws_sns as _aws_cdk_aws_sns_889c7272
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_48bffef9
import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_aws_s3_55f001a5.IBucketNotificationDestination)
class LambdaDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3-notifications.LambdaDestination",
):
    '''Use a Lambda function as a bucket notification destination.

    :exampleMetadata: infused

    Example::

        # my_lambda: lambda.Function
        
        bucket = s3.Bucket.from_bucket_attributes(self, "ImportedBucket",
            bucket_arn="arn:aws:s3:::my-bucket"
        )
        
        # now you can just call methods on the bucket
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(my_lambda), prefix="home/myusername/*")
    '''

    def __init__(self, fn: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''
        :param fn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1ee3bcbf5e3e73e5ce656f7dc91f463202c4d07f09da89cbd121acc60dd0bc)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        jsii.create(self.__class__, self, [fn])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    ) -> _aws_cdk_aws_s3_55f001a5.BucketNotificationDestinationConfig:
        '''Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param _scope: -
        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8f765c2c3bf56a814f12058688743411a1bff07bc12c89d8d627c74015473d)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(_aws_cdk_aws_s3_55f001a5.BucketNotificationDestinationConfig, jsii.invoke(self, "bind", [_scope, bucket]))


@jsii.implements(_aws_cdk_aws_s3_55f001a5.IBucketNotificationDestination)
class SnsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3-notifications.SnsDestination",
):
    '''Use an SNS topic as a bucket notification destination.

    :exampleMetadata: infused

    Example::

        bucket = s3.Bucket(self, "MyBucket")
        topic = sns.Topic(self, "MyTopic")
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.SnsDestination(topic))
    '''

    def __init__(self, topic: _aws_cdk_aws_sns_889c7272.ITopic) -> None:
        '''
        :param topic: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a556b2bd0e35311824833162bc7cb351e4a428aa215f5078b809eaa3d87352b0)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        jsii.create(self.__class__, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    ) -> _aws_cdk_aws_s3_55f001a5.BucketNotificationDestinationConfig:
        '''Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param _scope: -
        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512a109093e7745d3c5bdd16203b1e0c8e0efac9181aabf206d01943efc41567)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(_aws_cdk_aws_s3_55f001a5.BucketNotificationDestinationConfig, jsii.invoke(self, "bind", [_scope, bucket]))


@jsii.implements(_aws_cdk_aws_s3_55f001a5.IBucketNotificationDestination)
class SqsDestination(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3-notifications.SqsDestination",
):
    '''Use an SQS queue as a bucket notification destination.

    :exampleMetadata: infused

    Example::

        # my_queue: sqs.Queue
        
        bucket = s3.Bucket(self, "MyBucket")
        bucket.add_event_notification(s3.EventType.OBJECT_REMOVED,
            s3n.SqsDestination(my_queue), prefix="foo/", suffix=".jpg")
    '''

    def __init__(self, queue: _aws_cdk_aws_sqs_48bffef9.IQueue) -> None:
        '''
        :param queue: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0277f42ce9945e5e7b7e0f3bb4929b19f21d7e0a57f903e54d1b29b24d0f7453)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        jsii.create(self.__class__, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _aws_cdk_core_f4b25747.Construct,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    ) -> _aws_cdk_aws_s3_55f001a5.BucketNotificationDestinationConfig:
        '''Allows using SQS queues as destinations for bucket notifications.

        Use ``bucket.onEvent(event, queue)`` to subscribe.

        :param _scope: -
        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cba65b4d21a56893ca8389044b36522fed0bb23ca27ca3ec5a97f3fdb9c0981)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(_aws_cdk_aws_s3_55f001a5.BucketNotificationDestinationConfig, jsii.invoke(self, "bind", [_scope, bucket]))


__all__ = [
    "LambdaDestination",
    "SnsDestination",
    "SqsDestination",
]

publication.publish()

def _typecheckingstub__5a1ee3bcbf5e3e73e5ce656f7dc91f463202c4d07f09da89cbd121acc60dd0bc(
    fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8f765c2c3bf56a814f12058688743411a1bff07bc12c89d8d627c74015473d(
    _scope: _aws_cdk_core_f4b25747.Construct,
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a556b2bd0e35311824833162bc7cb351e4a428aa215f5078b809eaa3d87352b0(
    topic: _aws_cdk_aws_sns_889c7272.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512a109093e7745d3c5bdd16203b1e0c8e0efac9181aabf206d01943efc41567(
    _scope: _aws_cdk_core_f4b25747.Construct,
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0277f42ce9945e5e7b7e0f3bb4929b19f21d7e0a57f903e54d1b29b24d0f7453(
    queue: _aws_cdk_aws_sqs_48bffef9.IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cba65b4d21a56893ca8389044b36522fed0bb23ca27ca3ec5a97f3fdb9c0981(
    _scope: _aws_cdk_core_f4b25747.Construct,
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
) -> None:
    """Type checking stubs"""
    pass
