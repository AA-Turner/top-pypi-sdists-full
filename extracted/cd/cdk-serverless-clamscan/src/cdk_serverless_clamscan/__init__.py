r'''
# cdk-serverless-clamscan

[![npm version](https://badge.fury.io/js/cdk-serverless-clamscan.svg)](https://badge.fury.io/js/cdk-serverless-clamscan)
[![PyPI version](https://badge.fury.io/py/cdk-serverless-clamscan.svg)](https://badge.fury.io/py/cdk-serverless-clamscan)

An [aws-cdk](https://github.com/aws/aws-cdk) construct that uses [ClamAV®](https://www.clamav.net/) to scan newly uploaded objects to Amazon S3 for viruses. The construct provides a flexible interface for a system to act based on the results of a ClamAV virus scan. Check out this [blogpost](https://aws.amazon.com/blogs/developer/virus-scan-s3-buckets-with-a-serverless-clamav-based-cdk-construct/) for a guided walkthrough.

![Overview](serverless-clamscan.png)

## Pre-Requisites

**Docker:** The ClamAV Lambda functions utilizes a [container image](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/) that is built locally using [docker bundling](https://aws.amazon.com/blogs/devops/building-apps-with-aws-cdk/)

## Examples

This project uses [projen](https://github.com/projen/projen) and thus all the constructs follow language specific standards and naming patterns. For more information on how to translate the following examples into your desired language read the CDK guide on [Translating TypeScript AWS CDK code to other languages](https://docs.aws.amazon.com/cdk/latest/guide/multiple_languages.html)

### Example 1. (Default destinations with rule target)

<details><summary>typescript</summary>
<p>

```python
import { RuleTargetInput } from 'aws-cdk-lib/aws-events';
import { SnsTopic } from 'aws-cdk-lib/aws-events-targets';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { Topic } from 'aws-cdk-lib/aws-sns';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ServerlessClamscan } from 'cdk-serverless-clamscan';

export class CdkTestStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const bucket_1 = new Bucket(this, 'rBucket1');
    const bucket_2 = new Bucket(this, 'rBucket2');
    const bucketList = [bucket_1, bucket_2];
    const sc = new ServerlessClamscan(this, 'rClamscan', {
      buckets: bucketList,
    });
    const bucket_3 = new Bucket(this, 'rBucket3');
    sc.addSourceBucket(bucket_3);
    const infectedTopic = new Topic(this, 'rInfectedTopic');
    sc.infectedRule?.addTarget(
      new SnsTopic(infectedTopic, {
        message: RuleTargetInput.fromEventPath(
          '$.detail.responsePayload.message',
        ),
      }),
    );
  }
}
```

</p>
</details><details><summary>python</summary>
<p>

```python
from aws_cdk import (
  Stack,
  aws_events as events,
  aws_events_targets as events_targets,
  aws_s3 as s3,
  aws_sns as sns
)
from cdk_serverless_clamscan import ServerlessClamscan
from constructs import Construct

class CdkTestStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    bucket_1 = s3.Bucket(self, "rBucket1")
    bucket_2 = s3.Bucket(self, "rBucket2")
    bucketList = [ bucket_1, bucket_2 ]
    sc = ServerlessClamscan(self, "rClamScan",
      buckets=bucketList,
    )
    bucket_3 = s3.Bucket(self, "rBucket3")
    sc.add_source_bucket(bucket_3)
    infected_topic = sns.Topic(self, "rInfectedTopic")
    if sc.infected_rule != None:
      sc.infected_rule.add_target(
        events_targets.SnsTopic(
          infected_topic,
          message=events.RuleTargetInput.from_event_path('$.detail.responsePayload.message'),
        )
      )
```

</p>
</details>

### Example 2. (Bring your own destinations)

<details><summary>typescript</summary>
<p>

```python
import {
  SqsDestination,
  EventBridgeDestination,
} from 'aws-cdk-lib/aws-lambda-destinations';
import { Bucket } from 'aws-cdk-lib/aws-s3';
import { Queue } from 'aws-cdk-lib/aws-sqs';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { ServerlessClamscan } from 'cdk-serverless-clamscan';

export class CdkTestStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const bucket_1 = new Bucket(this, 'rBucket1');
    const bucket_2 = new Bucket(this, 'rBucket2');
    const bucketList = [bucket_1, bucket_2];
    const queue = new Queue(this, 'rQueue');
    const sc = new ServerlessClamscan(this, 'default', {
      buckets: bucketList,
      onResult: new EventBridgeDestination(),
      onError: new SqsDestination(queue),
    });
    const bucket_3 = new Bucket(this, 'rBucket3');
    sc.addSourceBucket(bucket_3);
  }
}
```

</p>
</details><details><summary>python</summary>
<p>

```python
from aws_cdk import (
  Stack,
  aws_lambda_destinations as lambda_destinations,
  aws_s3 as s3,
  aws_sqs as sqs
)
from cdk_serverless_clamscan import ServerlessClamscan
from constructs import Construct

class CdkTestStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    bucket_1 = s3.Bucket(self, "rBucket1")
    bucket_2 = s3.Bucket(self, "rBucket2")
    bucketList = [ bucket_1, bucket_2 ]
    queue = sqs.Queue(self, "rQueue")
    sc = ServerlessClamscan(self, "rClamScan",
      buckets=bucketList,
      on_result=lambda_destinations.EventBridgeDestination(),
      on_error=lambda_destinations.SqsDestination(queue),
    )
    bucket_3 = s3.Bucket(self, "rBucket3")
    sc.add_source_bucket(bucket_3)
```

</p>
</details>

## Operation and Maintenance

When ClamAV publishes updates to the scanner you will see “Your ClamAV installation is OUTDATED” in your scan results. While the construct creates a system to keep the database definitions up to date, you must update the scanner to detect all the latest Viruses.

Update the docker images of the Lambda functions with the latest version of ClamAV by re-running `cdk deploy`.

## Optionally Skip Files

In certain situations, you may have files which are already scanned and you wish to omit them from ClamAV scanning. In that case, simply tag the s3 object with `"scan-status": "N/A"` and the file will be automatically skipped.

### Example 1. (Upload file to skip)

<details><summary>python/boto</summary>
<p>

```python
boto3.client('s3').upload_file(
    Filename=file_path,
    Bucket=bucket_name,
    Key=object_key,
    ExtraArgs={'Tagging': 'scan-status=N/A'}
)
```

</p></details><details><summary>typscript/aws-sdk</summary>
<p>

```python
const params = {
  Bucket: bucketName,
  Key: objectKey,
  Body: fileContent,
  Tagging: 'scan-status=N/A',
};
const command = new PutObjectCommand(params);
const response = await (new S3Client()).send(command);
```

</p>
</details>

## API Reference

See [API.md](./API.md).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
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
import aws_cdk.aws_efs as _aws_cdk_aws_efs_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import constructs as _constructs_77d1e7e8


class ServerlessClamscan(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-serverless-clamscan.ServerlessClamscan",
):
    '''An `aws-cdk <https://github.com/aws/aws-cdk>`_ construct that uses `ClamAV® <https://www.clamav.net/>`_. to scan objects in Amazon S3 for viruses. The construct provides a flexible interface for a system to act based on the results of a ClamAV virus scan.

    The construct creates a Lambda function with EFS integration to support larger files.
    A VPC with isolated subnets, a S3 Gateway endpoint will also be created.

    Additionally creates an twice-daily job to download the latest ClamAV definition files to the
    Virus Definitions S3 Bucket by utilizing an EventBridge rule and a Lambda function and
    publishes CloudWatch Metrics to the 'serverless-clamscan' namespace.

    **Important O&M**:
    When ClamAV publishes updates to the scanner you will see “Your ClamAV installation is OUTDATED” in your scan results.
    While the construct creates a system to keep the database definitions up to date, you must update the scanner to
    detect all the latest Viruses.

    Update the docker images of the Lambda functions with the latest version of ClamAV by re-running ``cdk deploy``.

    Successful Scan Event format Example::

       {
          "source": "serverless-clamscan",
          "input_bucket": <input_bucket_name>,
          "input_key": <object_key>,
          "status": <"CLEAN"|"INFECTED"|"N/A">,
          "message": <scan_summary>,
        }

    Note: The Virus Definitions bucket policy will likely cause a deletion error if you choose to delete
    the stack associated in the construct. However since the bucket itself gets deleted, you can delete
    the stack again to resolve the error.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        accept_responsibility_for_using_imported_bucket: typing.Optional[builtins.bool] = None,
        buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        defs_bucket_access_logs_config: typing.Optional[typing.Union["ServerlessClamscanLoggingProps", typing.Dict[builtins.str, typing.Any]]] = None,
        defs_bucket_allow_policy_mutation: typing.Optional[builtins.bool] = None,
        efs_encryption: typing.Optional[builtins.bool] = None,
        efs_performance_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode] = None,
        efs_provisioned_throughput_per_second: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        efs_throughput_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode] = None,
        on_error: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_result: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        reserved_concurrency: typing.Optional[jsii.Number] = None,
        scan_function_memory_size: typing.Optional[jsii.Number] = None,
        scan_function_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Creates a ServerlessClamscan construct.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param accept_responsibility_for_using_imported_bucket: Allows the use of imported buckets. When using imported buckets the user is responsible for adding the required policy statement to the bucket policy: ``getPolicyStatementForBucket()`` can be used to retrieve the policy statement required by the solution.
        :param buckets: An optional list of S3 buckets to configure for ClamAV Virus Scanning; buckets can be added later by calling addSourceBucket.
        :param defs_bucket_access_logs_config: Whether or not to enable Access Logging for the Virus Definitions bucket, you can specify an existing bucket and prefix (Default: Creates a new S3 Bucket for access logs).
        :param defs_bucket_allow_policy_mutation: Allow for non-root users to modify/delete the bucket policy on the Virus Definitions bucket. Warning: changing this flag from 'false' to 'true' on existing deployments will cause updates to fail. Default: false
        :param efs_encryption: Whether or not to enable encryption on EFS filesystem (Default: enabled).
        :param efs_performance_mode: Set the performance mode of the EFS file system (Default: GENERAL_PURPOSE).
        :param efs_provisioned_throughput_per_second: Provisioned throughput for the EFS file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s (Default: none).
        :param efs_throughput_mode: Set the throughput mode of the EFS file system (Default: BURSTING).
        :param on_error: The Lambda Destination for files that fail to scan and are marked 'ERROR' or stuck 'IN PROGRESS' due to a Lambda timeout (Default: Creates and publishes to a new SQS queue if unspecified).
        :param on_result: The Lambda Destination for files marked 'CLEAN' or 'INFECTED' based on the ClamAV Virus scan or 'N/A' for scans triggered by S3 folder creation events marked (Default: Creates and publishes to a new Event Bridge Bus if unspecified).
        :param reserved_concurrency: Optionally set a reserved concurrency for the virus scanning Lambda.
        :param scan_function_memory_size: Optionally set the memory allocation for the scan function. Note that low memory allocations may cause errors. (Default: 10240).
        :param scan_function_timeout: Optionally set the timeout for the scan function. (Default: 15 minutes).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8d91de6d3b1d3b5b25b039320198cf5ad1c0f9205948695f5a09421a986084)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServerlessClamscanProps(
            accept_responsibility_for_using_imported_bucket=accept_responsibility_for_using_imported_bucket,
            buckets=buckets,
            defs_bucket_access_logs_config=defs_bucket_access_logs_config,
            defs_bucket_allow_policy_mutation=defs_bucket_allow_policy_mutation,
            efs_encryption=efs_encryption,
            efs_performance_mode=efs_performance_mode,
            efs_provisioned_throughput_per_second=efs_provisioned_throughput_per_second,
            efs_throughput_mode=efs_throughput_mode,
            on_error=on_error,
            on_result=on_result,
            reserved_concurrency=reserved_concurrency,
            scan_function_memory_size=scan_function_memory_size,
            scan_function_timeout=scan_function_timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSourceBucket")
    def add_source_bucket(self, bucket: _aws_cdk_aws_s3_ceddda9d.IBucket) -> None:
        '''Sets the specified S3 Bucket as a s3:ObjectCreate* for the ClamAV function.

        Grants the ClamAV function permissions to get and tag objects.
        Adds a bucket policy to disallow GetObject operations on files that are tagged 'IN PROGRESS', 'INFECTED', or 'ERROR'.

        :param bucket: The bucket to add the scanning bucket policy and s3:ObjectCreate* trigger to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e814dc0b4006f620db601182ab2e1605421bf11a1ddd8d6862a3542134d7568)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(None, jsii.invoke(self, "addSourceBucket", [bucket]))

    @jsii.member(jsii_name="getPolicyStatementForBucket")
    def get_policy_statement_for_bucket(
        self,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    ) -> _aws_cdk_aws_iam_ceddda9d.PolicyStatement:
        '''Returns the statement that should be added to the bucket policy in order to prevent objects to be accessed when they are not clean or there have been scanning errors: this policy should be added manually if external buckets are passed to addSourceBucket().

        :param bucket: The bucket which you need to protect with the policy.

        :return: PolicyStatement the policy statement if available
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7810beb50932b9b83ee8c63bc62209567de654d2032fafbe7348d1b7415fa413)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PolicyStatement, jsii.invoke(self, "getPolicyStatementForBucket", [bucket]))

    @builtins.property
    @jsii.member(jsii_name="errorDest")
    def error_dest(self) -> _aws_cdk_aws_lambda_ceddda9d.IDestination:
        '''The Lambda Destination for failed on erred scans [ERROR, IN PROGRESS (If error is due to Lambda timeout)].'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IDestination, jsii.get(self, "errorDest"))

    @builtins.property
    @jsii.member(jsii_name="resultDest")
    def result_dest(self) -> _aws_cdk_aws_lambda_ceddda9d.IDestination:
        '''The Lambda Destination for completed ClamAV scans [CLEAN, INFECTED].'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IDestination, jsii.get(self, "resultDest"))

    @builtins.property
    @jsii.member(jsii_name="scanAssumedPrincipal")
    def scan_assumed_principal(self) -> _aws_cdk_aws_iam_ceddda9d.ArnPrincipal:
        '''
        :return: ArnPrincipal the ARN of the assumed role principal for the scan function
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.ArnPrincipal, jsii.get(self, "scanAssumedPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="cleanRule")
    def clean_rule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Rule]:
        '''Conditional: An Event Bridge Rule for files that are marked 'CLEAN' by ClamAV if a success destination was not specified.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Rule], jsii.get(self, "cleanRule"))

    @builtins.property
    @jsii.member(jsii_name="defsAccessLogsBucket")
    def defs_access_logs_bucket(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''Conditional: The Bucket for access logs for the virus definitions bucket if logging is enabled (defsBucketAccessLogsConfig).'''
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], jsii.get(self, "defsAccessLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="errorDeadLetterQueue")
    def error_dead_letter_queue(
        self,
    ) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.Queue]:
        '''Conditional: The SQS Dead Letter Queue for the errorQueue if a failure (onError) destination was not specified.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.Queue], jsii.get(self, "errorDeadLetterQueue"))

    @builtins.property
    @jsii.member(jsii_name="errorQueue")
    def error_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.Queue]:
        '''Conditional: The SQS Queue for erred scans if a failure (onError) destination was not specified.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.Queue], jsii.get(self, "errorQueue"))

    @builtins.property
    @jsii.member(jsii_name="infectedRule")
    def infected_rule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Rule]:
        '''Conditional: An Event Bridge Rule for files that are marked 'INFECTED' by ClamAV if a success destination was not specified.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Rule], jsii.get(self, "infectedRule"))

    @builtins.property
    @jsii.member(jsii_name="resultBus")
    def result_bus(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.EventBus]:
        '''Conditional: The Event Bridge Bus for completed ClamAV scans if a success (onResult) destination was not specified.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.EventBus], jsii.get(self, "resultBus"))

    @builtins.property
    @jsii.member(jsii_name="useImportedBuckets")
    def use_imported_buckets(self) -> typing.Optional[builtins.bool]:
        '''Conditional: When true, the user accepted the responsibility for using imported buckets.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useImportedBuckets"))


@jsii.data_type(
    jsii_type="cdk-serverless-clamscan.ServerlessClamscanLoggingProps",
    jsii_struct_bases=[],
    name_mapping={"logs_bucket": "logsBucket", "logs_prefix": "logsPrefix"},
)
class ServerlessClamscanLoggingProps:
    def __init__(
        self,
        *,
        logs_bucket: typing.Optional[typing.Union[builtins.bool, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        logs_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Interface for ServerlessClamscan Virus Definitions S3 Bucket Logging.

        :param logs_bucket: Destination bucket for the server access logs (Default: Creates a new S3 Bucket for access logs).
        :param logs_prefix: Optional log file prefix to use for the bucket's access logs, option is ignored if logs_bucket is set to false.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6710eb9eef2e9b05a93d9fba80fbf988499356d748d843afa0ab4772c40b9a4)
            check_type(argname="argument logs_bucket", value=logs_bucket, expected_type=type_hints["logs_bucket"])
            check_type(argname="argument logs_prefix", value=logs_prefix, expected_type=type_hints["logs_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if logs_bucket is not None:
            self._values["logs_bucket"] = logs_bucket
        if logs_prefix is not None:
            self._values["logs_prefix"] = logs_prefix

    @builtins.property
    def logs_bucket(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_aws_s3_ceddda9d.IBucket]]:
        '''Destination bucket for the server access logs (Default: Creates a new S3 Bucket for access logs).'''
        result = self._values.get("logs_bucket")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_aws_s3_ceddda9d.IBucket]], result)

    @builtins.property
    def logs_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional log file prefix to use for the bucket's access logs, option is ignored if logs_bucket is set to false.'''
        result = self._values.get("logs_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessClamscanLoggingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-serverless-clamscan.ServerlessClamscanProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_responsibility_for_using_imported_bucket": "acceptResponsibilityForUsingImportedBucket",
        "buckets": "buckets",
        "defs_bucket_access_logs_config": "defsBucketAccessLogsConfig",
        "defs_bucket_allow_policy_mutation": "defsBucketAllowPolicyMutation",
        "efs_encryption": "efsEncryption",
        "efs_performance_mode": "efsPerformanceMode",
        "efs_provisioned_throughput_per_second": "efsProvisionedThroughputPerSecond",
        "efs_throughput_mode": "efsThroughputMode",
        "on_error": "onError",
        "on_result": "onResult",
        "reserved_concurrency": "reservedConcurrency",
        "scan_function_memory_size": "scanFunctionMemorySize",
        "scan_function_timeout": "scanFunctionTimeout",
    },
)
class ServerlessClamscanProps:
    def __init__(
        self,
        *,
        accept_responsibility_for_using_imported_bucket: typing.Optional[builtins.bool] = None,
        buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
        defs_bucket_access_logs_config: typing.Optional[typing.Union[ServerlessClamscanLoggingProps, typing.Dict[builtins.str, typing.Any]]] = None,
        defs_bucket_allow_policy_mutation: typing.Optional[builtins.bool] = None,
        efs_encryption: typing.Optional[builtins.bool] = None,
        efs_performance_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode] = None,
        efs_provisioned_throughput_per_second: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        efs_throughput_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode] = None,
        on_error: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_result: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        reserved_concurrency: typing.Optional[jsii.Number] = None,
        scan_function_memory_size: typing.Optional[jsii.Number] = None,
        scan_function_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Interface for creating a ServerlessClamscan.

        :param accept_responsibility_for_using_imported_bucket: Allows the use of imported buckets. When using imported buckets the user is responsible for adding the required policy statement to the bucket policy: ``getPolicyStatementForBucket()`` can be used to retrieve the policy statement required by the solution.
        :param buckets: An optional list of S3 buckets to configure for ClamAV Virus Scanning; buckets can be added later by calling addSourceBucket.
        :param defs_bucket_access_logs_config: Whether or not to enable Access Logging for the Virus Definitions bucket, you can specify an existing bucket and prefix (Default: Creates a new S3 Bucket for access logs).
        :param defs_bucket_allow_policy_mutation: Allow for non-root users to modify/delete the bucket policy on the Virus Definitions bucket. Warning: changing this flag from 'false' to 'true' on existing deployments will cause updates to fail. Default: false
        :param efs_encryption: Whether or not to enable encryption on EFS filesystem (Default: enabled).
        :param efs_performance_mode: Set the performance mode of the EFS file system (Default: GENERAL_PURPOSE).
        :param efs_provisioned_throughput_per_second: Provisioned throughput for the EFS file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s (Default: none).
        :param efs_throughput_mode: Set the throughput mode of the EFS file system (Default: BURSTING).
        :param on_error: The Lambda Destination for files that fail to scan and are marked 'ERROR' or stuck 'IN PROGRESS' due to a Lambda timeout (Default: Creates and publishes to a new SQS queue if unspecified).
        :param on_result: The Lambda Destination for files marked 'CLEAN' or 'INFECTED' based on the ClamAV Virus scan or 'N/A' for scans triggered by S3 folder creation events marked (Default: Creates and publishes to a new Event Bridge Bus if unspecified).
        :param reserved_concurrency: Optionally set a reserved concurrency for the virus scanning Lambda.
        :param scan_function_memory_size: Optionally set the memory allocation for the scan function. Note that low memory allocations may cause errors. (Default: 10240).
        :param scan_function_timeout: Optionally set the timeout for the scan function. (Default: 15 minutes).
        '''
        if isinstance(defs_bucket_access_logs_config, dict):
            defs_bucket_access_logs_config = ServerlessClamscanLoggingProps(**defs_bucket_access_logs_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf16e4cfa40d24a942937d7d5ee19975f275f2c96366670b2ec79ce3f1a2213)
            check_type(argname="argument accept_responsibility_for_using_imported_bucket", value=accept_responsibility_for_using_imported_bucket, expected_type=type_hints["accept_responsibility_for_using_imported_bucket"])
            check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
            check_type(argname="argument defs_bucket_access_logs_config", value=defs_bucket_access_logs_config, expected_type=type_hints["defs_bucket_access_logs_config"])
            check_type(argname="argument defs_bucket_allow_policy_mutation", value=defs_bucket_allow_policy_mutation, expected_type=type_hints["defs_bucket_allow_policy_mutation"])
            check_type(argname="argument efs_encryption", value=efs_encryption, expected_type=type_hints["efs_encryption"])
            check_type(argname="argument efs_performance_mode", value=efs_performance_mode, expected_type=type_hints["efs_performance_mode"])
            check_type(argname="argument efs_provisioned_throughput_per_second", value=efs_provisioned_throughput_per_second, expected_type=type_hints["efs_provisioned_throughput_per_second"])
            check_type(argname="argument efs_throughput_mode", value=efs_throughput_mode, expected_type=type_hints["efs_throughput_mode"])
            check_type(argname="argument on_error", value=on_error, expected_type=type_hints["on_error"])
            check_type(argname="argument on_result", value=on_result, expected_type=type_hints["on_result"])
            check_type(argname="argument reserved_concurrency", value=reserved_concurrency, expected_type=type_hints["reserved_concurrency"])
            check_type(argname="argument scan_function_memory_size", value=scan_function_memory_size, expected_type=type_hints["scan_function_memory_size"])
            check_type(argname="argument scan_function_timeout", value=scan_function_timeout, expected_type=type_hints["scan_function_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_responsibility_for_using_imported_bucket is not None:
            self._values["accept_responsibility_for_using_imported_bucket"] = accept_responsibility_for_using_imported_bucket
        if buckets is not None:
            self._values["buckets"] = buckets
        if defs_bucket_access_logs_config is not None:
            self._values["defs_bucket_access_logs_config"] = defs_bucket_access_logs_config
        if defs_bucket_allow_policy_mutation is not None:
            self._values["defs_bucket_allow_policy_mutation"] = defs_bucket_allow_policy_mutation
        if efs_encryption is not None:
            self._values["efs_encryption"] = efs_encryption
        if efs_performance_mode is not None:
            self._values["efs_performance_mode"] = efs_performance_mode
        if efs_provisioned_throughput_per_second is not None:
            self._values["efs_provisioned_throughput_per_second"] = efs_provisioned_throughput_per_second
        if efs_throughput_mode is not None:
            self._values["efs_throughput_mode"] = efs_throughput_mode
        if on_error is not None:
            self._values["on_error"] = on_error
        if on_result is not None:
            self._values["on_result"] = on_result
        if reserved_concurrency is not None:
            self._values["reserved_concurrency"] = reserved_concurrency
        if scan_function_memory_size is not None:
            self._values["scan_function_memory_size"] = scan_function_memory_size
        if scan_function_timeout is not None:
            self._values["scan_function_timeout"] = scan_function_timeout

    @builtins.property
    def accept_responsibility_for_using_imported_bucket(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''Allows the use of imported buckets.

        When using imported buckets the user is responsible for adding the required policy statement to the bucket policy: ``getPolicyStatementForBucket()`` can be used to retrieve the policy statement required by the solution.
        '''
        result = self._values.get("accept_responsibility_for_using_imported_bucket")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def buckets(self) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]]:
        '''An optional list of S3 buckets to configure for ClamAV Virus Scanning;

        buckets can be added later by calling addSourceBucket.
        '''
        result = self._values.get("buckets")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IBucket]], result)

    @builtins.property
    def defs_bucket_access_logs_config(
        self,
    ) -> typing.Optional[ServerlessClamscanLoggingProps]:
        '''Whether or not to enable Access Logging for the Virus Definitions bucket, you can specify an existing bucket and prefix (Default: Creates a new S3 Bucket for access logs).'''
        result = self._values.get("defs_bucket_access_logs_config")
        return typing.cast(typing.Optional[ServerlessClamscanLoggingProps], result)

    @builtins.property
    def defs_bucket_allow_policy_mutation(self) -> typing.Optional[builtins.bool]:
        '''Allow for non-root users to modify/delete the bucket policy on the Virus Definitions bucket.

        Warning: changing this flag from 'false' to 'true' on existing deployments will cause updates to fail.

        :default: false
        '''
        result = self._values.get("defs_bucket_allow_policy_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def efs_encryption(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to enable encryption on EFS filesystem (Default: enabled).'''
        result = self._values.get("efs_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def efs_performance_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode]:
        '''Set the performance mode of the EFS file system (Default: GENERAL_PURPOSE).'''
        result = self._values.get("efs_performance_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode], result)

    @builtins.property
    def efs_provisioned_throughput_per_second(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''Provisioned throughput for the EFS file system.

        This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s (Default: none).
        '''
        result = self._values.get("efs_provisioned_throughput_per_second")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def efs_throughput_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode]:
        '''Set the throughput mode of the EFS file system (Default: BURSTING).'''
        result = self._values.get("efs_throughput_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode], result)

    @builtins.property
    def on_error(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination]:
        '''The Lambda Destination for files that fail to scan and are marked 'ERROR' or stuck 'IN PROGRESS' due to a Lambda timeout (Default: Creates and publishes to a new SQS queue if unspecified).'''
        result = self._values.get("on_error")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination], result)

    @builtins.property
    def on_result(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination]:
        '''The Lambda Destination for files marked 'CLEAN' or 'INFECTED' based on the ClamAV Virus scan or 'N/A' for scans triggered by S3 folder creation events marked (Default: Creates and publishes to a new Event Bridge Bus if unspecified).'''
        result = self._values.get("on_result")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination], result)

    @builtins.property
    def reserved_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Optionally set a reserved concurrency for the virus scanning Lambda.

        :see: https://docs.aws.amazon.com/lambda/latest/operatorguide/reserved-concurrency.html
        '''
        result = self._values.get("reserved_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scan_function_memory_size(self) -> typing.Optional[jsii.Number]:
        '''Optionally set the memory allocation for the scan function.

        Note that low memory allocations may cause errors. (Default: 10240).

        :see: https://docs.aws.amazon.com/lambda/latest/operatorguide/computing-power.html
        '''
        result = self._values.get("scan_function_memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scan_function_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Optionally set the timeout for the scan function.

        (Default: 15 minutes).
        '''
        result = self._values.get("scan_function_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessClamscanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ServerlessClamscan",
    "ServerlessClamscanLoggingProps",
    "ServerlessClamscanProps",
]

publication.publish()

def _typecheckingstub__ed8d91de6d3b1d3b5b25b039320198cf5ad1c0f9205948695f5a09421a986084(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    accept_responsibility_for_using_imported_bucket: typing.Optional[builtins.bool] = None,
    buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    defs_bucket_access_logs_config: typing.Optional[typing.Union[ServerlessClamscanLoggingProps, typing.Dict[builtins.str, typing.Any]]] = None,
    defs_bucket_allow_policy_mutation: typing.Optional[builtins.bool] = None,
    efs_encryption: typing.Optional[builtins.bool] = None,
    efs_performance_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode] = None,
    efs_provisioned_throughput_per_second: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    efs_throughput_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode] = None,
    on_error: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_result: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    reserved_concurrency: typing.Optional[jsii.Number] = None,
    scan_function_memory_size: typing.Optional[jsii.Number] = None,
    scan_function_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e814dc0b4006f620db601182ab2e1605421bf11a1ddd8d6862a3542134d7568(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7810beb50932b9b83ee8c63bc62209567de654d2032fafbe7348d1b7415fa413(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6710eb9eef2e9b05a93d9fba80fbf988499356d748d843afa0ab4772c40b9a4(
    *,
    logs_bucket: typing.Optional[typing.Union[builtins.bool, _aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    logs_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf16e4cfa40d24a942937d7d5ee19975f275f2c96366670b2ec79ce3f1a2213(
    *,
    accept_responsibility_for_using_imported_bucket: typing.Optional[builtins.bool] = None,
    buckets: typing.Optional[typing.Sequence[_aws_cdk_aws_s3_ceddda9d.IBucket]] = None,
    defs_bucket_access_logs_config: typing.Optional[typing.Union[ServerlessClamscanLoggingProps, typing.Dict[builtins.str, typing.Any]]] = None,
    defs_bucket_allow_policy_mutation: typing.Optional[builtins.bool] = None,
    efs_encryption: typing.Optional[builtins.bool] = None,
    efs_performance_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode] = None,
    efs_provisioned_throughput_per_second: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    efs_throughput_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode] = None,
    on_error: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_result: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    reserved_concurrency: typing.Optional[jsii.Number] = None,
    scan_function_memory_size: typing.Optional[jsii.Number] = None,
    scan_function_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
