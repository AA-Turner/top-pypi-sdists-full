r'''
# Amazon Data Firehose Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All constructs moved to aws-cdk-lib/aws-kinesisfirehose.

[Amazon Data Firehose](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html), [formerly known as Amazon Kinesis Data Firehose](https://aws.amazon.com/about-aws/whats-new/2024/02/amazon-data-firehose-formerly-kinesis-data-firehose/),
is a service for fully-managed delivery of real-time streaming data to storage services
such as Amazon S3, Amazon Redshift, Amazon Elasticsearch, Splunk, or any custom HTTP
endpoint or third-party services such as Datadog, Dynatrace, LogicMonitor, MongoDB, New
Relic, and Sumo Logic.

Amazon Data Firehose delivery streams are distinguished from Kinesis data streams in
their models of consumption. Whereas consumers read from a data stream by actively pulling
data from the stream, a delivery stream pushes data to its destination on a regular
cadence. This means that data streams are intended to have consumers that do on-demand
processing, like AWS Lambda or Amazon EC2. On the other hand, delivery streams are
intended to have destinations that are sources for offline processing and analytics, such
as Amazon S3 and Amazon Redshift.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk)
project. It allows you to define Amazon Data Firehose delivery streams.

## Defining a Delivery Stream

In order to define a Delivery Stream, you must specify a destination. An S3 bucket can be
used as a destination. Currently the CDK supports only S3 as a destination which is covered [below](#destinations).

```python
bucket = s3.Bucket(self, "Bucket")
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destinations.S3Bucket(bucket)
)
```

The above example defines the following resources:

* An S3 bucket
* An Amazon Data Firehose delivery stream with Direct PUT as the source and CloudWatch
  error logging turned on.
* An IAM role which gives the delivery stream permission to write to the S3 bucket.

## Sources

An Amazon Data Firehose delivery stream can accept data from three main sources: Kinesis Data Streams, Managed Streaming for Apache Kafka (MSK), or via a "direct put" (API calls). Currently only Kinesis Data Streams and direct put are supported in the CDK.

See: [Sending Data to a Delivery Stream](https://docs.aws.amazon.com/firehose/latest/dev/basic-write.html)
in the *Amazon Data Firehose Developer Guide*.

### Kinesis Data Stream

A delivery stream can read directly from a Kinesis data stream as a consumer of the data
stream. Configure this behaviour by passing in a data stream in the `source`
property via the `KinesisStreamSource` class when constructing a delivery stream:

```python
# destination: firehose.IDestination

source_stream = kinesis.Stream(self, "Source Stream")

firehose.DeliveryStream(self, "Delivery Stream",
    source=firehose.KinesisStreamSource(source_stream),
    destination=destination
)
```

### Direct Put

Data must be provided via "direct put", ie., by using a `PutRecord` or
`PutRecordBatch` API call. There are a number of ways of doing so, such as:

* Kinesis Agent: a standalone Java application that monitors and delivers files while
  handling file rotation, checkpointing, and retries. See: [Writing to Amazon Data Firehose Using Kinesis Agent](https://docs.aws.amazon.com/firehose/latest/dev/writing-with-agents.html)
  in the *Amazon Data Firehose Developer Guide*.
* AWS SDK: a general purpose solution that allows you to deliver data to a delivery stream
  from anywhere using Java, .NET, Node.js, Python, or Ruby. See: [Writing to Amazon Data Firehose Using the AWS SDK](https://docs.aws.amazon.com/firehose/latest/dev/writing-with-sdk.html)
  in the *Amazon Data Firehose Developer Guide*.
* CloudWatch Logs: subscribe to a log group and receive filtered log events directly into
  a delivery stream. See: [logs-destinations](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-logs-destinations-readme.html).
* Eventbridge: add an event rule target to send events to a delivery stream based on the
  rule filtering. See: [events-targets](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-events-targets-readme.html).
* SNS: add a subscription to send all notifications from the topic to a delivery
  stream. See: [sns-subscriptions](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-sns-subscriptions-readme.html).
* IoT: add an action to an IoT rule to send various IoT information to a delivery stream

## Destinations

Amazon Data Firehose supports multiple AWS and third-party services as destinations, including Amazon S3, Amazon Redshift, and more. You can find the full list of supported destination [here](https://docs.aws.amazon.com/firehose/latest/dev/create-destination.html).

Currently in the AWS CDK, only S3 is implemented as an L2 construct destination. Other destinations can still be configured using L1 constructs. See [kinesisfirehose-destinations](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-kinesisfirehose-destinations-readme.html)
for the implementations of these destinations.

### S3

Defining a delivery stream with an S3 bucket destination:

```python
# bucket: s3.Bucket

s3_destination = destinations.S3Bucket(bucket)

firehose.DeliveryStream(self, "Delivery Stream",
    destination=s3_destination
)
```

The S3 destination also supports custom dynamic prefixes. `dataOutputPrefix`
will be used for files successfully delivered to S3. `errorOutputPrefix` will be added to
failed records before writing them to S3.

```python
# bucket: s3.Bucket

s3_destination = destinations.S3Bucket(bucket,
    data_output_prefix="myFirehose/DeliveredYear=!{timestamp:yyyy}/anyMonth/rand=!{firehose:random-string}",
    error_output_prefix="myFirehoseFailures/!{firehose:error-output-type}/!{timestamp:yyyy}/anyMonth/!{timestamp:dd}"
)
```

See: [Custom S3 Prefixes](https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html)
in the *Amazon Data Firehose Developer Guide*.

## Server-side Encryption

Enabling server-side encryption (SSE) requires Amazon Data Firehose to encrypt all data
sent to delivery stream when it is stored at rest. This means that data is encrypted
before being written to the service's internal storage layer and decrypted after it is
received from the internal storage layer. The service manages keys and cryptographic
operations so that sources and destinations do not need to, as the data is encrypted and
decrypted at the boundaries of the service (i.e., before the data is delivered to a
destination). By default, delivery streams do not have SSE enabled.

The Key Management Service keys (KMS keys) used for SSE can either be AWS-owned or
customer-managed. AWS-owned KMS keys are created, owned and managed by AWS for use in
multiple AWS accounts. As a customer, you cannot view, use, track, or manage these keys,
and you are not charged for their use. On the other hand, customer-managed KMS keys are
created and owned within your account and managed entirely by you. As a customer, you are
responsible for managing access, rotation, aliases, and deletion for these keys, and you
are changed for their use.

See: [AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys)
in the *KMS Developer Guide*.

```python
# destination: firehose.IDestination
# SSE with an customer-managed key that is explicitly specified
# key: kms.Key


# SSE with an AWS-owned key
firehose.DeliveryStream(self, "Delivery Stream with AWS Owned Key",
    encryption=firehose.StreamEncryption.aws_owned_key(),
    destination=destination
)
# SSE with an customer-managed key that is created automatically by the CDK
firehose.DeliveryStream(self, "Delivery Stream with Customer Managed Key",
    encryption=firehose.StreamEncryption.customer_managed_key(),
    destination=destination
)
firehose.DeliveryStream(self, "Delivery Stream with Customer Managed and Provided Key",
    encryption=firehose.StreamEncryption.customer_managed_key(key),
    destination=destination
)
```

See: [Data Protection](https://docs.aws.amazon.com/firehose/latest/dev/encryption.html)
in the *Amazon Data Firehose Developer Guide*.

## Monitoring

Amazon Data Firehose is integrated with CloudWatch, so you can monitor the performance of
your delivery streams via logs and metrics.

### Logs

Amazon Data Firehose will send logs to CloudWatch when data transformation or data
delivery fails. The CDK will enable logging by default and create a CloudWatch LogGroup
and LogStream with default settings for your Delivery Stream.

When creating a destination, you can provide an `ILoggingConfig`, which can either be an `EnableLogging` or `DisableLogging` instance.
If you use `EnableLogging`, the CDK will create a CloudWatch LogGroup and LogStream with all CloudFormation default settings for you, or you can optionally
specify your own log group to be used for capturing and storing log events. For example:

```python
import aws_cdk.aws_logs as logs
# bucket: s3.Bucket


log_group = logs.LogGroup(self, "Log Group")
destination = destinations.S3Bucket(bucket,
    logging_config=destinations.EnableLogging(log_group)
)

firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination
)
```

Logging can also be disabled:

```python
# bucket: s3.Bucket

destination = destinations.S3Bucket(bucket,
    logging_config=destinations.DisableLogging()
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination
)
```

See: [Monitoring using CloudWatch Logs](https://docs.aws.amazon.com/firehose/latest/dev/monitoring-with-cloudwatch-logs.html)
in the *Amazon Data Firehose Developer Guide*.

### Metrics

Amazon Data Firehose sends metrics to CloudWatch so that you can collect and analyze the
performance of the delivery stream, including data delivery, data ingestion, data
transformation, format conversion, API usage, encryption, and resource usage. You can then
use CloudWatch alarms to alert you, for example, when data freshness (the age of the
oldest record in the delivery stream) exceeds the buffering limit (indicating that data is
not being delivered to your destination), or when the rate of incoming records exceeds the
limit of records per second (indicating data is flowing into your delivery stream faster
than it is configured to process).

CDK provides methods for accessing delivery stream metrics with default configuration,
such as `metricIncomingBytes`, and `metricIncomingRecords` (see [`IDeliveryStream`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisfirehose.IDeliveryStream.html)
for a full list). CDK also provides a generic `metric` method that can be used to produce
metric configurations for any metric provided by Amazon Data Firehose; the configurations
are pre-populated with the correct dimensions for the delivery stream.

```python
import aws_cdk.aws_cloudwatch as cloudwatch

# delivery_stream: firehose.DeliveryStream


# Alarm that triggers when the per-second average of incoming bytes exceeds 90% of the current service limit
incoming_bytes_percent_of_limit = cloudwatch.MathExpression(
    expression="incomingBytes / 300 / bytePerSecLimit",
    using_metrics={
        "incoming_bytes": delivery_stream.metric_incoming_bytes(statistic=cloudwatch.Statistic.SUM),
        "byte_per_sec_limit": delivery_stream.metric("BytesPerSecondLimit")
    }
)

cloudwatch.Alarm(self, "Alarm",
    metric=incoming_bytes_percent_of_limit,
    threshold=0.9,
    evaluation_periods=3
)
```

See: [Monitoring Using CloudWatch Metrics](https://docs.aws.amazon.com/firehose/latest/dev/monitoring-with-cloudwatch-metrics.html)
in the *Amazon Data Firehose Developer Guide*.

## Compression

Your data can automatically be compressed when it is delivered to S3 as either a final or
an intermediary/backup destination. Supported compression formats are: gzip, Snappy,
Hadoop-compatible Snappy, and ZIP, except for Redshift destinations, where Snappy
(regardless of Hadoop-compatibility) and ZIP are not supported. By default, data is
delivered to S3 without compression.

```python
# Compress data delivered to S3 using Snappy
# bucket: s3.Bucket

s3_destination = destinations.S3Bucket(bucket,
    compression=destinations.Compression.SNAPPY
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=s3_destination
)
```

## Buffering

Incoming data is buffered before it is delivered to the specified destination. The
delivery stream will wait until the amount of incoming data has exceeded some threshold
(the "buffer size") or until the time since the last data delivery occurred exceeds some
threshold (the "buffer interval"), whichever happens first. You can configure these
thresholds based on the capabilities of the destination and your use-case. By default, the
buffer size is 5 MiB and the buffer interval is 5 minutes.

```python
# Increase the buffer interval and size to 10 minutes and 8 MiB, respectively
# bucket: s3.Bucket

destination = destinations.S3Bucket(bucket,
    buffering_interval=Duration.minutes(10),
    buffering_size=Size.mebibytes(8)
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination
)
```

See: [Data Delivery Frequency](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html#frequency)
in the *Amazon Data Firehose Developer Guide*.

Zero buffering, where Amazon Data Firehose stream can be configured to not buffer data before delivery, is supported by
setting the "buffer interval" to 0.

```python
# Setup zero buffering
# bucket: s3.Bucket

destination = destinations.S3Bucket(bucket,
    buffering_interval=Duration.seconds(0)
)
firehose.DeliveryStream(self, "ZeroBufferDeliveryStream",
    destination=destination
)
```

See: [Buffering Hints](https://docs.aws.amazon.com/firehose/latest/dev/buffering-hints.html).

## Destination Encryption

Your data can be automatically encrypted when it is delivered to S3 as a final or an
intermediary/backup destination. Amazon Data Firehose supports Amazon S3 server-side
encryption with AWS Key Management Service (AWS KMS) for encrypting delivered data in
Amazon S3. You can choose to not encrypt the data or to encrypt with a key from the list
of AWS KMS keys that you own. For more information,
see [Protecting Data Using Server-Side Encryption with AWS KMS–Managed Keys (SSE-KMS)](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html).
By default, encryption isn’t directly enabled on the delivery stream; instead, it uses the default encryption settings of the destination S3 bucket.

```python
# bucket: s3.Bucket
# key: kms.Key

destination = destinations.S3Bucket(bucket,
    encryption_key=key
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination
)
```

## Backup

A delivery stream can be configured to back up data to S3 that it attempted to deliver to
the configured destination. Backed up data can be all the data that the delivery stream
attempted to deliver or just data that it failed to deliver (Redshift and S3 destinations
can only back up all data). CDK can create a new S3 bucket where it will back up data, or
you can provide a bucket where data will be backed up. You can also provide a prefix under
which your backed-up data will be placed within the bucket. By default, source data is not
backed up to S3.

```python
# Enable backup of all source records (to an S3 bucket created by CDK).
# bucket: s3.Bucket
# Explicitly provide an S3 bucket to which all source records will be backed up.
# backup_bucket: s3.Bucket

firehose.DeliveryStream(self, "Delivery Stream Backup All",
    destination=
    destinations.S3Bucket(bucket,
        s3_backup=destinations.DestinationS3BackupProps(
            mode=destinations.BackupMode.ALL
        )
    )
)
firehose.DeliveryStream(self, "Delivery Stream Backup All Explicit Bucket",
    destination=
    destinations.S3Bucket(bucket,
        s3_backup=destinations.DestinationS3BackupProps(
            bucket=backup_bucket
        )
    )
)
# Explicitly provide an S3 prefix under which all source records will be backed up.
firehose.DeliveryStream(self, "Delivery Stream Backup All Explicit Prefix",
    destination=
    destinations.S3Bucket(bucket,
        s3_backup=destinations.DestinationS3BackupProps(
            mode=destinations.BackupMode.ALL,
            data_output_prefix="mybackup"
        )
    )
)
```

If any Data Processing or Transformation is configured on your Delivery Stream, the source
records will be backed up in their original format.

## Data Processing/Transformation

Data can be transformed before being delivered to destinations. There are two types of
data processing for delivery streams: record transformation with AWS Lambda, and record
format conversion using a schema stored in an AWS Glue table. If both types of data
processing are configured, then the Lambda transformation is performed first. By default,
no data processing occurs. This construct library currently only supports data
transformation with AWS Lambda. See [#15501](https://github.com/aws/aws-cdk/issues/15501)
to track the status of adding support for record format conversion.

### Data transformation with AWS Lambda

To transform the data, Amazon Data Firehose will call a Lambda function that you provide
and deliver the data returned in place of the source record. The function must return a
result that contains records in a specific format, including the following fields:

* `recordId` -- the ID of the input record that corresponds the results.
* `result` -- the status of the transformation of the record: "Ok" (success), "Dropped"
  (not processed intentionally), or "ProcessingFailed" (not processed due to an error).
* `data` -- the transformed data, Base64-encoded.

The data is buffered up to 1 minute and up to 3 MiB by default before being sent to the
function, but can be configured using `bufferInterval` and `bufferSize`
in the processor configuration (see: [Buffering](#buffering)). If the function invocation
fails due to a network timeout or because of hitting an invocation limit, the invocation
is retried 3 times by default, but can be configured using `retries` in the processor
configuration.

```python
# bucket: s3.Bucket
# Provide a Lambda function that will transform records before delivery, with custom
# buffering and retry configuration
lambda_function = lambda_.Function(self, "Processor",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "process-records"))
)
lambda_processor = firehose.LambdaFunctionProcessor(lambda_function,
    buffer_interval=Duration.minutes(5),
    buffer_size=Size.mebibytes(5),
    retries=5
)
s3_destination = destinations.S3Bucket(bucket,
    processor=lambda_processor
)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=s3_destination
)
```

```python
import path as path
import aws_cdk.aws_kinesisfirehose_alpha as firehose
import aws_cdk.aws_kms as kms
import aws_cdk.aws_lambda_nodejs as lambdanodejs
import aws_cdk.aws_logs as logs
import aws_cdk.aws_s3 as s3
import aws_cdk as cdk
import aws_cdk.aws_kinesisfirehose_destinations_alpha as destinations
from aws_cdk.integ_tests_alpha import AwsApiCall, ExpectedResult, IntegTest

app = cdk.App()

stack = cdk.Stack(app, "aws-cdk-firehose-delivery-stream-s3-all-properties")

bucket = s3.Bucket(stack, "FirehoseDeliveryStreamS3AllPropertiesBucket",
    removal_policy=cdk.RemovalPolicy.DESTROY,
    auto_delete_objects=True
)

backup_bucket = s3.Bucket(stack, "FirehoseDeliveryStreamS3AllPropertiesBackupBucket",
    removal_policy=cdk.RemovalPolicy.DESTROY,
    auto_delete_objects=True
)
log_group = logs.LogGroup(stack, "LogGroup",
    removal_policy=cdk.RemovalPolicy.DESTROY
)

data_processor_function = lambdanodejs.NodejsFunction(stack, "DataProcessorFunction",
    entry=path.join(__dirname, "lambda-data-processor.js"),
    timeout=cdk.Duration.minutes(1)
)

processor = firehose.LambdaFunctionProcessor(data_processor_function,
    buffer_interval=cdk.Duration.seconds(60),
    buffer_size=cdk.Size.mebibytes(1),
    retries=1
)

key = kms.Key(stack, "Key",
    removal_policy=cdk.RemovalPolicy.DESTROY
)

backup_key = kms.Key(stack, "BackupKey",
    removal_policy=cdk.RemovalPolicy.DESTROY
)

delivery_stream = firehose.DeliveryStream(stack, "DeliveryStream",
    destination=destinations.S3Bucket(bucket,
        logging_config=destinations.EnableLogging(log_group),
        processor=processor,
        compression=destinations.Compression.GZIP,
        data_output_prefix="regularPrefix",
        error_output_prefix="errorPrefix",
        buffering_interval=cdk.Duration.seconds(60),
        buffering_size=cdk.Size.mebibytes(1),
        encryption_key=key,
        s3_backup=destinations.DestinationS3BackupProps(
            mode=destinations.BackupMode.ALL,
            bucket=backup_bucket,
            compression=destinations.Compression.ZIP,
            data_output_prefix="backupPrefix",
            error_output_prefix="backupErrorPrefix",
            buffering_interval=cdk.Duration.seconds(60),
            buffering_size=cdk.Size.mebibytes(1),
            encryption_key=backup_key
        )
    )
)

firehose.DeliveryStream(stack, "ZeroBufferingDeliveryStream",
    destination=destinations.S3Bucket(bucket,
        compression=destinations.Compression.GZIP,
        data_output_prefix="regularPrefix",
        error_output_prefix="errorPrefix",
        buffering_interval=cdk.Duration.seconds(0)
    )
)

test_case = IntegTest(app, "integ-tests",
    test_cases=[stack],
    regions=["us-east-1"]
)

test_case.assertions.aws_api_call("Firehose", "putRecord", {
    "DeliveryStreamName": delivery_stream.delivery_stream_name,
    "Record": {
        "Data": "testData123"
    }
})

s3_api_call = test_case.assertions.aws_api_call("S3", "listObjectsV2", {
    "Bucket": bucket.bucket_name,
    "MaxKeys": 1
}).expect(ExpectedResult.object_like({
    "KeyCount": 1
})).wait_for_assertions(
    interval=cdk.Duration.seconds(30),
    total_timeout=cdk.Duration.minutes(10)
)

if s3_api_call instanceof AwsApiCall && s3_api_call.waiter_provider:
    s3_api_call.waiter_provider.add_to_role_policy({
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:ListBucket"],
        "Resource": ["*"]
    })
```

See: [Data Transformation](https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html)
in the *Amazon Data Firehose Developer Guide*.

## Specifying an IAM role

The DeliveryStream class automatically creates IAM service roles with all the minimum
necessary permissions for Amazon Data Firehose to access the resources referenced by your
delivery stream. One service role is created for the delivery stream that allows Amazon
Data Firehose to read from a Kinesis data stream (if one is configured as the delivery
stream source) and for server-side encryption. Note that if the DeliveryStream is created
without specifying a `source` or `encryptionKey`, this role is not created as it is not needed.

Another service role is created for each destination, which gives Amazon Data Firehose write
access to the destination resource, as well as the ability to invoke data transformers and
read schemas for record format conversion. If you wish, you may specify your own IAM role for
either the delivery stream or the destination service role, or both. It must have the correct
trust policy (it must allow Amazon Data Firehose to assume it) or delivery stream creation or
data delivery will fail. Other required permissions to destination resources, encryption keys, etc.,
will be provided automatically.

```python
# Specify the roles created above when defining the destination and delivery stream.
# bucket: s3.Bucket
# Create service roles for the delivery stream and destination.
# These can be used for other purposes and granted access to different resources.
# They must include the Amazon Data Firehose service principal in their trust policies.
# Two separate roles are shown below, but the same role can be used for both purposes.
delivery_stream_role = iam.Role(self, "Delivery Stream Role",
    assumed_by=iam.ServicePrincipal("firehose.amazonaws.com")
)
destination_role = iam.Role(self, "Destination Role",
    assumed_by=iam.ServicePrincipal("firehose.amazonaws.com")
)
destination = destinations.S3Bucket(bucket, role=destination_role)
firehose.DeliveryStream(self, "Delivery Stream",
    destination=destination,
    role=delivery_stream_role
)
```

See [Controlling Access](https://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html)
in the *Amazon Data Firehose Developer Guide*.

## Granting application access to a delivery stream

IAM roles, users or groups which need to be able to work with delivery streams should be
granted IAM permissions.

Any object that implements the `IGrantable` interface (i.e., has an associated principal)
can be granted permissions to a delivery stream by calling:

* `grantPutRecords(principal)` - grants the principal the ability to put records onto the
  delivery stream
* `grant(principal, ...actions)` - grants the principal permission to a custom set of
  actions

```python
# Give the role permissions to write data to the delivery stream
# delivery_stream: firehose.DeliveryStream
lambda_role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
)
delivery_stream.grant_put_records(lambda_role)
```

The following write permissions are provided to a service principal by the
`grantPutRecords()` method:

* `firehose:PutRecord`
* `firehose:PutRecordBatch`

## Granting a delivery stream access to a resource

Conversely to the above, Amazon Data Firehose requires permissions in order for delivery
streams to interact with resources that you own. For example, if an S3 bucket is specified
as a destination of a delivery stream, the delivery stream must be granted permissions to
put and get objects from the bucket. When using the built-in AWS service destinations
found in the `@aws-cdk/aws-kinesisfirehose-destinations-alpha` module, the CDK grants the
permissions automatically. However, custom or third-party destinations may require custom
permissions. In this case, use the delivery stream as an `IGrantable`, as follows:

```python
# delivery_stream: firehose.DeliveryStream
fn = lambda_.Function(self, "Function",
    code=lambda_.Code.from_inline("exports.handler = (event) => {}"),
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler"
)
fn.grant_invoke(delivery_stream)
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_ceddda9d
import aws_cdk.aws_kinesisfirehose as _aws_cdk_aws_kinesisfirehose_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DataProcessorBindOptions",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class DataProcessorBindOptions:
    def __init__(self, *, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(deprecated) Options when binding a DataProcessor to a delivery stream destination.

        :param role: (deprecated) The IAM role assumed by Kinesis Data Firehose to write to the destination that this DataProcessor will bind to.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisfirehose_alpha as kinesisfirehose_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            data_processor_bind_options = kinesisfirehose_alpha.DataProcessorBindOptions(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb128eca4e7ba1f83c4f0e58098f008795374fee30ada93711dd3b253dad0ef8)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
        }

    @builtins.property
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(deprecated) The IAM role assumed by Kinesis Data Firehose to write to the destination that this DataProcessor will bind to.

        :stability: deprecated
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProcessorBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DataProcessorConfig",
    jsii_struct_bases=[],
    name_mapping={
        "processor_identifier": "processorIdentifier",
        "processor_type": "processorType",
    },
)
class DataProcessorConfig:
    def __init__(
        self,
        *,
        processor_identifier: typing.Union["DataProcessorIdentifier", typing.Dict[builtins.str, typing.Any]],
        processor_type: builtins.str,
    ) -> None:
        '''(deprecated) The full configuration of a data processor.

        :param processor_identifier: (deprecated) The key-value pair that identifies the underlying processor resource.
        :param processor_type: (deprecated) The type of the underlying processor resource. Must be an accepted value in ``CfnDeliveryStream.ProcessorProperty.Type``.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisfirehose_alpha as kinesisfirehose_alpha
            
            data_processor_config = kinesisfirehose_alpha.DataProcessorConfig(
                processor_identifier=kinesisfirehose_alpha.DataProcessorIdentifier(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                ),
                processor_type="processorType"
            )
        '''
        if isinstance(processor_identifier, dict):
            processor_identifier = DataProcessorIdentifier(**processor_identifier)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d8516a4394f7676eff7b29cec88a391ff919bb6bbda458b6e8e06f6ddb7a88)
            check_type(argname="argument processor_identifier", value=processor_identifier, expected_type=type_hints["processor_identifier"])
            check_type(argname="argument processor_type", value=processor_type, expected_type=type_hints["processor_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "processor_identifier": processor_identifier,
            "processor_type": processor_type,
        }

    @builtins.property
    def processor_identifier(self) -> "DataProcessorIdentifier":
        '''(deprecated) The key-value pair that identifies the underlying processor resource.

        :stability: deprecated
        '''
        result = self._values.get("processor_identifier")
        assert result is not None, "Required property 'processor_identifier' is missing"
        return typing.cast("DataProcessorIdentifier", result)

    @builtins.property
    def processor_type(self) -> builtins.str:
        '''(deprecated) The type of the underlying processor resource.

        Must be an accepted value in ``CfnDeliveryStream.ProcessorProperty.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html#cfn-kinesisfirehose-deliverystream-processor-type
        :stability: deprecated

        Example::

            "Lambda"
        '''
        result = self._values.get("processor_type")
        assert result is not None, "Required property 'processor_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProcessorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DataProcessorIdentifier",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_name": "parameterName",
        "parameter_value": "parameterValue",
    },
)
class DataProcessorIdentifier:
    def __init__(
        self,
        *,
        parameter_name: builtins.str,
        parameter_value: builtins.str,
    ) -> None:
        '''(deprecated) The key-value pair that identifies the underlying processor resource.

        :param parameter_name: (deprecated) The parameter name that corresponds to the processor resource's identifier. Must be an accepted value in ``CfnDeliveryStream.ProcessoryParameterProperty.ParameterName``.
        :param parameter_value: (deprecated) The identifier of the underlying processor resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html
        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisfirehose_alpha as kinesisfirehose_alpha
            
            data_processor_identifier = kinesisfirehose_alpha.DataProcessorIdentifier(
                parameter_name="parameterName",
                parameter_value="parameterValue"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5e177461759fec4dd89a5e4a7730bec0e39ea197243fa5f2eceea512a39f24)
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parameter_name": parameter_name,
            "parameter_value": parameter_value,
        }

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''(deprecated) The parameter name that corresponds to the processor resource's identifier.

        Must be an accepted value in ``CfnDeliveryStream.ProcessoryParameterProperty.ParameterName``.

        :stability: deprecated
        '''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_value(self) -> builtins.str:
        '''(deprecated) The identifier of the underlying processor resource.

        :stability: deprecated
        '''
        result = self._values.get("parameter_value")
        assert result is not None, "Required property 'parameter_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProcessorIdentifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DataProcessorProps",
    jsii_struct_bases=[],
    name_mapping={
        "buffer_interval": "bufferInterval",
        "buffer_size": "bufferSize",
        "retries": "retries",
    },
)
class DataProcessorProps:
    def __init__(
        self,
        *,
        buffer_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        buffer_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(deprecated) Configure the data processor.

        :param buffer_interval: (deprecated) The length of time Kinesis Data Firehose will buffer incoming data before calling the processor. s Default: Duration.minutes(1)
        :param buffer_size: (deprecated) The amount of incoming data Kinesis Data Firehose will buffer before calling the processor. Default: Size.mebibytes(3)
        :param retries: (deprecated) The number of times Kinesis Data Firehose will retry the processor invocation after a failure due to network timeout or invocation limits. Default: 3

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            # bucket: s3.Bucket
            # Provide a Lambda function that will transform records before delivery, with custom
            # buffering and retry configuration
            lambda_function = lambda_.Function(self, "Processor",
                runtime=lambda_.Runtime.NODEJS_LATEST,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "process-records"))
            )
            lambda_processor = firehose.LambdaFunctionProcessor(lambda_function,
                buffer_interval=Duration.minutes(5),
                buffer_size=Size.mebibytes(5),
                retries=5
            )
            s3_destination = destinations.S3Bucket(bucket,
                processor=lambda_processor
            )
            firehose.DeliveryStream(self, "Delivery Stream",
                destination=s3_destination
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f8aa68afc823d87c695ee05759728c85e4023a37cf01cf765a10be84fbcac8)
            check_type(argname="argument buffer_interval", value=buffer_interval, expected_type=type_hints["buffer_interval"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if buffer_interval is not None:
            self._values["buffer_interval"] = buffer_interval
        if buffer_size is not None:
            self._values["buffer_size"] = buffer_size
        if retries is not None:
            self._values["retries"] = retries

    @builtins.property
    def buffer_interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The length of time Kinesis Data Firehose will buffer incoming data before calling the processor.

        s

        :default: Duration.minutes(1)

        :stability: deprecated
        '''
        result = self._values.get("buffer_interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def buffer_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(deprecated) The amount of incoming data Kinesis Data Firehose will buffer before calling the processor.

        :default: Size.mebibytes(3)

        :stability: deprecated
        '''
        result = self._values.get("buffer_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The number of times Kinesis Data Firehose will retry the processor invocation after a failure due to network timeout or invocation limits.

        :default: 3

        :stability: deprecated
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProcessorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DeliveryStreamAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_stream_arn": "deliveryStreamArn",
        "delivery_stream_name": "deliveryStreamName",
        "role": "role",
    },
)
class DeliveryStreamAttributes:
    def __init__(
        self,
        *,
        delivery_stream_arn: typing.Optional[builtins.str] = None,
        delivery_stream_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(deprecated) A full specification of a delivery stream that can be used to import it fluently into the CDK application.

        :param delivery_stream_arn: (deprecated) The ARN of the delivery stream. At least one of deliveryStreamArn and deliveryStreamName must be provided. Default: - derived from ``deliveryStreamName``.
        :param delivery_stream_name: (deprecated) The name of the delivery stream. At least one of deliveryStreamName and deliveryStreamArn must be provided. Default: - derived from ``deliveryStreamArn``.
        :param role: (deprecated) The IAM role associated with this delivery stream. Assumed by Kinesis Data Firehose to read from sources and encrypt data server-side. Default: - the imported stream cannot be granted access to other resources as an ``iam.IGrantable``.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisfirehose_alpha as kinesisfirehose_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            delivery_stream_attributes = kinesisfirehose_alpha.DeliveryStreamAttributes(
                delivery_stream_arn="deliveryStreamArn",
                delivery_stream_name="deliveryStreamName",
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a349f2444857db9da26d39113740e8ab10e954d7aef8340312a07dcb3ca0c72)
            check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delivery_stream_arn is not None:
            self._values["delivery_stream_arn"] = delivery_stream_arn
        if delivery_stream_name is not None:
            self._values["delivery_stream_name"] = delivery_stream_name
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def delivery_stream_arn(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The ARN of the delivery stream.

        At least one of deliveryStreamArn and deliveryStreamName must be provided.

        :default: - derived from ``deliveryStreamName``.

        :stability: deprecated
        '''
        result = self._values.get("delivery_stream_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delivery_stream_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the delivery stream.

        At least one of deliveryStreamName and deliveryStreamArn  must be provided.

        :default: - derived from ``deliveryStreamArn``.

        :stability: deprecated
        '''
        result = self._values.get("delivery_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) The IAM role associated with this delivery stream.

        Assumed by Kinesis Data Firehose to read from sources and encrypt data server-side.

        :default: - the imported stream cannot be granted access to other resources as an ``iam.IGrantable``.

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeliveryStreamAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DeliveryStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "delivery_stream_name": "deliveryStreamName",
        "encryption": "encryption",
        "role": "role",
        "source": "source",
    },
)
class DeliveryStreamProps:
    def __init__(
        self,
        *,
        destination: "IDestination",
        delivery_stream_name: typing.Optional[builtins.str] = None,
        encryption: typing.Optional["StreamEncryption"] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        source: typing.Optional["ISource"] = None,
    ) -> None:
        '''(deprecated) Properties for a new delivery stream.

        :param destination: (deprecated) The destination that this delivery stream will deliver data to.
        :param delivery_stream_name: (deprecated) A name for the delivery stream. Default: - a name is generated by CloudFormation.
        :param encryption: (deprecated) Indicates the type of customer master key (CMK) to use for server-side encryption, if any. Default: StreamEncryption.unencrypted()
        :param role: (deprecated) The IAM role associated with this delivery stream. Assumed by Kinesis Data Firehose to read from sources and encrypt data server-side. Default: - a role will be created with default permissions.
        :param source: (deprecated) The Kinesis data stream to use as a source for this delivery stream. Default: - data must be written to the delivery stream via a direct put.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            # bucket: s3.Bucket
            # Provide a Lambda function that will transform records before delivery, with custom
            # buffering and retry configuration
            lambda_function = lambda_.Function(self, "Processor",
                runtime=lambda_.Runtime.NODEJS_LATEST,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "process-records"))
            )
            lambda_processor = firehose.LambdaFunctionProcessor(lambda_function,
                buffer_interval=Duration.minutes(5),
                buffer_size=Size.mebibytes(5),
                retries=5
            )
            s3_destination = destinations.S3Bucket(bucket,
                processor=lambda_processor
            )
            firehose.DeliveryStream(self, "Delivery Stream",
                destination=s3_destination
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9413f788fdc9578de6565f85eb1d6d397a1047293bb85b71a059af7643ba38)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
        }
        if delivery_stream_name is not None:
            self._values["delivery_stream_name"] = delivery_stream_name
        if encryption is not None:
            self._values["encryption"] = encryption
        if role is not None:
            self._values["role"] = role
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def destination(self) -> "IDestination":
        '''(deprecated) The destination that this delivery stream will deliver data to.

        :stability: deprecated
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("IDestination", result)

    @builtins.property
    def delivery_stream_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) A name for the delivery stream.

        :default: - a name is generated by CloudFormation.

        :stability: deprecated
        '''
        result = self._values.get("delivery_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(self) -> typing.Optional["StreamEncryption"]:
        '''(deprecated) Indicates the type of customer master key (CMK) to use for server-side encryption, if any.

        :default: StreamEncryption.unencrypted()

        :stability: deprecated
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional["StreamEncryption"], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) The IAM role associated with this delivery stream.

        Assumed by Kinesis Data Firehose to read from sources and encrypt data server-side.

        :default: - a role will be created with default permissions.

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def source(self) -> typing.Optional["ISource"]:
        '''(deprecated) The Kinesis data stream to use as a source for this delivery stream.

        :default: - data must be written to the delivery stream via a direct put.

        :stability: deprecated
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["ISource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeliveryStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DestinationBindOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DestinationBindOptions:
    def __init__(self) -> None:
        '''(deprecated) Options when binding a destination to a delivery stream.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisfirehose_alpha as kinesisfirehose_alpha
            
            destination_bind_options = kinesisfirehose_alpha.DestinationBindOptions()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DestinationBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DestinationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "dependables": "dependables",
        "extended_s3_destination_configuration": "extendedS3DestinationConfiguration",
    },
)
class DestinationConfig:
    def __init__(
        self,
        *,
        dependables: typing.Optional[typing.Sequence[_constructs_77d1e7e8.IDependable]] = None,
        extended_s3_destination_configuration: typing.Optional[typing.Union[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(deprecated) A Kinesis Data Firehose delivery stream destination configuration.

        :param dependables: (deprecated) Any resources that were created by the destination when binding it to the stack that must be deployed before the delivery stream is deployed. Default: []
        :param extended_s3_destination_configuration: (deprecated) S3 destination configuration properties. Default: - S3 destination is not used.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisfirehose_alpha as kinesisfirehose_alpha
            import constructs as constructs
            
            # dependable: constructs.IDependable
            
            destination_config = kinesisfirehose_alpha.DestinationConfig(
                dependables=[dependable],
                extended_s3_destination_configuration=ExtendedS3DestinationConfigurationProperty(
                    bucket_arn="bucketArn",
                    role_arn="roleArn",
            
                    # the properties below are optional
                    buffering_hints=BufferingHintsProperty(
                        interval_in_seconds=123,
                        size_in_mBs=123
                    ),
                    cloud_watch_logging_options=CloudWatchLoggingOptionsProperty(
                        enabled=False,
                        log_group_name="logGroupName",
                        log_stream_name="logStreamName"
                    ),
                    compression_format="compressionFormat",
                    custom_time_zone="customTimeZone",
                    data_format_conversion_configuration=DataFormatConversionConfigurationProperty(
                        enabled=False,
                        input_format_configuration=InputFormatConfigurationProperty(
                            deserializer=DeserializerProperty(
                                hive_json_ser_de=HiveJsonSerDeProperty(
                                    timestamp_formats=["timestampFormats"]
                                ),
                                open_xJson_ser_de=OpenXJsonSerDeProperty(
                                    case_insensitive=False,
                                    column_to_json_key_mappings={
                                        "column_to_json_key_mappings_key": "columnToJsonKeyMappings"
                                    },
                                    convert_dots_in_json_keys_to_underscores=False
                                )
                            )
                        ),
                        output_format_configuration=OutputFormatConfigurationProperty(
                            serializer=SerializerProperty(
                                orc_ser_de=OrcSerDeProperty(
                                    block_size_bytes=123,
                                    bloom_filter_columns=["bloomFilterColumns"],
                                    bloom_filter_false_positive_probability=123,
                                    compression="compression",
                                    dictionary_key_threshold=123,
                                    enable_padding=False,
                                    format_version="formatVersion",
                                    padding_tolerance=123,
                                    row_index_stride=123,
                                    stripe_size_bytes=123
                                ),
                                parquet_ser_de=ParquetSerDeProperty(
                                    block_size_bytes=123,
                                    compression="compression",
                                    enable_dictionary_compression=False,
                                    max_padding_bytes=123,
                                    page_size_bytes=123,
                                    writer_version="writerVersion"
                                )
                            )
                        ),
                        schema_configuration=SchemaConfigurationProperty(
                            catalog_id="catalogId",
                            database_name="databaseName",
                            region="region",
                            role_arn="roleArn",
                            table_name="tableName",
                            version_id="versionId"
                        )
                    ),
                    dynamic_partitioning_configuration=DynamicPartitioningConfigurationProperty(
                        enabled=False,
                        retry_options=RetryOptionsProperty(
                            duration_in_seconds=123
                        )
                    ),
                    encryption_configuration=EncryptionConfigurationProperty(
                        kms_encryption_config=KMSEncryptionConfigProperty(
                            awskms_key_arn="awskmsKeyArn"
                        ),
                        no_encryption_config="noEncryptionConfig"
                    ),
                    error_output_prefix="errorOutputPrefix",
                    file_extension="fileExtension",
                    prefix="prefix",
                    processing_configuration=ProcessingConfigurationProperty(
                        enabled=False,
                        processors=[ProcessorProperty(
                            type="type",
            
                            # the properties below are optional
                            parameters=[ProcessorParameterProperty(
                                parameter_name="parameterName",
                                parameter_value="parameterValue"
                            )]
                        )]
                    ),
                    s3_backup_configuration=S3DestinationConfigurationProperty(
                        bucket_arn="bucketArn",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        buffering_hints=BufferingHintsProperty(
                            interval_in_seconds=123,
                            size_in_mBs=123
                        ),
                        cloud_watch_logging_options=CloudWatchLoggingOptionsProperty(
                            enabled=False,
                            log_group_name="logGroupName",
                            log_stream_name="logStreamName"
                        ),
                        compression_format="compressionFormat",
                        encryption_configuration=EncryptionConfigurationProperty(
                            kms_encryption_config=KMSEncryptionConfigProperty(
                                awskms_key_arn="awskmsKeyArn"
                            ),
                            no_encryption_config="noEncryptionConfig"
                        ),
                        error_output_prefix="errorOutputPrefix",
                        prefix="prefix"
                    ),
                    s3_backup_mode="s3BackupMode"
                )
            )
        '''
        if isinstance(extended_s3_destination_configuration, dict):
            extended_s3_destination_configuration = _aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty(**extended_s3_destination_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173daa2306128c47572263a530e0a02f73aa7e3f60be737ce497d123e3edc32d)
            check_type(argname="argument dependables", value=dependables, expected_type=type_hints["dependables"])
            check_type(argname="argument extended_s3_destination_configuration", value=extended_s3_destination_configuration, expected_type=type_hints["extended_s3_destination_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dependables is not None:
            self._values["dependables"] = dependables
        if extended_s3_destination_configuration is not None:
            self._values["extended_s3_destination_configuration"] = extended_s3_destination_configuration

    @builtins.property
    def dependables(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.IDependable]]:
        '''(deprecated) Any resources that were created by the destination when binding it to the stack that must be deployed before the delivery stream is deployed.

        :default: []

        :stability: deprecated
        '''
        result = self._values.get("dependables")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.IDependable]], result)

    @builtins.property
    def extended_s3_destination_configuration(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty]:
        '''(deprecated) S3 destination configuration properties.

        :default: - S3 destination is not used.

        :stability: deprecated
        '''
        result = self._values.get("extended_s3_destination_configuration")
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.IDataProcessor")
class IDataProcessor(typing_extensions.Protocol):
    '''(deprecated) A data processor that Kinesis Data Firehose will call to transform records before delivering data.

    :stability: deprecated
    '''

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> DataProcessorProps:
        '''(deprecated) The constructor props of the DataProcessor.

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> DataProcessorConfig:
        '''(deprecated) Binds this processor to a destination of a delivery stream.

        Implementers should use this method to grant processor invocation permissions to the provided stream and return the
        necessary configuration to register as a processor.

        :param scope: -
        :param role: (deprecated) The IAM role assumed by Kinesis Data Firehose to write to the destination that this DataProcessor will bind to.

        :stability: deprecated
        '''
        ...


class _IDataProcessorProxy:
    '''(deprecated) A data processor that Kinesis Data Firehose will call to transform records before delivering data.

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-kinesisfirehose-alpha.IDataProcessor"

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> DataProcessorProps:
        '''(deprecated) The constructor props of the DataProcessor.

        :stability: deprecated
        '''
        return typing.cast(DataProcessorProps, jsii.get(self, "props"))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> DataProcessorConfig:
        '''(deprecated) Binds this processor to a destination of a delivery stream.

        Implementers should use this method to grant processor invocation permissions to the provided stream and return the
        necessary configuration to register as a processor.

        :param scope: -
        :param role: (deprecated) The IAM role assumed by Kinesis Data Firehose to write to the destination that this DataProcessor will bind to.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c1e85da04925f59501768e65d47bdfdedeb6e3e0dfcee70ee80c529df93f3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = DataProcessorBindOptions(role=role)

        return typing.cast(DataProcessorConfig, jsii.invoke(self, "bind", [scope, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDataProcessor).__jsii_proxy_class__ = lambda : _IDataProcessorProxy


@jsii.interface(jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.IDeliveryStream")
class IDeliveryStream(
    _aws_cdk_ceddda9d.IResource,
    _aws_cdk_aws_iam_ceddda9d.IGrantable,
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    typing_extensions.Protocol,
):
    '''(deprecated) Represents a Kinesis Data Firehose delivery stream.

    :stability: deprecated
    '''

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        '''(deprecated) The ARN of the delivery stream.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        '''(deprecated) The name of the delivery stream.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the ``grantee`` identity permissions to perform ``actions``.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="grantPutRecords")
    def grant_put_records(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the ``grantee`` identity permissions to perform ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` actions on this delivery stream.

        :param grantee: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this delivery stream.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricBackupToS3Bytes")
    def metric_backup_to_s3_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of bytes delivered to Amazon S3 for backup over the specified time period.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricBackupToS3DataFreshness")
    def metric_backup_to_s3_data_freshness(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the age (from getting into Kinesis Data Firehose to now) of the oldest record in Kinesis Data Firehose.

        Any record older than this age has been delivered to the Amazon S3 bucket for backup.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricBackupToS3Records")
    def metric_backup_to_s3_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of records delivered to Amazon S3 for backup over the specified time period.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricIncomingBytes")
    def metric_incoming_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of bytes ingested successfully into the delivery stream over the specified time period after throttling.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricIncomingRecords")
    def metric_incoming_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of records ingested successfully into the delivery stream over the specified time period after throttling.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        ...


class _IDeliveryStreamProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_iam_ceddda9d.IGrantable), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
):
    '''(deprecated) Represents a Kinesis Data Firehose delivery stream.

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-kinesisfirehose-alpha.IDeliveryStream"

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        '''(deprecated) The ARN of the delivery stream.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        '''(deprecated) The name of the delivery stream.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the ``grantee`` identity permissions to perform ``actions``.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e83b2c41b0be3872a96c9d852da78dc5625213352508d0b4a5e81440d9d1a8e)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantPutRecords")
    def grant_put_records(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the ``grantee`` identity permissions to perform ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` actions on this delivery stream.

        :param grantee: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce79dffc4fc87d6b02f31af6954926f1cdb38d458bb0706848609d95b5e62915)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantPutRecords", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this delivery stream.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52389e5ce1f5828630ba548c0c34e45b5f8dfbc1ad4857c9e91cc7ac36dac99f)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricBackupToS3Bytes")
    def metric_backup_to_s3_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of bytes delivered to Amazon S3 for backup over the specified time period.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricBackupToS3Bytes", [props]))

    @jsii.member(jsii_name="metricBackupToS3DataFreshness")
    def metric_backup_to_s3_data_freshness(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the age (from getting into Kinesis Data Firehose to now) of the oldest record in Kinesis Data Firehose.

        Any record older than this age has been delivered to the Amazon S3 bucket for backup.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricBackupToS3DataFreshness", [props]))

    @jsii.member(jsii_name="metricBackupToS3Records")
    def metric_backup_to_s3_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of records delivered to Amazon S3 for backup over the specified time period.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricBackupToS3Records", [props]))

    @jsii.member(jsii_name="metricIncomingBytes")
    def metric_incoming_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of bytes ingested successfully into the delivery stream over the specified time period after throttling.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricIncomingBytes", [props]))

    @jsii.member(jsii_name="metricIncomingRecords")
    def metric_incoming_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of records ingested successfully into the delivery stream over the specified time period after throttling.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricIncomingRecords", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDeliveryStream).__jsii_proxy_class__ = lambda : _IDeliveryStreamProxy


@jsii.interface(jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.IDestination")
class IDestination(typing_extensions.Protocol):
    '''(deprecated) A Kinesis Data Firehose delivery stream destination.

    :stability: deprecated
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> DestinationConfig:
        '''(deprecated) Binds this destination to the Kinesis Data Firehose delivery stream.

        Implementers should use this method to bind resources to the stack and initialize values using the provided stream.

        :param scope: -

        :stability: deprecated
        '''
        ...


class _IDestinationProxy:
    '''(deprecated) A Kinesis Data Firehose delivery stream destination.

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-kinesisfirehose-alpha.IDestination"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> DestinationConfig:
        '''(deprecated) Binds this destination to the Kinesis Data Firehose delivery stream.

        Implementers should use this method to bind resources to the stack and initialize values using the provided stream.

        :param scope: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51d023ede755a18ed86b3caecd01c91773858417bf2e779e934ccc241569676)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        options = DestinationBindOptions()

        return typing.cast(DestinationConfig, jsii.invoke(self, "bind", [scope, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDestination).__jsii_proxy_class__ = lambda : _IDestinationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.ISource")
class ISource(typing_extensions.Protocol):
    '''(deprecated) An interface for defining a source that can be used in a Kinesis Data Firehose delivery stream.

    :stability: deprecated
    '''

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant read permissions for this source resource and its contents to an IAM principal (the delivery stream).

        If an encryption key is used, permission to use the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: deprecated
        '''
        ...


class _ISourceProxy:
    '''(deprecated) An interface for defining a source that can be used in a Kinesis Data Firehose delivery stream.

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-kinesisfirehose-alpha.ISource"

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant read permissions for this source resource and its contents to an IAM principal (the delivery stream).

        If an encryption key is used, permission to use the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e38f00a2c5d4f4f1043008d8d869ea146baac35f9de7d688c4b2a88b1d911c0)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISource).__jsii_proxy_class__ = lambda : _ISourceProxy


@jsii.implements(ISource)
class KinesisStreamSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.KinesisStreamSource",
):
    '''(deprecated) A Kinesis Data Firehose delivery stream source.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        # destination: firehose.IDestination
        
        source_stream = kinesis.Stream(self, "Source Stream")
        
        firehose.DeliveryStream(self, "Delivery Stream",
            source=firehose.KinesisStreamSource(source_stream),
            destination=destination
        )
    '''

    def __init__(self, stream: _aws_cdk_aws_kinesis_ceddda9d.IStream) -> None:
        '''(deprecated) Creates a new KinesisStreamSource.

        :param stream: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be146eea43ce8fa6a05401f7b8ca68f32e7321e6a045467730e4851ffce3f6a1)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        jsii.create(self.__class__, self, [stream])

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant read permissions for this source resource and its contents to an IAM principal (the delivery stream).

        If an encryption key is used, permission to use the key to decrypt the
        contents of the stream will also be granted.

        :param grantee: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d85e94231ec3fbfb3a342ccbdc43c4727a060af7c89163713c9b4a76c93d3e)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))


@jsii.implements(IDataProcessor)
class LambdaFunctionProcessor(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.LambdaFunctionProcessor",
):
    '''(deprecated) Use an AWS Lambda function to transform records.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        # bucket: s3.Bucket
        # Provide a Lambda function that will transform records before delivery, with custom
        # buffering and retry configuration
        lambda_function = lambda_.Function(self, "Processor",
            runtime=lambda_.Runtime.NODEJS_LATEST,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "process-records"))
        )
        lambda_processor = firehose.LambdaFunctionProcessor(lambda_function,
            buffer_interval=Duration.minutes(5),
            buffer_size=Size.mebibytes(5),
            retries=5
        )
        s3_destination = destinations.S3Bucket(bucket,
            processor=lambda_processor
        )
        firehose.DeliveryStream(self, "Delivery Stream",
            destination=s3_destination
        )
    '''

    def __init__(
        self,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        *,
        buffer_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        buffer_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        retries: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param lambda_function: -
        :param buffer_interval: (deprecated) The length of time Kinesis Data Firehose will buffer incoming data before calling the processor. s Default: Duration.minutes(1)
        :param buffer_size: (deprecated) The amount of incoming data Kinesis Data Firehose will buffer before calling the processor. Default: Size.mebibytes(3)
        :param retries: (deprecated) The number of times Kinesis Data Firehose will retry the processor invocation after a failure due to network timeout or invocation limits. Default: 3

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ad5ddd8cb82f7d48b10e7568eedd0f96f6c1002a8170490a68123a94b247e0)
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        props = DataProcessorProps(
            buffer_interval=buffer_interval, buffer_size=buffer_size, retries=retries
        )

        jsii.create(self.__class__, self, [lambda_function, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        *,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> DataProcessorConfig:
        '''(deprecated) Binds this processor to a destination of a delivery stream.

        Implementers should use this method to grant processor invocation permissions to the provided stream and return the
        necessary configuration to register as a processor.

        :param _scope: -
        :param role: (deprecated) The IAM role assumed by Kinesis Data Firehose to write to the destination that this DataProcessor will bind to.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ab51e341f9a14a9cabc6a1c4031e599b81834c9b42a486091b78758471db6d)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        options = DataProcessorBindOptions(role=role)

        return typing.cast(DataProcessorConfig, jsii.invoke(self, "bind", [_scope, options]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> DataProcessorProps:
        '''(deprecated) The constructor props of the LambdaFunctionProcessor.

        :stability: deprecated
        '''
        return typing.cast(DataProcessorProps, jsii.get(self, "props"))


class StreamEncryption(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.StreamEncryption",
):
    '''(deprecated) Represents server-side encryption for a Kinesis Firehose Delivery Stream.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        # destination: firehose.IDestination
        # SSE with an customer-managed key that is explicitly specified
        # key: kms.Key
        
        
        # SSE with an AWS-owned key
        firehose.DeliveryStream(self, "Delivery Stream with AWS Owned Key",
            encryption=firehose.StreamEncryption.aws_owned_key(),
            destination=destination
        )
        # SSE with an customer-managed key that is created automatically by the CDK
        firehose.DeliveryStream(self, "Delivery Stream with Customer Managed Key",
            encryption=firehose.StreamEncryption.customer_managed_key(),
            destination=destination
        )
        firehose.DeliveryStream(self, "Delivery Stream with Customer Managed and Provided Key",
            encryption=firehose.StreamEncryption.customer_managed_key(key),
            destination=destination
        )
    '''

    @jsii.member(jsii_name="awsOwnedKey")
    @builtins.classmethod
    def aws_owned_key(cls) -> "StreamEncryption":
        '''(deprecated) Configure server-side encryption using an AWS owned key.

        :stability: deprecated
        '''
        return typing.cast("StreamEncryption", jsii.sinvoke(cls, "awsOwnedKey", []))

    @jsii.member(jsii_name="customerManagedKey")
    @builtins.classmethod
    def customer_managed_key(
        cls,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> "StreamEncryption":
        '''(deprecated) Configure server-side encryption using customer managed keys.

        :param encryption_key: the KMS key for the delivery stream.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed40b501969f7200de5d0c8a7e56eb2dbe0ea99f831487a5f6bac96cef5d0eb3)
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        return typing.cast("StreamEncryption", jsii.sinvoke(cls, "customerManagedKey", [encryption_key]))

    @jsii.member(jsii_name="unencrypted")
    @builtins.classmethod
    def unencrypted(cls) -> "StreamEncryption":
        '''(deprecated) No server-side encryption is configured.

        :stability: deprecated
        '''
        return typing.cast("StreamEncryption", jsii.sinvoke(cls, "unencrypted", []))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "StreamEncryptionType":
        '''(deprecated) The type of server-side encryption for the Kinesis Firehose delivery stream.

        :stability: deprecated
        '''
        return typing.cast("StreamEncryptionType", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(deprecated) Optional KMS key used for customer managed encryption.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "encryptionKey"))


class _StreamEncryptionProxy(StreamEncryption):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, StreamEncryption).__jsii_proxy_class__ = lambda : _StreamEncryptionProxy


@jsii.enum(jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.StreamEncryptionType")
class StreamEncryptionType(enum.Enum):
    '''(deprecated) Options for server-side encryption of a delivery stream.

    :stability: deprecated
    '''

    UNENCRYPTED = "UNENCRYPTED"
    '''(deprecated) Data in the stream is stored unencrypted.

    :stability: deprecated
    '''
    CUSTOMER_MANAGED = "CUSTOMER_MANAGED"
    '''(deprecated) Data in the stream is stored encrypted by a KMS key managed by the customer.

    :stability: deprecated
    '''
    AWS_OWNED = "AWS_OWNED"
    '''(deprecated) Data in the stream is stored encrypted by a KMS key owned by AWS and managed for use in multiple AWS accounts.

    :stability: deprecated
    '''


@jsii.implements(IDeliveryStream)
class DeliveryStream(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesisfirehose-alpha.DeliveryStream",
):
    '''(deprecated) Create a Kinesis Data Firehose delivery stream.

    :stability: deprecated
    :resource: AWS::KinesisFirehose::DeliveryStream
    :exampleMetadata: infused

    Example::

        # bucket: s3.Bucket
        # Provide a Lambda function that will transform records before delivery, with custom
        # buffering and retry configuration
        lambda_function = lambda_.Function(self, "Processor",
            runtime=lambda_.Runtime.NODEJS_LATEST,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "process-records"))
        )
        lambda_processor = firehose.LambdaFunctionProcessor(lambda_function,
            buffer_interval=Duration.minutes(5),
            buffer_size=Size.mebibytes(5),
            retries=5
        )
        s3_destination = destinations.S3Bucket(bucket,
            processor=lambda_processor
        )
        firehose.DeliveryStream(self, "Delivery Stream",
            destination=s3_destination
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        destination: IDestination,
        delivery_stream_name: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[StreamEncryption] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        source: typing.Optional[ISource] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param destination: (deprecated) The destination that this delivery stream will deliver data to.
        :param delivery_stream_name: (deprecated) A name for the delivery stream. Default: - a name is generated by CloudFormation.
        :param encryption: (deprecated) Indicates the type of customer master key (CMK) to use for server-side encryption, if any. Default: StreamEncryption.unencrypted()
        :param role: (deprecated) The IAM role associated with this delivery stream. Assumed by Kinesis Data Firehose to read from sources and encrypt data server-side. Default: - a role will be created with default permissions.
        :param source: (deprecated) The Kinesis data stream to use as a source for this delivery stream. Default: - data must be written to the delivery stream via a direct put.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208f5c89209d3c20b3a3c0084efb06d5b736bd75af4a592867db25f4a68945e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DeliveryStreamProps(
            destination=destination,
            delivery_stream_name=delivery_stream_name,
            encryption=encryption,
            role=role,
            source=source,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDeliveryStreamArn")
    @builtins.classmethod
    def from_delivery_stream_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        delivery_stream_arn: builtins.str,
    ) -> IDeliveryStream:
        '''(deprecated) Import an existing delivery stream from its ARN.

        :param scope: -
        :param id: -
        :param delivery_stream_arn: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9fcc25a75b7a9f5bc9babea310bb6c89fb28bda587f324f1e0fc18ad762f10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
        return typing.cast(IDeliveryStream, jsii.sinvoke(cls, "fromDeliveryStreamArn", [scope, id, delivery_stream_arn]))

    @jsii.member(jsii_name="fromDeliveryStreamAttributes")
    @builtins.classmethod
    def from_delivery_stream_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        delivery_stream_arn: typing.Optional[builtins.str] = None,
        delivery_stream_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> IDeliveryStream:
        '''(deprecated) Import an existing delivery stream from its attributes.

        :param scope: -
        :param id: -
        :param delivery_stream_arn: (deprecated) The ARN of the delivery stream. At least one of deliveryStreamArn and deliveryStreamName must be provided. Default: - derived from ``deliveryStreamName``.
        :param delivery_stream_name: (deprecated) The name of the delivery stream. At least one of deliveryStreamName and deliveryStreamArn must be provided. Default: - derived from ``deliveryStreamArn``.
        :param role: (deprecated) The IAM role associated with this delivery stream. Assumed by Kinesis Data Firehose to read from sources and encrypt data server-side. Default: - the imported stream cannot be granted access to other resources as an ``iam.IGrantable``.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d1ffa9ef82ad136fc3ac357f1408c9cabf573565d041ea53e380db096eb6c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = DeliveryStreamAttributes(
            delivery_stream_arn=delivery_stream_arn,
            delivery_stream_name=delivery_stream_name,
            role=role,
        )

        return typing.cast(IDeliveryStream, jsii.sinvoke(cls, "fromDeliveryStreamAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromDeliveryStreamName")
    @builtins.classmethod
    def from_delivery_stream_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        delivery_stream_name: builtins.str,
    ) -> IDeliveryStream:
        '''(deprecated) Import an existing delivery stream from its name.

        :param scope: -
        :param id: -
        :param delivery_stream_name: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168d683020312f2b15764cdc25a6be82817b2514d1c2b88155f00def1ad9c568)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
        return typing.cast(IDeliveryStream, jsii.sinvoke(cls, "fromDeliveryStreamName", [scope, id, delivery_stream_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the ``grantee`` identity permissions to perform ``actions``.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515f94ece05e22db1e06d81218142285fb52fd10e8a6d6ee18155b380109775d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantPutRecords")
    def grant_put_records(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the ``grantee`` identity permissions to perform ``firehose:PutRecord`` and ``firehose:PutRecordBatch`` actions on this delivery stream.

        :param grantee: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e89f089940bed5c1c643dc6b376b126bd05eeb1447a041d52ce0d28a8908bd)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantPutRecords", [grantee]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this delivery stream.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c09c95f82beee7d5e89649a93759d6a7c6cc9c416bb7220f83b2f3463dc3b14)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricBackupToS3Bytes")
    def metric_backup_to_s3_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of bytes delivered to Amazon S3 for backup over the specified time period.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricBackupToS3Bytes", [props]))

    @jsii.member(jsii_name="metricBackupToS3DataFreshness")
    def metric_backup_to_s3_data_freshness(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the age (from getting into Kinesis Data Firehose to now) of the oldest record in Kinesis Data Firehose.

        Any record older than this age has been delivered to the Amazon S3 bucket for backup.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricBackupToS3DataFreshness", [props]))

    @jsii.member(jsii_name="metricBackupToS3Records")
    def metric_backup_to_s3_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of records delivered to Amazon S3 for backup over the specified time period.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricBackupToS3Records", [props]))

    @jsii.member(jsii_name="metricIncomingBytes")
    def metric_incoming_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of bytes ingested successfully into the delivery stream over the specified time period after throttling.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricIncomingBytes", [props]))

    @jsii.member(jsii_name="metricIncomingRecords")
    def metric_incoming_records(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of records ingested successfully into the delivery stream over the specified time period after throttling.

        By default, this metric will be calculated as an average over a period of 5 minutes.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricIncomingRecords", [props]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(deprecated) Network connections between Kinesis Data Firehose and other resources, i.e. Redshift cluster.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> builtins.str:
        '''(deprecated) The ARN of the delivery stream.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamArn"))

    @builtins.property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> builtins.str:
        '''(deprecated) The name of the delivery stream.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "deliveryStreamName"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(deprecated) The principal to grant permissions to.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))


__all__ = [
    "DataProcessorBindOptions",
    "DataProcessorConfig",
    "DataProcessorIdentifier",
    "DataProcessorProps",
    "DeliveryStream",
    "DeliveryStreamAttributes",
    "DeliveryStreamProps",
    "DestinationBindOptions",
    "DestinationConfig",
    "IDataProcessor",
    "IDeliveryStream",
    "IDestination",
    "ISource",
    "KinesisStreamSource",
    "LambdaFunctionProcessor",
    "StreamEncryption",
    "StreamEncryptionType",
]

publication.publish()

def _typecheckingstub__fb128eca4e7ba1f83c4f0e58098f008795374fee30ada93711dd3b253dad0ef8(
    *,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d8516a4394f7676eff7b29cec88a391ff919bb6bbda458b6e8e06f6ddb7a88(
    *,
    processor_identifier: typing.Union[DataProcessorIdentifier, typing.Dict[builtins.str, typing.Any]],
    processor_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5e177461759fec4dd89a5e4a7730bec0e39ea197243fa5f2eceea512a39f24(
    *,
    parameter_name: builtins.str,
    parameter_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f8aa68afc823d87c695ee05759728c85e4023a37cf01cf765a10be84fbcac8(
    *,
    buffer_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    buffer_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a349f2444857db9da26d39113740e8ab10e954d7aef8340312a07dcb3ca0c72(
    *,
    delivery_stream_arn: typing.Optional[builtins.str] = None,
    delivery_stream_name: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9413f788fdc9578de6565f85eb1d6d397a1047293bb85b71a059af7643ba38(
    *,
    destination: IDestination,
    delivery_stream_name: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[StreamEncryption] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    source: typing.Optional[ISource] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173daa2306128c47572263a530e0a02f73aa7e3f60be737ce497d123e3edc32d(
    *,
    dependables: typing.Optional[typing.Sequence[_constructs_77d1e7e8.IDependable]] = None,
    extended_s3_destination_configuration: typing.Optional[typing.Union[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c1e85da04925f59501768e65d47bdfdedeb6e3e0dfcee70ee80c529df93f3a(
    scope: _constructs_77d1e7e8.Construct,
    *,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e83b2c41b0be3872a96c9d852da78dc5625213352508d0b4a5e81440d9d1a8e(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce79dffc4fc87d6b02f31af6954926f1cdb38d458bb0706848609d95b5e62915(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52389e5ce1f5828630ba548c0c34e45b5f8dfbc1ad4857c9e91cc7ac36dac99f(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51d023ede755a18ed86b3caecd01c91773858417bf2e779e934ccc241569676(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e38f00a2c5d4f4f1043008d8d869ea146baac35f9de7d688c4b2a88b1d911c0(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be146eea43ce8fa6a05401f7b8ca68f32e7321e6a045467730e4851ffce3f6a1(
    stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d85e94231ec3fbfb3a342ccbdc43c4727a060af7c89163713c9b4a76c93d3e(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ad5ddd8cb82f7d48b10e7568eedd0f96f6c1002a8170490a68123a94b247e0(
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    *,
    buffer_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    buffer_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    retries: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ab51e341f9a14a9cabc6a1c4031e599b81834c9b42a486091b78758471db6d(
    _scope: _constructs_77d1e7e8.Construct,
    *,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed40b501969f7200de5d0c8a7e56eb2dbe0ea99f831487a5f6bac96cef5d0eb3(
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208f5c89209d3c20b3a3c0084efb06d5b736bd75af4a592867db25f4a68945e0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    destination: IDestination,
    delivery_stream_name: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[StreamEncryption] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    source: typing.Optional[ISource] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9fcc25a75b7a9f5bc9babea310bb6c89fb28bda587f324f1e0fc18ad762f10(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    delivery_stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d1ffa9ef82ad136fc3ac357f1408c9cabf573565d041ea53e380db096eb6c0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    delivery_stream_arn: typing.Optional[builtins.str] = None,
    delivery_stream_name: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168d683020312f2b15764cdc25a6be82817b2514d1c2b88155f00def1ad9c568(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    delivery_stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515f94ece05e22db1e06d81218142285fb52fd10e8a6d6ee18155b380109775d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e89f089940bed5c1c643dc6b376b126bd05eeb1447a041d52ce0d28a8908bd(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c09c95f82beee7d5e89649a93759d6a7c6cc9c416bb7220f83b2f3463dc3b14(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass
