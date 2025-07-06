'''
# AWS::Chatbot Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

AWS Chatbot is an AWS service that enables DevOps and software development teams to use Slack chat rooms to monitor and respond to operational events in their AWS Cloud. AWS Chatbot processes AWS service notifications from Amazon Simple Notification Service (Amazon SNS), and forwards them to Slack chat rooms so teams can analyze and act on them immediately, regardless of location.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_chatbot as chatbot
import aws_cdk.aws_sns as sns
import aws_cdk.aws_iam as iam


slack_channel = chatbot.SlackChannelConfiguration(self, "MySlackChannel",
    slack_channel_configuration_name="YOUR_CHANNEL_NAME",
    slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",
    slack_channel_id="YOUR_SLACK_CHANNEL_ID"
)

slack_channel.add_to_role_policy(iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    actions=["s3:GetObject"
    ],
    resources=["arn:aws:s3:::abc/xyz/123.txt"]
))

slack_channel.add_notification_topic(sns.Topic(self, "MyTopic"))
```

## Log Group

Slack channel configuration automatically create a log group with the name `/aws/chatbot/<configuration-name>` in `us-east-1` upon first execution with
log data set to never expire.

The `logRetention` property can be used to set a different expiration period. A log group will be created if not already exists.
If the log group already exists, it's expiration will be configured to the value specified in this construct (never expire, by default).

By default, CDK uses the AWS SDK retry options when interacting with the log group. The `logRetentionRetryOptions` property
allows you to customize the maximum number of retries and base backoff duration.

*Note* that, if `logRetention` is set, a [CloudFormation custom
resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html) is added
to the stack that pre-creates the log group as part of the stack deployment, if it already doesn't exist, and sets the
correct log retention period (never expire, by default).
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

import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_9b88bb94
import aws_cdk.aws_codestarnotifications as _aws_cdk_aws_codestarnotifications_391e8ded
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_logs as _aws_cdk_aws_logs_6c4320fb
import aws_cdk.aws_sns as _aws_cdk_aws_sns_889c7272
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnMicrosoftTeamsChannelConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-chatbot.CfnMicrosoftTeamsChannelConfiguration",
):
    '''A CloudFormation ``AWS::Chatbot::MicrosoftTeamsChannelConfiguration``.

    The ``AWS::Chatbot::MicrosoftTeamsChannelConfiguration`` resource configures a Microsoft Teams channel to allow users to use AWS Chatbot with AWS CloudFormation templates.

    This resource requires some setup to be done in the AWS Chatbot console. To provide the required Microsoft Teams team and tenant IDs, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console, then copy and paste the IDs from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .

    :cloudformationResource: AWS::Chatbot::MicrosoftTeamsChannelConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_chatbot as chatbot
        
        cfn_microsoft_teams_channel_configuration = chatbot.CfnMicrosoftTeamsChannelConfiguration(self, "MyCfnMicrosoftTeamsChannelConfiguration",
            configuration_name="configurationName",
            iam_role_arn="iamRoleArn",
            team_id="teamId",
            teams_channel_id="teamsChannelId",
            teams_tenant_id="teamsTenantId",
        
            # the properties below are optional
            guardrail_policies=["guardrailPolicies"],
            logging_level="loggingLevel",
            sns_topic_arns=["snsTopicArns"],
            user_role_required=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        configuration_name: builtins.str,
        iam_role_arn: builtins.str,
        team_id: builtins.str,
        teams_channel_id: builtins.str,
        teams_tenant_id: builtins.str,
        guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_level: typing.Optional[builtins.str] = None,
        sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::Chatbot::MicrosoftTeamsChannelConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration_name: The name of the configuration.
        :param iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot . This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .
        :param team_id: The ID of the Microsoft Team authorized with AWS Chatbot . To get the team ID, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console. Then you can copy and paste the team ID from the console. For more details, see steps 1-4 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .
        :param teams_channel_id: The ID of the Microsoft Teams channel. To get the channel ID, open Microsoft Teams, right click on the channel name in the left pane, then choose Copy. An example of the channel ID syntax is: ``19%3ab6ef35dc342d56ba5654e6fc6d25a071%40thread.tacv2`` .
        :param teams_tenant_id: The ID of the Microsoft Teams tenant. To get the tenant ID, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console. Then you can copy and paste the tenant ID from the console. For more details, see steps 1-4 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .
        :param guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .
        :param sns_topic_arns: The ARNs of the SNS topics that deliver notifications to AWS Chatbot .
        :param user_role_required: Enables use of a user role requirement in your chat configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9cdd297dd0d4306b166bba08ba7d8011e186c4d9e14c53be4668fcc6a06d8bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMicrosoftTeamsChannelConfigurationProps(
            configuration_name=configuration_name,
            iam_role_arn=iam_role_arn,
            team_id=team_id,
            teams_channel_id=teams_channel_id,
            teams_tenant_id=teams_tenant_id,
            guardrail_policies=guardrail_policies,
            logging_level=logging_level,
            sns_topic_arns=sns_topic_arns,
            user_role_required=user_role_required,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fd7a20be0aae6717c22436bf7b63127fa09aed564624fba710427f929dfd53)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6bdf7f2de7b7f471e32fc688e02f330ca0a2099d0ad6eb1832be331e3d408b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="configurationName")
    def configuration_name(self) -> builtins.str:
        '''The name of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-configurationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "configurationName"))

    @configuration_name.setter
    def configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcd09676ac423e19f1be01a8ed369f297fb6e349529cb0a22f8faf7f729e0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationName", value)

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that defines the permissions for AWS Chatbot .

        This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-iamrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b531682afd4f94c3d08155d5c459835507ece0fb23e2cb120d455811a887283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        '''The ID of the Microsoft Team authorized with AWS Chatbot .

        To get the team ID, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console. Then you can copy and paste the team ID from the console. For more details, see steps 1-4 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamid
        '''
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104d8c8daca025ad443f0945a83277bf614dbc2648c8e50f76da7aaf69f73138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="teamsChannelId")
    def teams_channel_id(self) -> builtins.str:
        '''The ID of the Microsoft Teams channel.

        To get the channel ID, open Microsoft Teams, right click on the channel name in the left pane, then choose Copy. An example of the channel ID syntax is: ``19%3ab6ef35dc342d56ba5654e6fc6d25a071%40thread.tacv2`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamschannelid
        '''
        return typing.cast(builtins.str, jsii.get(self, "teamsChannelId"))

    @teams_channel_id.setter
    def teams_channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc33ab91f0478ef0f8eb5260851ec77f07ebd42b9fe16b7eed3565225dfa2c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamsChannelId", value)

    @builtins.property
    @jsii.member(jsii_name="teamsTenantId")
    def teams_tenant_id(self) -> builtins.str:
        '''The ID of the Microsoft Teams tenant.

        To get the tenant ID, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console. Then you can copy and paste the tenant ID from the console. For more details, see steps 1-4 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamstenantid
        '''
        return typing.cast(builtins.str, jsii.get(self, "teamsTenantId"))

    @teams_tenant_id.setter
    def teams_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca4593fbbb6a49003f11c03627537a410cd89a9af02bb04e2590f678fe87ac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamsTenantId", value)

    @builtins.property
    @jsii.member(jsii_name="guardrailPolicies")
    def guardrail_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IAM policy ARNs that are applied as channel guardrails.

        The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-guardrailpolicies
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "guardrailPolicies"))

    @guardrail_policies.setter
    def guardrail_policies(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e49557a7bb28dc4c5ee358697d4f42f83aeffa6f5d90322f0b4fb4c41b23943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailPolicies", value)

    @builtins.property
    @jsii.member(jsii_name="loggingLevel")
    def logging_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs.

        Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-logginglevel
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingLevel"))

    @logging_level.setter
    def logging_level(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142dfaa688a3969e9ce7ae36f24c264b04d1224320f68b4b04eae227ac5edc24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingLevel", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArns")
    def sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the SNS topics that deliver notifications to AWS Chatbot .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-snstopicarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "snsTopicArns"))

    @sns_topic_arns.setter
    def sns_topic_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7062064fa522a7740768d0606ef69f6a4033cc3f2cd51be235fa0b82d3ab799d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopicArns", value)

    @builtins.property
    @jsii.member(jsii_name="userRoleRequired")
    def user_role_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-userrolerequired
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "userRoleRequired"))

    @user_role_required.setter
    def user_role_required(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ef144ce3dab77d5a40389ef1bf8d259f651b375a1c728c5be413dfa5fc29a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userRoleRequired", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-chatbot.CfnMicrosoftTeamsChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_name": "configurationName",
        "iam_role_arn": "iamRoleArn",
        "team_id": "teamId",
        "teams_channel_id": "teamsChannelId",
        "teams_tenant_id": "teamsTenantId",
        "guardrail_policies": "guardrailPolicies",
        "logging_level": "loggingLevel",
        "sns_topic_arns": "snsTopicArns",
        "user_role_required": "userRoleRequired",
    },
)
class CfnMicrosoftTeamsChannelConfigurationProps:
    def __init__(
        self,
        *,
        configuration_name: builtins.str,
        iam_role_arn: builtins.str,
        team_id: builtins.str,
        teams_channel_id: builtins.str,
        teams_tenant_id: builtins.str,
        guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_level: typing.Optional[builtins.str] = None,
        sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnMicrosoftTeamsChannelConfiguration``.

        :param configuration_name: The name of the configuration.
        :param iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot . This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .
        :param team_id: The ID of the Microsoft Team authorized with AWS Chatbot . To get the team ID, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console. Then you can copy and paste the team ID from the console. For more details, see steps 1-4 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .
        :param teams_channel_id: The ID of the Microsoft Teams channel. To get the channel ID, open Microsoft Teams, right click on the channel name in the left pane, then choose Copy. An example of the channel ID syntax is: ``19%3ab6ef35dc342d56ba5654e6fc6d25a071%40thread.tacv2`` .
        :param teams_tenant_id: The ID of the Microsoft Teams tenant. To get the tenant ID, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console. Then you can copy and paste the tenant ID from the console. For more details, see steps 1-4 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .
        :param guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .
        :param sns_topic_arns: The ARNs of the SNS topics that deliver notifications to AWS Chatbot .
        :param user_role_required: Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_chatbot as chatbot
            
            cfn_microsoft_teams_channel_configuration_props = chatbot.CfnMicrosoftTeamsChannelConfigurationProps(
                configuration_name="configurationName",
                iam_role_arn="iamRoleArn",
                team_id="teamId",
                teams_channel_id="teamsChannelId",
                teams_tenant_id="teamsTenantId",
            
                # the properties below are optional
                guardrail_policies=["guardrailPolicies"],
                logging_level="loggingLevel",
                sns_topic_arns=["snsTopicArns"],
                user_role_required=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1012c1dd3981a55fd2aec19147d88cc9aedd721341cd0e2cb1c4d1c20f85b888)
            check_type(argname="argument configuration_name", value=configuration_name, expected_type=type_hints["configuration_name"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument teams_channel_id", value=teams_channel_id, expected_type=type_hints["teams_channel_id"])
            check_type(argname="argument teams_tenant_id", value=teams_tenant_id, expected_type=type_hints["teams_tenant_id"])
            check_type(argname="argument guardrail_policies", value=guardrail_policies, expected_type=type_hints["guardrail_policies"])
            check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
            check_type(argname="argument sns_topic_arns", value=sns_topic_arns, expected_type=type_hints["sns_topic_arns"])
            check_type(argname="argument user_role_required", value=user_role_required, expected_type=type_hints["user_role_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_name": configuration_name,
            "iam_role_arn": iam_role_arn,
            "team_id": team_id,
            "teams_channel_id": teams_channel_id,
            "teams_tenant_id": teams_tenant_id,
        }
        if guardrail_policies is not None:
            self._values["guardrail_policies"] = guardrail_policies
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if sns_topic_arns is not None:
            self._values["sns_topic_arns"] = sns_topic_arns
        if user_role_required is not None:
            self._values["user_role_required"] = user_role_required

    @builtins.property
    def configuration_name(self) -> builtins.str:
        '''The name of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-configurationname
        '''
        result = self._values.get("configuration_name")
        assert result is not None, "Required property 'configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that defines the permissions for AWS Chatbot .

        This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''The ID of the Microsoft Team authorized with AWS Chatbot .

        To get the team ID, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console. Then you can copy and paste the team ID from the console. For more details, see steps 1-4 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamid
        '''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def teams_channel_id(self) -> builtins.str:
        '''The ID of the Microsoft Teams channel.

        To get the channel ID, open Microsoft Teams, right click on the channel name in the left pane, then choose Copy. An example of the channel ID syntax is: ``19%3ab6ef35dc342d56ba5654e6fc6d25a071%40thread.tacv2`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamschannelid
        '''
        result = self._values.get("teams_channel_id")
        assert result is not None, "Required property 'teams_channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def teams_tenant_id(self) -> builtins.str:
        '''The ID of the Microsoft Teams tenant.

        To get the tenant ID, you must perform the initial authorization flow with Microsoft Teams in the AWS Chatbot console. Then you can copy and paste the tenant ID from the console. For more details, see steps 1-4 in `Get started with Microsoft Teams <https://docs.aws.amazon.com/chatbot/latest/adminguide/teams-setup.html#teams-client-setup>`_ in the *AWS Chatbot Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-teamstenantid
        '''
        result = self._values.get("teams_tenant_id")
        assert result is not None, "Required property 'teams_tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def guardrail_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IAM policy ARNs that are applied as channel guardrails.

        The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-guardrailpolicies
        '''
        result = self._values.get("guardrail_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs.

        Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-logginglevel
        '''
        result = self._values.get("logging_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the SNS topics that deliver notifications to AWS Chatbot .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-snstopicarns
        '''
        result = self._values.get("sns_topic_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_role_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-microsoftteamschannelconfiguration.html#cfn-chatbot-microsoftteamschannelconfiguration-userrolerequired
        '''
        result = self._values.get("user_role_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMicrosoftTeamsChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSlackChannelConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-chatbot.CfnSlackChannelConfiguration",
):
    '''A CloudFormation ``AWS::Chatbot::SlackChannelConfiguration``.

    The ``AWS::Chatbot::SlackChannelConfiguration`` resource configures a Slack channel to allow users to use AWS Chatbot with AWS CloudFormation templates.

    This resource requires some setup to be done in the AWS Chatbot console. To provide the required Slack workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console, then copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .

    :cloudformationResource: AWS::Chatbot::SlackChannelConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_chatbot as chatbot
        
        cfn_slack_channel_configuration = chatbot.CfnSlackChannelConfiguration(self, "MyCfnSlackChannelConfiguration",
            configuration_name="configurationName",
            iam_role_arn="iamRoleArn",
            slack_channel_id="slackChannelId",
            slack_workspace_id="slackWorkspaceId",
        
            # the properties below are optional
            guardrail_policies=["guardrailPolicies"],
            logging_level="loggingLevel",
            sns_topic_arns=["snsTopicArns"],
            user_role_required=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        configuration_name: builtins.str,
        iam_role_arn: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_level: typing.Optional[builtins.str] = None,
        sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::Chatbot::SlackChannelConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration_name: The name of the configuration.
        :param iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot . This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ``ABCBBLZZZ`` .
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot . To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .
        :param guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .
        :param sns_topic_arns: The ARNs of the SNS topics that deliver notifications to AWS Chatbot .
        :param user_role_required: Enables use of a user role requirement in your chat configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c7f370da3f6de7524649bcd9c8be7f706ca1f57ae1e377dcf69a45e4ff6f33)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSlackChannelConfigurationProps(
            configuration_name=configuration_name,
            iam_role_arn=iam_role_arn,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
            guardrail_policies=guardrail_policies,
            logging_level=logging_level,
            sns_topic_arns=sns_topic_arns,
            user_role_required=user_role_required,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5c6045283704721e78e2eb25db228fd1752f893c5306532dd8085cf4558dd9)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55eb0f59ee6376cff3b8c1943081ac0abe386c5cc4fc00ebbb2fbe1ff467695)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="configurationName")
    def configuration_name(self) -> builtins.str:
        '''The name of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "configurationName"))

    @configuration_name.setter
    def configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f862e4c363f4b7ae8641152e672451118d0cd76bc3f5becfc13ce711f80efa96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationName", value)

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that defines the permissions for AWS Chatbot .

        This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51b6df5d375e112e5d3219114e26c87802428c0a42a51b432c550c2b37f4e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="slackChannelId")
    def slack_channel_id(self) -> builtins.str:
        '''The ID of the Slack channel.

        To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ``ABCBBLZZZ`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelId"))

    @slack_channel_id.setter
    def slack_channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616d1868aaf3af188eca4204786564fdebda8499e1cce2ee5af7a65bce28866e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackChannelId", value)

    @builtins.property
    @jsii.member(jsii_name="slackWorkspaceId")
    def slack_workspace_id(self) -> builtins.str:
        '''The ID of the Slack workspace authorized with AWS Chatbot .

        To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackWorkspaceId"))

    @slack_workspace_id.setter
    def slack_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144315cc987e7fdf7d5e2ba13af40037a92f9039708adb2b358d6435c80caf3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackWorkspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="guardrailPolicies")
    def guardrail_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IAM policy ARNs that are applied as channel guardrails.

        The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-guardrailpolicies
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "guardrailPolicies"))

    @guardrail_policies.setter
    def guardrail_policies(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289b840e15b556bcf9a9a0c39b64221c00ce3c9257524d23f34d47e66d8d0a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailPolicies", value)

    @builtins.property
    @jsii.member(jsii_name="loggingLevel")
    def logging_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs.

        Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingLevel"))

    @logging_level.setter
    def logging_level(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a95ccd5107475d408eaa912d4aa083488a119c6a8cc44147e6a9fd7d152b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingLevel", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArns")
    def sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the SNS topics that deliver notifications to AWS Chatbot .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "snsTopicArns"))

    @sns_topic_arns.setter
    def sns_topic_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a431842e31df08b1dcd496deb27d57569f8d98ddcea27d1804f3de3f2a3dea88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopicArns", value)

    @builtins.property
    @jsii.member(jsii_name="userRoleRequired")
    def user_role_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-userrolerequired
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "userRoleRequired"))

    @user_role_required.setter
    def user_role_required(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a448ad59ffb961c47457f63a4eef9762a73b7cb6dcd0622aa0eab35e871820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userRoleRequired", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-chatbot.CfnSlackChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_name": "configurationName",
        "iam_role_arn": "iamRoleArn",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
        "guardrail_policies": "guardrailPolicies",
        "logging_level": "loggingLevel",
        "sns_topic_arns": "snsTopicArns",
        "user_role_required": "userRoleRequired",
    },
)
class CfnSlackChannelConfigurationProps:
    def __init__(
        self,
        *,
        configuration_name: builtins.str,
        iam_role_arn: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_level: typing.Optional[builtins.str] = None,
        sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSlackChannelConfiguration``.

        :param configuration_name: The name of the configuration.
        :param iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot . This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ``ABCBBLZZZ`` .
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot . To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .
        :param guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .
        :param sns_topic_arns: The ARNs of the SNS topics that deliver notifications to AWS Chatbot .
        :param user_role_required: Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_chatbot as chatbot
            
            cfn_slack_channel_configuration_props = chatbot.CfnSlackChannelConfigurationProps(
                configuration_name="configurationName",
                iam_role_arn="iamRoleArn",
                slack_channel_id="slackChannelId",
                slack_workspace_id="slackWorkspaceId",
            
                # the properties below are optional
                guardrail_policies=["guardrailPolicies"],
                logging_level="loggingLevel",
                sns_topic_arns=["snsTopicArns"],
                user_role_required=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cea1b2f4ee1d014aa161b367eccdc08c039f2ff9729bf1fbf77c46414bb9d2)
            check_type(argname="argument configuration_name", value=configuration_name, expected_type=type_hints["configuration_name"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument slack_channel_id", value=slack_channel_id, expected_type=type_hints["slack_channel_id"])
            check_type(argname="argument slack_workspace_id", value=slack_workspace_id, expected_type=type_hints["slack_workspace_id"])
            check_type(argname="argument guardrail_policies", value=guardrail_policies, expected_type=type_hints["guardrail_policies"])
            check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
            check_type(argname="argument sns_topic_arns", value=sns_topic_arns, expected_type=type_hints["sns_topic_arns"])
            check_type(argname="argument user_role_required", value=user_role_required, expected_type=type_hints["user_role_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_name": configuration_name,
            "iam_role_arn": iam_role_arn,
            "slack_channel_id": slack_channel_id,
            "slack_workspace_id": slack_workspace_id,
        }
        if guardrail_policies is not None:
            self._values["guardrail_policies"] = guardrail_policies
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if sns_topic_arns is not None:
            self._values["sns_topic_arns"] = sns_topic_arns
        if user_role_required is not None:
            self._values["user_role_required"] = user_role_required

    @builtins.property
    def configuration_name(self) -> builtins.str:
        '''The name of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        '''
        result = self._values.get("configuration_name")
        assert result is not None, "Required property 'configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that defines the permissions for AWS Chatbot .

        This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_channel_id(self) -> builtins.str:
        '''The ID of the Slack channel.

        To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ``ABCBBLZZZ`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        '''
        result = self._values.get("slack_channel_id")
        assert result is not None, "Required property 'slack_channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_workspace_id(self) -> builtins.str:
        '''The ID of the Slack workspace authorized with AWS Chatbot .

        To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        '''
        result = self._values.get("slack_workspace_id")
        assert result is not None, "Required property 'slack_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def guardrail_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IAM policy ARNs that are applied as channel guardrails.

        The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-guardrailpolicies
        '''
        result = self._values.get("guardrail_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs.

        Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        '''
        result = self._values.get("logging_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the SNS topics that deliver notifications to AWS Chatbot .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        '''
        result = self._values.get("sns_topic_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_role_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-userrolerequired
        '''
        result = self._values.get("user_role_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-chatbot.ISlackChannelConfiguration")
class ISlackChannelConfiguration(
    _aws_cdk_core_f4b25747.IResource,
    _aws_cdk_aws_iam_940a1ce0.IGrantable,
    _aws_cdk_aws_codestarnotifications_391e8ded.INotificationRuleTarget,
    typing_extensions.Protocol,
):
    '''Represents a Slack channel configuration.'''

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> builtins.str:
        '''The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> builtins.str:
        '''The name of Slack channel configuration.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The permission role of Slack channel configuration.

        :default: - A role will be created.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    ) -> None:
        '''Adds a statement to the IAM role.

        :param statement: -
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Return the given named metric for this SlackChannelConfiguration.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        ...


class _ISlackChannelConfigurationProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_iam_940a1ce0.IGrantable), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_codestarnotifications_391e8ded.INotificationRuleTarget), # type: ignore[misc]
):
    '''Represents a Slack channel configuration.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-chatbot.ISlackChannelConfiguration"

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> builtins.str:
        '''The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> builtins.str:
        '''The name of Slack channel configuration.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The permission role of Slack channel configuration.

        :default: - A role will be created.

        :attribute: true
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], jsii.get(self, "role"))

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    ) -> None:
        '''Adds a statement to the IAM role.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc968dda378a3b3747e1bc242fffcd30a86adaf991e2a9a7e3c7b626f79eaa64)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Return the given named metric for this SlackChannelConfiguration.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475c5c5b7b4888a9831dd49f89a97a9416b9cc39b1624fd77cbdc90685e3286a)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metric", [metric_name, props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISlackChannelConfiguration).__jsii_proxy_class__ = lambda : _ISlackChannelConfigurationProxy


@jsii.enum(jsii_type="@aws-cdk/aws-chatbot.LoggingLevel")
class LoggingLevel(enum.Enum):
    '''Logging levels include ERROR, INFO, or NONE.'''

    ERROR = "ERROR"
    '''ERROR.'''
    INFO = "INFO"
    '''INFO.'''
    NONE = "NONE"
    '''NONE.'''


@jsii.implements(ISlackChannelConfiguration)
class SlackChannelConfiguration(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-chatbot.SlackChannelConfiguration",
):
    '''A new Slack channel configuration.

    :exampleMetadata: infused

    Example::

        # Define CodeStar Notification rules for Pipelines
        import aws_cdk.aws_chatbot as chatbot
        
        # pipeline: codepipeline.Pipeline
        
        target = chatbot.SlackChannelConfiguration(self, "MySlackChannel",
            slack_channel_configuration_name="YOUR_CHANNEL_NAME",
            slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",
            slack_channel_id="YOUR_SLACK_CHANNEL_ID"
        )
        rule = pipeline.notify_on_execution_state_change("NotifyOnExecutionStateChange", target)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        slack_channel_configuration_name: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        logging_level: typing.Optional[LoggingLevel] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_6c4320fb.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_logs_6c4320fb.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        notification_topics: typing.Optional[typing.Sequence[_aws_cdk_aws_sns_889c7272.ITopic]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param slack_channel_configuration_name: The name of Slack channel configuration.
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot. To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Default: LoggingLevel.NONE
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param notification_topics: The SNS topics that deliver notifications to AWS Chatbot. Default: None
        :param role: The permission role of Slack channel configuration. Default: - A role will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff1d0f5022dd09efcf6c9f7df000179e4bae9e90244a951a4aec6b57d38f78a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SlackChannelConfigurationProps(
            slack_channel_configuration_name=slack_channel_configuration_name,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
            logging_level=logging_level,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            notification_topics=notification_topics,
            role=role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSlackChannelConfigurationArn")
    @builtins.classmethod
    def from_slack_channel_configuration_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        slack_channel_configuration_arn: builtins.str,
    ) -> ISlackChannelConfiguration:
        '''Import an existing Slack channel configuration provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param slack_channel_configuration_arn: configuration ARN (i.e. arn:aws:chatbot::1234567890:chat-configuration/slack-channel/my-slack).

        :return: a reference to the existing Slack channel configuration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873a967754e979ddcbb76380b810df583a5c26d254f917a860a0784a3fcf3799)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument slack_channel_configuration_arn", value=slack_channel_configuration_arn, expected_type=type_hints["slack_channel_configuration_arn"])
        return typing.cast(ISlackChannelConfiguration, jsii.sinvoke(cls, "fromSlackChannelConfigurationArn", [scope, id, slack_channel_configuration_arn]))

    @jsii.member(jsii_name="metricAll")
    @builtins.classmethod
    def metric_all(
        cls,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Return the given named metric for All SlackChannelConfigurations.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c766f59ff486fa82644b7bfd86c977a4d7d1bbcb19daabfa12470df675b15df)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.sinvoke(cls, "metricAll", [metric_name, props]))

    @jsii.member(jsii_name="addNotificationTopic")
    def add_notification_topic(
        self,
        notification_topic: _aws_cdk_aws_sns_889c7272.ITopic,
    ) -> None:
        '''Adds a SNS topic that deliver notifications to AWS Chatbot.

        :param notification_topic: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc40bd846897c818c84a1ae27c87ad7bf0f1d015c8dfcc4db52a3747a24e6d68)
            check_type(argname="argument notification_topic", value=notification_topic, expected_type=type_hints["notification_topic"])
        return typing.cast(None, jsii.invoke(self, "addNotificationTopic", [notification_topic]))

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    ) -> None:
        '''Adds extra permission to iam-role of Slack channel configuration.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd58edcd1450979b31c74df668ad381ca95565eab6ed55af0e93923b687fa6a)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.member(jsii_name="bindAsNotificationRuleTarget")
    def bind_as_notification_rule_target(
        self,
        _scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_codestarnotifications_391e8ded.NotificationRuleTargetConfig:
        '''Returns a target configuration for notification rule.

        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f080afe93f57c67a851672ad730fdb2732788d9bde3446f52ece72648a2b416)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(_aws_cdk_aws_codestarnotifications_391e8ded.NotificationRuleTargetConfig, jsii.invoke(self, "bindAsNotificationRuleTarget", [_scope]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_9b88bb94.Metric:
        '''Return the given named metric for this SlackChannelConfiguration.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c2d7e64d2730ceda26d685dbb4cbbda8132027e60ae55e66fd8ea1dab6db98)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_9b88bb94.MetricOptions(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_9b88bb94.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_940a1ce0.IPrincipal:
        '''The principal to grant permissions to.'''
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> builtins.str:
        '''The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.'''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> builtins.str:
        '''The name of Slack channel configuration.'''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The permission role of Slack channel configuration.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-chatbot.SlackChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "slack_channel_configuration_name": "slackChannelConfigurationName",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
        "logging_level": "loggingLevel",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "notification_topics": "notificationTopics",
        "role": "role",
    },
)
class SlackChannelConfigurationProps:
    def __init__(
        self,
        *,
        slack_channel_configuration_name: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        logging_level: typing.Optional[LoggingLevel] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_6c4320fb.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_logs_6c4320fb.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        notification_topics: typing.Optional[typing.Sequence[_aws_cdk_aws_sns_889c7272.ITopic]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''Properties for a new Slack channel configuration.

        :param slack_channel_configuration_name: The name of Slack channel configuration.
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot. To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Default: LoggingLevel.NONE
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param notification_topics: The SNS topics that deliver notifications to AWS Chatbot. Default: None
        :param role: The permission role of Slack channel configuration. Default: - A role will be created.

        :exampleMetadata: infused

        Example::

            # Define CodeStar Notification rules for Pipelines
            import aws_cdk.aws_chatbot as chatbot
            
            # pipeline: codepipeline.Pipeline
            
            target = chatbot.SlackChannelConfiguration(self, "MySlackChannel",
                slack_channel_configuration_name="YOUR_CHANNEL_NAME",
                slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",
                slack_channel_id="YOUR_SLACK_CHANNEL_ID"
            )
            rule = pipeline.notify_on_execution_state_change("NotifyOnExecutionStateChange", target)
        '''
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _aws_cdk_aws_logs_6c4320fb.LogRetentionRetryOptions(**log_retention_retry_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23826c80727ceab4bcf17b16e85ef31ecb627859bcb3acf755537b24c6952cb6)
            check_type(argname="argument slack_channel_configuration_name", value=slack_channel_configuration_name, expected_type=type_hints["slack_channel_configuration_name"])
            check_type(argname="argument slack_channel_id", value=slack_channel_id, expected_type=type_hints["slack_channel_id"])
            check_type(argname="argument slack_workspace_id", value=slack_workspace_id, expected_type=type_hints["slack_workspace_id"])
            check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument log_retention_role", value=log_retention_role, expected_type=type_hints["log_retention_role"])
            check_type(argname="argument notification_topics", value=notification_topics, expected_type=type_hints["notification_topics"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "slack_channel_configuration_name": slack_channel_configuration_name,
            "slack_channel_id": slack_channel_id,
            "slack_workspace_id": slack_workspace_id,
        }
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if notification_topics is not None:
            self._values["notification_topics"] = notification_topics
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def slack_channel_configuration_name(self) -> builtins.str:
        '''The name of Slack channel configuration.'''
        result = self._values.get("slack_channel_configuration_name")
        assert result is not None, "Required property 'slack_channel_configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_channel_id(self) -> builtins.str:
        '''The ID of the Slack channel.

        To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link.
        The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.
        '''
        result = self._values.get("slack_channel_id")
        assert result is not None, "Required property 'slack_channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_workspace_id(self) -> builtins.str:
        '''The ID of the Slack workspace authorized with AWS Chatbot.

        To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console.
        Then you can copy and paste the workspace ID from the console.
        For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.

        :see: https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro
        '''
        result = self._values.get("slack_workspace_id")
        assert result is not None, "Required property 'slack_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def logging_level(self) -> typing.Optional[LoggingLevel]:
        '''Specifies the logging level for this configuration.

        This property affects the log entries pushed to Amazon CloudWatch Logs.

        :default: LoggingLevel.NONE
        '''
        result = self._values.get("logging_level")
        return typing.cast(typing.Optional[LoggingLevel], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.RetentionDays]:
        '''The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.RetentionDays], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_6c4320fb.LogRetentionRetryOptions]:
        '''When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        :default: - Default AWS SDK retry options.
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_6c4320fb.LogRetentionRetryOptions], result)

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - A new role is created.
        '''
        result = self._values.get("log_retention_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def notification_topics(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_sns_889c7272.ITopic]]:
        '''The SNS topics that deliver notifications to AWS Chatbot.

        :default: None
        '''
        result = self._values.get("notification_topics")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_sns_889c7272.ITopic]], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The permission role of Slack channel configuration.

        :default: - A role will be created.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMicrosoftTeamsChannelConfiguration",
    "CfnMicrosoftTeamsChannelConfigurationProps",
    "CfnSlackChannelConfiguration",
    "CfnSlackChannelConfigurationProps",
    "ISlackChannelConfiguration",
    "LoggingLevel",
    "SlackChannelConfiguration",
    "SlackChannelConfigurationProps",
]

