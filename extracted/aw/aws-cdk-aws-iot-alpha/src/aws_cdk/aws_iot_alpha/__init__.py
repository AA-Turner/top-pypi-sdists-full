r'''
# AWS IoT Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS IoT Core lets you connect billions of IoT devices and route trillions of
messages to AWS services without managing infrastructure.

## `TopicRule`

Create a topic rule that give your devices the ability to interact with AWS services.
You can create a topic rule with an action that invoke the Lambda action as following:

```python
func = lambda_.Function(self, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_inline("""
            exports.handler = (event) => {
              console.log("It is test for lambda action of AWS IoT Rule.", event);
            };""")
)

iot.TopicRule(self, "TopicRule",
    topic_rule_name="MyTopicRule",  # optional
    description="invokes the lambda function",  # optional
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
    actions=[actions.LambdaFunctionAction(func)]
)
```

Or, you can add an action after constructing the `TopicRule` instance as following:

```python
# func: lambda.Function


topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'")
)
topic_rule.add_action(actions.LambdaFunctionAction(func))
```

You can also supply `errorAction` as following,
and the IoT Rule will trigger it if a rule's action is unable to perform:

```python
import aws_cdk.aws_logs as logs


log_group = logs.LogGroup(self, "MyLogGroup")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
    error_action=actions.CloudWatchLogsAction(log_group)
)
```

If you wanna make the topic rule disable, add property `enabled: false` as following:

```python
iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
    enabled=False
)
```

See also [@aws-cdk/aws-iot-actions-alpha](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-iot-actions-alpha-readme.html) for other actions.

## Logging

AWS IoT provides a [logging feature](https://docs.aws.amazon.com/iot/latest/developerguide/configure-logging.html) that allows you to monitor and log AWS IoT activity.

You can enable IoT logging with the following code:

```python
iot.Logging(self, "Logging",
    log_level=iot.LogLevel.INFO
)
```

**Note**: All logs are forwarded to the `AWSIotLogsV2` log group in CloudWatch.

## Audit

An [AWS IoT Device Defender audit looks](https://docs.aws.amazon.com/iot-device-defender/latest/devguide/device-defender-audit.html) at account- and device-related settings and policies to ensure security measures are in place.
An audit can help you detect any drifts from security best practices or access policies.

### Account Audit Configuration

The IoT audit includes [various audit checks](https://docs.aws.amazon.com/iot-device-defender/latest/devguide/device-defender-audit-checks.html), and it is necessary to configure settings to enable those checks.

You can enable an account audit configuration with the following code:

```python
# Audit notification are sent to the SNS topic
# target_topic: sns.ITopic


iot.AccountAuditConfiguration(self, "AuditConfiguration",
    target_topic=target_topic
)
```

By default, all audit checks are enabled, but it is also possible to enable only specific audit checks.

```python
iot.AccountAuditConfiguration(self, "AuditConfiguration",
    check_configuration=iot.CheckConfiguration(
        # enabled
        authenticated_cognito_role_overly_permissive_check=True,
        # enabled by default
        ca_certificate_expiring_check=undefined,
        # disabled
        ca_certificate_key_quality_check=False,
        conflicting_client_ids_check=False,
        device_certificate_age_check=False,
        device_certificate_expiring_check=False,
        device_certificate_key_quality_check=False,
        device_certificate_shared_check=False,
        intermediate_ca_revoked_for_active_device_certificates_check=False,
        io_tPolicy_potential_mis_configuration_check=False,
        iot_policy_overly_permissive_check=False,
        iot_role_alias_allows_access_to_unused_services_check=False,
        iot_role_alias_overly_permissive_check=False,
        logging_disabled_check=False,
        revoked_ca_certificate_still_active_check=False,
        revoked_device_certificate_still_active_check=False,
        unauthenticated_cognito_role_overly_permissive_check=False
    )
)
```

To configure [the device certificate age check](https://docs.aws.amazon.com/iot-device-defender/latest/devguide/device-certificate-age-check.html), you can specify the duration for the check:

```python
from aws_cdk import Duration


iot.AccountAuditConfiguration(self, "AuditConfiguration",
    check_configuration=iot.CheckConfiguration(
        device_certificate_age_check=True,
        # The default value is 365 days
        # Valid values range from 30 days (minimum) to 3650 days (10 years, maximum)
        device_certificate_age_check_duration=Duration.days(365)
    )
)
```

### Scheduled Audit

You can create a [scheduled audit](https://docs.aws.amazon.com/iot-device-defender/latest/devguide/AuditCommands.html#device-defender-AuditCommandsManageSchedules) that is run at a specified time interval. Checks must be enabled for your account by creating `AccountAuditConfiguration`.

```python
# config: iot.AccountAuditConfiguration


# Daily audit
daily_audit = iot.ScheduledAudit(self, "DailyAudit",
    account_audit_configuration=config,
    frequency=iot.Frequency.DAILY,
    audit_checks=[iot.AuditCheck.AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK
    ]
)

# Weekly audit
weekly_audit = iot.ScheduledAudit(self, "WeeklyAudit",
    account_audit_configuration=config,
    frequency=iot.Frequency.WEEKLY,
    day_of_week=iot.DayOfWeek.SUNDAY,
    audit_checks=[iot.AuditCheck.CA_CERTIFICATE_EXPIRING_CHECK
    ]
)

# Monthly audit
monthly_audit = iot.ScheduledAudit(self, "MonthlyAudit",
    account_audit_configuration=config,
    frequency=iot.Frequency.MONTHLY,
    day_of_month=iot.DayOfMonth.of(1),
    audit_checks=[iot.AuditCheck.CA_CERTIFICATE_KEY_QUALITY_CHECK
    ]
)
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
import aws_cdk.aws_iot as _aws_cdk_aws_iot_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.AccountAuditConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "check_configuration": "checkConfiguration",
        "target_topic": "targetTopic",
    },
)
class AccountAuditConfigurationProps:
    def __init__(
        self,
        *,
        check_configuration: typing.Optional[typing.Union["CheckConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        target_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    ) -> None:
        '''(experimental) Properties for defining AWS IoT Audit Configuration.

        :param check_configuration: (experimental) Specifies which audit checks are enabled and disabled for this account. Default: - all checks are enabled
        :param target_topic: (experimental) The target SNS topic to which audit notifications are sent. Default: - no notifications are sent

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk import Duration
            
            
            iot.AccountAuditConfiguration(self, "AuditConfiguration",
                check_configuration=iot.CheckConfiguration(
                    device_certificate_age_check=True,
                    # The default value is 365 days
                    # Valid values range from 30 days (minimum) to 3650 days (10 years, maximum)
                    device_certificate_age_check_duration=Duration.days(365)
                )
            )
        '''
        if isinstance(check_configuration, dict):
            check_configuration = CheckConfiguration(**check_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ef57f1dae6189d9b6717339eb57703831b4cdca305db4315a06756bad305b2)
            check_type(argname="argument check_configuration", value=check_configuration, expected_type=type_hints["check_configuration"])
            check_type(argname="argument target_topic", value=target_topic, expected_type=type_hints["target_topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if check_configuration is not None:
            self._values["check_configuration"] = check_configuration
        if target_topic is not None:
            self._values["target_topic"] = target_topic

    @builtins.property
    def check_configuration(self) -> typing.Optional["CheckConfiguration"]:
        '''(experimental) Specifies which audit checks are enabled and disabled for this account.

        :default: - all checks are enabled

        :stability: experimental
        '''
        result = self._values.get("check_configuration")
        return typing.cast(typing.Optional["CheckConfiguration"], result)

    @builtins.property
    def target_topic(self) -> typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic]:
        '''(experimental) The target SNS topic to which audit notifications are sent.

        :default: - no notifications are sent

        :stability: experimental
        '''
        result = self._values.get("target_topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountAuditConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.ActionConfig",
    jsii_struct_bases=[],
    name_mapping={"configuration": "configuration"},
)
class ActionConfig:
    def __init__(
        self,
        *,
        configuration: typing.Union[_aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Properties for an topic rule action.

        :param configuration: (experimental) The configuration for this action.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_alpha as iot_alpha
            
            action_config = iot_alpha.ActionConfig(
                configuration=ActionProperty(
                    cloudwatch_alarm=CloudwatchAlarmActionProperty(
                        alarm_name="alarmName",
                        role_arn="roleArn",
                        state_reason="stateReason",
                        state_value="stateValue"
                    ),
                    cloudwatch_logs=CloudwatchLogsActionProperty(
                        log_group_name="logGroupName",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        batch_mode=False
                    ),
                    cloudwatch_metric=CloudwatchMetricActionProperty(
                        metric_name="metricName",
                        metric_namespace="metricNamespace",
                        metric_unit="metricUnit",
                        metric_value="metricValue",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        metric_timestamp="metricTimestamp"
                    ),
                    dynamo_db=DynamoDBActionProperty(
                        hash_key_field="hashKeyField",
                        hash_key_value="hashKeyValue",
                        role_arn="roleArn",
                        table_name="tableName",
            
                        # the properties below are optional
                        hash_key_type="hashKeyType",
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue"
                    ),
                    dynamo_dBv2=DynamoDBv2ActionProperty(
                        put_item=PutItemInputProperty(
                            table_name="tableName"
                        ),
                        role_arn="roleArn"
                    ),
                    elasticsearch=ElasticsearchActionProperty(
                        endpoint="endpoint",
                        id="id",
                        index="index",
                        role_arn="roleArn",
                        type="type"
                    ),
                    firehose=FirehoseActionProperty(
                        delivery_stream_name="deliveryStreamName",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        batch_mode=False,
                        separator="separator"
                    ),
                    http=HttpActionProperty(
                        url="url",
            
                        # the properties below are optional
                        auth=HttpAuthorizationProperty(
                            sigv4=SigV4AuthorizationProperty(
                                role_arn="roleArn",
                                service_name="serviceName",
                                signing_region="signingRegion"
                            )
                        ),
                        confirmation_url="confirmationUrl",
                        headers=[HttpActionHeaderProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    iot_analytics=IotAnalyticsActionProperty(
                        channel_name="channelName",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        batch_mode=False
                    ),
                    iot_events=IotEventsActionProperty(
                        input_name="inputName",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        batch_mode=False,
                        message_id="messageId"
                    ),
                    iot_site_wise=IotSiteWiseActionProperty(
                        put_asset_property_value_entries=[PutAssetPropertyValueEntryProperty(
                            property_values=[AssetPropertyValueProperty(
                                timestamp=AssetPropertyTimestampProperty(
                                    time_in_seconds="timeInSeconds",
            
                                    # the properties below are optional
                                    offset_in_nanos="offsetInNanos"
                                ),
                                value=AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                ),
            
                                # the properties below are optional
                                quality="quality"
                            )],
            
                            # the properties below are optional
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId"
                        )],
                        role_arn="roleArn"
                    ),
                    kafka=KafkaActionProperty(
                        client_properties={
                            "client_properties_key": "clientProperties"
                        },
                        destination_arn="destinationArn",
                        topic="topic",
            
                        # the properties below are optional
                        headers=[KafkaActionHeaderProperty(
                            key="key",
                            value="value"
                        )],
                        key="key",
                        partition="partition"
                    ),
                    kinesis=KinesisActionProperty(
                        role_arn="roleArn",
                        stream_name="streamName",
            
                        # the properties below are optional
                        partition_key="partitionKey"
                    ),
                    lambda_=LambdaActionProperty(
                        function_arn="functionArn"
                    ),
                    location=LocationActionProperty(
                        device_id="deviceId",
                        latitude="latitude",
                        longitude="longitude",
                        role_arn="roleArn",
                        tracker_name="trackerName",
            
                        # the properties below are optional
                        timestamp=TimestampProperty(
                            value="value",
            
                            # the properties below are optional
                            unit="unit"
                        )
                    ),
                    open_search=OpenSearchActionProperty(
                        endpoint="endpoint",
                        id="id",
                        index="index",
                        role_arn="roleArn",
                        type="type"
                    ),
                    republish=RepublishActionProperty(
                        role_arn="roleArn",
                        topic="topic",
            
                        # the properties below are optional
                        headers=RepublishActionHeadersProperty(
                            content_type="contentType",
                            correlation_data="correlationData",
                            message_expiry="messageExpiry",
                            payload_format_indicator="payloadFormatIndicator",
                            response_topic="responseTopic",
                            user_properties=[UserPropertyProperty(
                                key="key",
                                value="value"
                            )]
                        ),
                        qos=123
                    ),
                    s3=S3ActionProperty(
                        bucket_name="bucketName",
                        key="key",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        canned_acl="cannedAcl"
                    ),
                    sns=SnsActionProperty(
                        role_arn="roleArn",
                        target_arn="targetArn",
            
                        # the properties below are optional
                        message_format="messageFormat"
                    ),
                    sqs=SqsActionProperty(
                        queue_url="queueUrl",
                        role_arn="roleArn",
            
                        # the properties below are optional
                        use_base64=False
                    ),
                    step_functions=StepFunctionsActionProperty(
                        role_arn="roleArn",
                        state_machine_name="stateMachineName",
            
                        # the properties below are optional
                        execution_name_prefix="executionNamePrefix"
                    ),
                    timestream=TimestreamActionProperty(
                        database_name="databaseName",
                        dimensions=[TimestreamDimensionProperty(
                            name="name",
                            value="value"
                        )],
                        role_arn="roleArn",
                        table_name="tableName",
            
                        # the properties below are optional
                        timestamp=TimestreamTimestampProperty(
                            unit="unit",
                            value="value"
                        )
                    )
                )
            )
        '''
        if isinstance(configuration, dict):
            configuration = _aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db72c5f97249b79d721bcd6a87436f822fe27caf16ccc0ae7aaa3671a54e7e5f)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
        }

    @builtins.property
    def configuration(self) -> _aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty:
        '''(experimental) The configuration for this action.

        :stability: experimental
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast(_aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-iot-alpha.AuditCheck")
class AuditCheck(enum.Enum):
    '''(experimental) The AWS IoT Device Defender audit checks.

    :see: https://docs.aws.amazon.com/iot-device-defender/latest/devguide/device-defender-audit-checks.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # config: iot.AccountAuditConfiguration
        
        
        # Daily audit
        daily_audit = iot.ScheduledAudit(self, "DailyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.DAILY,
            audit_checks=[iot.AuditCheck.AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK
            ]
        )
        
        # Weekly audit
        weekly_audit = iot.ScheduledAudit(self, "WeeklyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.WEEKLY,
            day_of_week=iot.DayOfWeek.SUNDAY,
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_EXPIRING_CHECK
            ]
        )
        
        # Monthly audit
        monthly_audit = iot.ScheduledAudit(self, "MonthlyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.MONTHLY,
            day_of_month=iot.DayOfMonth.of(1),
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_KEY_QUALITY_CHECK
            ]
        )
    '''

    AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK = "AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK"
    '''(experimental) Checks the permissiveness of an authenticated Amazon Cognito identity pool role.

    For this check, AWS IoT Device Defender audits all Amazon Cognito identity pools that have been used to connect to the AWS IoT message broker
    during the 31 days before the audit is performed.

    :stability: experimental
    '''
    CA_CERTIFICATE_EXPIRING_CHECK = "CA_CERTIFICATE_EXPIRING_CHECK"
    '''(experimental) Checks if a CA certificate is expiring.

    This check applies to CA certificates expiring within 30 days or that have expired.

    :stability: experimental
    '''
    CA_CERTIFICATE_KEY_QUALITY_CHECK = "CA_CERTIFICATE_KEY_QUALITY_CHECK"
    '''(experimental) Checks the quality of the CA certificate key.

    The quality checks if the key is in a valid format, not expired, and if the key meets a minimum required size.

    This check applies to CA certificates that are ACTIVE or PENDING_TRANSFER.

    :stability: experimental
    '''
    CONFLICTING_CLIENT_IDS_CHECK = "CONFLICTING_CLIENT_IDS_CHECK"
    '''(experimental) Checks if multiple devices connect using the same client ID.

    :stability: experimental
    '''
    DEVICE_CERTIFICATE_EXPIRING_CHECK = "DEVICE_CERTIFICATE_EXPIRING_CHECK"
    '''(experimental) Checks if a device certificate is expiring.

    This check applies to device certificates expiring within 30 days or that have expired.

    :stability: experimental
    '''
    DEVICE_CERTIFICATE_KEY_QUALITY_CHECK = "DEVICE_CERTIFICATE_KEY_QUALITY_CHECK"
    '''(experimental) Checks the quality of the device certificate key.

    The quality checks if the key is in a valid format, not expired, signed by a registered certificate authority,
    and if the key meets a minimum required size.

    :stability: experimental
    '''
    DEVICE_CERTIFICATE_SHARED_CHECK = "DEVICE_CERTIFICATE_SHARED_CHECK"
    '''(experimental) Checks if multiple concurrent connections use the same X.509 certificate to authenticate with AWS IoT.

    :stability: experimental
    '''
    IOT_POLICY_OVERLY_PERMISSIVE_CHECK = "IOT_POLICY_OVERLY_PERMISSIVE_CHECK"
    '''(experimental) Checks the permissiveness of a policy attached to an authenticated Amazon Cognito identity pool role.

    :stability: experimental
    '''
    IOT_ROLE_ALIAS_ALLOWS_ACCESS_TO_UNUSED_SERVICES_CHECK = "IOT_ROLE_ALIAS_ALLOWS_ACCESS_TO_UNUSED_SERVICES_CHECK"
    '''(experimental) Checks if a role alias has access to services that haven't been used for the AWS IoT device in the last year.

    :stability: experimental
    '''
    IOT_ROLE_ALIAS_OVERLY_PERMISSIVE_CHECK = "IOT_ROLE_ALIAS_OVERLY_PERMISSIVE_CHECK"
    '''(experimental) Checks if the temporary credentials provided by AWS IoT role aliases are overly permissive.

    :stability: experimental
    '''
    LOGGING_DISABLED_CHECK = "LOGGING_DISABLED_CHECK"
    '''(experimental) Checks if AWS IoT logs are disabled.

    :stability: experimental
    '''
    REVOKED_CA_CERTIFICATE_STILL_ACTIVE_CHECK = "REVOKED_CA_CERTIFICATE_STILL_ACTIVE_CHECK"
    '''(experimental) Checks if a revoked CA certificate is still active.

    :stability: experimental
    '''
    REVOKED_DEVICE_CERTIFICATE_STILL_ACTIVE_CHECK = "REVOKED_DEVICE_CERTIFICATE_STILL_ACTIVE_CHECK"
    '''(experimental) Checks if a revoked device certificate is still active.

    :stability: experimental
    '''
    UNAUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK = "UNAUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK"
    '''(experimental) Checks if policy attached to an unauthenticated Amazon Cognito identity pool role is too permissive.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.CheckConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "authenticated_cognito_role_overly_permissive_check": "authenticatedCognitoRoleOverlyPermissiveCheck",
        "ca_certificate_expiring_check": "caCertificateExpiringCheck",
        "ca_certificate_key_quality_check": "caCertificateKeyQualityCheck",
        "conflicting_client_ids_check": "conflictingClientIdsCheck",
        "device_certificate_age_check": "deviceCertificateAgeCheck",
        "device_certificate_age_check_duration": "deviceCertificateAgeCheckDuration",
        "device_certificate_expiring_check": "deviceCertificateExpiringCheck",
        "device_certificate_key_quality_check": "deviceCertificateKeyQualityCheck",
        "device_certificate_shared_check": "deviceCertificateSharedCheck",
        "intermediate_ca_revoked_for_active_device_certificates_check": "intermediateCaRevokedForActiveDeviceCertificatesCheck",
        "iot_policy_overly_permissive_check": "iotPolicyOverlyPermissiveCheck",
        "io_t_policy_potential_mis_configuration_check": "ioTPolicyPotentialMisConfigurationCheck",
        "iot_role_alias_allows_access_to_unused_services_check": "iotRoleAliasAllowsAccessToUnusedServicesCheck",
        "iot_role_alias_overly_permissive_check": "iotRoleAliasOverlyPermissiveCheck",
        "logging_disabled_check": "loggingDisabledCheck",
        "revoked_ca_certificate_still_active_check": "revokedCaCertificateStillActiveCheck",
        "revoked_device_certificate_still_active_check": "revokedDeviceCertificateStillActiveCheck",
        "unauthenticated_cognito_role_overly_permissive_check": "unauthenticatedCognitoRoleOverlyPermissiveCheck",
    },
)
class CheckConfiguration:
    def __init__(
        self,
        *,
        authenticated_cognito_role_overly_permissive_check: typing.Optional[builtins.bool] = None,
        ca_certificate_expiring_check: typing.Optional[builtins.bool] = None,
        ca_certificate_key_quality_check: typing.Optional[builtins.bool] = None,
        conflicting_client_ids_check: typing.Optional[builtins.bool] = None,
        device_certificate_age_check: typing.Optional[builtins.bool] = None,
        device_certificate_age_check_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        device_certificate_expiring_check: typing.Optional[builtins.bool] = None,
        device_certificate_key_quality_check: typing.Optional[builtins.bool] = None,
        device_certificate_shared_check: typing.Optional[builtins.bool] = None,
        intermediate_ca_revoked_for_active_device_certificates_check: typing.Optional[builtins.bool] = None,
        iot_policy_overly_permissive_check: typing.Optional[builtins.bool] = None,
        io_t_policy_potential_mis_configuration_check: typing.Optional[builtins.bool] = None,
        iot_role_alias_allows_access_to_unused_services_check: typing.Optional[builtins.bool] = None,
        iot_role_alias_overly_permissive_check: typing.Optional[builtins.bool] = None,
        logging_disabled_check: typing.Optional[builtins.bool] = None,
        revoked_ca_certificate_still_active_check: typing.Optional[builtins.bool] = None,
        revoked_device_certificate_still_active_check: typing.Optional[builtins.bool] = None,
        unauthenticated_cognito_role_overly_permissive_check: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The types of audit checks.

        :param authenticated_cognito_role_overly_permissive_check: (experimental) Checks the permissiveness of an authenticated Amazon Cognito identity pool role. For this check, AWS IoT Device Defender audits all Amazon Cognito identity pools that have been used to connect to the AWS IoT message broker during the 31 days before the audit is performed. Default: true
        :param ca_certificate_expiring_check: (experimental) Checks if a CA certificate is expiring. This check applies to CA certificates expiring within 30 days or that have expired. Default: true
        :param ca_certificate_key_quality_check: (experimental) Checks the quality of the CA certificate key. The quality checks if the key is in a valid format, not expired, and if the key meets a minimum required size. This check applies to CA certificates that are ACTIVE or PENDING_TRANSFER. Default: true
        :param conflicting_client_ids_check: (experimental) Checks if multiple devices connect using the same client ID. Default: true
        :param device_certificate_age_check: (experimental) Checks when a device certificate has been active for a number of days greater than or equal to the number you specify. Default: true
        :param device_certificate_age_check_duration: (experimental) The duration used to check if a device certificate has been active for a number of days greater than or equal to the number you specify. Valid values range from 30 days (minimum) to 3650 days (10 years, maximum). You cannot specify a value for this check if ``deviceCertificateAgeCheck`` is set to ``false``. Default: - 365 days
        :param device_certificate_expiring_check: (experimental) Checks if a device certificate is expiring. This check applies to device certificates expiring within 30 days or that have expired. Default: true
        :param device_certificate_key_quality_check: (experimental) Checks the quality of the device certificate key. The quality checks if the key is in a valid format, not expired, signed by a registered certificate authority, and if the key meets a minimum required size. Default: true
        :param device_certificate_shared_check: (experimental) Checks if multiple concurrent connections use the same X.509 certificate to authenticate with AWS IoT. Default: true
        :param intermediate_ca_revoked_for_active_device_certificates_check: (experimental) Checks if device certificates are still active despite being revoked by an intermediate CA. Default: true
        :param iot_policy_overly_permissive_check: (experimental) Checks the permissiveness of a policy attached to an authenticated Amazon Cognito identity pool role. Default: true
        :param io_t_policy_potential_mis_configuration_check: (experimental) Checks if an AWS IoT policy is potentially misconfigured. Misconfigured policies, including overly permissive policies, can cause security incidents like allowing devices access to unintended resources. This check is a warning for you to make sure that only intended actions are allowed before updating the policy. Default: true
        :param iot_role_alias_allows_access_to_unused_services_check: (experimental) Checks if a role alias has access to services that haven't been used for the AWS IoT device in the last year. Default: true
        :param iot_role_alias_overly_permissive_check: (experimental) Checks if the temporary credentials provided by AWS IoT role aliases are overly permissive. Default: true
        :param logging_disabled_check: (experimental) Checks if AWS IoT logs are disabled. Default: true
        :param revoked_ca_certificate_still_active_check: (experimental) Checks if a revoked CA certificate is still active. Default: true
        :param revoked_device_certificate_still_active_check: (experimental) Checks if a revoked device certificate is still active. Default: true
        :param unauthenticated_cognito_role_overly_permissive_check: (experimental) Checks if policy attached to an unauthenticated Amazon Cognito identity pool role is too permissive. Default: true

        :see: https://docs.aws.amazon.com/iot-device-defender/latest/devguide/device-defender-audit-checks.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            iot.AccountAuditConfiguration(self, "AuditConfiguration",
                check_configuration=iot.CheckConfiguration(
                    # enabled
                    authenticated_cognito_role_overly_permissive_check=True,
                    # enabled by default
                    ca_certificate_expiring_check=undefined,
                    # disabled
                    ca_certificate_key_quality_check=False,
                    conflicting_client_ids_check=False,
                    device_certificate_age_check=False,
                    device_certificate_expiring_check=False,
                    device_certificate_key_quality_check=False,
                    device_certificate_shared_check=False,
                    intermediate_ca_revoked_for_active_device_certificates_check=False,
                    io_tPolicy_potential_mis_configuration_check=False,
                    iot_policy_overly_permissive_check=False,
                    iot_role_alias_allows_access_to_unused_services_check=False,
                    iot_role_alias_overly_permissive_check=False,
                    logging_disabled_check=False,
                    revoked_ca_certificate_still_active_check=False,
                    revoked_device_certificate_still_active_check=False,
                    unauthenticated_cognito_role_overly_permissive_check=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9c5c9d3626b3241033eaae1616063003470252ba449cc0716435adb7ac0c89)
            check_type(argname="argument authenticated_cognito_role_overly_permissive_check", value=authenticated_cognito_role_overly_permissive_check, expected_type=type_hints["authenticated_cognito_role_overly_permissive_check"])
            check_type(argname="argument ca_certificate_expiring_check", value=ca_certificate_expiring_check, expected_type=type_hints["ca_certificate_expiring_check"])
            check_type(argname="argument ca_certificate_key_quality_check", value=ca_certificate_key_quality_check, expected_type=type_hints["ca_certificate_key_quality_check"])
            check_type(argname="argument conflicting_client_ids_check", value=conflicting_client_ids_check, expected_type=type_hints["conflicting_client_ids_check"])
            check_type(argname="argument device_certificate_age_check", value=device_certificate_age_check, expected_type=type_hints["device_certificate_age_check"])
            check_type(argname="argument device_certificate_age_check_duration", value=device_certificate_age_check_duration, expected_type=type_hints["device_certificate_age_check_duration"])
            check_type(argname="argument device_certificate_expiring_check", value=device_certificate_expiring_check, expected_type=type_hints["device_certificate_expiring_check"])
            check_type(argname="argument device_certificate_key_quality_check", value=device_certificate_key_quality_check, expected_type=type_hints["device_certificate_key_quality_check"])
            check_type(argname="argument device_certificate_shared_check", value=device_certificate_shared_check, expected_type=type_hints["device_certificate_shared_check"])
            check_type(argname="argument intermediate_ca_revoked_for_active_device_certificates_check", value=intermediate_ca_revoked_for_active_device_certificates_check, expected_type=type_hints["intermediate_ca_revoked_for_active_device_certificates_check"])
            check_type(argname="argument iot_policy_overly_permissive_check", value=iot_policy_overly_permissive_check, expected_type=type_hints["iot_policy_overly_permissive_check"])
            check_type(argname="argument io_t_policy_potential_mis_configuration_check", value=io_t_policy_potential_mis_configuration_check, expected_type=type_hints["io_t_policy_potential_mis_configuration_check"])
            check_type(argname="argument iot_role_alias_allows_access_to_unused_services_check", value=iot_role_alias_allows_access_to_unused_services_check, expected_type=type_hints["iot_role_alias_allows_access_to_unused_services_check"])
            check_type(argname="argument iot_role_alias_overly_permissive_check", value=iot_role_alias_overly_permissive_check, expected_type=type_hints["iot_role_alias_overly_permissive_check"])
            check_type(argname="argument logging_disabled_check", value=logging_disabled_check, expected_type=type_hints["logging_disabled_check"])
            check_type(argname="argument revoked_ca_certificate_still_active_check", value=revoked_ca_certificate_still_active_check, expected_type=type_hints["revoked_ca_certificate_still_active_check"])
            check_type(argname="argument revoked_device_certificate_still_active_check", value=revoked_device_certificate_still_active_check, expected_type=type_hints["revoked_device_certificate_still_active_check"])
            check_type(argname="argument unauthenticated_cognito_role_overly_permissive_check", value=unauthenticated_cognito_role_overly_permissive_check, expected_type=type_hints["unauthenticated_cognito_role_overly_permissive_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authenticated_cognito_role_overly_permissive_check is not None:
            self._values["authenticated_cognito_role_overly_permissive_check"] = authenticated_cognito_role_overly_permissive_check
        if ca_certificate_expiring_check is not None:
            self._values["ca_certificate_expiring_check"] = ca_certificate_expiring_check
        if ca_certificate_key_quality_check is not None:
            self._values["ca_certificate_key_quality_check"] = ca_certificate_key_quality_check
        if conflicting_client_ids_check is not None:
            self._values["conflicting_client_ids_check"] = conflicting_client_ids_check
        if device_certificate_age_check is not None:
            self._values["device_certificate_age_check"] = device_certificate_age_check
        if device_certificate_age_check_duration is not None:
            self._values["device_certificate_age_check_duration"] = device_certificate_age_check_duration
        if device_certificate_expiring_check is not None:
            self._values["device_certificate_expiring_check"] = device_certificate_expiring_check
        if device_certificate_key_quality_check is not None:
            self._values["device_certificate_key_quality_check"] = device_certificate_key_quality_check
        if device_certificate_shared_check is not None:
            self._values["device_certificate_shared_check"] = device_certificate_shared_check
        if intermediate_ca_revoked_for_active_device_certificates_check is not None:
            self._values["intermediate_ca_revoked_for_active_device_certificates_check"] = intermediate_ca_revoked_for_active_device_certificates_check
        if iot_policy_overly_permissive_check is not None:
            self._values["iot_policy_overly_permissive_check"] = iot_policy_overly_permissive_check
        if io_t_policy_potential_mis_configuration_check is not None:
            self._values["io_t_policy_potential_mis_configuration_check"] = io_t_policy_potential_mis_configuration_check
        if iot_role_alias_allows_access_to_unused_services_check is not None:
            self._values["iot_role_alias_allows_access_to_unused_services_check"] = iot_role_alias_allows_access_to_unused_services_check
        if iot_role_alias_overly_permissive_check is not None:
            self._values["iot_role_alias_overly_permissive_check"] = iot_role_alias_overly_permissive_check
        if logging_disabled_check is not None:
            self._values["logging_disabled_check"] = logging_disabled_check
        if revoked_ca_certificate_still_active_check is not None:
            self._values["revoked_ca_certificate_still_active_check"] = revoked_ca_certificate_still_active_check
        if revoked_device_certificate_still_active_check is not None:
            self._values["revoked_device_certificate_still_active_check"] = revoked_device_certificate_still_active_check
        if unauthenticated_cognito_role_overly_permissive_check is not None:
            self._values["unauthenticated_cognito_role_overly_permissive_check"] = unauthenticated_cognito_role_overly_permissive_check

    @builtins.property
    def authenticated_cognito_role_overly_permissive_check(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks the permissiveness of an authenticated Amazon Cognito identity pool role.

        For this check, AWS IoT Device Defender audits all Amazon Cognito identity pools that have been used to connect to the AWS IoT message broker
        during the 31 days before the audit is performed.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("authenticated_cognito_role_overly_permissive_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ca_certificate_expiring_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if a CA certificate is expiring.

        This check applies to CA certificates expiring within 30 days or that have expired.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ca_certificate_expiring_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ca_certificate_key_quality_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks the quality of the CA certificate key.

        The quality checks if the key is in a valid format, not expired, and if the key meets a minimum required size.

        This check applies to CA certificates that are ACTIVE or PENDING_TRANSFER.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ca_certificate_key_quality_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def conflicting_client_ids_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if multiple devices connect using the same client ID.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("conflicting_client_ids_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def device_certificate_age_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks when a device certificate has been active for a number of days greater than or equal to the number you specify.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("device_certificate_age_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def device_certificate_age_check_duration(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The duration used to check if a device certificate has been active for a number of days greater than or equal to the number you specify.

        Valid values range from 30 days (minimum) to 3650 days (10 years, maximum).

        You cannot specify a value for this check if ``deviceCertificateAgeCheck`` is set to ``false``.

        :default: - 365 days

        :stability: experimental
        '''
        result = self._values.get("device_certificate_age_check_duration")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def device_certificate_expiring_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if a device certificate is expiring.

        This check applies to device certificates expiring within 30 days or that have expired.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("device_certificate_expiring_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def device_certificate_key_quality_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks the quality of the device certificate key.

        The quality checks if the key is in a valid format, not expired, signed by a registered certificate authority,
        and if the key meets a minimum required size.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("device_certificate_key_quality_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def device_certificate_shared_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if multiple concurrent connections use the same X.509 certificate to authenticate with AWS IoT.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("device_certificate_shared_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def intermediate_ca_revoked_for_active_device_certificates_check(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if device certificates are still active despite being revoked by an intermediate CA.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("intermediate_ca_revoked_for_active_device_certificates_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iot_policy_overly_permissive_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks the permissiveness of a policy attached to an authenticated Amazon Cognito identity pool role.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("iot_policy_overly_permissive_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def io_t_policy_potential_mis_configuration_check(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if an AWS IoT policy is potentially misconfigured.

        Misconfigured policies, including overly permissive policies, can cause security incidents like allowing devices access to unintended resources.

        This check is a warning for you to make sure that only intended actions are allowed before updating the policy.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("io_t_policy_potential_mis_configuration_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iot_role_alias_allows_access_to_unused_services_check(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if a role alias has access to services that haven't been used for the AWS IoT device in the last year.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("iot_role_alias_allows_access_to_unused_services_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iot_role_alias_overly_permissive_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if the temporary credentials provided by AWS IoT role aliases are overly permissive.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("iot_role_alias_overly_permissive_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def logging_disabled_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if AWS IoT logs are disabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("logging_disabled_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def revoked_ca_certificate_still_active_check(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if a revoked CA certificate is still active.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("revoked_ca_certificate_still_active_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def revoked_device_certificate_still_active_check(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if a revoked device certificate is still active.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("revoked_device_certificate_still_active_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def unauthenticated_cognito_role_overly_permissive_check(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''(experimental) Checks if policy attached to an unauthenticated Amazon Cognito identity pool role is too permissive.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("unauthenticated_cognito_role_overly_permissive_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DayOfMonth(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-alpha.DayOfMonth",
):
    '''(experimental) The day of the month on which the scheduled audit takes place.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # config: iot.AccountAuditConfiguration
        
        
        # Daily audit
        daily_audit = iot.ScheduledAudit(self, "DailyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.DAILY,
            audit_checks=[iot.AuditCheck.AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK
            ]
        )
        
        # Weekly audit
        weekly_audit = iot.ScheduledAudit(self, "WeeklyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.WEEKLY,
            day_of_week=iot.DayOfWeek.SUNDAY,
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_EXPIRING_CHECK
            ]
        )
        
        # Monthly audit
        monthly_audit = iot.ScheduledAudit(self, "MonthlyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.MONTHLY,
            day_of_month=iot.DayOfMonth.of(1),
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_KEY_QUALITY_CHECK
            ]
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, day: jsii.Number) -> "DayOfMonth":
        '''(experimental) Custom day of the month.

        :param day: the day of the month.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb73a8431c3f75f699052b2df93d897fdf174897f29d4825684600931e6f035)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
        return typing.cast("DayOfMonth", jsii.sinvoke(cls, "of", [day]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LAST_DAY")
    def LAST_DAY(cls) -> "DayOfMonth":
        '''(experimental) The last day of the month.

        :stability: experimental
        '''
        return typing.cast("DayOfMonth", jsii.sget(cls, "LAST_DAY"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> builtins.str:
        '''(experimental) The day of the month.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "day"))


@jsii.enum(jsii_type="@aws-cdk/aws-iot-alpha.DayOfWeek")
class DayOfWeek(enum.Enum):
    '''(experimental) The day of the week on which the scheduled audit takes place.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # config: iot.AccountAuditConfiguration
        
        
        # Daily audit
        daily_audit = iot.ScheduledAudit(self, "DailyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.DAILY,
            audit_checks=[iot.AuditCheck.AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK
            ]
        )
        
        # Weekly audit
        weekly_audit = iot.ScheduledAudit(self, "WeeklyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.WEEKLY,
            day_of_week=iot.DayOfWeek.SUNDAY,
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_EXPIRING_CHECK
            ]
        )
        
        # Monthly audit
        monthly_audit = iot.ScheduledAudit(self, "MonthlyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.MONTHLY,
            day_of_month=iot.DayOfMonth.of(1),
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_KEY_QUALITY_CHECK
            ]
        )
    '''

    SUNDAY = "SUNDAY"
    '''(experimental) Sunday.

    :stability: experimental
    '''
    MONDAY = "MONDAY"
    '''(experimental) Monday.

    :stability: experimental
    '''
    TUESDAY = "TUESDAY"
    '''(experimental) Tuesday.

    :stability: experimental
    '''
    WEDNESDAY = "WEDNESDAY"
    '''(experimental) Wednesday.

    :stability: experimental
    '''
    THURSDAY = "THURSDAY"
    '''(experimental) Thursday.

    :stability: experimental
    '''
    FRIDAY = "FRIDAY"
    '''(experimental) Friday.

    :stability: experimental
    '''
    SATURDAY = "SATURDAY"
    '''(experimental) Saturday.

    :stability: experimental
    '''
    UNSET_VALUE = "UNSET_VALUE"
    '''(experimental) UNSET_VALUE.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-iot-alpha.Frequency")
class Frequency(enum.Enum):
    '''(experimental) The frequency at which the scheduled audit takes place.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # config: iot.AccountAuditConfiguration
        
        
        # Daily audit
        daily_audit = iot.ScheduledAudit(self, "DailyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.DAILY,
            audit_checks=[iot.AuditCheck.AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK
            ]
        )
        
        # Weekly audit
        weekly_audit = iot.ScheduledAudit(self, "WeeklyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.WEEKLY,
            day_of_week=iot.DayOfWeek.SUNDAY,
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_EXPIRING_CHECK
            ]
        )
        
        # Monthly audit
        monthly_audit = iot.ScheduledAudit(self, "MonthlyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.MONTHLY,
            day_of_month=iot.DayOfMonth.of(1),
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_KEY_QUALITY_CHECK
            ]
        )
    '''

    DAILY = "DAILY"
    '''(experimental) Daily.

    :stability: experimental
    '''
    WEEKLY = "WEEKLY"
    '''(experimental) Weekly.

    :stability: experimental
    '''
    BI_WEEKLY = "BI_WEEKLY"
    '''(experimental) Bi-weekly.

    :stability: experimental
    '''
    MONTHLY = "MONTHLY"
    '''(experimental) Monthly.

    :stability: experimental
    '''


@jsii.interface(jsii_type="@aws-cdk/aws-iot-alpha.IAccountAuditConfiguration")
class IAccountAuditConfiguration(
    _aws_cdk_ceddda9d.IResource,
    typing_extensions.Protocol,
):
    '''(experimental) Represents AWS IoT Audit Configuration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        '''(experimental) The account ID.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAccountAuditConfigurationProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents AWS IoT Audit Configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iot-alpha.IAccountAuditConfiguration"

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        '''(experimental) The account ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAccountAuditConfiguration).__jsii_proxy_class__ = lambda : _IAccountAuditConfigurationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iot-alpha.IAction")
class IAction(typing_extensions.Protocol):
    '''(experimental) An abstract action for TopicRule.

    :stability: experimental
    '''

    pass


class _IActionProxy:
    '''(experimental) An abstract action for TopicRule.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iot-alpha.IAction"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAction).__jsii_proxy_class__ = lambda : _IActionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iot-alpha.ILogging")
class ILogging(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents AWS IoT Logging.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="logId")
    def log_id(self) -> builtins.str:
        '''(experimental) The log ID.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ILoggingProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents AWS IoT Logging.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iot-alpha.ILogging"

    @builtins.property
    @jsii.member(jsii_name="logId")
    def log_id(self) -> builtins.str:
        '''(experimental) The log ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogging).__jsii_proxy_class__ = lambda : _ILoggingProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iot-alpha.IScheduledAudit")
class IScheduledAudit(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents AWS IoT Scheduled Audit.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="scheduledAuditArn")
    def scheduled_audit_arn(self) -> builtins.str:
        '''(experimental) The ARN of the scheduled audit.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scheduledAuditName")
    def scheduled_audit_name(self) -> builtins.str:
        '''(experimental) The scheduled audit name.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IScheduledAuditProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents AWS IoT Scheduled Audit.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iot-alpha.IScheduledAudit"

    @builtins.property
    @jsii.member(jsii_name="scheduledAuditArn")
    def scheduled_audit_arn(self) -> builtins.str:
        '''(experimental) The ARN of the scheduled audit.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduledAuditArn"))

    @builtins.property
    @jsii.member(jsii_name="scheduledAuditName")
    def scheduled_audit_name(self) -> builtins.str:
        '''(experimental) The scheduled audit name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduledAuditName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IScheduledAudit).__jsii_proxy_class__ = lambda : _IScheduledAuditProxy


@jsii.interface(jsii_type="@aws-cdk/aws-iot-alpha.ITopicRule")
class ITopicRule(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an AWS IoT Rule.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="topicRuleArn")
    def topic_rule_arn(self) -> builtins.str:
        '''(experimental) The value of the topic rule Amazon Resource Name (ARN), such as arn:aws:iot:us-east-2:123456789012:rule/rule_name.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="topicRuleName")
    def topic_rule_name(self) -> builtins.str:
        '''(experimental) The name topic rule.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ITopicRuleProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an AWS IoT Rule.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-iot-alpha.ITopicRule"

    @builtins.property
    @jsii.member(jsii_name="topicRuleArn")
    def topic_rule_arn(self) -> builtins.str:
        '''(experimental) The value of the topic rule Amazon Resource Name (ARN), such as arn:aws:iot:us-east-2:123456789012:rule/rule_name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="topicRuleName")
    def topic_rule_name(self) -> builtins.str:
        '''(experimental) The name topic rule.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicRuleName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITopicRule).__jsii_proxy_class__ = lambda : _ITopicRuleProxy


class IotSql(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-iot-alpha.IotSql",
):
    '''(experimental) Defines AWS IoT SQL.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        
        
        topic = sns.Topic(self, "MyTopic")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.SnsTopicAction(topic,
                    message_format=actions.SnsActionMessageFormat.JSON
                )
            ]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromStringAsVer20151008")
    @builtins.classmethod
    def from_string_as_ver20151008(cls, sql: builtins.str) -> "IotSql":
        '''(experimental) Uses the original SQL version built on 2015-10-08.

        :param sql: The actual SQL-like syntax query.

        :return: Instance of IotSql

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b60afd6a89f56eb454ee327bd143df85ea1ea9518d995f338ac85c6f9172ef)
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        return typing.cast("IotSql", jsii.sinvoke(cls, "fromStringAsVer20151008", [sql]))

    @jsii.member(jsii_name="fromStringAsVer20160323")
    @builtins.classmethod
    def from_string_as_ver20160323(cls, sql: builtins.str) -> "IotSql":
        '''(experimental) Uses the SQL version built on 2016-03-23.

        :param sql: The actual SQL-like syntax query.

        :return: Instance of IotSql

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246c805677b75001ec2445224c8ee29056b92709ee8d3bb168587a48bc5d0fb5)
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        return typing.cast("IotSql", jsii.sinvoke(cls, "fromStringAsVer20160323", [sql]))

    @jsii.member(jsii_name="fromStringAsVerNewestUnstable")
    @builtins.classmethod
    def from_string_as_ver_newest_unstable(cls, sql: builtins.str) -> "IotSql":
        '''(experimental) Uses the most recent beta SQL version.

        If you use this version, it might
        introduce breaking changes to your rules.

        :param sql: The actual SQL-like syntax query.

        :return: Instance of IotSql

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715467063ed924cc91a9fa5b60c44d4b1b82edbc8eb085d68321fd0014a32067)
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        return typing.cast("IotSql", jsii.sinvoke(cls, "fromStringAsVerNewestUnstable", [sql]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "IotSqlConfig":
        '''(experimental) Returns the IoT SQL configuration.

        :param scope: -

        :stability: experimental
        '''
        ...


class _IotSqlProxy(IotSql):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "IotSqlConfig":
        '''(experimental) Returns the IoT SQL configuration.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d3862c5242014e403c7a2af3ffcf5d3a77ce6e5376d651493716a5b5061bd9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("IotSqlConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, IotSql).__jsii_proxy_class__ = lambda : _IotSqlProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.IotSqlConfig",
    jsii_struct_bases=[],
    name_mapping={"aws_iot_sql_version": "awsIotSqlVersion", "sql": "sql"},
)
class IotSqlConfig:
    def __init__(self, *, aws_iot_sql_version: builtins.str, sql: builtins.str) -> None:
        '''(experimental) The type returned from the ``bind()`` method in ``IotSql``.

        :param aws_iot_sql_version: (experimental) The version of the SQL rules engine to use when evaluating the rule.
        :param sql: (experimental) The SQL statement used to query the topic.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_alpha as iot_alpha
            
            iot_sql_config = iot_alpha.IotSqlConfig(
                aws_iot_sql_version="awsIotSqlVersion",
                sql="sql"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887fb9654c4aa0ba71be51a8acf671f0dc89cdb21899f13ebce575d2da566e05)
            check_type(argname="argument aws_iot_sql_version", value=aws_iot_sql_version, expected_type=type_hints["aws_iot_sql_version"])
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_iot_sql_version": aws_iot_sql_version,
            "sql": sql,
        }

    @builtins.property
    def aws_iot_sql_version(self) -> builtins.str:
        '''(experimental) The version of the SQL rules engine to use when evaluating the rule.

        :stability: experimental
        '''
        result = self._values.get("aws_iot_sql_version")
        assert result is not None, "Required property 'aws_iot_sql_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql(self) -> builtins.str:
        '''(experimental) The SQL statement used to query the topic.

        :stability: experimental
        '''
        result = self._values.get("sql")
        assert result is not None, "Required property 'sql' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotSqlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-iot-alpha.LogLevel")
class LogLevel(enum.Enum):
    '''(experimental) The log level for the AWS IoT Logging.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        iot.Logging(self, "Logging",
            log_level=iot.LogLevel.INFO
        )
    '''

    ERROR = "ERROR"
    '''(experimental) Any error that causes an operation to fail.

    Logs include ERROR information only

    :stability: experimental
    '''
    WARN = "WARN"
    '''(experimental) Anything that can potentially cause inconsistencies in the system, but might not cause the operation to fail.

    Logs include ERROR and WARN information

    :stability: experimental
    '''
    INFO = "INFO"
    '''(experimental) High-level information about the flow of things.

    Logs include INFO, ERROR, and WARN information

    :stability: experimental
    '''
    DEBUG = "DEBUG"
    '''(experimental) Information that might be helpful when debugging a problem.

    Logs include DEBUG, INFO, ERROR, and WARN information

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) All logging is disabled.

    :stability: experimental
    '''


@jsii.implements(ILogging)
class Logging(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-alpha.Logging",
):
    '''(experimental) Defines AWS IoT Logging.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        iot.Logging(self, "Logging",
            log_level=iot.LogLevel.INFO
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_level: typing.Optional[LogLevel] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_level: (experimental) The log level for the AWS IoT Logging. Default: LogLevel.ERROR

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e352fb2a762be72085ea51f1a46a8e422901ecf3dbeaa4d542bc8e765ede38c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LoggingProps(log_level=log_level)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogId")
    @builtins.classmethod
    def from_log_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        log_id: builtins.str,
    ) -> ILogging:
        '''(experimental) Import an existing AWS IoT Logging.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param log_id: AWS IoT Logging ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99da511bd810901da44a2d46c1b46942903f1621bdf2704460e995700e2fe1e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_id", value=log_id, expected_type=type_hints["log_id"])
        return typing.cast(ILogging, jsii.sinvoke(cls, "fromLogId", [scope, id, log_id]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="logId")
    def log_id(self) -> builtins.str:
        '''(experimental) The logging ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "logId"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.LoggingProps",
    jsii_struct_bases=[],
    name_mapping={"log_level": "logLevel"},
)
class LoggingProps:
    def __init__(self, *, log_level: typing.Optional[LogLevel] = None) -> None:
        '''(experimental) Properties for defining AWS IoT Logging.

        :param log_level: (experimental) The log level for the AWS IoT Logging. Default: LogLevel.ERROR

        :stability: experimental
        :exampleMetadata: infused

        Example::

            iot.Logging(self, "Logging",
                log_level=iot.LogLevel.INFO
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40b8e7e00237816e95880f570241f023097cd35cee2a70c6572617e8534056c)
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_level is not None:
            self._values["log_level"] = log_level

    @builtins.property
    def log_level(self) -> typing.Optional[LogLevel]:
        '''(experimental) The log level for the AWS IoT Logging.

        :default: LogLevel.ERROR

        :stability: experimental
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[LogLevel], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IScheduledAudit)
class ScheduledAudit(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-alpha.ScheduledAudit",
):
    '''(experimental) Defines AWS IoT Scheduled Audit.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # config: iot.AccountAuditConfiguration
        
        
        # Daily audit
        daily_audit = iot.ScheduledAudit(self, "DailyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.DAILY,
            audit_checks=[iot.AuditCheck.AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK
            ]
        )
        
        # Weekly audit
        weekly_audit = iot.ScheduledAudit(self, "WeeklyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.WEEKLY,
            day_of_week=iot.DayOfWeek.SUNDAY,
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_EXPIRING_CHECK
            ]
        )
        
        # Monthly audit
        monthly_audit = iot.ScheduledAudit(self, "MonthlyAudit",
            account_audit_configuration=config,
            frequency=iot.Frequency.MONTHLY,
            day_of_month=iot.DayOfMonth.of(1),
            audit_checks=[iot.AuditCheck.CA_CERTIFICATE_KEY_QUALITY_CHECK
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_audit_configuration: IAccountAuditConfiguration,
        audit_checks: typing.Sequence[AuditCheck],
        frequency: Frequency,
        day_of_month: typing.Optional[DayOfMonth] = None,
        day_of_week: typing.Optional[DayOfWeek] = None,
        scheduled_audit_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account_audit_configuration: (experimental) Account audit configuration. The audit checks specified in ``auditChecks`` must be enabled in this configuration.
        :param audit_checks: (experimental) Which checks are performed during the scheduled audit. Checks must be enabled for your account.
        :param frequency: (experimental) How often the scheduled audit occurs.
        :param day_of_month: (experimental) The day of the month on which the scheduled audit is run (if the frequency is "MONTHLY"). If days 29-31 are specified, and the month does not have that many days, the audit takes place on the "LAST" day of the month. Default: - required if frequency is "MONTHLY", not allowed otherwise
        :param day_of_week: (experimental) The day of the week on which the scheduled audit is run (if the frequency is "WEEKLY" or "BIWEEKLY"). Default: - required if frequency is "WEEKLY" or "BIWEEKLY", not allowed otherwise
        :param scheduled_audit_name: (experimental) The name of the scheduled audit. Default: - auto generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe70deb5f2117b5167fbc54c0f3804db0558b4f51ed7326da4904fd6db84b28)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduledAuditProps(
            account_audit_configuration=account_audit_configuration,
            audit_checks=audit_checks,
            frequency=frequency,
            day_of_month=day_of_month,
            day_of_week=day_of_week,
            scheduled_audit_name=scheduled_audit_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromScheduledAuditArn")
    @builtins.classmethod
    def from_scheduled_audit_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        scheduled_audit_arn: builtins.str,
    ) -> IScheduledAudit:
        '''(experimental) Import an existing AWS IoT Scheduled Audit from its ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param scheduled_audit_arn: The ARN of the scheduled audit.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8915542465bf341fcdbf13f7cb50020d6357ea6919124ae06915fb51694d8890)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument scheduled_audit_arn", value=scheduled_audit_arn, expected_type=type_hints["scheduled_audit_arn"])
        return typing.cast(IScheduledAudit, jsii.sinvoke(cls, "fromScheduledAuditArn", [scope, id, scheduled_audit_arn]))

    @jsii.member(jsii_name="fromScheduledAuditAttributes")
    @builtins.classmethod
    def from_scheduled_audit_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        scheduled_audit_arn: builtins.str,
        scheduled_audit_name: builtins.str,
    ) -> IScheduledAudit:
        '''(experimental) Import an existing AWS IoT Scheduled Audit from its attributes.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param scheduled_audit_arn: (experimental) The ARN of the scheduled audit.
        :param scheduled_audit_name: (experimental) The scheduled audit name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd4dbeddc9751449b7be522e3e80c0310244510fbcd2f8541c6088349b2fb1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ScheduledAuditAttributes(
            scheduled_audit_arn=scheduled_audit_arn,
            scheduled_audit_name=scheduled_audit_name,
        )

        return typing.cast(IScheduledAudit, jsii.sinvoke(cls, "fromScheduledAuditAttributes", [scope, id, attrs]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="scheduledAuditArn")
    def scheduled_audit_arn(self) -> builtins.str:
        '''(experimental) The ARN of the scheduled audit.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduledAuditArn"))

    @builtins.property
    @jsii.member(jsii_name="scheduledAuditName")
    def scheduled_audit_name(self) -> builtins.str:
        '''(experimental) The scheduled audit name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduledAuditName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.ScheduledAuditAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "scheduled_audit_arn": "scheduledAuditArn",
        "scheduled_audit_name": "scheduledAuditName",
    },
)
class ScheduledAuditAttributes:
    def __init__(
        self,
        *,
        scheduled_audit_arn: builtins.str,
        scheduled_audit_name: builtins.str,
    ) -> None:
        '''(experimental) Construction properties for a Scheduled Audit.

        :param scheduled_audit_arn: (experimental) The ARN of the scheduled audit.
        :param scheduled_audit_name: (experimental) The scheduled audit name.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_alpha as iot_alpha
            
            scheduled_audit_attributes = iot_alpha.ScheduledAuditAttributes(
                scheduled_audit_arn="scheduledAuditArn",
                scheduled_audit_name="scheduledAuditName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ad0f3087ab74e23760b9e73acddd4e907b0e15c156e17b4a99310e0c141f0db)
            check_type(argname="argument scheduled_audit_arn", value=scheduled_audit_arn, expected_type=type_hints["scheduled_audit_arn"])
            check_type(argname="argument scheduled_audit_name", value=scheduled_audit_name, expected_type=type_hints["scheduled_audit_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scheduled_audit_arn": scheduled_audit_arn,
            "scheduled_audit_name": scheduled_audit_name,
        }

    @builtins.property
    def scheduled_audit_arn(self) -> builtins.str:
        '''(experimental) The ARN of the scheduled audit.

        :stability: experimental
        '''
        result = self._values.get("scheduled_audit_arn")
        assert result is not None, "Required property 'scheduled_audit_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scheduled_audit_name(self) -> builtins.str:
        '''(experimental) The scheduled audit name.

        :stability: experimental
        '''
        result = self._values.get("scheduled_audit_name")
        assert result is not None, "Required property 'scheduled_audit_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledAuditAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.ScheduledAuditProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_audit_configuration": "accountAuditConfiguration",
        "audit_checks": "auditChecks",
        "frequency": "frequency",
        "day_of_month": "dayOfMonth",
        "day_of_week": "dayOfWeek",
        "scheduled_audit_name": "scheduledAuditName",
    },
)
class ScheduledAuditProps:
    def __init__(
        self,
        *,
        account_audit_configuration: IAccountAuditConfiguration,
        audit_checks: typing.Sequence[AuditCheck],
        frequency: Frequency,
        day_of_month: typing.Optional[DayOfMonth] = None,
        day_of_week: typing.Optional[DayOfWeek] = None,
        scheduled_audit_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining AWS IoT Scheduled Audit.

        :param account_audit_configuration: (experimental) Account audit configuration. The audit checks specified in ``auditChecks`` must be enabled in this configuration.
        :param audit_checks: (experimental) Which checks are performed during the scheduled audit. Checks must be enabled for your account.
        :param frequency: (experimental) How often the scheduled audit occurs.
        :param day_of_month: (experimental) The day of the month on which the scheduled audit is run (if the frequency is "MONTHLY"). If days 29-31 are specified, and the month does not have that many days, the audit takes place on the "LAST" day of the month. Default: - required if frequency is "MONTHLY", not allowed otherwise
        :param day_of_week: (experimental) The day of the week on which the scheduled audit is run (if the frequency is "WEEKLY" or "BIWEEKLY"). Default: - required if frequency is "WEEKLY" or "BIWEEKLY", not allowed otherwise
        :param scheduled_audit_name: (experimental) The name of the scheduled audit. Default: - auto generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # config: iot.AccountAuditConfiguration
            
            
            # Daily audit
            daily_audit = iot.ScheduledAudit(self, "DailyAudit",
                account_audit_configuration=config,
                frequency=iot.Frequency.DAILY,
                audit_checks=[iot.AuditCheck.AUTHENTICATED_COGNITO_ROLE_OVERLY_PERMISSIVE_CHECK
                ]
            )
            
            # Weekly audit
            weekly_audit = iot.ScheduledAudit(self, "WeeklyAudit",
                account_audit_configuration=config,
                frequency=iot.Frequency.WEEKLY,
                day_of_week=iot.DayOfWeek.SUNDAY,
                audit_checks=[iot.AuditCheck.CA_CERTIFICATE_EXPIRING_CHECK
                ]
            )
            
            # Monthly audit
            monthly_audit = iot.ScheduledAudit(self, "MonthlyAudit",
                account_audit_configuration=config,
                frequency=iot.Frequency.MONTHLY,
                day_of_month=iot.DayOfMonth.of(1),
                audit_checks=[iot.AuditCheck.CA_CERTIFICATE_KEY_QUALITY_CHECK
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce3ff21c49ce66bfc46926d58b6c0194629b53bae7ffa22dd7039080d31025d)
            check_type(argname="argument account_audit_configuration", value=account_audit_configuration, expected_type=type_hints["account_audit_configuration"])
            check_type(argname="argument audit_checks", value=audit_checks, expected_type=type_hints["audit_checks"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument day_of_month", value=day_of_month, expected_type=type_hints["day_of_month"])
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument scheduled_audit_name", value=scheduled_audit_name, expected_type=type_hints["scheduled_audit_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_audit_configuration": account_audit_configuration,
            "audit_checks": audit_checks,
            "frequency": frequency,
        }
        if day_of_month is not None:
            self._values["day_of_month"] = day_of_month
        if day_of_week is not None:
            self._values["day_of_week"] = day_of_week
        if scheduled_audit_name is not None:
            self._values["scheduled_audit_name"] = scheduled_audit_name

    @builtins.property
    def account_audit_configuration(self) -> IAccountAuditConfiguration:
        '''(experimental) Account audit configuration.

        The audit checks specified in ``auditChecks`` must be enabled in this configuration.

        :stability: experimental
        '''
        result = self._values.get("account_audit_configuration")
        assert result is not None, "Required property 'account_audit_configuration' is missing"
        return typing.cast(IAccountAuditConfiguration, result)

    @builtins.property
    def audit_checks(self) -> typing.List[AuditCheck]:
        '''(experimental) Which checks are performed during the scheduled audit.

        Checks must be enabled for your account.

        :stability: experimental
        '''
        result = self._values.get("audit_checks")
        assert result is not None, "Required property 'audit_checks' is missing"
        return typing.cast(typing.List[AuditCheck], result)

    @builtins.property
    def frequency(self) -> Frequency:
        '''(experimental) How often the scheduled audit occurs.

        :stability: experimental
        '''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(Frequency, result)

    @builtins.property
    def day_of_month(self) -> typing.Optional[DayOfMonth]:
        '''(experimental) The day of the month on which the scheduled audit is run (if the frequency is "MONTHLY").

        If days 29-31 are specified, and the month does not have that many days, the audit takes place on the "LAST" day of the month.

        :default: - required if frequency is "MONTHLY", not allowed otherwise

        :stability: experimental
        '''
        result = self._values.get("day_of_month")
        return typing.cast(typing.Optional[DayOfMonth], result)

    @builtins.property
    def day_of_week(self) -> typing.Optional[DayOfWeek]:
        '''(experimental) The day of the week on which the scheduled audit is run (if the frequency is "WEEKLY" or "BIWEEKLY").

        :default: - required if frequency is "WEEKLY" or "BIWEEKLY", not allowed otherwise

        :stability: experimental
        '''
        result = self._values.get("day_of_week")
        return typing.cast(typing.Optional[DayOfWeek], result)

    @builtins.property
    def scheduled_audit_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the scheduled audit.

        :default: - auto generated name

        :stability: experimental
        '''
        result = self._values.get("scheduled_audit_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledAuditProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITopicRule)
class TopicRule(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-alpha.TopicRule",
):
    '''(experimental) Defines an AWS IoT Rule in this stack.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        
        
        topic = sns.Topic(self, "MyTopic")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.SnsTopicAction(topic,
                    message_format=actions.SnsActionMessageFormat.JSON
                )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        sql: IotSql,
        actions: typing.Optional[typing.Sequence[IAction]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        error_action: typing.Optional[IAction] = None,
        topic_rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sql: (experimental) A simplified SQL syntax to filter messages received on an MQTT topic and push the data elsewhere.
        :param actions: (experimental) The actions associated with the topic rule. Default: No actions will be perform
        :param description: (experimental) A textual description of the topic rule. Default: None
        :param enabled: (experimental) Specifies whether the rule is enabled. Default: true
        :param error_action: (experimental) The action AWS IoT performs when it is unable to perform a rule's action. Default: - no action will be performed
        :param topic_rule_name: (experimental) The name of the topic rule. Default: None

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5629ae4086674af1b4cd4c3b55a1d2cd04d194fe7dd7d9a1a08478dc69d9ac5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TopicRuleProps(
            sql=sql,
            actions=actions,
            description=description,
            enabled=enabled,
            error_action=error_action,
            topic_rule_name=topic_rule_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTopicRuleArn")
    @builtins.classmethod
    def from_topic_rule_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        topic_rule_arn: builtins.str,
    ) -> ITopicRule:
        '''(experimental) Import an existing AWS IoT Rule provided an ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param topic_rule_arn: AWS IoT Rule ARN (i.e. arn:aws:iot:::rule/MyRule).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a02640c49b9d9e3824df915f05b77c597b5dfd5d900377ada5b2b60b004bbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument topic_rule_arn", value=topic_rule_arn, expected_type=type_hints["topic_rule_arn"])
        return typing.cast(ITopicRule, jsii.sinvoke(cls, "fromTopicRuleArn", [scope, id, topic_rule_arn]))

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: IAction) -> None:
        '''(experimental) Add a action to the topic rule.

        :param action: the action to associate with the topic rule.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6d84c555ae6d88e9f422f5418183ec42014991c6a48af643a3d0341a35a73a)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        return typing.cast(None, jsii.invoke(self, "addAction", [action]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="topicRuleArn")
    def topic_rule_arn(self) -> builtins.str:
        '''(experimental) Arn of this topic rule.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="topicRuleName")
    def topic_rule_name(self) -> builtins.str:
        '''(experimental) Name of this topic rule.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "topicRuleName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-alpha.TopicRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "sql": "sql",
        "actions": "actions",
        "description": "description",
        "enabled": "enabled",
        "error_action": "errorAction",
        "topic_rule_name": "topicRuleName",
    },
)
class TopicRuleProps:
    def __init__(
        self,
        *,
        sql: IotSql,
        actions: typing.Optional[typing.Sequence[IAction]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        error_action: typing.Optional[IAction] = None,
        topic_rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining an AWS IoT Rule.

        :param sql: (experimental) A simplified SQL syntax to filter messages received on an MQTT topic and push the data elsewhere.
        :param actions: (experimental) The actions associated with the topic rule. Default: No actions will be perform
        :param description: (experimental) A textual description of the topic rule. Default: None
        :param enabled: (experimental) Specifies whether the rule is enabled. Default: true
        :param error_action: (experimental) The action AWS IoT performs when it is unable to perform a rule's action. Default: - no action will be performed
        :param topic_rule_name: (experimental) The name of the topic rule. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_sns as sns
            
            
            topic = sns.Topic(self, "MyTopic")
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
                actions=[
                    actions.SnsTopicAction(topic,
                        message_format=actions.SnsActionMessageFormat.JSON
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590edde80b67943632c721759786da252d24ea6e116cd451e3e93bb968888414)
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument error_action", value=error_action, expected_type=type_hints["error_action"])
            check_type(argname="argument topic_rule_name", value=topic_rule_name, expected_type=type_hints["topic_rule_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sql": sql,
        }
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if error_action is not None:
            self._values["error_action"] = error_action
        if topic_rule_name is not None:
            self._values["topic_rule_name"] = topic_rule_name

    @builtins.property
    def sql(self) -> IotSql:
        '''(experimental) A simplified SQL syntax to filter messages received on an MQTT topic and push the data elsewhere.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-sql-reference.html
        :stability: experimental
        '''
        result = self._values.get("sql")
        assert result is not None, "Required property 'sql' is missing"
        return typing.cast(IotSql, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[IAction]]:
        '''(experimental) The actions associated with the topic rule.

        :default: No actions will be perform

        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[IAction]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A textual description of the topic rule.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the rule is enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def error_action(self) -> typing.Optional[IAction]:
        '''(experimental) The action AWS IoT performs when it is unable to perform a rule's action.

        :default: - no action will be performed

        :stability: experimental
        '''
        result = self._values.get("error_action")
        return typing.cast(typing.Optional[IAction], result)

    @builtins.property
    def topic_rule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the topic rule.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("topic_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TopicRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAccountAuditConfiguration)
class AccountAuditConfiguration(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-alpha.AccountAuditConfiguration",
):
    '''(experimental) Defines AWS IoT Audit Configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk import Duration
        
        
        iot.AccountAuditConfiguration(self, "AuditConfiguration",
            check_configuration=iot.CheckConfiguration(
                device_certificate_age_check=True,
                # The default value is 365 days
                # Valid values range from 30 days (minimum) to 3650 days (10 years, maximum)
                device_certificate_age_check_duration=Duration.days(365)
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        check_configuration: typing.Optional[typing.Union[CheckConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        target_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param check_configuration: (experimental) Specifies which audit checks are enabled and disabled for this account. Default: - all checks are enabled
        :param target_topic: (experimental) The target SNS topic to which audit notifications are sent. Default: - no notifications are sent

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5770f1ef794fc5270fd80ca239780b8bbda72293489a6c4bde130ea0c17cb0f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AccountAuditConfigurationProps(
            check_configuration=check_configuration, target_topic=target_topic
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAccountId")
    @builtins.classmethod
    def from_account_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        account_id: builtins.str,
    ) -> IAccountAuditConfiguration:
        '''(experimental) Import an existing AWS IoT Audit Configuration.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param account_id: The account ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3712cb14c2a0307906b9375e5b0b298caf9a979068b6e55717fe108f0ce164f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        return typing.cast(IAccountAuditConfiguration, jsii.sinvoke(cls, "fromAccountId", [scope, id, account_id]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        '''(experimental) The account ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accountId"))


__all__ = [
    "AccountAuditConfiguration",
    "AccountAuditConfigurationProps",
    "ActionConfig",
    "AuditCheck",
    "CheckConfiguration",
    "DayOfMonth",
    "DayOfWeek",
    "Frequency",
    "IAccountAuditConfiguration",
    "IAction",
    "ILogging",
    "IScheduledAudit",
    "ITopicRule",
    "IotSql",
    "IotSqlConfig",
    "LogLevel",
    "Logging",
    "LoggingProps",
    "ScheduledAudit",
    "ScheduledAuditAttributes",
    "ScheduledAuditProps",
    "TopicRule",
    "TopicRuleProps",
]

publication.publish()

def _typecheckingstub__91ef57f1dae6189d9b6717339eb57703831b4cdca305db4315a06756bad305b2(
    *,
    check_configuration: typing.Optional[typing.Union[CheckConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    target_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db72c5f97249b79d721bcd6a87436f822fe27caf16ccc0ae7aaa3671a54e7e5f(
    *,
    configuration: typing.Union[_aws_cdk_aws_iot_ceddda9d.CfnTopicRule.ActionProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9c5c9d3626b3241033eaae1616063003470252ba449cc0716435adb7ac0c89(
    *,
    authenticated_cognito_role_overly_permissive_check: typing.Optional[builtins.bool] = None,
    ca_certificate_expiring_check: typing.Optional[builtins.bool] = None,
    ca_certificate_key_quality_check: typing.Optional[builtins.bool] = None,
    conflicting_client_ids_check: typing.Optional[builtins.bool] = None,
    device_certificate_age_check: typing.Optional[builtins.bool] = None,
    device_certificate_age_check_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    device_certificate_expiring_check: typing.Optional[builtins.bool] = None,
    device_certificate_key_quality_check: typing.Optional[builtins.bool] = None,
    device_certificate_shared_check: typing.Optional[builtins.bool] = None,
    intermediate_ca_revoked_for_active_device_certificates_check: typing.Optional[builtins.bool] = None,
    iot_policy_overly_permissive_check: typing.Optional[builtins.bool] = None,
    io_t_policy_potential_mis_configuration_check: typing.Optional[builtins.bool] = None,
    iot_role_alias_allows_access_to_unused_services_check: typing.Optional[builtins.bool] = None,
    iot_role_alias_overly_permissive_check: typing.Optional[builtins.bool] = None,
    logging_disabled_check: typing.Optional[builtins.bool] = None,
    revoked_ca_certificate_still_active_check: typing.Optional[builtins.bool] = None,
    revoked_device_certificate_still_active_check: typing.Optional[builtins.bool] = None,
    unauthenticated_cognito_role_overly_permissive_check: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb73a8431c3f75f699052b2df93d897fdf174897f29d4825684600931e6f035(
    day: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b60afd6a89f56eb454ee327bd143df85ea1ea9518d995f338ac85c6f9172ef(
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246c805677b75001ec2445224c8ee29056b92709ee8d3bb168587a48bc5d0fb5(
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715467063ed924cc91a9fa5b60c44d4b1b82edbc8eb085d68321fd0014a32067(
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3862c5242014e403c7a2af3ffcf5d3a77ce6e5376d651493716a5b5061bd9a(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887fb9654c4aa0ba71be51a8acf671f0dc89cdb21899f13ebce575d2da566e05(
    *,
    aws_iot_sql_version: builtins.str,
    sql: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e352fb2a762be72085ea51f1a46a8e422901ecf3dbeaa4d542bc8e765ede38c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_level: typing.Optional[LogLevel] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99da511bd810901da44a2d46c1b46942903f1621bdf2704460e995700e2fe1e4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    log_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40b8e7e00237816e95880f570241f023097cd35cee2a70c6572617e8534056c(
    *,
    log_level: typing.Optional[LogLevel] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe70deb5f2117b5167fbc54c0f3804db0558b4f51ed7326da4904fd6db84b28(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_audit_configuration: IAccountAuditConfiguration,
    audit_checks: typing.Sequence[AuditCheck],
    frequency: Frequency,
    day_of_month: typing.Optional[DayOfMonth] = None,
    day_of_week: typing.Optional[DayOfWeek] = None,
    scheduled_audit_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8915542465bf341fcdbf13f7cb50020d6357ea6919124ae06915fb51694d8890(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    scheduled_audit_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd4dbeddc9751449b7be522e3e80c0310244510fbcd2f8541c6088349b2fb1e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    scheduled_audit_arn: builtins.str,
    scheduled_audit_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad0f3087ab74e23760b9e73acddd4e907b0e15c156e17b4a99310e0c141f0db(
    *,
    scheduled_audit_arn: builtins.str,
    scheduled_audit_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce3ff21c49ce66bfc46926d58b6c0194629b53bae7ffa22dd7039080d31025d(
    *,
    account_audit_configuration: IAccountAuditConfiguration,
    audit_checks: typing.Sequence[AuditCheck],
    frequency: Frequency,
    day_of_month: typing.Optional[DayOfMonth] = None,
    day_of_week: typing.Optional[DayOfWeek] = None,
    scheduled_audit_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5629ae4086674af1b4cd4c3b55a1d2cd04d194fe7dd7d9a1a08478dc69d9ac5f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    sql: IotSql,
    actions: typing.Optional[typing.Sequence[IAction]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    error_action: typing.Optional[IAction] = None,
    topic_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a02640c49b9d9e3824df915f05b77c597b5dfd5d900377ada5b2b60b004bbf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    topic_rule_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6d84c555ae6d88e9f422f5418183ec42014991c6a48af643a3d0341a35a73a(
    action: IAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590edde80b67943632c721759786da252d24ea6e116cd451e3e93bb968888414(
    *,
    sql: IotSql,
    actions: typing.Optional[typing.Sequence[IAction]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    error_action: typing.Optional[IAction] = None,
    topic_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5770f1ef794fc5270fd80ca239780b8bbda72293489a6c4bde130ea0c17cb0f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    check_configuration: typing.Optional[typing.Union[CheckConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    target_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3712cb14c2a0307906b9375e5b0b298caf9a979068b6e55717fe108f0ce164f3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