publication.publish()

def _typecheckingstub__d9cdd297dd0d4306b166bba08ba7d8011e186c4d9e14c53be4668fcc6a06d8bb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    configuration_name: builtins.str,
    iam_role_arn: builtins.str,
    team_id: builtins.str,
    teams_channel_id: builtins.str,
    teams_tenant_id: builtins.str,
    guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fd7a20be0aae6717c22436bf7b63127fa09aed564624fba710427f929dfd53(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6bdf7f2de7b7f471e32fc688e02f330ca0a2099d0ad6eb1832be331e3d408b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcd09676ac423e19f1be01a8ed369f297fb6e349529cb0a22f8faf7f729e0ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b531682afd4f94c3d08155d5c459835507ece0fb23e2cb120d455811a887283(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104d8c8daca025ad443f0945a83277bf614dbc2648c8e50f76da7aaf69f73138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc33ab91f0478ef0f8eb5260851ec77f07ebd42b9fe16b7eed3565225dfa2c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca4593fbbb6a49003f11c03627537a410cd89a9af02bb04e2590f678fe87ac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e49557a7bb28dc4c5ee358697d4f42f83aeffa6f5d90322f0b4fb4c41b23943(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142dfaa688a3969e9ce7ae36f24c264b04d1224320f68b4b04eae227ac5edc24(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7062064fa522a7740768d0606ef69f6a4033cc3f2cd51be235fa0b82d3ab799d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ef144ce3dab77d5a40389ef1bf8d259f651b375a1c728c5be413dfa5fc29a0(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1012c1dd3981a55fd2aec19147d88cc9aedd721341cd0e2cb1c4d1c20f85b888(
    *,
    configuration_name: builtins.str,
    iam_role_arn: builtins.str,
    team_id: builtins.str,
    teams_channel_id: builtins.str,
    teams_tenant_id: builtins.str,
    guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c7f370da3f6de7524649bcd9c8be7f706ca1f57ae1e377dcf69a45e4ff6f33(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    configuration_name: builtins.str,
    iam_role_arn: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5c6045283704721e78e2eb25db228fd1752f893c5306532dd8085cf4558dd9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55eb0f59ee6376cff3b8c1943081ac0abe386c5cc4fc00ebbb2fbe1ff467695(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f862e4c363f4b7ae8641152e672451118d0cd76bc3f5becfc13ce711f80efa96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51b6df5d375e112e5d3219114e26c87802428c0a42a51b432c550c2b37f4e19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616d1868aaf3af188eca4204786564fdebda8499e1cce2ee5af7a65bce28866e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144315cc987e7fdf7d5e2ba13af40037a92f9039708adb2b358d6435c80caf3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289b840e15b556bcf9a9a0c39b64221c00ce3c9257524d23f34d47e66d8d0a96(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a95ccd5107475d408eaa912d4aa083488a119c6a8cc44147e6a9fd7d152b65(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a431842e31df08b1dcd496deb27d57569f8d98ddcea27d1804f3de3f2a3dea88(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a448ad59ffb961c47457f63a4eef9762a73b7cb6dcd0622aa0eab35e871820(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cea1b2f4ee1d014aa161b367eccdc08c039f2ff9729bf1fbf77c46414bb9d2(
    *,
    configuration_name: builtins.str,
    iam_role_arn: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_role_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc968dda378a3b3747e1bc242fffcd30a86adaf991e2a9a7e3c7b626f79eaa64(
    statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475c5c5b7b4888a9831dd49f89a97a9416b9cc39b1624fd77cbdc90685e3286a(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff1d0f5022dd09efcf6c9f7df000179e4bae9e90244a951a4aec6b57d38f78a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    slack_channel_configuration_name: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    logging_level: typing.Optional[LoggingLevel] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_6c4320fb.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_logs_6c4320fb.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    notification_topics: typing.Optional[typing.Sequence[_aws_cdk_aws_sns_889c7272.ITopic]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873a967754e979ddcbb76380b810df583a5c26d254f917a860a0784a3fcf3799(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    slack_channel_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c766f59ff486fa82644b7bfd86c977a4d7d1bbcb19daabfa12470df675b15df(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc40bd846897c818c84a1ae27c87ad7bf0f1d015c8dfcc4db52a3747a24e6d68(
    notification_topic: _aws_cdk_aws_sns_889c7272.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd58edcd1450979b31c74df668ad381ca95565eab6ed55af0e93923b687fa6a(
    statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f080afe93f57c67a851672ad730fdb2732788d9bde3446f52ece72648a2b416(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c2d7e64d2730ceda26d685dbb4cbbda8132027e60ae55e66fd8ea1dab6db98(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_9b88bb94.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23826c80727ceab4bcf17b16e85ef31ecb627859bcb3acf755537b24c6952cb6(
    *,
    slack_channel_configuration_name: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    logging_level: typing.Optional[LoggingLevel] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_6c4320fb.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_logs_6c4320fb.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    notification_topics: typing.Optional[typing.Sequence[_aws_cdk_aws_sns_889c7272.ITopic]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass
