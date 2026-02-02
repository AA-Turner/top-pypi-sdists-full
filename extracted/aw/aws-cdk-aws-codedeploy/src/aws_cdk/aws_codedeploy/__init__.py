'''
# AWS CodeDeploy Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

AWS CodeDeploy is a deployment service that automates application deployments to
Amazon EC2 instances, on-premises instances, serverless Lambda functions, or
Amazon ECS services.

The CDK currently supports Amazon EC2, on-premise and AWS Lambda applications.

## EC2/on-premise Applications

To create a new CodeDeploy Application that deploys to EC2/on-premise instances:

```python
application = codedeploy.ServerApplication(self, "CodeDeployApplication",
    application_name="MyApplication"
)
```

To import an already existing Application:

```python
application = codedeploy.ServerApplication.from_server_application_name(self, "ExistingCodeDeployApplication", "MyExistingApplication")
```

## EC2/on-premise Deployment Groups

To create a new CodeDeploy Deployment Group that deploys to EC2/on-premise instances:

```python
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_cloudwatch as cloudwatch

# application: codedeploy.ServerApplication
# asg: autoscaling.AutoScalingGroup
# alarm: cloudwatch.Alarm

deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyDeploymentGroup",
    auto_scaling_groups=[asg],
    # adds User Data that installs the CodeDeploy agent on your auto-scaling groups hosts
    # default: true
    install_agent=True,
    # adds EC2 instances matching tags
    ec2_instance_tags=codedeploy.InstanceTagSet({
        # any instance with tags satisfying
        # key1=v1 or key1=v2 or key2 (any value) or value v3 (any key)
        # will match this group
        "key1": ["v1", "v2"],
        "key2": [],
        "": ["v3"]
    }),
    # adds on-premise instances matching tags
    on_premise_instance_tags=codedeploy.InstanceTagSet({
        "key1": ["v1", "v2"]
    }, {
        "key2": ["v3"]
    }),
    # CloudWatch alarms
    alarms=[alarm],
    # whether to ignore failure to fetch the status of alarms from CloudWatch
    # default: false
    ignore_poll_alarms_failure=False,
    # auto-rollback configuration
    auto_rollback=codedeploy.AutoRollbackConfig(
        failed_deployment=True,  # default: true
        stopped_deployment=True,  # default: false
        deployment_in_alarm=True
    )
)
```

All properties are optional - if you don't provide an Application,
one will be automatically created.

To import an already existing Deployment Group:

```python
# application: codedeploy.ServerApplication

deployment_group = codedeploy.ServerDeploymentGroup.from_server_deployment_group_attributes(self, "ExistingCodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyExistingDeploymentGroup"
)
```

### Load balancers

You can [specify a load balancer](https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html)
with the `loadBalancer` property when creating a Deployment Group.

`LoadBalancer` is an abstract class with static factory methods that allow you to create instances of it from various sources.

With Classic Elastic Load Balancer, you provide it directly:

```python
import aws_cdk.aws_elasticloadbalancing as elb

# lb: elb.LoadBalancer

lb.add_listener(
    external_port=80
)

deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
    load_balancer=codedeploy.LoadBalancer.classic(lb)
)
```

With Application Load Balancer or Network Load Balancer,
you provide a Target Group as the load balancer:

```python
import aws_cdk.aws_elasticloadbalancingv2 as elbv2

# alb: elbv2.ApplicationLoadBalancer

listener = alb.add_listener("Listener", port=80)
target_group = listener.add_targets("Fleet", port=80)

deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
    load_balancer=codedeploy.LoadBalancer.application(target_group)
)
```

## Deployment Configurations

You can also pass a Deployment Configuration when creating the Deployment Group:

```python
deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
    deployment_config=codedeploy.ServerDeploymentConfig.ALL_AT_ONCE
)
```

The default Deployment Configuration is `ServerDeploymentConfig.ONE_AT_A_TIME`.

You can also create a custom Deployment Configuration:

```python
deployment_config = codedeploy.ServerDeploymentConfig(self, "DeploymentConfiguration",
    deployment_config_name="MyDeploymentConfiguration",  # optional property
    # one of these is required, but both cannot be specified at the same time
    minimum_healthy_hosts=codedeploy.MinimumHealthyHosts.count(2)
)
```

Or import an existing one:

```python
deployment_config = codedeploy.ServerDeploymentConfig.from_server_deployment_config_name(self, "ExistingDeploymentConfiguration", "MyExistingDeploymentConfiguration")
```

## Lambda Applications

To create a new CodeDeploy Application that deploys to a Lambda function:

```python
application = codedeploy.LambdaApplication(self, "CodeDeployApplication",
    application_name="MyApplication"
)
```

To import an already existing Application:

```python
application = codedeploy.LambdaApplication.from_lambda_application_name(self, "ExistingCodeDeployApplication", "MyExistingApplication")
```

## Lambda Deployment Groups

To enable traffic shifting deployments for Lambda functions, CodeDeploy uses Lambda Aliases, which can balance incoming traffic between two different versions of your function.
Before deployment, the alias sends 100% of invokes to the version used in production.
When you publish a new version of the function to your stack, CodeDeploy will send a small percentage of traffic to the new version, monitor, and validate before shifting 100% of traffic to the new version.

To create a new CodeDeploy Deployment Group that deploys to a Lambda function:

```python
# my_application: codedeploy.LambdaApplication
# func: lambda.Function

version = func.current_version
version1_alias = lambda_.Alias(self, "alias",
    alias_name="prod",
    version=version
)

deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
    application=my_application,  # optional property: one will be created for you if not provided
    alias=version1_alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE
)
```

In order to deploy a new version of this function:

1. Reference the version with the latest changes `const version = func.currentVersion`.
2. Re-deploy the stack (this will trigger a deployment).
3. Monitor the CodeDeploy deployment as traffic shifts between the versions.

### Create a custom Deployment Config

CodeDeploy for Lambda comes with built-in configurations for traffic shifting.
If you want to specify your own strategy,
you can do so with the CustomLambdaDeploymentConfig construct,
letting you specify precisely how fast a new function version is deployed.

```python
# application: codedeploy.LambdaApplication
# alias: lambda.Alias
config = codedeploy.CustomLambdaDeploymentConfig(self, "CustomConfig",
    type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
    interval=Duration.minutes(1),
    percentage=5
)
deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
    application=application,
    alias=alias,
    deployment_config=config
)
```

You can specify a custom name for your deployment config, but if you do you will not be able to update the interval/percentage through CDK.

```python
config = codedeploy.CustomLambdaDeploymentConfig(self, "CustomConfig",
    type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
    interval=Duration.minutes(1),
    percentage=5,
    deployment_config_name="MyDeploymentConfig"
)
```

### Rollbacks and Alarms

CodeDeploy will roll back if the deployment fails. You can optionally trigger a rollback when one or more alarms are in a failed state:

```python
import aws_cdk.aws_cloudwatch as cloudwatch

# alias: lambda.Alias

# or add alarms to an existing group
# blue_green_alias: lambda.Alias

alarm = cloudwatch.Alarm(self, "Errors",
    comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
    threshold=1,
    evaluation_periods=1,
    metric=alias.metric_errors()
)
deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
    alias=alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
    alarms=[alarm
    ]
)
deployment_group.add_alarm(cloudwatch.Alarm(self, "BlueGreenErrors",
    comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
    threshold=1,
    evaluation_periods=1,
    metric=blue_green_alias.metric_errors()
))
```

### Pre and Post Hooks

CodeDeploy allows you to run an arbitrary Lambda function before traffic shifting actually starts (PreTraffic Hook) and after it completes (PostTraffic Hook).
With either hook, you have the opportunity to run logic that determines whether the deployment must succeed or fail.
For example, with PreTraffic hook you could run integration tests against the newly created Lambda version (but not serving traffic). With PostTraffic hook, you could run end-to-end validation checks.

```python
# warm_up_user_cache: lambda.Function
# end_to_end_validation: lambda.Function
# alias: lambda.Alias


# pass a hook whe creating the deployment group
deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
    alias=alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
    pre_hook=warm_up_user_cache
)

# or configure one on an existing deployment group
deployment_group.add_post_hook(end_to_end_validation)
```

### Import an existing Deployment Group

To import an already existing Deployment Group:

```python
# application: codedeploy.LambdaApplication

deployment_group = codedeploy.LambdaDeploymentGroup.from_lambda_deployment_group_attributes(self, "ExistingCodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyExistingDeploymentGroup"
)
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

import aws_cdk.aws_autoscaling as _aws_cdk_aws_autoscaling_92cc07a7
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_9b88bb94
import aws_cdk.aws_elasticloadbalancing as _aws_cdk_aws_elasticloadbalancing_976be337
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_e93c784f
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.AutoRollbackConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_in_alarm": "deploymentInAlarm",
        "failed_deployment": "failedDeployment",
        "stopped_deployment": "stoppedDeployment",
    },
)
class AutoRollbackConfig:
    def __init__(
        self,
        *,
        deployment_in_alarm: typing.Optional[builtins.bool] = None,
        failed_deployment: typing.Optional[builtins.bool] = None,
        stopped_deployment: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''The configuration for automatically rolling back deployments in a given Deployment Group.

        :param deployment_in_alarm: Whether to automatically roll back a deployment during which one of the configured CloudWatch alarms for this Deployment Group went off. Default: true if you've provided any Alarms with the ``alarms`` property, false otherwise
        :param failed_deployment: Whether to automatically roll back a deployment that fails. Default: true
        :param stopped_deployment: Whether to automatically roll back a deployment that was manually stopped. Default: false

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_autoscaling as autoscaling
            import aws_cdk.aws_cloudwatch as cloudwatch
            
            # application: codedeploy.ServerApplication
            # asg: autoscaling.AutoScalingGroup
            # alarm: cloudwatch.Alarm
            
            deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
                application=application,
                deployment_group_name="MyDeploymentGroup",
                auto_scaling_groups=[asg],
                # adds User Data that installs the CodeDeploy agent on your auto-scaling groups hosts
                # default: true
                install_agent=True,
                # adds EC2 instances matching tags
                ec2_instance_tags=codedeploy.InstanceTagSet({
                    # any instance with tags satisfying
                    # key1=v1 or key1=v2 or key2 (any value) or value v3 (any key)
                    # will match this group
                    "key1": ["v1", "v2"],
                    "key2": [],
                    "": ["v3"]
                }),
                # adds on-premise instances matching tags
                on_premise_instance_tags=codedeploy.InstanceTagSet({
                    "key1": ["v1", "v2"]
                }, {
                    "key2": ["v3"]
                }),
                # CloudWatch alarms
                alarms=[alarm],
                # whether to ignore failure to fetch the status of alarms from CloudWatch
                # default: false
                ignore_poll_alarms_failure=False,
                # auto-rollback configuration
                auto_rollback=codedeploy.AutoRollbackConfig(
                    failed_deployment=True,  # default: true
                    stopped_deployment=True,  # default: false
                    deployment_in_alarm=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605851913ed777aee04db2e3c374d7fe83f634585d1e95effc589bd736845166)
            check_type(argname="argument deployment_in_alarm", value=deployment_in_alarm, expected_type=type_hints["deployment_in_alarm"])
            check_type(argname="argument failed_deployment", value=failed_deployment, expected_type=type_hints["failed_deployment"])
            check_type(argname="argument stopped_deployment", value=stopped_deployment, expected_type=type_hints["stopped_deployment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_in_alarm is not None:
            self._values["deployment_in_alarm"] = deployment_in_alarm
        if failed_deployment is not None:
            self._values["failed_deployment"] = failed_deployment
        if stopped_deployment is not None:
            self._values["stopped_deployment"] = stopped_deployment

    @builtins.property
    def deployment_in_alarm(self) -> typing.Optional[builtins.bool]:
        '''Whether to automatically roll back a deployment during which one of the configured CloudWatch alarms for this Deployment Group went off.

        :default: true if you've provided any Alarms with the ``alarms`` property, false otherwise
        '''
        result = self._values.get("deployment_in_alarm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def failed_deployment(self) -> typing.Optional[builtins.bool]:
        '''Whether to automatically roll back a deployment that fails.

        :default: true
        '''
        result = self._values.get("failed_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stopped_deployment(self) -> typing.Optional[builtins.bool]:
        '''Whether to automatically roll back a deployment that was manually stopped.

        :default: false
        '''
        result = self._values.get("stopped_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoRollbackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.CfnApplication",
):
    '''A CloudFormation ``AWS::CodeDeploy::Application``.

    The ``AWS::CodeDeploy::Application`` resource creates an AWS CodeDeploy application. In CodeDeploy , an application is a name that functions as a container to ensure that the correct combination of revision, deployment configuration, and deployment group are referenced during a deployment. You can use the ``AWS::CodeDeploy::DeploymentGroup`` resource to associate the application with a CodeDeploy deployment group. For more information, see `CodeDeploy Deployments <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps.html>`_ in the *AWS CodeDeploy User Guide* .

    :cloudformationResource: AWS::CodeDeploy::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_codedeploy as codedeploy
        
        cfn_application = codedeploy.CfnApplication(self, "MyCfnApplication",
            application_name="applicationName",
            compute_platform="computePlatform",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeDeploy::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: A name for the application. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: Updates to ``ApplicationName`` are not supported.
        :param compute_platform: The compute platform that CodeDeploy deploys the application to.
        :param tags: The metadata that you apply to CodeDeploy applications to help you organize and categorize them. Each tag consists of a key and an optional value, both of which you define.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57070171a52dbcb8c8007b068e92610e76ea3736bf16da94bae78c926cd0adcb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            application_name=application_name,
            compute_platform=compute_platform,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f6849f15c9bdb611442d516d0f6b52593a57f70c5d2e288d16c43e495ac496)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e66640ebe0980baefbd22e3b5f35b2468aca6d1f282fd238cb8a2fb216645f9c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The metadata that you apply to CodeDeploy applications to help you organize and categorize them.

        Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> typing.Optional[builtins.str]:
        '''A name for the application.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           Updates to ``ApplicationName`` are not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036ddbacf10084fe8aeedbf98ed8f631ed6ff7b122d703b8e75f94b319f243a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The compute platform that CodeDeploy deploys the application to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computePlatform"))

    @compute_platform.setter
    def compute_platform(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cecb3429c262600af779d07124a8c383cfb8bae0037c1dfbce324ebc9e8e169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computePlatform", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "compute_platform": "computePlatform",
        "tags": "tags",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param application_name: A name for the application. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: Updates to ``ApplicationName`` are not supported.
        :param compute_platform: The compute platform that CodeDeploy deploys the application to.
        :param tags: The metadata that you apply to CodeDeploy applications to help you organize and categorize them. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codedeploy as codedeploy
            
            cfn_application_props = codedeploy.CfnApplicationProps(
                application_name="applicationName",
                compute_platform="computePlatform",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58d7b812cf377e04d7149ca17f0b92069a11575036f5a81b910127af7b77615a)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''A name for the application.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           Updates to ``ApplicationName`` are not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The compute platform that CodeDeploy deploys the application to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The metadata that you apply to CodeDeploy applications to help you organize and categorize them.

        Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDeploymentConfig(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig",
):
    '''A CloudFormation ``AWS::CodeDeploy::DeploymentConfig``.

    The ``AWS::CodeDeploy::DeploymentConfig`` resource creates a set of deployment rules, deployment success conditions, and deployment failure conditions that AWS CodeDeploy uses during a deployment. The deployment configuration specifies, through the use of a ``MinimumHealthyHosts`` value, the number or percentage of instances that must remain available at any time during a deployment.

    :cloudformationResource: AWS::CodeDeploy::DeploymentConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_codedeploy as codedeploy
        
        cfn_deployment_config = codedeploy.CfnDeploymentConfig(self, "MyCfnDeploymentConfig",
            compute_platform="computePlatform",
            deployment_config_name="deploymentConfigName",
            minimum_healthy_hosts=codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty(
                type="type",
                value=123
            ),
            traffic_routing_config=codedeploy.CfnDeploymentConfig.TrafficRoutingConfigProperty(
                type="type",
        
                # the properties below are optional
                time_based_canary=codedeploy.CfnDeploymentConfig.TimeBasedCanaryProperty(
                    canary_interval=123,
                    canary_percentage=123
                ),
                time_based_linear=codedeploy.CfnDeploymentConfig.TimeBasedLinearProperty(
                    linear_interval=123,
                    linear_percentage=123
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        compute_platform: typing.Optional[builtins.str] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        minimum_healthy_hosts: typing.Optional[typing.Union[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        traffic_routing_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentConfig.TrafficRoutingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeDeploy::DeploymentConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compute_platform: The destination platform type for the deployment ( ``Lambda`` , ``Server`` , or ``ECS`` ).
        :param deployment_config_name: A name for the deployment configuration. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the deployment configuration name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param minimum_healthy_hosts: The minimum number of healthy instances that should be available at any time during the deployment. There are two parameters expected in the input: type and value. The type parameter takes either of the following values: - HOST_COUNT: The value parameter represents the minimum number of healthy instances as an absolute value. - FLEET_PERCENT: The value parameter represents the minimum number of healthy instances as a percentage of the total number of instances in the deployment. If you specify FLEET_PERCENT, at the start of the deployment, AWS CodeDeploy converts the percentage to the equivalent number of instance and rounds up fractional instances. The value parameter takes an integer. For example, to set a minimum of 95% healthy instance, specify a type of FLEET_PERCENT and a value of 95. For more information about instance health, see `CodeDeploy Instance Health <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-health.html>`_ in the AWS CodeDeploy User Guide.
        :param traffic_routing_config: The configuration that specifies how the deployment traffic is routed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f1fc004e296fae6e27af576eecb11fed838de28169a83d7a45d7888b755cac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeploymentConfigProps(
            compute_platform=compute_platform,
            deployment_config_name=deployment_config_name,
            minimum_healthy_hosts=minimum_healthy_hosts,
            traffic_routing_config=traffic_routing_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef54e07197b0477f8a7ee45cb97dc1280eb2cfa4e087ce945a1c9f31dda83ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ada52b09cbd16bb11ba784bd5a704a890cccc4083c70314faf7913828a45ad91)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The destination platform type for the deployment ( ``Lambda`` , ``Server`` , or ``ECS`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-computeplatform
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computePlatform"))

    @compute_platform.setter
    def compute_platform(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5348b2627f88113b047f5ded63617f4e7e3f8e203e9d7e263bd10cdce7b2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computePlatform", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''A name for the deployment configuration.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the deployment configuration name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentConfigName"))

    @deployment_config_name.setter
    def deployment_config_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4dd14739bd1c9b089872d80465742d359387d9923b3174455eb151e1662217a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="minimumHealthyHosts")
    def minimum_healthy_hosts(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The minimum number of healthy instances that should be available at any time during the deployment.

        There are two parameters expected in the input: type and value.

        The type parameter takes either of the following values:

        - HOST_COUNT: The value parameter represents the minimum number of healthy instances as an absolute value.
        - FLEET_PERCENT: The value parameter represents the minimum number of healthy instances as a percentage of the total number of instances in the deployment. If you specify FLEET_PERCENT, at the start of the deployment, AWS CodeDeploy converts the percentage to the equivalent number of instance and rounds up fractional instances.

        The value parameter takes an integer.

        For example, to set a minimum of 95% healthy instance, specify a type of FLEET_PERCENT and a value of 95.

        For more information about instance health, see `CodeDeploy Instance Health <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-health.html>`_ in the AWS CodeDeploy User Guide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "minimumHealthyHosts"))

    @minimum_healthy_hosts.setter
    def minimum_healthy_hosts(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58087e08b52b1bf97151460b4a1dee1e057b8bbb688b9010467ffa2c6702790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumHealthyHosts", value)

    @builtins.property
    @jsii.member(jsii_name="trafficRoutingConfig")
    def traffic_routing_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentConfig.TrafficRoutingConfigProperty"]]:
        '''The configuration that specifies how the deployment traffic is routed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentConfig.TrafficRoutingConfigProperty"]], jsii.get(self, "trafficRoutingConfig"))

    @traffic_routing_config.setter
    def traffic_routing_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentConfig.TrafficRoutingConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9f1a5b5e2860f72b63c42ebf27eec7560dadeee919e3e5feedcd93f9ee26bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trafficRoutingConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class MinimumHealthyHostsProperty:
        def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
            '''``MinimumHealthyHosts`` is a property of the `DeploymentConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html>`_ resource that defines how many instances must remain healthy during an AWS CodeDeploy deployment.

            :param type: The minimum healthy instance type:. - HOST_COUNT: The minimum number of healthy instance as an absolute value. - FLEET_PERCENT: The minimum number of healthy instance as a percentage of the total number of instance in the deployment. In an example of nine instance, if a HOST_COUNT of six is specified, deploy to up to three instances at a time. The deployment is successful if six or more instances are deployed to successfully. Otherwise, the deployment fails. If a FLEET_PERCENT of 40 is specified, deploy to up to five instance at a time. The deployment is successful if four or more instance are deployed to successfully. Otherwise, the deployment fails. .. epigraph:: In a call to ``GetDeploymentConfig`` , CodeDeployDefault.OneAtATime returns a minimum healthy instance type of MOST_CONCURRENCY and a value of 1. This means a deployment to only one instance at a time. (You cannot set the type to MOST_CONCURRENCY, only to HOST_COUNT or FLEET_PERCENT.) In addition, with CodeDeployDefault.OneAtATime, AWS CodeDeploy attempts to ensure that all instances but one are kept in a healthy state during the deployment. Although this allows one instance at a time to be taken offline for a new deployment, it also means that if the deployment to the last instance fails, the overall deployment is still successful. For more information, see `AWS CodeDeploy Instance Health <https://docs.aws.amazon.com//codedeploy/latest/userguide/instances-health.html>`_ in the *AWS CodeDeploy User Guide* .
            :param value: The minimum healthy instance value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                minimum_healthy_hosts_property = codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__067c76eb1570e8ace61108a4926d15106ce2dfe743bbd2a27f81a90e2bd91edc)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''The minimum healthy instance type:.

            - HOST_COUNT: The minimum number of healthy instance as an absolute value.
            - FLEET_PERCENT: The minimum number of healthy instance as a percentage of the total number of instance in the deployment.

            In an example of nine instance, if a HOST_COUNT of six is specified, deploy to up to three instances at a time. The deployment is successful if six or more instances are deployed to successfully. Otherwise, the deployment fails. If a FLEET_PERCENT of 40 is specified, deploy to up to five instance at a time. The deployment is successful if four or more instance are deployed to successfully. Otherwise, the deployment fails.
            .. epigraph::

               In a call to ``GetDeploymentConfig`` , CodeDeployDefault.OneAtATime returns a minimum healthy instance type of MOST_CONCURRENCY and a value of 1. This means a deployment to only one instance at a time. (You cannot set the type to MOST_CONCURRENCY, only to HOST_COUNT or FLEET_PERCENT.) In addition, with CodeDeployDefault.OneAtATime, AWS CodeDeploy attempts to ensure that all instances but one are kept in a healthy state during the deployment. Although this allows one instance at a time to be taken offline for a new deployment, it also means that if the deployment to the last instance fails, the overall deployment is still successful.

            For more information, see `AWS CodeDeploy Instance Health <https://docs.aws.amazon.com//codedeploy/latest/userguide/instances-health.html>`_ in the *AWS CodeDeploy User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> jsii.Number:
            '''The minimum healthy instance value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MinimumHealthyHostsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig.TimeBasedCanaryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "canary_interval": "canaryInterval",
            "canary_percentage": "canaryPercentage",
        },
    )
    class TimeBasedCanaryProperty:
        def __init__(
            self,
            *,
            canary_interval: jsii.Number,
            canary_percentage: jsii.Number,
        ) -> None:
            '''A configuration that shifts traffic from one version of a Lambda function or Amazon ECS task set to another in two increments.

            The original and target Lambda function versions or ECS task sets are specified in the deployment's AppSpec file.

            :param canary_interval: The number of minutes between the first and second traffic shifts of a ``TimeBasedCanary`` deployment.
            :param canary_percentage: The percentage of traffic to shift in the first increment of a ``TimeBasedCanary`` deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedcanary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                time_based_canary_property = codedeploy.CfnDeploymentConfig.TimeBasedCanaryProperty(
                    canary_interval=123,
                    canary_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__050b52f4f9272ece28171329a0fadfa68ba88ea5ec4a9269c7c4468dd9596cc0)
                check_type(argname="argument canary_interval", value=canary_interval, expected_type=type_hints["canary_interval"])
                check_type(argname="argument canary_percentage", value=canary_percentage, expected_type=type_hints["canary_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "canary_interval": canary_interval,
                "canary_percentage": canary_percentage,
            }

        @builtins.property
        def canary_interval(self) -> jsii.Number:
            '''The number of minutes between the first and second traffic shifts of a ``TimeBasedCanary`` deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedcanary.html#cfn-codedeploy-deploymentconfig-timebasedcanary-canaryinterval
            '''
            result = self._values.get("canary_interval")
            assert result is not None, "Required property 'canary_interval' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def canary_percentage(self) -> jsii.Number:
            '''The percentage of traffic to shift in the first increment of a ``TimeBasedCanary`` deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedcanary.html#cfn-codedeploy-deploymentconfig-timebasedcanary-canarypercentage
            '''
            result = self._values.get("canary_percentage")
            assert result is not None, "Required property 'canary_percentage' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedCanaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig.TimeBasedLinearProperty",
        jsii_struct_bases=[],
        name_mapping={
            "linear_interval": "linearInterval",
            "linear_percentage": "linearPercentage",
        },
    )
    class TimeBasedLinearProperty:
        def __init__(
            self,
            *,
            linear_interval: jsii.Number,
            linear_percentage: jsii.Number,
        ) -> None:
            '''A configuration that shifts traffic from one version of a Lambda function or ECS task set to another in equal increments, with an equal number of minutes between each increment.

            The original and target Lambda function versions or ECS task sets are specified in the deployment's AppSpec file.

            :param linear_interval: The number of minutes between each incremental traffic shift of a ``TimeBasedLinear`` deployment.
            :param linear_percentage: The percentage of traffic that is shifted at the start of each increment of a ``TimeBasedLinear`` deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedlinear.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                time_based_linear_property = codedeploy.CfnDeploymentConfig.TimeBasedLinearProperty(
                    linear_interval=123,
                    linear_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83ec2fa88d9e338a88798602fff3be534859979c88ed5ae34ed05e0c34085c1d)
                check_type(argname="argument linear_interval", value=linear_interval, expected_type=type_hints["linear_interval"])
                check_type(argname="argument linear_percentage", value=linear_percentage, expected_type=type_hints["linear_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "linear_interval": linear_interval,
                "linear_percentage": linear_percentage,
            }

        @builtins.property
        def linear_interval(self) -> jsii.Number:
            '''The number of minutes between each incremental traffic shift of a ``TimeBasedLinear`` deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedlinear.html#cfn-codedeploy-deploymentconfig-timebasedlinear-linearinterval
            '''
            result = self._values.get("linear_interval")
            assert result is not None, "Required property 'linear_interval' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def linear_percentage(self) -> jsii.Number:
            '''The percentage of traffic that is shifted at the start of each increment of a ``TimeBasedLinear`` deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-timebasedlinear.html#cfn-codedeploy-deploymentconfig-timebasedlinear-linearpercentage
            '''
            result = self._values.get("linear_percentage")
            assert result is not None, "Required property 'linear_percentage' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedLinearProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig.TrafficRoutingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "time_based_canary": "timeBasedCanary",
            "time_based_linear": "timeBasedLinear",
        },
    )
    class TrafficRoutingConfigProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            time_based_canary: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentConfig.TimeBasedCanaryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            time_based_linear: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentConfig.TimeBasedLinearProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration that specifies how traffic is shifted from one version of a Lambda function to another version during an AWS Lambda deployment, or from one Amazon ECS task set to another during an Amazon ECS deployment.

            :param type: The type of traffic shifting ( ``TimeBasedCanary`` or ``TimeBasedLinear`` ) used by a deployment configuration.
            :param time_based_canary: A configuration that shifts traffic from one version of a Lambda function or ECS task set to another in two increments. The original and target Lambda function versions or ECS task sets are specified in the deployment's AppSpec file.
            :param time_based_linear: A configuration that shifts traffic from one version of a Lambda function or Amazon ECS task set to another in equal increments, with an equal number of minutes between each increment. The original and target Lambda function versions or Amazon ECS task sets are specified in the deployment's AppSpec file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-trafficroutingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                traffic_routing_config_property = codedeploy.CfnDeploymentConfig.TrafficRoutingConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    time_based_canary=codedeploy.CfnDeploymentConfig.TimeBasedCanaryProperty(
                        canary_interval=123,
                        canary_percentage=123
                    ),
                    time_based_linear=codedeploy.CfnDeploymentConfig.TimeBasedLinearProperty(
                        linear_interval=123,
                        linear_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__20c13213d6b7d84a46c3b432bf8a7f5b623ee5d4c5cd8725d239d40307224d8f)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument time_based_canary", value=time_based_canary, expected_type=type_hints["time_based_canary"])
                check_type(argname="argument time_based_linear", value=time_based_linear, expected_type=type_hints["time_based_linear"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if time_based_canary is not None:
                self._values["time_based_canary"] = time_based_canary
            if time_based_linear is not None:
                self._values["time_based_linear"] = time_based_linear

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of traffic shifting ( ``TimeBasedCanary`` or ``TimeBasedLinear`` ) used by a deployment configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-trafficroutingconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def time_based_canary(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentConfig.TimeBasedCanaryProperty"]]:
            '''A configuration that shifts traffic from one version of a Lambda function or ECS task set to another in two increments.

            The original and target Lambda function versions or ECS task sets are specified in the deployment's AppSpec file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-trafficroutingconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig-timebasedcanary
            '''
            result = self._values.get("time_based_canary")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentConfig.TimeBasedCanaryProperty"]], result)

        @builtins.property
        def time_based_linear(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentConfig.TimeBasedLinearProperty"]]:
            '''A configuration that shifts traffic from one version of a Lambda function or Amazon ECS task set to another in equal increments, with an equal number of minutes between each increment.

            The original and target Lambda function versions or Amazon ECS task sets are specified in the deployment's AppSpec file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-trafficroutingconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig-timebasedlinear
            '''
            result = self._values.get("time_based_linear")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentConfig.TimeBasedLinearProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrafficRoutingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_platform": "computePlatform",
        "deployment_config_name": "deploymentConfigName",
        "minimum_healthy_hosts": "minimumHealthyHosts",
        "traffic_routing_config": "trafficRoutingConfig",
    },
)
class CfnDeploymentConfigProps:
    def __init__(
        self,
        *,
        compute_platform: typing.Optional[builtins.str] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        minimum_healthy_hosts: typing.Optional[typing.Union[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        traffic_routing_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentConfig.TrafficRoutingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDeploymentConfig``.

        :param compute_platform: The destination platform type for the deployment ( ``Lambda`` , ``Server`` , or ``ECS`` ).
        :param deployment_config_name: A name for the deployment configuration. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the deployment configuration name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param minimum_healthy_hosts: The minimum number of healthy instances that should be available at any time during the deployment. There are two parameters expected in the input: type and value. The type parameter takes either of the following values: - HOST_COUNT: The value parameter represents the minimum number of healthy instances as an absolute value. - FLEET_PERCENT: The value parameter represents the minimum number of healthy instances as a percentage of the total number of instances in the deployment. If you specify FLEET_PERCENT, at the start of the deployment, AWS CodeDeploy converts the percentage to the equivalent number of instance and rounds up fractional instances. The value parameter takes an integer. For example, to set a minimum of 95% healthy instance, specify a type of FLEET_PERCENT and a value of 95. For more information about instance health, see `CodeDeploy Instance Health <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-health.html>`_ in the AWS CodeDeploy User Guide.
        :param traffic_routing_config: The configuration that specifies how the deployment traffic is routed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codedeploy as codedeploy
            
            cfn_deployment_config_props = codedeploy.CfnDeploymentConfigProps(
                compute_platform="computePlatform",
                deployment_config_name="deploymentConfigName",
                minimum_healthy_hosts=codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty(
                    type="type",
                    value=123
                ),
                traffic_routing_config=codedeploy.CfnDeploymentConfig.TrafficRoutingConfigProperty(
                    type="type",
            
                    # the properties below are optional
                    time_based_canary=codedeploy.CfnDeploymentConfig.TimeBasedCanaryProperty(
                        canary_interval=123,
                        canary_percentage=123
                    ),
                    time_based_linear=codedeploy.CfnDeploymentConfig.TimeBasedLinearProperty(
                        linear_interval=123,
                        linear_percentage=123
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e19ebdd6f3f4b5754c88f2a801ba3acad8eba9dd91abfd1df9601d18cb45b2b)
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
            check_type(argname="argument minimum_healthy_hosts", value=minimum_healthy_hosts, expected_type=type_hints["minimum_healthy_hosts"])
            check_type(argname="argument traffic_routing_config", value=traffic_routing_config, expected_type=type_hints["traffic_routing_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name
        if minimum_healthy_hosts is not None:
            self._values["minimum_healthy_hosts"] = minimum_healthy_hosts
        if traffic_routing_config is not None:
            self._values["traffic_routing_config"] = traffic_routing_config

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The destination platform type for the deployment ( ``Lambda`` , ``Server`` , or ``ECS`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-computeplatform
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''A name for the deployment configuration.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the deployment configuration name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_healthy_hosts(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The minimum number of healthy instances that should be available at any time during the deployment.

        There are two parameters expected in the input: type and value.

        The type parameter takes either of the following values:

        - HOST_COUNT: The value parameter represents the minimum number of healthy instances as an absolute value.
        - FLEET_PERCENT: The value parameter represents the minimum number of healthy instances as a percentage of the total number of instances in the deployment. If you specify FLEET_PERCENT, at the start of the deployment, AWS CodeDeploy converts the percentage to the equivalent number of instance and rounds up fractional instances.

        The value parameter takes an integer.

        For example, to set a minimum of 95% healthy instance, specify a type of FLEET_PERCENT and a value of 95.

        For more information about instance health, see `CodeDeploy Instance Health <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-health.html>`_ in the AWS CodeDeploy User Guide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        '''
        result = self._values.get("minimum_healthy_hosts")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def traffic_routing_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentConfig.TrafficRoutingConfigProperty]]:
        '''The configuration that specifies how the deployment traffic is routed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-trafficroutingconfig
        '''
        result = self._values.get("traffic_routing_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentConfig.TrafficRoutingConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDeploymentGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup",
):
    '''A CloudFormation ``AWS::CodeDeploy::DeploymentGroup``.

    The ``AWS::CodeDeploy::DeploymentGroup`` resource creates an AWS CodeDeploy deployment group that specifies which instances your application revisions are deployed to, along with other deployment options. For more information, see `CreateDeploymentGroup <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_CreateDeploymentGroup.html>`_ in the *CodeDeploy API Reference* .
    .. epigraph::

       Amazon ECS blue/green deployments through CodeDeploy do not use the ``AWS::CodeDeploy::DeploymentGroup`` resource. To perform Amazon ECS blue/green deployments, use the ``AWS::CodeDeploy::BlueGreen`` hook. See `Perform Amazon ECS blue/green deployments through CodeDeploy using AWS CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html>`_ for more information.

    :cloudformationResource: AWS::CodeDeploy::DeploymentGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_codedeploy as codedeploy
        
        cfn_deployment_group = codedeploy.CfnDeploymentGroup(self, "MyCfnDeploymentGroup",
            application_name="applicationName",
            service_role_arn="serviceRoleArn",
        
            # the properties below are optional
            alarm_configuration=codedeploy.CfnDeploymentGroup.AlarmConfigurationProperty(
                alarms=[codedeploy.CfnDeploymentGroup.AlarmProperty(
                    name="name"
                )],
                enabled=False,
                ignore_poll_alarm_failure=False
            ),
            auto_rollback_configuration=codedeploy.CfnDeploymentGroup.AutoRollbackConfigurationProperty(
                enabled=False,
                events=["events"]
            ),
            auto_scaling_groups=["autoScalingGroups"],
            blue_green_deployment_configuration=codedeploy.CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty(
                deployment_ready_option=codedeploy.CfnDeploymentGroup.DeploymentReadyOptionProperty(
                    action_on_timeout="actionOnTimeout",
                    wait_time_in_minutes=123
                ),
                green_fleet_provisioning_option=codedeploy.CfnDeploymentGroup.GreenFleetProvisioningOptionProperty(
                    action="action"
                ),
                terminate_blue_instances_on_deployment_success=codedeploy.CfnDeploymentGroup.BlueInstanceTerminationOptionProperty(
                    action="action",
                    termination_wait_time_in_minutes=123
                )
            ),
            deployment=codedeploy.CfnDeploymentGroup.DeploymentProperty(
                revision=codedeploy.CfnDeploymentGroup.RevisionLocationProperty(
                    git_hub_location=codedeploy.CfnDeploymentGroup.GitHubLocationProperty(
                        commit_id="commitId",
                        repository="repository"
                    ),
                    revision_type="revisionType",
                    s3_location=codedeploy.CfnDeploymentGroup.S3LocationProperty(
                        bucket="bucket",
                        key="key",
        
                        # the properties below are optional
                        bundle_type="bundleType",
                        e_tag="eTag",
                        version="version"
                    )
                ),
        
                # the properties below are optional
                description="description",
                ignore_application_stop_failures=False
            ),
            deployment_config_name="deploymentConfigName",
            deployment_group_name="deploymentGroupName",
            deployment_style=codedeploy.CfnDeploymentGroup.DeploymentStyleProperty(
                deployment_option="deploymentOption",
                deployment_type="deploymentType"
            ),
            ec2_tag_filters=[codedeploy.CfnDeploymentGroup.EC2TagFilterProperty(
                key="key",
                type="type",
                value="value"
            )],
            ec2_tag_set=codedeploy.CfnDeploymentGroup.EC2TagSetProperty(
                ec2_tag_set_list=[codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty(
                    ec2_tag_group=[codedeploy.CfnDeploymentGroup.EC2TagFilterProperty(
                        key="key",
                        type="type",
                        value="value"
                    )]
                )]
            ),
            ecs_services=[codedeploy.CfnDeploymentGroup.ECSServiceProperty(
                cluster_name="clusterName",
                service_name="serviceName"
            )],
            load_balancer_info=codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty(
                elb_info_list=[codedeploy.CfnDeploymentGroup.ELBInfoProperty(
                    name="name"
                )],
                target_group_info_list=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
                    name="name"
                )],
                target_group_pair_info_list=[codedeploy.CfnDeploymentGroup.TargetGroupPairInfoProperty(
                    prod_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                        listener_arns=["listenerArns"]
                    ),
                    target_groups=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
                        name="name"
                    )],
                    test_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                        listener_arns=["listenerArns"]
                    )
                )]
            ),
            on_premises_instance_tag_filters=[codedeploy.CfnDeploymentGroup.TagFilterProperty(
                key="key",
                type="type",
                value="value"
            )],
            on_premises_tag_set=codedeploy.CfnDeploymentGroup.OnPremisesTagSetProperty(
                on_premises_tag_set_list=[codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty(
                    on_premises_tag_group=[codedeploy.CfnDeploymentGroup.TagFilterProperty(
                        key="key",
                        type="type",
                        value="value"
                    )]
                )]
            ),
            outdated_instances_strategy="outdatedInstancesStrategy",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trigger_configurations=[codedeploy.CfnDeploymentGroup.TriggerConfigProperty(
                trigger_events=["triggerEvents"],
                trigger_name="triggerName",
                trigger_target_arn="triggerTargetArn"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_name: builtins.str,
        service_role_arn: builtins.str,
        alarm_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.AlarmConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_rollback_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.AutoRollbackConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_scaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        blue_green_deployment_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.DeploymentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.DeploymentStyleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ec2_tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.EC2TagSetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ecs_services: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.ECSServiceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        load_balancer_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.LoadBalancerInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        on_premises_instance_tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        on_premises_tag_set: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.OnPremisesTagSetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        outdated_instances_strategy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trigger_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.TriggerConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeDeploy::DeploymentGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: The name of an existing CodeDeploy application to associate this deployment group with.
        :param service_role_arn: A service role Amazon Resource Name (ARN) that grants CodeDeploy permission to make calls to AWS services on your behalf. For more information, see `Create a Service Role for AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-service-role.html>`_ in the *AWS CodeDeploy User Guide* . .. epigraph:: In some cases, you might need to add a dependency on the service role's policy. For more information, see IAM role policy in `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .
        :param alarm_configuration: Information about the Amazon CloudWatch alarms that are associated with the deployment group.
        :param auto_rollback_configuration: Information about the automatic rollback configuration that is associated with the deployment group. If you specify this property, don't specify the ``Deployment`` property.
        :param auto_scaling_groups: A list of associated Auto Scaling groups that CodeDeploy automatically deploys revisions to when new instances are created. Duplicates are not allowed.
        :param blue_green_deployment_configuration: Information about blue/green deployment options for a deployment group.
        :param deployment: The application revision to deploy to this deployment group. If you specify this property, your target application revision is deployed as soon as the provisioning process is complete. If you specify this property, don't specify the ``AutoRollbackConfiguration`` property.
        :param deployment_config_name: A deployment configuration name or a predefined configuration name. With predefined configurations, you can deploy application revisions to one instance at a time ( ``CodeDeployDefault.OneAtATime`` ), half of the instances at a time ( ``CodeDeployDefault.HalfAtATime`` ), or all the instances at once ( ``CodeDeployDefault.AllAtOnce`` ). For more information and valid values, see `Working with Deployment Configurations <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html>`_ in the *AWS CodeDeploy User Guide* .
        :param deployment_group_name: A name for the deployment group. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the deployment group name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param deployment_style: Attributes that determine the type of deployment to run and whether to route deployment traffic behind a load balancer. If you specify this property with a blue/green deployment type, don't specify the ``AutoScalingGroups`` , ``LoadBalancerInfo`` , or ``Deployment`` properties. .. epigraph:: For blue/green deployments, AWS CloudFormation supports deployments on Lambda compute platforms only. You can perform Amazon ECS blue/green deployments using ``AWS::CodeDeploy::BlueGreen`` hook. See `Perform Amazon ECS blue/green deployments through CodeDeploy using AWS CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html>`_ for more information.
        :param ec2_tag_filters: The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group. CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group. Duplicates are not allowed. You can specify ``EC2TagFilters`` or ``Ec2TagSet`` , but not both.
        :param ec2_tag_set: Information about groups of tags applied to Amazon EC2 instances. The deployment group includes only Amazon EC2 instances identified by all the tag groups. Cannot be used in the same call as ``ec2TagFilter`` .
        :param ecs_services: The target Amazon ECS services in the deployment group. This applies only to deployment groups that use the Amazon ECS compute platform. A target Amazon ECS service is specified as an Amazon ECS cluster and service name pair using the format ``<clustername>:<servicename>`` .
        :param load_balancer_info: Information about the load balancer to use in a deployment. For more information, see `Integrating CodeDeploy with Elastic Load Balancing <https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html>`_ in the *AWS CodeDeploy User Guide* .
        :param on_premises_instance_tag_filters: The on-premises instance tags already applied to on-premises instances that you want to include in the deployment group. CodeDeploy includes all on-premises instances identified by any of the tags you specify in this deployment group. To register on-premises instances with CodeDeploy , see `Working with On-Premises Instances for CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-on-premises.html>`_ in the *AWS CodeDeploy User Guide* . Duplicates are not allowed. You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.
        :param on_premises_tag_set: Information about groups of tags applied to on-premises instances. The deployment group includes only on-premises instances identified by all the tag groups. You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.
        :param outdated_instances_strategy: ``AWS::CodeDeploy::DeploymentGroup.OutdatedInstancesStrategy``.
        :param tags: ``AWS::CodeDeploy::DeploymentGroup.Tags``.
        :param trigger_configurations: Information about triggers associated with the deployment group. Duplicates are not allowed
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95d485a4928133eade6a5746d8b869f3e1eec126410c040e8a17b7927c8a977)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeploymentGroupProps(
            application_name=application_name,
            service_role_arn=service_role_arn,
            alarm_configuration=alarm_configuration,
            auto_rollback_configuration=auto_rollback_configuration,
            auto_scaling_groups=auto_scaling_groups,
            blue_green_deployment_configuration=blue_green_deployment_configuration,
            deployment=deployment,
            deployment_config_name=deployment_config_name,
            deployment_group_name=deployment_group_name,
            deployment_style=deployment_style,
            ec2_tag_filters=ec2_tag_filters,
            ec2_tag_set=ec2_tag_set,
            ecs_services=ecs_services,
            load_balancer_info=load_balancer_info,
            on_premises_instance_tag_filters=on_premises_instance_tag_filters,
            on_premises_tag_set=on_premises_tag_set,
            outdated_instances_strategy=outdated_instances_strategy,
            tags=tags,
            trigger_configurations=trigger_configurations,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e038f11d648429cc1962c39ff4f56fc3e85ba36217ca66ea4b78edd69cc479b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6867e67aeee5a75fa5d501ab2ffee05422bdc46d5095c98924f07a9b189753a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::CodeDeploy::DeploymentGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''The name of an existing CodeDeploy application to associate this deployment group with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39c582d1c2caee3f96b221093309f964e8d3e095332f5ffbf9b796cc6349325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        '''A service role Amazon Resource Name (ARN) that grants CodeDeploy permission to make calls to AWS services on your behalf.

        For more information, see `Create a Service Role for AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-service-role.html>`_ in the *AWS CodeDeploy User Guide* .
        .. epigraph::

           In some cases, you might need to add a dependency on the service role's policy. For more information, see IAM role policy in `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca3e28b31d1043e3516e03d7f3bfab87f3c200093722b8a744de19b139b0ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="alarmConfiguration")
    def alarm_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.AlarmConfigurationProperty"]]:
        '''Information about the Amazon CloudWatch alarms that are associated with the deployment group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.AlarmConfigurationProperty"]], jsii.get(self, "alarmConfiguration"))

    @alarm_configuration.setter
    def alarm_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.AlarmConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d00940baadfac660c47c9b837c4390f3ed8e30de5b9748cf11cdb2d9c9251a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfiguration")
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.AutoRollbackConfigurationProperty"]]:
        '''Information about the automatic rollback configuration that is associated with the deployment group.

        If you specify this property, don't specify the ``Deployment`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.AutoRollbackConfigurationProperty"]], jsii.get(self, "autoRollbackConfiguration"))

    @auto_rollback_configuration.setter
    def auto_rollback_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.AutoRollbackConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cca6d2eb3cfdf1d3492f0d0ad571471480bca384234889419a7c57a5384d5c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoRollbackConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of associated Auto Scaling groups that CodeDeploy automatically deploys revisions to when new instances are created.

        Duplicates are not allowed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "autoScalingGroups"))

    @auto_scaling_groups.setter
    def auto_scaling_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e609c28a5df074ac5b8f0e87ceb0e1620a04a75c58df16e8c8bcb482a70c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoScalingGroups", value)

    @builtins.property
    @jsii.member(jsii_name="blueGreenDeploymentConfiguration")
    def blue_green_deployment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty"]]:
        '''Information about blue/green deployment options for a deployment group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty"]], jsii.get(self, "blueGreenDeploymentConfiguration"))

    @blue_green_deployment_configuration.setter
    def blue_green_deployment_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc853ba4aefef735099fdc93b20025d3885a18938727c7bcbf58dfe98346f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blueGreenDeploymentConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.DeploymentProperty"]]:
        '''The application revision to deploy to this deployment group.

        If you specify this property, your target application revision is deployed as soon as the provisioning process is complete. If you specify this property, don't specify the ``AutoRollbackConfiguration`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.DeploymentProperty"]], jsii.get(self, "deployment"))

    @deployment.setter
    def deployment(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.DeploymentProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c37dd51dfc99e4b3c20e0f4864aa6501e1c741122524b87cd25dc261da86010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployment", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''A deployment configuration name or a predefined configuration name.

        With predefined configurations, you can deploy application revisions to one instance at a time ( ``CodeDeployDefault.OneAtATime`` ), half of the instances at a time ( ``CodeDeployDefault.HalfAtATime`` ), or all the instances at once ( ``CodeDeployDefault.AllAtOnce`` ). For more information and valid values, see `Working with Deployment Configurations <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html>`_ in the *AWS CodeDeploy User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentConfigName"))

    @deployment_config_name.setter
    def deployment_config_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8eb3ae1c9b54eea4f388aad8be7102e30b3cf69c4f3a3a029b7dd5c6600458e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''A name for the deployment group.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the deployment group name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentGroupName"))

    @deployment_group_name.setter
    def deployment_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d70dc9848ed6202f0ce82ec76e2c252552dbfe8abb3293de90447b44fadcce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentStyle")
    def deployment_style(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.DeploymentStyleProperty"]]:
        '''Attributes that determine the type of deployment to run and whether to route deployment traffic behind a load balancer.

        If you specify this property with a blue/green deployment type, don't specify the ``AutoScalingGroups`` , ``LoadBalancerInfo`` , or ``Deployment`` properties.
        .. epigraph::

           For blue/green deployments, AWS CloudFormation supports deployments on Lambda compute platforms only. You can perform Amazon ECS blue/green deployments using ``AWS::CodeDeploy::BlueGreen`` hook. See `Perform Amazon ECS blue/green deployments through CodeDeploy using AWS CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html>`_ for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.DeploymentStyleProperty"]], jsii.get(self, "deploymentStyle"))

    @deployment_style.setter
    def deployment_style(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.DeploymentStyleProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7a3736c71edfbfa61d8e29da612add92a505b233cb16df24d3d6ef9bcc1619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentStyle", value)

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilters")
    def ec2_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]]:
        '''The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group.

        CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group. Duplicates are not allowed.

        You can specify ``EC2TagFilters`` or ``Ec2TagSet`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]], jsii.get(self, "ec2TagFilters"))

    @ec2_tag_filters.setter
    def ec2_tag_filters(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316af0ae6ee1665191c52a9898322d517e413c26f933cc0a1648ee7a3ab3f06e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2TagFilters", value)

    @builtins.property
    @jsii.member(jsii_name="ec2TagSet")
    def ec2_tag_set(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagSetProperty"]]:
        '''Information about groups of tags applied to Amazon EC2 instances.

        The deployment group includes only Amazon EC2 instances identified by all the tag groups. Cannot be used in the same call as ``ec2TagFilter`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagSetProperty"]], jsii.get(self, "ec2TagSet"))

    @ec2_tag_set.setter
    def ec2_tag_set(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagSetProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b830a6718978d7143c40a2e722c089de1553c73a1edcad7370e665e9f8a4ea16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2TagSet", value)

    @builtins.property
    @jsii.member(jsii_name="ecsServices")
    def ecs_services(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.ECSServiceProperty"]]]]:
        '''The target Amazon ECS services in the deployment group.

        This applies only to deployment groups that use the Amazon ECS compute platform. A target Amazon ECS service is specified as an Amazon ECS cluster and service name pair using the format ``<clustername>:<servicename>`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ecsservices
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.ECSServiceProperty"]]]], jsii.get(self, "ecsServices"))

    @ecs_services.setter
    def ecs_services(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.ECSServiceProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68842caab6c87e2eddf975b8ea0dc2e17e79972f26fc536fcdc0fc1a16ef3129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecsServices", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInfo")
    def load_balancer_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.LoadBalancerInfoProperty"]]:
        '''Information about the load balancer to use in a deployment.

        For more information, see `Integrating CodeDeploy with Elastic Load Balancing <https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html>`_ in the *AWS CodeDeploy User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.LoadBalancerInfoProperty"]], jsii.get(self, "loadBalancerInfo"))

    @load_balancer_info.setter
    def load_balancer_info(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.LoadBalancerInfoProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a847944247bd7d95118b7ce5e95c3be1902d4041d0cd2b3e7a83f275ff36d181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerInfo", value)

    @builtins.property
    @jsii.member(jsii_name="onPremisesInstanceTagFilters")
    def on_premises_instance_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]]:
        '''The on-premises instance tags already applied to on-premises instances that you want to include in the deployment group.

        CodeDeploy includes all on-premises instances identified by any of the tags you specify in this deployment group. To register on-premises instances with CodeDeploy , see `Working with On-Premises Instances for CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-on-premises.html>`_ in the *AWS CodeDeploy User Guide* . Duplicates are not allowed.

        You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]], jsii.get(self, "onPremisesInstanceTagFilters"))

    @on_premises_instance_tag_filters.setter
    def on_premises_instance_tag_filters(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08756510974482c0f196ae15eda8a4d5f03856707e74f2d253c435eda61bd4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremisesInstanceTagFilters", value)

    @builtins.property
    @jsii.member(jsii_name="onPremisesTagSet")
    def on_premises_tag_set(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.OnPremisesTagSetProperty"]]:
        '''Information about groups of tags applied to on-premises instances.

        The deployment group includes only on-premises instances identified by all the tag groups.

        You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.OnPremisesTagSetProperty"]], jsii.get(self, "onPremisesTagSet"))

    @on_premises_tag_set.setter
    def on_premises_tag_set(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.OnPremisesTagSetProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077a2fd4e7ccd378baf86d8f8b24361b2c638ce1df4ceffd833f2a6cd277aba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremisesTagSet", value)

    @builtins.property
    @jsii.member(jsii_name="outdatedInstancesStrategy")
    def outdated_instances_strategy(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::DeploymentGroup.OutdatedInstancesStrategy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-outdatedinstancesstrategy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outdatedInstancesStrategy"))

    @outdated_instances_strategy.setter
    def outdated_instances_strategy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28169e8766e476263e1d44dbd0fe172c026dbcef4f49f465261fd17aa1b5cb4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outdatedInstancesStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="triggerConfigurations")
    def trigger_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TriggerConfigProperty"]]]]:
        '''Information about triggers associated with the deployment group.

        Duplicates are not allowed

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TriggerConfigProperty"]]]], jsii.get(self, "triggerConfigurations"))

    @trigger_configurations.setter
    def trigger_configurations(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TriggerConfigProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b0a771fd74097c279e0b5b97cc323e6dceaf400e4a14d6d9fefba01366f08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerConfigurations", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AlarmConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarms": "alarms",
            "enabled": "enabled",
            "ignore_poll_alarm_failure": "ignorePollAlarmFailure",
        },
    )
    class AlarmConfigurationProperty:
        def __init__(
            self,
            *,
            alarms: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.AlarmProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''The ``AlarmConfiguration`` property type configures CloudWatch alarms for an AWS CodeDeploy deployment group.

            ``AlarmConfiguration`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource.

            :param alarms: A list of alarms configured for the deployment or deployment group. A maximum of 10 alarms can be added.
            :param enabled: Indicates whether the alarm configuration is enabled.
            :param ignore_poll_alarm_failure: Indicates whether a deployment should continue if information about the current state of alarms cannot be retrieved from Amazon CloudWatch . The default value is ``false`` . - ``true`` : The deployment proceeds even if alarm status information can't be retrieved from CloudWatch . - ``false`` : The deployment stops if alarm status information can't be retrieved from CloudWatch .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                alarm_configuration_property = codedeploy.CfnDeploymentGroup.AlarmConfigurationProperty(
                    alarms=[codedeploy.CfnDeploymentGroup.AlarmProperty(
                        name="name"
                    )],
                    enabled=False,
                    ignore_poll_alarm_failure=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3c8c62dcf61aa9385b775f860ad9636fcfc138e3250a98cddd0e62f322727ce)
                check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument ignore_poll_alarm_failure", value=ignore_poll_alarm_failure, expected_type=type_hints["ignore_poll_alarm_failure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarms is not None:
                self._values["alarms"] = alarms
            if enabled is not None:
                self._values["enabled"] = enabled
            if ignore_poll_alarm_failure is not None:
                self._values["ignore_poll_alarm_failure"] = ignore_poll_alarm_failure

        @builtins.property
        def alarms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.AlarmProperty"]]]]:
            '''A list of alarms configured for the deployment or deployment group.

            A maximum of 10 alarms can be added.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-alarms
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.AlarmProperty"]]]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the alarm configuration is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def ignore_poll_alarm_failure(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether a deployment should continue if information about the current state of alarms cannot be retrieved from Amazon CloudWatch .

            The default value is ``false`` .

            - ``true`` : The deployment proceeds even if alarm status information can't be retrieved from CloudWatch .
            - ``false`` : The deployment stops if alarm status information can't be retrieved from CloudWatch .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-ignorepollalarmfailure
            '''
            result = self._values.get("ignore_poll_alarm_failure")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AlarmProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class AlarmProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The ``Alarm`` property type specifies a CloudWatch alarm to use for an AWS CodeDeploy deployment group.

            The ``Alarm`` property of the `CodeDeploy DeploymentGroup AlarmConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html>`_ property contains a list of ``Alarm`` property types.

            :param name: The name of the alarm. Maximum length is 255 characters. Each alarm name can be used only once in a list of alarms.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                alarm_property = codedeploy.CfnDeploymentGroup.AlarmProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45193bd8a7ece69b47f0ba563bdfdc61466d988183dae6f3faef1e710a15ad78)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the alarm.

            Maximum length is 255 characters. Each alarm name can be used only once in a list of alarms.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html#cfn-codedeploy-deploymentgroup-alarm-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AutoRollbackConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "events": "events"},
    )
    class AutoRollbackConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            events: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``AutoRollbackConfiguration`` property type configures automatic rollback for an AWS CodeDeploy deployment group when a deployment is not completed successfully.

            For more information, see `Automatic Rollbacks <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html#deployments-rollback-and-redeploy-automatic-rollbacks>`_ in the *AWS CodeDeploy User Guide* .

            ``AutoRollbackConfiguration`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource.

            :param enabled: Indicates whether a defined automatic rollback configuration is currently enabled.
            :param events: The event type or types that trigger a rollback. Valid values are ``DEPLOYMENT_FAILURE`` , ``DEPLOYMENT_STOP_ON_ALARM`` , or ``DEPLOYMENT_STOP_ON_REQUEST`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                auto_rollback_configuration_property = codedeploy.CfnDeploymentGroup.AutoRollbackConfigurationProperty(
                    enabled=False,
                    events=["events"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a0a738bad235b2c4aa8ec9bdd9b7c9ba60435bbdf583d0474ca8d0c9c9bf115)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether a defined automatic rollback configuration is currently enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The event type or types that trigger a rollback.

            Valid values are ``DEPLOYMENT_FAILURE`` , ``DEPLOYMENT_STOP_ON_ALARM`` , or ``DEPLOYMENT_STOP_ON_REQUEST`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoRollbackConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_ready_option": "deploymentReadyOption",
            "green_fleet_provisioning_option": "greenFleetProvisioningOption",
            "terminate_blue_instances_on_deployment_success": "terminateBlueInstancesOnDeploymentSuccess",
        },
    )
    class BlueGreenDeploymentConfigurationProperty:
        def __init__(
            self,
            *,
            deployment_ready_option: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.DeploymentReadyOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            green_fleet_provisioning_option: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.GreenFleetProvisioningOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.BlueInstanceTerminationOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about blue/green deployment options for a deployment group.

            :param deployment_ready_option: Information about the action to take when newly provisioned instances are ready to receive traffic in a blue/green deployment.
            :param green_fleet_provisioning_option: Information about how instances are provisioned for a replacement environment in a blue/green deployment.
            :param terminate_blue_instances_on_deployment_success: Information about whether to terminate instances in the original fleet during a blue/green deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-bluegreendeploymentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                blue_green_deployment_configuration_property = codedeploy.CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty(
                    deployment_ready_option=codedeploy.CfnDeploymentGroup.DeploymentReadyOptionProperty(
                        action_on_timeout="actionOnTimeout",
                        wait_time_in_minutes=123
                    ),
                    green_fleet_provisioning_option=codedeploy.CfnDeploymentGroup.GreenFleetProvisioningOptionProperty(
                        action="action"
                    ),
                    terminate_blue_instances_on_deployment_success=codedeploy.CfnDeploymentGroup.BlueInstanceTerminationOptionProperty(
                        action="action",
                        termination_wait_time_in_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__750b2a264d6615f1fe1caf8f5b2183c0a93dede85e2ff87a46665bb958a82c83)
                check_type(argname="argument deployment_ready_option", value=deployment_ready_option, expected_type=type_hints["deployment_ready_option"])
                check_type(argname="argument green_fleet_provisioning_option", value=green_fleet_provisioning_option, expected_type=type_hints["green_fleet_provisioning_option"])
                check_type(argname="argument terminate_blue_instances_on_deployment_success", value=terminate_blue_instances_on_deployment_success, expected_type=type_hints["terminate_blue_instances_on_deployment_success"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_ready_option is not None:
                self._values["deployment_ready_option"] = deployment_ready_option
            if green_fleet_provisioning_option is not None:
                self._values["green_fleet_provisioning_option"] = green_fleet_provisioning_option
            if terminate_blue_instances_on_deployment_success is not None:
                self._values["terminate_blue_instances_on_deployment_success"] = terminate_blue_instances_on_deployment_success

        @builtins.property
        def deployment_ready_option(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.DeploymentReadyOptionProperty"]]:
            '''Information about the action to take when newly provisioned instances are ready to receive traffic in a blue/green deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-bluegreendeploymentconfiguration.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-deploymentreadyoption
            '''
            result = self._values.get("deployment_ready_option")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.DeploymentReadyOptionProperty"]], result)

        @builtins.property
        def green_fleet_provisioning_option(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.GreenFleetProvisioningOptionProperty"]]:
            '''Information about how instances are provisioned for a replacement environment in a blue/green deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-bluegreendeploymentconfiguration.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-greenfleetprovisioningoption
            '''
            result = self._values.get("green_fleet_provisioning_option")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.GreenFleetProvisioningOptionProperty"]], result)

        @builtins.property
        def terminate_blue_instances_on_deployment_success(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.BlueInstanceTerminationOptionProperty"]]:
            '''Information about whether to terminate instances in the original fleet during a blue/green deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-bluegreendeploymentconfiguration.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-terminateblueinstancesondeploymentsuccess
            '''
            result = self._values.get("terminate_blue_instances_on_deployment_success")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.BlueInstanceTerminationOptionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlueGreenDeploymentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.BlueInstanceTerminationOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "termination_wait_time_in_minutes": "terminationWaitTimeInMinutes",
        },
    )
    class BlueInstanceTerminationOptionProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about whether instances in the original environment are terminated when a blue/green deployment is successful.

            ``BlueInstanceTerminationOption`` does not apply to Lambda deployments.

            :param action: The action to take on instances in the original environment after a successful blue/green deployment. - ``TERMINATE`` : Instances are terminated after a specified wait time. - ``KEEP_ALIVE`` : Instances are left running after they are deregistered from the load balancer and removed from the deployment group.
            :param termination_wait_time_in_minutes: For an Amazon EC2 deployment, the number of minutes to wait after a successful blue/green deployment before terminating instances from the original environment. For an Amazon ECS deployment, the number of minutes before deleting the original (blue) task set. During an Amazon ECS deployment, CodeDeploy shifts traffic from the original (blue) task set to a replacement (green) task set. The maximum setting is 2880 minutes (2 days).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-blueinstanceterminationoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                blue_instance_termination_option_property = codedeploy.CfnDeploymentGroup.BlueInstanceTerminationOptionProperty(
                    action="action",
                    termination_wait_time_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5bbc5dcf0d68a7b9226f773453a766a7ab513891a0b212d40fb4902039c3e212)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument termination_wait_time_in_minutes", value=termination_wait_time_in_minutes, expected_type=type_hints["termination_wait_time_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if termination_wait_time_in_minutes is not None:
                self._values["termination_wait_time_in_minutes"] = termination_wait_time_in_minutes

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to take on instances in the original environment after a successful blue/green deployment.

            - ``TERMINATE`` : Instances are terminated after a specified wait time.
            - ``KEEP_ALIVE`` : Instances are left running after they are deregistered from the load balancer and removed from the deployment group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-blueinstanceterminationoption.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-blueinstanceterminationoption-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def termination_wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''For an Amazon EC2 deployment, the number of minutes to wait after a successful blue/green deployment before terminating instances from the original environment.

            For an Amazon ECS deployment, the number of minutes before deleting the original (blue) task set. During an Amazon ECS deployment, CodeDeploy shifts traffic from the original (blue) task set to a replacement (green) task set.

            The maximum setting is 2880 minutes (2 days).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-blueinstanceterminationoption.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-blueinstanceterminationoption-terminationwaittimeinminutes
            '''
            result = self._values.get("termination_wait_time_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlueInstanceTerminationOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.DeploymentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "revision": "revision",
            "description": "description",
            "ignore_application_stop_failures": "ignoreApplicationStopFailures",
        },
    )
    class DeploymentProperty:
        def __init__(
            self,
            *,
            revision: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.RevisionLocationProperty", typing.Dict[builtins.str, typing.Any]]],
            description: typing.Optional[builtins.str] = None,
            ignore_application_stop_failures: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''``Deployment`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource that specifies an AWS CodeDeploy application revision to be deployed to instances in the deployment group. If you specify an application revision, your target revision is deployed as soon as the provisioning process is complete.

            :param revision: Information about the location of stored application artifacts and the service from which to retrieve them.
            :param description: A comment about the deployment.
            :param ignore_application_stop_failures: If true, then if an ``ApplicationStop`` , ``BeforeBlockTraffic`` , or ``AfterBlockTraffic`` deployment lifecycle event to an instance fails, then the deployment continues to the next deployment lifecycle event. For example, if ``ApplicationStop`` fails, the deployment continues with DownloadBundle. If ``BeforeBlockTraffic`` fails, the deployment continues with ``BlockTraffic`` . If ``AfterBlockTraffic`` fails, the deployment continues with ``ApplicationStop`` . If false or not specified, then if a lifecycle event fails during a deployment to an instance, that deployment fails. If deployment to that instance is part of an overall deployment and the number of healthy hosts is not less than the minimum number of healthy hosts, then a deployment to the next instance is attempted. During a deployment, the AWS CodeDeploy agent runs the scripts specified for ``ApplicationStop`` , ``BeforeBlockTraffic`` , and ``AfterBlockTraffic`` in the AppSpec file from the previous successful deployment. (All other scripts are run from the AppSpec file in the current deployment.) If one of these scripts contains an error and does not run successfully, the deployment can fail. If the cause of the failure is a script from the last successful deployment that will never run successfully, create a new deployment and use ``ignoreApplicationStopFailures`` to specify that the ``ApplicationStop`` , ``BeforeBlockTraffic`` , and ``AfterBlockTraffic`` failures should be ignored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                deployment_property = codedeploy.CfnDeploymentGroup.DeploymentProperty(
                    revision=codedeploy.CfnDeploymentGroup.RevisionLocationProperty(
                        git_hub_location=codedeploy.CfnDeploymentGroup.GitHubLocationProperty(
                            commit_id="commitId",
                            repository="repository"
                        ),
                        revision_type="revisionType",
                        s3_location=codedeploy.CfnDeploymentGroup.S3LocationProperty(
                            bucket="bucket",
                            key="key",
                
                            # the properties below are optional
                            bundle_type="bundleType",
                            e_tag="eTag",
                            version="version"
                        )
                    ),
                
                    # the properties below are optional
                    description="description",
                    ignore_application_stop_failures=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c9e7f9793c200e263c0ca670579df13092f8ced397fad8a6d272a8cefd7401d)
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument ignore_application_stop_failures", value=ignore_application_stop_failures, expected_type=type_hints["ignore_application_stop_failures"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "revision": revision,
            }
            if description is not None:
                self._values["description"] = description
            if ignore_application_stop_failures is not None:
                self._values["ignore_application_stop_failures"] = ignore_application_stop_failures

        @builtins.property
        def revision(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.RevisionLocationProperty"]:
            '''Information about the location of stored application artifacts and the service from which to retrieve them.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision
            '''
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.RevisionLocationProperty"], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A comment about the deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ignore_application_stop_failures(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If true, then if an ``ApplicationStop`` , ``BeforeBlockTraffic`` , or ``AfterBlockTraffic`` deployment lifecycle event to an instance fails, then the deployment continues to the next deployment lifecycle event.

            For example, if ``ApplicationStop`` fails, the deployment continues with DownloadBundle. If ``BeforeBlockTraffic`` fails, the deployment continues with ``BlockTraffic`` . If ``AfterBlockTraffic`` fails, the deployment continues with ``ApplicationStop`` .

            If false or not specified, then if a lifecycle event fails during a deployment to an instance, that deployment fails. If deployment to that instance is part of an overall deployment and the number of healthy hosts is not less than the minimum number of healthy hosts, then a deployment to the next instance is attempted.

            During a deployment, the AWS CodeDeploy agent runs the scripts specified for ``ApplicationStop`` , ``BeforeBlockTraffic`` , and ``AfterBlockTraffic`` in the AppSpec file from the previous successful deployment. (All other scripts are run from the AppSpec file in the current deployment.) If one of these scripts contains an error and does not run successfully, the deployment can fail.

            If the cause of the failure is a script from the last successful deployment that will never run successfully, create a new deployment and use ``ignoreApplicationStopFailures`` to specify that the ``ApplicationStop`` , ``BeforeBlockTraffic`` , and ``AfterBlockTraffic`` failures should be ignored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-ignoreapplicationstopfailures
            '''
            result = self._values.get("ignore_application_stop_failures")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.DeploymentReadyOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_on_timeout": "actionOnTimeout",
            "wait_time_in_minutes": "waitTimeInMinutes",
        },
    )
    class DeploymentReadyOptionProperty:
        def __init__(
            self,
            *,
            action_on_timeout: typing.Optional[builtins.str] = None,
            wait_time_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about how traffic is rerouted to instances in a replacement environment in a blue/green deployment.

            :param action_on_timeout: Information about when to reroute traffic from an original environment to a replacement environment in a blue/green deployment. - CONTINUE_DEPLOYMENT: Register new instances with the load balancer immediately after the new application revision is installed on the instances in the replacement environment. - STOP_DEPLOYMENT: Do not register new instances with a load balancer unless traffic rerouting is started using `ContinueDeployment <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_ContinueDeployment.html>`_ . If traffic rerouting is not started before the end of the specified wait period, the deployment status is changed to Stopped.
            :param wait_time_in_minutes: The number of minutes to wait before the status of a blue/green deployment is changed to Stopped if rerouting is not started manually. Applies only to the ``STOP_DEPLOYMENT`` option for ``actionOnTimeout`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentreadyoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                deployment_ready_option_property = codedeploy.CfnDeploymentGroup.DeploymentReadyOptionProperty(
                    action_on_timeout="actionOnTimeout",
                    wait_time_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37cb709bfd169e790006ffdc2a15548b968a024ff825f6f5925e15c70ecd68f2)
                check_type(argname="argument action_on_timeout", value=action_on_timeout, expected_type=type_hints["action_on_timeout"])
                check_type(argname="argument wait_time_in_minutes", value=wait_time_in_minutes, expected_type=type_hints["wait_time_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action_on_timeout is not None:
                self._values["action_on_timeout"] = action_on_timeout
            if wait_time_in_minutes is not None:
                self._values["wait_time_in_minutes"] = wait_time_in_minutes

        @builtins.property
        def action_on_timeout(self) -> typing.Optional[builtins.str]:
            '''Information about when to reroute traffic from an original environment to a replacement environment in a blue/green deployment.

            - CONTINUE_DEPLOYMENT: Register new instances with the load balancer immediately after the new application revision is installed on the instances in the replacement environment.
            - STOP_DEPLOYMENT: Do not register new instances with a load balancer unless traffic rerouting is started using `ContinueDeployment <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_ContinueDeployment.html>`_ . If traffic rerouting is not started before the end of the specified wait period, the deployment status is changed to Stopped.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentreadyoption.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-deploymentreadyoption-actionontimeout
            '''
            result = self._values.get("action_on_timeout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The number of minutes to wait before the status of a blue/green deployment is changed to Stopped if rerouting is not started manually.

            Applies only to the ``STOP_DEPLOYMENT`` option for ``actionOnTimeout`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentreadyoption.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-deploymentreadyoption-waittimeinminutes
            '''
            result = self._values.get("wait_time_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentReadyOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.DeploymentStyleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_option": "deploymentOption",
            "deployment_type": "deploymentType",
        },
    )
    class DeploymentStyleProperty:
        def __init__(
            self,
            *,
            deployment_option: typing.Optional[builtins.str] = None,
            deployment_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the type of deployment, either in-place or blue/green, you want to run and whether to route deployment traffic behind a load balancer.

            :param deployment_option: Indicates whether to route deployment traffic behind a load balancer. .. epigraph:: An Amazon EC2 Application Load Balancer or Network Load Balancer is required for an Amazon ECS deployment.
            :param deployment_type: Indicates whether to run an in-place or blue/green deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                deployment_style_property = codedeploy.CfnDeploymentGroup.DeploymentStyleProperty(
                    deployment_option="deploymentOption",
                    deployment_type="deploymentType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aec5c208fef39c240620a9a796e7caece22751adedcf1dd71ebd1bd586b23b4d)
                check_type(argname="argument deployment_option", value=deployment_option, expected_type=type_hints["deployment_option"])
                check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_option is not None:
                self._values["deployment_option"] = deployment_option
            if deployment_type is not None:
                self._values["deployment_type"] = deployment_type

        @builtins.property
        def deployment_option(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to route deployment traffic behind a load balancer.

            .. epigraph::

               An Amazon EC2 Application Load Balancer or Network Load Balancer is required for an Amazon ECS deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymentoption
            '''
            result = self._values.get("deployment_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def deployment_type(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to run an in-place or blue/green deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymenttype
            '''
            result = self._values.get("deployment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentStyleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type", "value": "value"},
    )
    class EC2TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about an Amazon EC2 tag filter.

            For more information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ in the *AWS CodeDeploy User Guide* .

            :param key: The tag filter key.
            :param type: The tag filter type:. - ``KEY_ONLY`` : Key only. - ``VALUE_ONLY`` : Value only. - ``KEY_AND_VALUE`` : Key and value.
            :param value: The tag filter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                e_c2_tag_filter_property = codedeploy.CfnDeploymentGroup.EC2TagFilterProperty(
                    key="key",
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eacd8ee63f774a8946719ed0af134a9e27d2a1baf50ea2836b900186354a92b4)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag filter key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The tag filter type:.

            - ``KEY_ONLY`` : Key only.
            - ``VALUE_ONLY`` : Value only.
            - ``KEY_AND_VALUE`` : Key and value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag filter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"ec2_tag_group": "ec2TagGroup"},
    )
    class EC2TagSetListObjectProperty:
        def __init__(
            self,
            *,
            ec2_tag_group: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``EC2TagSet`` property type specifies information about groups of tags applied to Amazon EC2 instances.

            The deployment group includes only Amazon EC2 instances identified by all the tag groups. Cannot be used in the same template as EC2TagFilters.

            For more information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ in the *AWS CodeDeploy User Guide* .

            ``EC2TagSet`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource type.

            :param ec2_tag_group: A list that contains other lists of Amazon EC2 instance tag groups. For an instance to be included in the deployment group, it must be identified by all of the tag groups in the list.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                e_c2_tag_set_list_object_property = codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty(
                    ec2_tag_group=[codedeploy.CfnDeploymentGroup.EC2TagFilterProperty(
                        key="key",
                        type="type",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8eb5f57b9ed9a32de3e7db7fcbae560f1052ec90428062a4b4071a018b4dacd5)
                check_type(argname="argument ec2_tag_group", value=ec2_tag_group, expected_type=type_hints["ec2_tag_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ec2_tag_group is not None:
                self._values["ec2_tag_group"] = ec2_tag_group

        @builtins.property
        def ec2_tag_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]]:
            '''A list that contains other lists of Amazon EC2 instance tag groups.

            For an instance to be included in the deployment group, it must be identified by all of the tag groups in the list.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html#cfn-codedeploy-deploymentgroup-ec2tagsetlistobject-ec2taggroup
            '''
            result = self._values.get("ec2_tag_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagSetListObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagSetProperty",
        jsii_struct_bases=[],
        name_mapping={"ec2_tag_set_list": "ec2TagSetList"},
    )
    class EC2TagSetProperty:
        def __init__(
            self,
            *,
            ec2_tag_set_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.EC2TagSetListObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``EC2TagSet`` property type specifies information about groups of tags applied to Amazon EC2 instances.

            The deployment group includes only Amazon EC2 instances identified by all the tag groups. ``EC2TagSet`` cannot be used in the same template as ``EC2TagFilter`` .

            For information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ .

            :param ec2_tag_set_list: The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group. CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group. Duplicates are not allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                e_c2_tag_set_property = codedeploy.CfnDeploymentGroup.EC2TagSetProperty(
                    ec2_tag_set_list=[codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty(
                        ec2_tag_group=[codedeploy.CfnDeploymentGroup.EC2TagFilterProperty(
                            key="key",
                            type="type",
                            value="value"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f15744d000d2706fd6c381dd06af7a21dcfe1d0481373c4f80c053557e023954)
                check_type(argname="argument ec2_tag_set_list", value=ec2_tag_set_list, expected_type=type_hints["ec2_tag_set_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ec2_tag_set_list is not None:
                self._values["ec2_tag_set_list"] = ec2_tag_set_list

        @builtins.property
        def ec2_tag_set_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagSetListObjectProperty"]]]]:
            '''The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group.

            CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group.

            Duplicates are not allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html#cfn-codedeploy-deploymentgroup-ec2tagset-ec2tagsetlist
            '''
            result = self._values.get("ec2_tag_set_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.EC2TagSetListObjectProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.ECSServiceProperty",
        jsii_struct_bases=[],
        name_mapping={"cluster_name": "clusterName", "service_name": "serviceName"},
    )
    class ECSServiceProperty:
        def __init__(
            self,
            *,
            cluster_name: builtins.str,
            service_name: builtins.str,
        ) -> None:
            '''Contains the service and cluster names used to identify an Amazon ECS deployment's target.

            :param cluster_name: The name of the cluster that the Amazon ECS service is associated with.
            :param service_name: The name of the target Amazon ECS service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ecsservice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                e_cSService_property = codedeploy.CfnDeploymentGroup.ECSServiceProperty(
                    cluster_name="clusterName",
                    service_name="serviceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__090e50bc68a192fd778a12a9810451fe8b55e0ea35a27c0f5553cb2ace63a947)
                check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cluster_name": cluster_name,
                "service_name": service_name,
            }

        @builtins.property
        def cluster_name(self) -> builtins.str:
            '''The name of the cluster that the Amazon ECS service is associated with.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ecsservice.html#cfn-codedeploy-deploymentgroup-ecsservice-clustername
            '''
            result = self._values.get("cluster_name")
            assert result is not None, "Required property 'cluster_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def service_name(self) -> builtins.str:
            '''The name of the target Amazon ECS service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ecsservice.html#cfn-codedeploy-deploymentgroup-ecsservice-servicename
            '''
            result = self._values.get("service_name")
            assert result is not None, "Required property 'service_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ECSServiceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.ELBInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class ELBInfoProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The ``ELBInfo`` property type specifies information about the Elastic Load Balancing load balancer used for an CodeDeploy deployment group.

            If you specify the ``ELBInfo`` property, the ``DeploymentStyle.DeploymentOption`` property must be set to ``WITH_TRAFFIC_CONTROL`` for AWS CodeDeploy to route your traffic using the specified load balancers.

            ``ELBInfo`` is a property of the `AWS CodeDeploy DeploymentGroup LoadBalancerInfo <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html>`_ property type.

            :param name: For blue/green deployments, the name of the load balancer that is used to route traffic from original instances to replacement instances in a blue/green deployment. For in-place deployments, the name of the load balancer that instances are deregistered from so they are not serving traffic during a deployment, and then re-registered with after the deployment is complete. .. epigraph:: AWS CloudFormation supports blue/green deployments on AWS Lambda compute platforms only.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                e_lBInfo_property = codedeploy.CfnDeploymentGroup.ELBInfoProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ca14c2421963a6eeba5a31651f8260ff7125a735713d359ecceefca86fba9ff)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''For blue/green deployments, the name of the load balancer that is used to route traffic from original instances to replacement instances in a blue/green deployment.

            For in-place deployments, the name of the load balancer that instances are deregistered from so they are not serving traffic during a deployment, and then re-registered with after the deployment is complete.
            .. epigraph::

               AWS CloudFormation supports blue/green deployments on AWS Lambda compute platforms only.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html#cfn-codedeploy-deploymentgroup-elbinfo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ELBInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.GitHubLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"commit_id": "commitId", "repository": "repository"},
    )
    class GitHubLocationProperty:
        def __init__(
            self,
            *,
            commit_id: builtins.str,
            repository: builtins.str,
        ) -> None:
            '''``GitHubLocation`` is a property of the `CodeDeploy DeploymentGroup Revision <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html>`_ property that specifies the location of an application revision that is stored in GitHub.

            :param commit_id: The SHA1 commit ID of the GitHub commit that represents the bundled artifacts for the application revision.
            :param repository: The GitHub account and repository pair that stores a reference to the commit that represents the bundled artifacts for the application revision. Specify the value as ``account/repository`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                git_hub_location_property = codedeploy.CfnDeploymentGroup.GitHubLocationProperty(
                    commit_id="commitId",
                    repository="repository"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbf3e9c63163ff3e85724337ef3a68ee0fc629928a93912237e878709c594ef3)
                check_type(argname="argument commit_id", value=commit_id, expected_type=type_hints["commit_id"])
                check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "commit_id": commit_id,
                "repository": repository,
            }

        @builtins.property
        def commit_id(self) -> builtins.str:
            '''The SHA1 commit ID of the GitHub commit that represents the bundled artifacts for the application revision.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation-commitid
            '''
            result = self._values.get("commit_id")
            assert result is not None, "Required property 'commit_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def repository(self) -> builtins.str:
            '''The GitHub account and repository pair that stores a reference to the commit that represents the bundled artifacts for the application revision.

            Specify the value as ``account/repository`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation-repository
            '''
            result = self._values.get("repository")
            assert result is not None, "Required property 'repository' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitHubLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.GreenFleetProvisioningOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action"},
    )
    class GreenFleetProvisioningOptionProperty:
        def __init__(self, *, action: typing.Optional[builtins.str] = None) -> None:
            '''Information about the instances that belong to the replacement environment in a blue/green deployment.

            :param action: The method used to add instances to a replacement environment. - ``DISCOVER_EXISTING`` : Use instances that already exist or will be created manually. - ``COPY_AUTO_SCALING_GROUP`` : Use settings from a specified Auto Scaling group to define and create instances in a new Auto Scaling group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-greenfleetprovisioningoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                green_fleet_provisioning_option_property = codedeploy.CfnDeploymentGroup.GreenFleetProvisioningOptionProperty(
                    action="action"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__955b6a8750e6f0227bae7bd92ec12951a0a2ca191046321ee2d0c93b4d5ab745)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The method used to add instances to a replacement environment.

            - ``DISCOVER_EXISTING`` : Use instances that already exist or will be created manually.
            - ``COPY_AUTO_SCALING_GROUP`` : Use settings from a specified Auto Scaling group to define and create instances in a new Auto Scaling group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-greenfleetprovisioningoption.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration-greenfleetprovisioningoption-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GreenFleetProvisioningOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "elb_info_list": "elbInfoList",
            "target_group_info_list": "targetGroupInfoList",
            "target_group_pair_info_list": "targetGroupPairInfoList",
        },
    )
    class LoadBalancerInfoProperty:
        def __init__(
            self,
            *,
            elb_info_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.ELBInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_group_info_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.TargetGroupInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_group_pair_info_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.TargetGroupPairInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``LoadBalancerInfo`` property type specifies information about the load balancer or target group used for an AWS CodeDeploy deployment group.

            For more information, see `Integrating CodeDeploy with Elastic Load Balancing <https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html>`_ in the *AWS CodeDeploy User Guide* .

            For AWS CloudFormation to use the properties specified in ``LoadBalancerInfo`` , the ``DeploymentStyle.DeploymentOption`` property must be set to ``WITH_TRAFFIC_CONTROL`` . If ``DeploymentStyle.DeploymentOption`` is not set to ``WITH_TRAFFIC_CONTROL`` , AWS CloudFormation ignores any settings specified in ``LoadBalancerInfo`` .
            .. epigraph::

               AWS CloudFormation supports blue/green deployments on the AWS Lambda compute platform only.

            ``LoadBalancerInfo`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource.

            :param elb_info_list: An array that contains information about the load balancer to use for load balancing in a deployment. In Elastic Load Balancing, load balancers are used with Classic Load Balancers. .. epigraph:: Adding more than one load balancer to the array is not supported.
            :param target_group_info_list: An array that contains information about the target group to use for load balancing in a deployment. In Elastic Load Balancing , target groups are used with Application Load Balancers . .. epigraph:: Adding more than one target group to the array is not supported.
            :param target_group_pair_info_list: ``CfnDeploymentGroup.LoadBalancerInfoProperty.TargetGroupPairInfoList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                load_balancer_info_property = codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty(
                    elb_info_list=[codedeploy.CfnDeploymentGroup.ELBInfoProperty(
                        name="name"
                    )],
                    target_group_info_list=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
                        name="name"
                    )],
                    target_group_pair_info_list=[codedeploy.CfnDeploymentGroup.TargetGroupPairInfoProperty(
                        prod_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                            listener_arns=["listenerArns"]
                        ),
                        target_groups=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
                            name="name"
                        )],
                        test_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                            listener_arns=["listenerArns"]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb0ff8b5cb32d65c037fe993b5cfd941ee1d576aa807118432fb679a7c723ed2)
                check_type(argname="argument elb_info_list", value=elb_info_list, expected_type=type_hints["elb_info_list"])
                check_type(argname="argument target_group_info_list", value=target_group_info_list, expected_type=type_hints["target_group_info_list"])
                check_type(argname="argument target_group_pair_info_list", value=target_group_pair_info_list, expected_type=type_hints["target_group_pair_info_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if elb_info_list is not None:
                self._values["elb_info_list"] = elb_info_list
            if target_group_info_list is not None:
                self._values["target_group_info_list"] = target_group_info_list
            if target_group_pair_info_list is not None:
                self._values["target_group_pair_info_list"] = target_group_pair_info_list

        @builtins.property
        def elb_info_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.ELBInfoProperty"]]]]:
            '''An array that contains information about the load balancer to use for load balancing in a deployment.

            In Elastic Load Balancing, load balancers are used with Classic Load Balancers.
            .. epigraph::

               Adding more than one load balancer to the array is not supported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-elbinfolist
            '''
            result = self._values.get("elb_info_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.ELBInfoProperty"]]]], result)

        @builtins.property
        def target_group_info_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TargetGroupInfoProperty"]]]]:
            '''An array that contains information about the target group to use for load balancing in a deployment.

            In Elastic Load Balancing , target groups are used with Application Load Balancers .
            .. epigraph::

               Adding more than one target group to the array is not supported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-targetgroupinfolist
            '''
            result = self._values.get("target_group_info_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TargetGroupInfoProperty"]]]], result)

        @builtins.property
        def target_group_pair_info_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TargetGroupPairInfoProperty"]]]]:
            '''``CfnDeploymentGroup.LoadBalancerInfoProperty.TargetGroupPairInfoList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-targetgrouppairinfolist
            '''
            result = self._values.get("target_group_pair_info_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TargetGroupPairInfoProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoadBalancerInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"on_premises_tag_group": "onPremisesTagGroup"},
    )
    class OnPremisesTagSetListObjectProperty:
        def __init__(
            self,
            *,
            on_premises_tag_group: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``OnPremisesTagSetListObject`` property type specifies lists of on-premises instance tag groups.

            In order for an instance to be included in the deployment group, it must be identified by all the tag groups in the list.

            ``OnPremisesTagSetListObject`` is a property of the `CodeDeploy DeploymentGroup OnPremisesTagSet <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html>`_ property type.

            :param on_premises_tag_group: Information about groups of on-premises instance tags.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                on_premises_tag_set_list_object_property = codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty(
                    on_premises_tag_group=[codedeploy.CfnDeploymentGroup.TagFilterProperty(
                        key="key",
                        type="type",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87eccb71adb9f86e141e17a68451b981b71f585ac8f0e4bf33453702b4328786)
                check_type(argname="argument on_premises_tag_group", value=on_premises_tag_group, expected_type=type_hints["on_premises_tag_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_premises_tag_group is not None:
                self._values["on_premises_tag_group"] = on_premises_tag_group

        @builtins.property
        def on_premises_tag_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]]:
            '''Information about groups of on-premises instance tags.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html#cfn-codedeploy-deploymentgroup-onpremisestagsetlistobject-onpremisestaggroup
            '''
            result = self._values.get("on_premises_tag_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremisesTagSetListObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.OnPremisesTagSetProperty",
        jsii_struct_bases=[],
        name_mapping={"on_premises_tag_set_list": "onPremisesTagSetList"},
    )
    class OnPremisesTagSetProperty:
        def __init__(
            self,
            *,
            on_premises_tag_set_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.OnPremisesTagSetListObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``OnPremisesTagSet`` property type specifies a list containing other lists of on-premises instance tag groups.

            In order for an instance to be included in the deployment group, it must be identified by all the tag groups in the list.

            For more information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ in the *AWS CodeDeploy User Guide* .

            ``OnPremisesTagSet`` is a property of the `DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource.

            :param on_premises_tag_set_list: A list that contains other lists of on-premises instance tag groups. For an instance to be included in the deployment group, it must be identified by all of the tag groups in the list. Duplicates are not allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                on_premises_tag_set_property = codedeploy.CfnDeploymentGroup.OnPremisesTagSetProperty(
                    on_premises_tag_set_list=[codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty(
                        on_premises_tag_group=[codedeploy.CfnDeploymentGroup.TagFilterProperty(
                            key="key",
                            type="type",
                            value="value"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b59946fdee8e1bfe3e95438b58d3c58685e30b6aac538907f66601323554a75b)
                check_type(argname="argument on_premises_tag_set_list", value=on_premises_tag_set_list, expected_type=type_hints["on_premises_tag_set_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_premises_tag_set_list is not None:
                self._values["on_premises_tag_set_list"] = on_premises_tag_set_list

        @builtins.property
        def on_premises_tag_set_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.OnPremisesTagSetListObjectProperty"]]]]:
            '''A list that contains other lists of on-premises instance tag groups.

            For an instance to be included in the deployment group, it must be identified by all of the tag groups in the list.

            Duplicates are not allowed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html#cfn-codedeploy-deploymentgroup-onpremisestagset-onpremisestagsetlist
            '''
            result = self._values.get("on_premises_tag_set_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.OnPremisesTagSetListObjectProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremisesTagSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.RevisionLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "git_hub_location": "gitHubLocation",
            "revision_type": "revisionType",
            "s3_location": "s3Location",
        },
    )
    class RevisionLocationProperty:
        def __init__(
            self,
            *,
            git_hub_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.GitHubLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            revision_type: typing.Optional[builtins.str] = None,
            s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``RevisionLocation`` is a property that defines the location of the CodeDeploy application revision to deploy.

            :param git_hub_location: Information about the location of application artifacts stored in GitHub.
            :param revision_type: The type of application revision:. - S3: An application revision stored in Amazon S3. - GitHub: An application revision stored in GitHub (EC2/On-premises deployments only). - String: A YAML-formatted or JSON-formatted string ( AWS Lambda deployments only). - AppSpecContent: An ``AppSpecContent`` object that contains the contents of an AppSpec file for an AWS Lambda or Amazon ECS deployment. The content is formatted as JSON or YAML stored as a RawString.
            :param s3_location: Information about the location of a revision stored in Amazon S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                revision_location_property = codedeploy.CfnDeploymentGroup.RevisionLocationProperty(
                    git_hub_location=codedeploy.CfnDeploymentGroup.GitHubLocationProperty(
                        commit_id="commitId",
                        repository="repository"
                    ),
                    revision_type="revisionType",
                    s3_location=codedeploy.CfnDeploymentGroup.S3LocationProperty(
                        bucket="bucket",
                        key="key",
                
                        # the properties below are optional
                        bundle_type="bundleType",
                        e_tag="eTag",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b4c29be242d375a46503ce1033f0b668156aca0230778a95967aac6066d41d6)
                check_type(argname="argument git_hub_location", value=git_hub_location, expected_type=type_hints["git_hub_location"])
                check_type(argname="argument revision_type", value=revision_type, expected_type=type_hints["revision_type"])
                check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if git_hub_location is not None:
                self._values["git_hub_location"] = git_hub_location
            if revision_type is not None:
                self._values["revision_type"] = revision_type
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def git_hub_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.GitHubLocationProperty"]]:
            '''Information about the location of application artifacts stored in GitHub.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation
            '''
            result = self._values.get("git_hub_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.GitHubLocationProperty"]], result)

        @builtins.property
        def revision_type(self) -> typing.Optional[builtins.str]:
            '''The type of application revision:.

            - S3: An application revision stored in Amazon S3.
            - GitHub: An application revision stored in GitHub (EC2/On-premises deployments only).
            - String: A YAML-formatted or JSON-formatted string ( AWS Lambda deployments only).
            - AppSpecContent: An ``AppSpecContent`` object that contains the contents of an AppSpec file for an AWS Lambda or Amazon ECS deployment. The content is formatted as JSON or YAML stored as a RawString.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-revisiontype
            '''
            result = self._values.get("revision_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.S3LocationProperty"]]:
            '''Information about the location of a revision stored in Amazon S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location
            '''
            result = self._values.get("s3_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RevisionLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "bundle_type": "bundleType",
            "e_tag": "eTag",
            "version": "version",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            bundle_type: typing.Optional[builtins.str] = None,
            e_tag: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``S3Location`` is a property of the `CodeDeploy DeploymentGroup Revision <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html>`_ property that specifies the location of an application revision that is stored in Amazon Simple Storage Service ( Amazon S3 ).

            :param bucket: The name of the Amazon S3 bucket where the application revision is stored.
            :param key: The name of the Amazon S3 object that represents the bundled artifacts for the application revision.
            :param bundle_type: The file type of the application revision. Must be one of the following:. - JSON - tar: A tar archive file. - tgz: A compressed tar archive file. - YAML - zip: A zip archive file.
            :param e_tag: The ETag of the Amazon S3 object that represents the bundled artifacts for the application revision. If the ETag is not specified as an input parameter, ETag validation of the object is skipped.
            :param version: A specific version of the Amazon S3 object that represents the bundled artifacts for the application revision. If the version is not specified, the system uses the most recent version by default.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                s3_location_property = codedeploy.CfnDeploymentGroup.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    bundle_type="bundleType",
                    e_tag="eTag",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51c7a1f811d3545fc6314b3ff07cf93d3d140d41bcdfb23a4bd6eaa4a6a35848)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument bundle_type", value=bundle_type, expected_type=type_hints["bundle_type"])
                check_type(argname="argument e_tag", value=e_tag, expected_type=type_hints["e_tag"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if bundle_type is not None:
                self._values["bundle_type"] = bundle_type
            if e_tag is not None:
                self._values["e_tag"] = e_tag
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''The name of the Amazon S3 bucket where the application revision is stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''The name of the Amazon S3 object that represents the bundled artifacts for the application revision.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bundle_type(self) -> typing.Optional[builtins.str]:
            '''The file type of the application revision. Must be one of the following:.

            - JSON
            - tar: A tar archive file.
            - tgz: A compressed tar archive file.
            - YAML
            - zip: A zip archive file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-bundletype
            '''
            result = self._values.get("bundle_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def e_tag(self) -> typing.Optional[builtins.str]:
            '''The ETag of the Amazon S3 object that represents the bundled artifacts for the application revision.

            If the ETag is not specified as an input parameter, ETag validation of the object is skipped.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-etag
            '''
            result = self._values.get("e_tag")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''A specific version of the Amazon S3 object that represents the bundled artifacts for the application revision.

            If the version is not specified, the system uses the most recent version by default.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-value
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type", "value": "value"},
    )
    class TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``TagFilter`` is a property type of the `AWS::CodeDeploy::DeploymentGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html>`_ resource that specifies which on-premises instances to associate with the deployment group. To register on-premise instances with AWS CodeDeploy , see `Configure Existing On-Premises Instances by Using AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-on-premises.html>`_ in the *AWS CodeDeploy User Guide* .

            For more information about using tags and tag groups to help manage your Amazon EC2 instances and on-premises instances, see `Tagging Instances for Deployment Groups in AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-tagging.html>`_ in the *AWS CodeDeploy User Guide* .

            :param key: The on-premises instance tag filter key.
            :param type: The on-premises instance tag filter type:. - KEY_ONLY: Key only. - VALUE_ONLY: Value only. - KEY_AND_VALUE: Key and value.
            :param value: The on-premises instance tag filter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                tag_filter_property = codedeploy.CfnDeploymentGroup.TagFilterProperty(
                    key="key",
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__662b8e7a786d5d29bc7de1c947f63d36919ddb171dcf7f55125894ab8a165679)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The on-premises instance tag filter key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The on-premises instance tag filter type:.

            - KEY_ONLY: Key only.
            - VALUE_ONLY: Value only.
            - KEY_AND_VALUE: Key and value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The on-premises instance tag filter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class TargetGroupInfoProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The ``TargetGroupInfo`` property type specifies information about a target group in Elastic Load Balancing to use in a deployment.

            Instances are registered as targets in a target group, and traffic is routed to the target group. For more information, see `TargetGroupInfo <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_TargetGroupInfo.html>`_ in the *AWS CodeDeploy API Reference*

            If you specify the ``TargetGroupInfo`` property, the ``DeploymentStyle.DeploymentOption`` property must be set to ``WITH_TRAFFIC_CONTROL`` for CodeDeploy to route your traffic using the specified target groups.

            ``TargetGroupInfo`` is a property of the `LoadBalancerInfo <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html>`_ property type.

            :param name: For blue/green deployments, the name of the target group that instances in the original environment are deregistered from, and instances in the replacement environment registered with. For in-place deployments, the name of the target group that instances are deregistered from, so they are not serving traffic during a deployment, and then re-registered with after the deployment completes. No duplicates allowed. .. epigraph:: AWS CloudFormation supports blue/green deployments on AWS Lambda compute platforms only. This value cannot exceed 32 characters, so you should use the ``Name`` property of the target group, or the ``TargetGroupName`` attribute with the ``Fn::GetAtt`` intrinsic function, as shown in the following example. Don't use the group's Amazon Resource Name (ARN) or ``TargetGroupFullName`` attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                target_group_info_property = codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92609e668302326a6dd512565c0f4d74ba84021072744b7da06ccc30e00278c6)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''For blue/green deployments, the name of the target group that instances in the original environment are deregistered from, and instances in the replacement environment registered with.

            For in-place deployments, the name of the target group that instances are deregistered from, so they are not serving traffic during a deployment, and then re-registered with after the deployment completes. No duplicates allowed.
            .. epigraph::

               AWS CloudFormation supports blue/green deployments on AWS Lambda compute platforms only.

            This value cannot exceed 32 characters, so you should use the ``Name`` property of the target group, or the ``TargetGroupName`` attribute with the ``Fn::GetAtt`` intrinsic function, as shown in the following example. Don't use the group's Amazon Resource Name (ARN) or ``TargetGroupFullName`` attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html#cfn-codedeploy-deploymentgroup-targetgroupinfo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TargetGroupPairInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prod_traffic_route": "prodTrafficRoute",
            "target_groups": "targetGroups",
            "test_traffic_route": "testTrafficRoute",
        },
    )
    class TargetGroupPairInfoProperty:
        def __init__(
            self,
            *,
            prod_traffic_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.TrafficRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.TargetGroupInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            test_traffic_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeploymentGroup.TrafficRouteProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param prod_traffic_route: ``CfnDeploymentGroup.TargetGroupPairInfoProperty.ProdTrafficRoute``.
            :param target_groups: ``CfnDeploymentGroup.TargetGroupPairInfoProperty.TargetGroups``.
            :param test_traffic_route: ``CfnDeploymentGroup.TargetGroupPairInfoProperty.TestTrafficRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgrouppairinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                target_group_pair_info_property = codedeploy.CfnDeploymentGroup.TargetGroupPairInfoProperty(
                    prod_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                        listener_arns=["listenerArns"]
                    ),
                    target_groups=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
                        name="name"
                    )],
                    test_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                        listener_arns=["listenerArns"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__331d1e2a2c4f04e057bfc15dda83dc34f57b3f49ba1634d92b92556f47d886a6)
                check_type(argname="argument prod_traffic_route", value=prod_traffic_route, expected_type=type_hints["prod_traffic_route"])
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
                check_type(argname="argument test_traffic_route", value=test_traffic_route, expected_type=type_hints["test_traffic_route"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if prod_traffic_route is not None:
                self._values["prod_traffic_route"] = prod_traffic_route
            if target_groups is not None:
                self._values["target_groups"] = target_groups
            if test_traffic_route is not None:
                self._values["test_traffic_route"] = test_traffic_route

        @builtins.property
        def prod_traffic_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TrafficRouteProperty"]]:
            '''``CfnDeploymentGroup.TargetGroupPairInfoProperty.ProdTrafficRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgrouppairinfo.html#cfn-codedeploy-deploymentgroup-targetgrouppairinfo-prodtrafficroute
            '''
            result = self._values.get("prod_traffic_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TrafficRouteProperty"]], result)

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TargetGroupInfoProperty"]]]]:
            '''``CfnDeploymentGroup.TargetGroupPairInfoProperty.TargetGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgrouppairinfo.html#cfn-codedeploy-deploymentgroup-targetgrouppairinfo-targetgroups
            '''
            result = self._values.get("target_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TargetGroupInfoProperty"]]]], result)

        @builtins.property
        def test_traffic_route(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TrafficRouteProperty"]]:
            '''``CfnDeploymentGroup.TargetGroupPairInfoProperty.TestTrafficRoute``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgrouppairinfo.html#cfn-codedeploy-deploymentgroup-targetgrouppairinfo-testtrafficroute
            '''
            result = self._values.get("test_traffic_route")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeploymentGroup.TrafficRouteProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupPairInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TrafficRouteProperty",
        jsii_struct_bases=[],
        name_mapping={"listener_arns": "listenerArns"},
    )
    class TrafficRouteProperty:
        def __init__(
            self,
            *,
            listener_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param listener_arns: ``CfnDeploymentGroup.TrafficRouteProperty.ListenerArns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-trafficroute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                traffic_route_property = codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                    listener_arns=["listenerArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b90ebd86517bc152cc6fed54d7422ddac9fb112def88475e5806d06ea0790ec)
                check_type(argname="argument listener_arns", value=listener_arns, expected_type=type_hints["listener_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if listener_arns is not None:
                self._values["listener_arns"] = listener_arns

        @builtins.property
        def listener_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnDeploymentGroup.TrafficRouteProperty.ListenerArns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-trafficroute.html#cfn-codedeploy-deploymentgroup-trafficroute-listenerarns
            '''
            result = self._values.get("listener_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrafficRouteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TriggerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trigger_events": "triggerEvents",
            "trigger_name": "triggerName",
            "trigger_target_arn": "triggerTargetArn",
        },
    )
    class TriggerConfigProperty:
        def __init__(
            self,
            *,
            trigger_events: typing.Optional[typing.Sequence[builtins.str]] = None,
            trigger_name: typing.Optional[builtins.str] = None,
            trigger_target_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about notification triggers for the deployment group.

            :param trigger_events: The event type or types that trigger notifications.
            :param trigger_name: The name of the notification trigger.
            :param trigger_target_arn: The Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic through which notifications about deployment or instance events are sent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codedeploy as codedeploy
                
                trigger_config_property = codedeploy.CfnDeploymentGroup.TriggerConfigProperty(
                    trigger_events=["triggerEvents"],
                    trigger_name="triggerName",
                    trigger_target_arn="triggerTargetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6c4d0f7b5ab989df16831c67f97942381ac0581a6f05241435aca79c40b5023)
                check_type(argname="argument trigger_events", value=trigger_events, expected_type=type_hints["trigger_events"])
                check_type(argname="argument trigger_name", value=trigger_name, expected_type=type_hints["trigger_name"])
                check_type(argname="argument trigger_target_arn", value=trigger_target_arn, expected_type=type_hints["trigger_target_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if trigger_events is not None:
                self._values["trigger_events"] = trigger_events
            if trigger_name is not None:
                self._values["trigger_name"] = trigger_name
            if trigger_target_arn is not None:
                self._values["trigger_target_arn"] = trigger_target_arn

        @builtins.property
        def trigger_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The event type or types that trigger notifications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggerevents
            '''
            result = self._values.get("trigger_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def trigger_name(self) -> typing.Optional[builtins.str]:
            '''The name of the notification trigger.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggername
            '''
            result = self._values.get("trigger_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trigger_target_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic through which notifications about deployment or instance events are sent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggertargetarn
            '''
            result = self._values.get("trigger_target_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "service_role_arn": "serviceRoleArn",
        "alarm_configuration": "alarmConfiguration",
        "auto_rollback_configuration": "autoRollbackConfiguration",
        "auto_scaling_groups": "autoScalingGroups",
        "blue_green_deployment_configuration": "blueGreenDeploymentConfiguration",
        "deployment": "deployment",
        "deployment_config_name": "deploymentConfigName",
        "deployment_group_name": "deploymentGroupName",
        "deployment_style": "deploymentStyle",
        "ec2_tag_filters": "ec2TagFilters",
        "ec2_tag_set": "ec2TagSet",
        "ecs_services": "ecsServices",
        "load_balancer_info": "loadBalancerInfo",
        "on_premises_instance_tag_filters": "onPremisesInstanceTagFilters",
        "on_premises_tag_set": "onPremisesTagSet",
        "outdated_instances_strategy": "outdatedInstancesStrategy",
        "tags": "tags",
        "trigger_configurations": "triggerConfigurations",
    },
)
class CfnDeploymentGroupProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        service_role_arn: builtins.str,
        alarm_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.AlarmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_rollback_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.AutoRollbackConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_scaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        blue_green_deployment_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.DeploymentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.DeploymentStyleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        ec2_tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.EC2TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.EC2TagSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        ecs_services: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.ECSServiceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        load_balancer_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.LoadBalancerInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        on_premises_instance_tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        on_premises_tag_set: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.OnPremisesTagSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        outdated_instances_strategy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trigger_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDeploymentGroup``.

        :param application_name: The name of an existing CodeDeploy application to associate this deployment group with.
        :param service_role_arn: A service role Amazon Resource Name (ARN) that grants CodeDeploy permission to make calls to AWS services on your behalf. For more information, see `Create a Service Role for AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-service-role.html>`_ in the *AWS CodeDeploy User Guide* . .. epigraph:: In some cases, you might need to add a dependency on the service role's policy. For more information, see IAM role policy in `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .
        :param alarm_configuration: Information about the Amazon CloudWatch alarms that are associated with the deployment group.
        :param auto_rollback_configuration: Information about the automatic rollback configuration that is associated with the deployment group. If you specify this property, don't specify the ``Deployment`` property.
        :param auto_scaling_groups: A list of associated Auto Scaling groups that CodeDeploy automatically deploys revisions to when new instances are created. Duplicates are not allowed.
        :param blue_green_deployment_configuration: Information about blue/green deployment options for a deployment group.
        :param deployment: The application revision to deploy to this deployment group. If you specify this property, your target application revision is deployed as soon as the provisioning process is complete. If you specify this property, don't specify the ``AutoRollbackConfiguration`` property.
        :param deployment_config_name: A deployment configuration name or a predefined configuration name. With predefined configurations, you can deploy application revisions to one instance at a time ( ``CodeDeployDefault.OneAtATime`` ), half of the instances at a time ( ``CodeDeployDefault.HalfAtATime`` ), or all the instances at once ( ``CodeDeployDefault.AllAtOnce`` ). For more information and valid values, see `Working with Deployment Configurations <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html>`_ in the *AWS CodeDeploy User Guide* .
        :param deployment_group_name: A name for the deployment group. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the deployment group name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param deployment_style: Attributes that determine the type of deployment to run and whether to route deployment traffic behind a load balancer. If you specify this property with a blue/green deployment type, don't specify the ``AutoScalingGroups`` , ``LoadBalancerInfo`` , or ``Deployment`` properties. .. epigraph:: For blue/green deployments, AWS CloudFormation supports deployments on Lambda compute platforms only. You can perform Amazon ECS blue/green deployments using ``AWS::CodeDeploy::BlueGreen`` hook. See `Perform Amazon ECS blue/green deployments through CodeDeploy using AWS CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html>`_ for more information.
        :param ec2_tag_filters: The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group. CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group. Duplicates are not allowed. You can specify ``EC2TagFilters`` or ``Ec2TagSet`` , but not both.
        :param ec2_tag_set: Information about groups of tags applied to Amazon EC2 instances. The deployment group includes only Amazon EC2 instances identified by all the tag groups. Cannot be used in the same call as ``ec2TagFilter`` .
        :param ecs_services: The target Amazon ECS services in the deployment group. This applies only to deployment groups that use the Amazon ECS compute platform. A target Amazon ECS service is specified as an Amazon ECS cluster and service name pair using the format ``<clustername>:<servicename>`` .
        :param load_balancer_info: Information about the load balancer to use in a deployment. For more information, see `Integrating CodeDeploy with Elastic Load Balancing <https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html>`_ in the *AWS CodeDeploy User Guide* .
        :param on_premises_instance_tag_filters: The on-premises instance tags already applied to on-premises instances that you want to include in the deployment group. CodeDeploy includes all on-premises instances identified by any of the tags you specify in this deployment group. To register on-premises instances with CodeDeploy , see `Working with On-Premises Instances for CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-on-premises.html>`_ in the *AWS CodeDeploy User Guide* . Duplicates are not allowed. You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.
        :param on_premises_tag_set: Information about groups of tags applied to on-premises instances. The deployment group includes only on-premises instances identified by all the tag groups. You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.
        :param outdated_instances_strategy: ``AWS::CodeDeploy::DeploymentGroup.OutdatedInstancesStrategy``.
        :param tags: ``AWS::CodeDeploy::DeploymentGroup.Tags``.
        :param trigger_configurations: Information about triggers associated with the deployment group. Duplicates are not allowed

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codedeploy as codedeploy
            
            cfn_deployment_group_props = codedeploy.CfnDeploymentGroupProps(
                application_name="applicationName",
                service_role_arn="serviceRoleArn",
            
                # the properties below are optional
                alarm_configuration=codedeploy.CfnDeploymentGroup.AlarmConfigurationProperty(
                    alarms=[codedeploy.CfnDeploymentGroup.AlarmProperty(
                        name="name"
                    )],
                    enabled=False,
                    ignore_poll_alarm_failure=False
                ),
                auto_rollback_configuration=codedeploy.CfnDeploymentGroup.AutoRollbackConfigurationProperty(
                    enabled=False,
                    events=["events"]
                ),
                auto_scaling_groups=["autoScalingGroups"],
                blue_green_deployment_configuration=codedeploy.CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty(
                    deployment_ready_option=codedeploy.CfnDeploymentGroup.DeploymentReadyOptionProperty(
                        action_on_timeout="actionOnTimeout",
                        wait_time_in_minutes=123
                    ),
                    green_fleet_provisioning_option=codedeploy.CfnDeploymentGroup.GreenFleetProvisioningOptionProperty(
                        action="action"
                    ),
                    terminate_blue_instances_on_deployment_success=codedeploy.CfnDeploymentGroup.BlueInstanceTerminationOptionProperty(
                        action="action",
                        termination_wait_time_in_minutes=123
                    )
                ),
                deployment=codedeploy.CfnDeploymentGroup.DeploymentProperty(
                    revision=codedeploy.CfnDeploymentGroup.RevisionLocationProperty(
                        git_hub_location=codedeploy.CfnDeploymentGroup.GitHubLocationProperty(
                            commit_id="commitId",
                            repository="repository"
                        ),
                        revision_type="revisionType",
                        s3_location=codedeploy.CfnDeploymentGroup.S3LocationProperty(
                            bucket="bucket",
                            key="key",
            
                            # the properties below are optional
                            bundle_type="bundleType",
                            e_tag="eTag",
                            version="version"
                        )
                    ),
            
                    # the properties below are optional
                    description="description",
                    ignore_application_stop_failures=False
                ),
                deployment_config_name="deploymentConfigName",
                deployment_group_name="deploymentGroupName",
                deployment_style=codedeploy.CfnDeploymentGroup.DeploymentStyleProperty(
                    deployment_option="deploymentOption",
                    deployment_type="deploymentType"
                ),
                ec2_tag_filters=[codedeploy.CfnDeploymentGroup.EC2TagFilterProperty(
                    key="key",
                    type="type",
                    value="value"
                )],
                ec2_tag_set=codedeploy.CfnDeploymentGroup.EC2TagSetProperty(
                    ec2_tag_set_list=[codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty(
                        ec2_tag_group=[codedeploy.CfnDeploymentGroup.EC2TagFilterProperty(
                            key="key",
                            type="type",
                            value="value"
                        )]
                    )]
                ),
                ecs_services=[codedeploy.CfnDeploymentGroup.ECSServiceProperty(
                    cluster_name="clusterName",
                    service_name="serviceName"
                )],
                load_balancer_info=codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty(
                    elb_info_list=[codedeploy.CfnDeploymentGroup.ELBInfoProperty(
                        name="name"
                    )],
                    target_group_info_list=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
                        name="name"
                    )],
                    target_group_pair_info_list=[codedeploy.CfnDeploymentGroup.TargetGroupPairInfoProperty(
                        prod_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                            listener_arns=["listenerArns"]
                        ),
                        target_groups=[codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty(
                            name="name"
                        )],
                        test_traffic_route=codedeploy.CfnDeploymentGroup.TrafficRouteProperty(
                            listener_arns=["listenerArns"]
                        )
                    )]
                ),
                on_premises_instance_tag_filters=[codedeploy.CfnDeploymentGroup.TagFilterProperty(
                    key="key",
                    type="type",
                    value="value"
                )],
                on_premises_tag_set=codedeploy.CfnDeploymentGroup.OnPremisesTagSetProperty(
                    on_premises_tag_set_list=[codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty(
                        on_premises_tag_group=[codedeploy.CfnDeploymentGroup.TagFilterProperty(
                            key="key",
                            type="type",
                            value="value"
                        )]
                    )]
                ),
                outdated_instances_strategy="outdatedInstancesStrategy",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trigger_configurations=[codedeploy.CfnDeploymentGroup.TriggerConfigProperty(
                    trigger_events=["triggerEvents"],
                    trigger_name="triggerName",
                    trigger_target_arn="triggerTargetArn"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a8d133dcae4b53273f86cc50d10afc50283d03497fd856ce0fae712135e42b)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument alarm_configuration", value=alarm_configuration, expected_type=type_hints["alarm_configuration"])
            check_type(argname="argument auto_rollback_configuration", value=auto_rollback_configuration, expected_type=type_hints["auto_rollback_configuration"])
            check_type(argname="argument auto_scaling_groups", value=auto_scaling_groups, expected_type=type_hints["auto_scaling_groups"])
            check_type(argname="argument blue_green_deployment_configuration", value=blue_green_deployment_configuration, expected_type=type_hints["blue_green_deployment_configuration"])
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument deployment_style", value=deployment_style, expected_type=type_hints["deployment_style"])
            check_type(argname="argument ec2_tag_filters", value=ec2_tag_filters, expected_type=type_hints["ec2_tag_filters"])
            check_type(argname="argument ec2_tag_set", value=ec2_tag_set, expected_type=type_hints["ec2_tag_set"])
            check_type(argname="argument ecs_services", value=ecs_services, expected_type=type_hints["ecs_services"])
            check_type(argname="argument load_balancer_info", value=load_balancer_info, expected_type=type_hints["load_balancer_info"])
            check_type(argname="argument on_premises_instance_tag_filters", value=on_premises_instance_tag_filters, expected_type=type_hints["on_premises_instance_tag_filters"])
            check_type(argname="argument on_premises_tag_set", value=on_premises_tag_set, expected_type=type_hints["on_premises_tag_set"])
            check_type(argname="argument outdated_instances_strategy", value=outdated_instances_strategy, expected_type=type_hints["outdated_instances_strategy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trigger_configurations", value=trigger_configurations, expected_type=type_hints["trigger_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_name": application_name,
            "service_role_arn": service_role_arn,
        }
        if alarm_configuration is not None:
            self._values["alarm_configuration"] = alarm_configuration
        if auto_rollback_configuration is not None:
            self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if auto_scaling_groups is not None:
            self._values["auto_scaling_groups"] = auto_scaling_groups
        if blue_green_deployment_configuration is not None:
            self._values["blue_green_deployment_configuration"] = blue_green_deployment_configuration
        if deployment is not None:
            self._values["deployment"] = deployment
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name
        if deployment_style is not None:
            self._values["deployment_style"] = deployment_style
        if ec2_tag_filters is not None:
            self._values["ec2_tag_filters"] = ec2_tag_filters
        if ec2_tag_set is not None:
            self._values["ec2_tag_set"] = ec2_tag_set
        if ecs_services is not None:
            self._values["ecs_services"] = ecs_services
        if load_balancer_info is not None:
            self._values["load_balancer_info"] = load_balancer_info
        if on_premises_instance_tag_filters is not None:
            self._values["on_premises_instance_tag_filters"] = on_premises_instance_tag_filters
        if on_premises_tag_set is not None:
            self._values["on_premises_tag_set"] = on_premises_tag_set
        if outdated_instances_strategy is not None:
            self._values["outdated_instances_strategy"] = outdated_instances_strategy
        if tags is not None:
            self._values["tags"] = tags
        if trigger_configurations is not None:
            self._values["trigger_configurations"] = trigger_configurations

    @builtins.property
    def application_name(self) -> builtins.str:
        '''The name of an existing CodeDeploy application to associate this deployment group with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_role_arn(self) -> builtins.str:
        '''A service role Amazon Resource Name (ARN) that grants CodeDeploy permission to make calls to AWS services on your behalf.

        For more information, see `Create a Service Role for AWS CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-service-role.html>`_ in the *AWS CodeDeploy User Guide* .
        .. epigraph::

           In some cases, you might need to add a dependency on the service role's policy. For more information, see IAM role policy in `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        assert result is not None, "Required property 'service_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.AlarmConfigurationProperty]]:
        '''Information about the Amazon CloudWatch alarms that are associated with the deployment group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        '''
        result = self._values.get("alarm_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.AlarmConfigurationProperty]], result)

    @builtins.property
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.AutoRollbackConfigurationProperty]]:
        '''Information about the automatic rollback configuration that is associated with the deployment group.

        If you specify this property, don't specify the ``Deployment`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        '''
        result = self._values.get("auto_rollback_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.AutoRollbackConfigurationProperty]], result)

    @builtins.property
    def auto_scaling_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of associated Auto Scaling groups that CodeDeploy automatically deploys revisions to when new instances are created.

        Duplicates are not allowed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        '''
        result = self._values.get("auto_scaling_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def blue_green_deployment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty]]:
        '''Information about blue/green deployment options for a deployment group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-bluegreendeploymentconfiguration
        '''
        result = self._values.get("blue_green_deployment_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty]], result)

    @builtins.property
    def deployment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.DeploymentProperty]]:
        '''The application revision to deploy to this deployment group.

        If you specify this property, your target application revision is deployed as soon as the provisioning process is complete. If you specify this property, don't specify the ``AutoRollbackConfiguration`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.DeploymentProperty]], result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''A deployment configuration name or a predefined configuration name.

        With predefined configurations, you can deploy application revisions to one instance at a time ( ``CodeDeployDefault.OneAtATime`` ), half of the instances at a time ( ``CodeDeployDefault.HalfAtATime`` ), or all the instances at once ( ``CodeDeployDefault.AllAtOnce`` ). For more information and valid values, see `Working with Deployment Configurations <https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html>`_ in the *AWS CodeDeploy User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''A name for the deployment group.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the deployment group name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        '''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_style(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.DeploymentStyleProperty]]:
        '''Attributes that determine the type of deployment to run and whether to route deployment traffic behind a load balancer.

        If you specify this property with a blue/green deployment type, don't specify the ``AutoScalingGroups`` , ``LoadBalancerInfo`` , or ``Deployment`` properties.
        .. epigraph::

           For blue/green deployments, AWS CloudFormation supports deployments on Lambda compute platforms only. You can perform Amazon ECS blue/green deployments using ``AWS::CodeDeploy::BlueGreen`` hook. See `Perform Amazon ECS blue/green deployments through CodeDeploy using AWS CloudFormation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html>`_ for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        '''
        result = self._values.get("deployment_style")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.DeploymentStyleProperty]], result)

    @builtins.property
    def ec2_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.EC2TagFilterProperty]]]]:
        '''The Amazon EC2 tags that are already applied to Amazon EC2 instances that you want to include in the deployment group.

        CodeDeploy includes all Amazon EC2 instances identified by any of the tags you specify in this deployment group. Duplicates are not allowed.

        You can specify ``EC2TagFilters`` or ``Ec2TagSet`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        '''
        result = self._values.get("ec2_tag_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.EC2TagFilterProperty]]]], result)

    @builtins.property
    def ec2_tag_set(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.EC2TagSetProperty]]:
        '''Information about groups of tags applied to Amazon EC2 instances.

        The deployment group includes only Amazon EC2 instances identified by all the tag groups. Cannot be used in the same call as ``ec2TagFilter`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        '''
        result = self._values.get("ec2_tag_set")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.EC2TagSetProperty]], result)

    @builtins.property
    def ecs_services(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.ECSServiceProperty]]]]:
        '''The target Amazon ECS services in the deployment group.

        This applies only to deployment groups that use the Amazon ECS compute platform. A target Amazon ECS service is specified as an Amazon ECS cluster and service name pair using the format ``<clustername>:<servicename>`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ecsservices
        '''
        result = self._values.get("ecs_services")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.ECSServiceProperty]]]], result)

    @builtins.property
    def load_balancer_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.LoadBalancerInfoProperty]]:
        '''Information about the load balancer to use in a deployment.

        For more information, see `Integrating CodeDeploy with Elastic Load Balancing <https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html>`_ in the *AWS CodeDeploy User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        '''
        result = self._values.get("load_balancer_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.LoadBalancerInfoProperty]], result)

    @builtins.property
    def on_premises_instance_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.TagFilterProperty]]]]:
        '''The on-premises instance tags already applied to on-premises instances that you want to include in the deployment group.

        CodeDeploy includes all on-premises instances identified by any of the tags you specify in this deployment group. To register on-premises instances with CodeDeploy , see `Working with On-Premises Instances for CodeDeploy <https://docs.aws.amazon.com/codedeploy/latest/userguide/instances-on-premises.html>`_ in the *AWS CodeDeploy User Guide* . Duplicates are not allowed.

        You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        '''
        result = self._values.get("on_premises_instance_tag_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.TagFilterProperty]]]], result)

    @builtins.property
    def on_premises_tag_set(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.OnPremisesTagSetProperty]]:
        '''Information about groups of tags applied to on-premises instances.

        The deployment group includes only on-premises instances identified by all the tag groups.

        You can specify ``OnPremisesInstanceTagFilters`` or ``OnPremisesInstanceTagSet`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        '''
        result = self._values.get("on_premises_tag_set")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.OnPremisesTagSetProperty]], result)

    @builtins.property
    def outdated_instances_strategy(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::DeploymentGroup.OutdatedInstancesStrategy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-outdatedinstancesstrategy
        '''
        result = self._values.get("outdated_instances_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''``AWS::CodeDeploy::DeploymentGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def trigger_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.TriggerConfigProperty]]]]:
        '''Information about triggers associated with the deployment group.

        Duplicates are not allowed

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        '''
        result = self._values.get("trigger_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.TriggerConfigProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.CustomLambdaDeploymentConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "interval": "interval",
        "percentage": "percentage",
        "type": "type",
        "deployment_config_name": "deploymentConfigName",
    },
)
class CustomLambdaDeploymentConfigProps:
    def __init__(
        self,
        *,
        interval: _aws_cdk_core_f4b25747.Duration,
        percentage: jsii.Number,
        type: "CustomLambdaDeploymentConfigType",
        deployment_config_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties of a reference to a CodeDeploy Lambda Deployment Configuration.

        :param interval: The interval, in number of minutes: - For LINEAR, how frequently additional traffic is shifted - For CANARY, how long to shift traffic before the full deployment.
        :param percentage: The integer percentage of traffic to shift: - For LINEAR, the percentage to shift every interval - For CANARY, the percentage to shift until the interval passes, before the full deployment.
        :param type: The type of deployment config, either CANARY or LINEAR.
        :param deployment_config_name: The verbatim name of the deployment config. Must be unique per account/region. Other parameters cannot be updated if this name is provided. Default: - automatically generated name

        :exampleMetadata: infused

        Example::

            # application: codedeploy.LambdaApplication
            # alias: lambda.Alias
            config = codedeploy.CustomLambdaDeploymentConfig(self, "CustomConfig",
                type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
                interval=Duration.minutes(1),
                percentage=5
            )
            deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
                application=application,
                alias=alias,
                deployment_config=config
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9feaae1d9b0c4dfb6d46153dd3b10f0cca0c561f5809080a8ca3627095f87281)
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interval": interval,
            "percentage": percentage,
            "type": type,
        }
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name

    @builtins.property
    def interval(self) -> _aws_cdk_core_f4b25747.Duration:
        '''The interval, in number of minutes: - For LINEAR, how frequently additional traffic is shifted - For CANARY, how long to shift traffic before the full deployment.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(_aws_cdk_core_f4b25747.Duration, result)

    @builtins.property
    def percentage(self) -> jsii.Number:
        '''The integer percentage of traffic to shift: - For LINEAR, the percentage to shift every interval - For CANARY, the percentage to shift until the interval passes, before the full deployment.'''
        result = self._values.get("percentage")
        assert result is not None, "Required property 'percentage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> "CustomLambdaDeploymentConfigType":
        '''The type of deployment config, either CANARY or LINEAR.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("CustomLambdaDeploymentConfigType", result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''The verbatim name of the deployment config.

        Must be unique per account/region.
        Other parameters cannot be updated if this name is provided.

        :default: - automatically generated name
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomLambdaDeploymentConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-codedeploy.CustomLambdaDeploymentConfigType")
class CustomLambdaDeploymentConfigType(enum.Enum):
    '''Lambda Deployment config type.

    :exampleMetadata: infused

    Example::

        # application: codedeploy.LambdaApplication
        # alias: lambda.Alias
        config = codedeploy.CustomLambdaDeploymentConfig(self, "CustomConfig",
            type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
            interval=Duration.minutes(1),
            percentage=5
        )
        deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
            application=application,
            alias=alias,
            deployment_config=config
        )
    '''

    CANARY = "CANARY"
    '''Canary deployment type.'''
    LINEAR = "LINEAR"
    '''Linear deployment type.'''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.EcsApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName"},
)
class EcsApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construction properties for {@link EcsApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codedeploy as codedeploy
            
            ecs_application_props = codedeploy.EcsApplicationProps(
                application_name="applicationName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbca5e37a04e380c6af6e64bd1931c5a09e46aecdafc0ea5357d6b2570e55f26)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The physical, human-readable name of the CodeDeploy Application.

        :default: an auto-generated name will be used
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsDeploymentConfig(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.EcsDeploymentConfig",
):
    '''A custom Deployment Configuration for an ECS Deployment Group.

    Note: This class currently stands as namespaced container of the default configurations
    until CloudFormation supports custom ECS Deployment Configs. Until then it is closed
    (private constructor) and does not extend {@link cdk.Construct}

    :resource: AWS::CodeDeploy::DeploymentConfig
    '''

    @jsii.member(jsii_name="fromEcsDeploymentConfigName")
    @builtins.classmethod
    def from_ecs_deployment_config_name(
        cls,
        _scope: _constructs_77d1e7e8.Construct,
        _id: builtins.str,
        ecs_deployment_config_name: builtins.str,
    ) -> "IEcsDeploymentConfig":
        '''Import a custom Deployment Configuration for an ECS Deployment Group defined outside the CDK.

        :param _scope: the parent Construct for this new Construct.
        :param _id: the logical ID of this new Construct.
        :param ecs_deployment_config_name: the name of the referenced custom Deployment Configuration.

        :return: a Construct representing a reference to an existing custom Deployment Configuration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be66b99c6bfa2b3df2a8fea748affba4c03af95be95a054c442e16af44d5a6c)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _id", value=_id, expected_type=type_hints["_id"])
            check_type(argname="argument ecs_deployment_config_name", value=ecs_deployment_config_name, expected_type=type_hints["ecs_deployment_config_name"])
        return typing.cast("IEcsDeploymentConfig", jsii.sinvoke(cls, "fromEcsDeploymentConfigName", [_scope, _id, ecs_deployment_config_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> "IEcsDeploymentConfig":
        return typing.cast("IEcsDeploymentConfig", jsii.sget(cls, "ALL_AT_ONCE"))


class EcsDeploymentGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.EcsDeploymentGroup",
):
    '''Note: This class currently stands as a namespaced container for importing an ECS Deployment Group defined outside the CDK app until CloudFormation supports provisioning ECS Deployment Groups.

    Until then it is closed (private constructor) and does not
    extend {@link cdk.Construct}.

    :resource: AWS::CodeDeploy::DeploymentGroup
    '''

    @jsii.member(jsii_name="fromEcsDeploymentGroupAttributes")
    @builtins.classmethod
    def from_ecs_deployment_group_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application: "IEcsApplication",
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional["IEcsDeploymentConfig"] = None,
    ) -> "IEcsDeploymentGroup":
        '''Import an ECS Deployment Group defined outside the CDK app.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: EcsDeploymentConfig.ALL_AT_ONCE

        :return: a Construct representing a reference to an existing Deployment Group
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478c802d3b879cff23e2fda7e29df1aa4a639fdf328f5e7e96b8420dd02382bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = EcsDeploymentGroupAttributes(
            application=application,
            deployment_group_name=deployment_group_name,
            deployment_config=deployment_config,
        )

        return typing.cast("IEcsDeploymentGroup", jsii.sinvoke(cls, "fromEcsDeploymentGroupAttributes", [scope, id, attrs]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.EcsDeploymentGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "deployment_group_name": "deploymentGroupName",
        "deployment_config": "deploymentConfig",
    },
)
class EcsDeploymentGroupAttributes:
    def __init__(
        self,
        *,
        application: "IEcsApplication",
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional["IEcsDeploymentConfig"] = None,
    ) -> None:
        '''Properties of a reference to a CodeDeploy ECS Deployment Group.

        :param application: The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: EcsDeploymentConfig.ALL_AT_ONCE

        :see: EcsDeploymentGroup#fromEcsDeploymentGroupAttributes
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codedeploy as codedeploy
            
            # ecs_application: codedeploy.EcsApplication
            # ecs_deployment_config: codedeploy.IEcsDeploymentConfig
            
            ecs_deployment_group_attributes = codedeploy.EcsDeploymentGroupAttributes(
                application=ecs_application,
                deployment_group_name="deploymentGroupName",
            
                # the properties below are optional
                deployment_config=ecs_deployment_config
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db916a90a6b615d5cc50b383fcb199b74a4638f7986f4255e7ead48eaf8a0c02)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument deployment_config", value=deployment_config, expected_type=type_hints["deployment_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application": application,
            "deployment_group_name": deployment_group_name,
        }
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> "IEcsApplication":
        '''The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.'''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast("IEcsApplication", result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        '''The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.'''
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_config(self) -> typing.Optional["IEcsDeploymentConfig"]:
        '''The Deployment Configuration this Deployment Group uses.

        :default: EcsDeploymentConfig.ALL_AT_ONCE
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional["IEcsDeploymentConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsDeploymentGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IEcsApplication")
class IEcsApplication(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''Represents a reference to a CodeDeploy Application deploying to Amazon ECS.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link EcsApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link EcsApplication#fromEcsApplicationName} method.
    '''

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...


class _IEcsApplicationProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Represents a reference to a CodeDeploy Application deploying to Amazon ECS.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link EcsApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link EcsApplication#fromEcsApplicationName} method.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.IEcsApplication"

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEcsApplication).__jsii_proxy_class__ = lambda : _IEcsApplicationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IEcsDeploymentConfig")
class IEcsDeploymentConfig(typing_extensions.Protocol):
    '''The Deployment Configuration of an ECS Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link EcsDeploymentConfig} class
    (for example, ``EcsDeploymentConfig.AllAtOnce``).

    Note: CloudFormation does not currently support creating custom ECS configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link EcsDeploymentConfig#fromEcsDeploymentConfigName}.
    '''

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        ...


class _IEcsDeploymentConfigProxy:
    '''The Deployment Configuration of an ECS Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link EcsDeploymentConfig} class
    (for example, ``EcsDeploymentConfig.AllAtOnce``).

    Note: CloudFormation does not currently support creating custom ECS configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link EcsDeploymentConfig#fromEcsDeploymentConfigName}.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.IEcsDeploymentConfig"

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEcsDeploymentConfig).__jsii_proxy_class__ = lambda : _IEcsDeploymentConfigProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IEcsDeploymentGroup")
class IEcsDeploymentGroup(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''Interface for an ECS deployment group.'''

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> IEcsApplication:
        '''The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IEcsDeploymentConfig:
        '''The Deployment Configuration this Group uses.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''The ARN of this Deployment Group.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''The physical name of the CodeDeploy Deployment Group.

        :attribute: true
        '''
        ...


class _IEcsDeploymentGroupProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Interface for an ECS deployment group.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.IEcsDeploymentGroup"

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> IEcsApplication:
        '''The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.'''
        return typing.cast(IEcsApplication, jsii.get(self, "application"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IEcsDeploymentConfig:
        '''The Deployment Configuration this Group uses.'''
        return typing.cast(IEcsDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''The ARN of this Deployment Group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''The physical name of the CodeDeploy Deployment Group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEcsDeploymentGroup).__jsii_proxy_class__ = lambda : _IEcsDeploymentGroupProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaApplication")
class ILambdaApplication(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''Represents a reference to a CodeDeploy Application deploying to AWS Lambda.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link LambdaApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link LambdaApplication#fromLambdaApplicationName} method.
    '''

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...


class _ILambdaApplicationProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Represents a reference to a CodeDeploy Application deploying to AWS Lambda.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link LambdaApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link LambdaApplication#fromLambdaApplicationName} method.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.ILambdaApplication"

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILambdaApplication).__jsii_proxy_class__ = lambda : _ILambdaApplicationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaDeploymentConfig")
class ILambdaDeploymentConfig(typing_extensions.Protocol):
    '''The Deployment Configuration of a Lambda Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link LambdaDeploymentConfig} class
    (``LambdaDeploymentConfig.AllAtOnce``, ``LambdaDeploymentConfig.Canary10Percent30Minutes``, etc.).

    Note: CloudFormation does not currently support creating custom lambda configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link LambdaDeploymentConfig#import}.
    '''

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        ...


class _ILambdaDeploymentConfigProxy:
    '''The Deployment Configuration of a Lambda Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link LambdaDeploymentConfig} class
    (``LambdaDeploymentConfig.AllAtOnce``, ``LambdaDeploymentConfig.Canary10Percent30Minutes``, etc.).

    Note: CloudFormation does not currently support creating custom lambda configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link LambdaDeploymentConfig#import}.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.ILambdaDeploymentConfig"

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILambdaDeploymentConfig).__jsii_proxy_class__ = lambda : _ILambdaDeploymentConfigProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaDeploymentGroup")
class ILambdaDeploymentGroup(
    _aws_cdk_core_f4b25747.IResource,
    typing_extensions.Protocol,
):
    '''Interface for a Lambda deployment groups.'''

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> ILambdaApplication:
        '''The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> ILambdaDeploymentConfig:
        '''The Deployment Configuration this Group uses.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''The ARN of this Deployment Group.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''The physical name of the CodeDeploy Deployment Group.

        :attribute: true
        '''
        ...


class _ILambdaDeploymentGroupProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Interface for a Lambda deployment groups.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.ILambdaDeploymentGroup"

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> ILambdaApplication:
        '''The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.'''
        return typing.cast(ILambdaApplication, jsii.get(self, "application"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> ILambdaDeploymentConfig:
        '''The Deployment Configuration this Group uses.'''
        return typing.cast(ILambdaDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''The ARN of this Deployment Group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''The physical name of the CodeDeploy Deployment Group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILambdaDeploymentGroup).__jsii_proxy_class__ = lambda : _ILambdaDeploymentGroupProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerApplication")
class IServerApplication(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''Represents a reference to a CodeDeploy Application deploying to EC2/on-premise instances.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link ServerApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link #fromServerApplicationName} method.
    '''

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...


class _IServerApplicationProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''Represents a reference to a CodeDeploy Application deploying to EC2/on-premise instances.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link ServerApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link #fromServerApplicationName} method.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.IServerApplication"

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServerApplication).__jsii_proxy_class__ = lambda : _IServerApplicationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerDeploymentConfig")
class IServerDeploymentConfig(typing_extensions.Protocol):
    '''The Deployment Configuration of an EC2/on-premise Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link ServerDeploymentConfig} class
    (``ServerDeploymentConfig.HALF_AT_A_TIME``, ``ServerDeploymentConfig.ALL_AT_ONCE``, etc.).
    To create a custom Deployment Configuration,
    instantiate the {@link ServerDeploymentConfig} Construct.
    '''

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...


class _IServerDeploymentConfigProxy:
    '''The Deployment Configuration of an EC2/on-premise Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link ServerDeploymentConfig} class
    (``ServerDeploymentConfig.HALF_AT_A_TIME``, ``ServerDeploymentConfig.ALL_AT_ONCE``, etc.).
    To create a custom Deployment Configuration,
    instantiate the {@link ServerDeploymentConfig} Construct.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.IServerDeploymentConfig"

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServerDeploymentConfig).__jsii_proxy_class__ = lambda : _IServerDeploymentConfigProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerDeploymentGroup")
class IServerDeploymentGroup(
    _aws_cdk_core_f4b25747.IResource,
    typing_extensions.Protocol,
):
    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> IServerApplication:
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IServerDeploymentConfig:
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        ...


class _IServerDeploymentGroupProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codedeploy.IServerDeploymentGroup"

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> IServerApplication:
        return typing.cast(IServerApplication, jsii.get(self, "application"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IServerDeploymentConfig:
        return typing.cast(IServerDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]], jsii.get(self, "autoScalingGroups"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], jsii.get(self, "role"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IServerDeploymentGroup).__jsii_proxy_class__ = lambda : _IServerDeploymentGroupProxy


class InstanceTagSet(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.InstanceTagSet",
):
    '''Represents a set of instance tag groups.

    An instance will match a set if it matches all of the groups in the set -
    in other words, sets follow 'and' semantics.
    You can have a maximum of 3 tag groups inside a set.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_autoscaling as autoscaling
        import aws_cdk.aws_cloudwatch as cloudwatch
        
        # application: codedeploy.ServerApplication
        # asg: autoscaling.AutoScalingGroup
        # alarm: cloudwatch.Alarm
        
        deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
            application=application,
            deployment_group_name="MyDeploymentGroup",
            auto_scaling_groups=[asg],
            # adds User Data that installs the CodeDeploy agent on your auto-scaling groups hosts
            # default: true
            install_agent=True,
            # adds EC2 instances matching tags
            ec2_instance_tags=codedeploy.InstanceTagSet({
                # any instance with tags satisfying
                # key1=v1 or key1=v2 or key2 (any value) or value v3 (any key)
                # will match this group
                "key1": ["v1", "v2"],
                "key2": [],
                "": ["v3"]
            }),
            # adds on-premise instances matching tags
            on_premise_instance_tags=codedeploy.InstanceTagSet({
                "key1": ["v1", "v2"]
            }, {
                "key2": ["v3"]
            }),
            # CloudWatch alarms
            alarms=[alarm],
            # whether to ignore failure to fetch the status of alarms from CloudWatch
            # default: false
            ignore_poll_alarms_failure=False,
            # auto-rollback configuration
            auto_rollback=codedeploy.AutoRollbackConfig(
                failed_deployment=True,  # default: true
                stopped_deployment=True,  # default: false
                deployment_in_alarm=True
            )
        )
    '''

    def __init__(
        self,
        *instance_tag_groups: typing.Mapping[builtins.str, typing.List[builtins.str]],
    ) -> None:
        '''
        :param instance_tag_groups: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51eea36e8ea4ea5b540cf931f80bdd815f59138a75b2b96f4fc4a5fe5ce9a7dd)
            check_type(argname="argument instance_tag_groups", value=instance_tag_groups, expected_type=typing.Tuple[type_hints["instance_tag_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*instance_tag_groups])

    @builtins.property
    @jsii.member(jsii_name="instanceTagGroups")
    def instance_tag_groups(
        self,
    ) -> typing.List[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        return typing.cast(typing.List[typing.Mapping[builtins.str, typing.List[builtins.str]]], jsii.get(self, "instanceTagGroups"))


@jsii.implements(ILambdaApplication)
class LambdaApplication(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.LambdaApplication",
):
    '''A CodeDeploy Application that deploys to an AWS Lambda function.

    :resource: AWS::CodeDeploy::Application
    :exampleMetadata: infused

    Example::

        application = codedeploy.LambdaApplication(self, "CodeDeployApplication",
            application_name="MyApplication"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3d4007fc8470b3911221c247263ec7f1bcd4d5908a970dc8b5e3016dd09cb9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaApplicationProps(application_name=application_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromLambdaApplicationName")
    @builtins.classmethod
    def from_lambda_application_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        lambda_application_name: builtins.str,
    ) -> ILambdaApplication:
        '''Import an Application defined either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param lambda_application_name: the name of the application to import.

        :return: a Construct representing a reference to an existing Application
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07be6c7dba10ea1f17730a9313391ec490570edf70793a78a6ab6c29e8c85281)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lambda_application_name", value=lambda_application_name, expected_type=type_hints["lambda_application_name"])
        return typing.cast(ILambdaApplication, jsii.sinvoke(cls, "fromLambdaApplicationName", [scope, id, lambda_application_name]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.LambdaApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName"},
)
class LambdaApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construction properties for {@link LambdaApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :exampleMetadata: infused

        Example::

            application = codedeploy.LambdaApplication(self, "CodeDeployApplication",
                application_name="MyApplication"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d218c184beddb4529b19437d4e36b191ae599a6bad4f297368fc9fb0d0f9c9d)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The physical, human-readable name of the CodeDeploy Application.

        :default: an auto-generated name will be used
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaDeploymentConfig(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentConfig",
):
    '''A custom Deployment Configuration for a Lambda Deployment Group.

    Note: This class currently stands as namespaced container of the default configurations
    until CloudFormation supports custom Lambda Deployment Configs. Until then it is closed
    (private constructor) and does not extend {@link cdk.Construct}

    :resource: AWS::CodeDeploy::DeploymentConfig
    :exampleMetadata: infused

    Example::

        # my_application: codedeploy.LambdaApplication
        # func: lambda.Function
        
        version = func.current_version
        version1_alias = lambda_.Alias(self, "alias",
            alias_name="prod",
            version=version
        )
        
        deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
            application=my_application,  # optional property: one will be created for you if not provided
            alias=version1_alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE
        )
    '''

    @jsii.member(jsii_name="import")
    @builtins.classmethod
    def import_(
        cls,
        _scope: _constructs_77d1e7e8.Construct,
        _id: builtins.str,
        *,
        deployment_config_name: builtins.str,
    ) -> ILambdaDeploymentConfig:
        '''Import a custom Deployment Configuration for a Lambda Deployment Group defined outside the CDK.

        :param _scope: the parent Construct for this new Construct.
        :param _id: the logical ID of this new Construct.
        :param deployment_config_name: The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        :return: a Construct representing a reference to an existing custom Deployment Configuration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ace3a1194fb6f1be0dce1ab20a666d2592b01d05cb716c02107f953d0af6855)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument _id", value=_id, expected_type=type_hints["_id"])
        props = LambdaDeploymentConfigImportProps(
            deployment_config_name=deployment_config_name
        )

        return typing.cast(ILambdaDeploymentConfig, jsii.sinvoke(cls, "import", [_scope, _id, props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "ALL_AT_ONCE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_10MINUTES")
    def CANARY_10_PERCENT_10_MINUTES(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "CANARY_10PERCENT_10MINUTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_15MINUTES")
    def CANARY_10_PERCENT_15_MINUTES(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "CANARY_10PERCENT_15MINUTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_30MINUTES")
    def CANARY_10_PERCENT_30_MINUTES(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "CANARY_10PERCENT_30MINUTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_5MINUTES")
    def CANARY_10_PERCENT_5_MINUTES(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "CANARY_10PERCENT_5MINUTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_10MINUTES")
    def LINEAR_10_PERCENT_EVERY_10_MINUTES(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "LINEAR_10PERCENT_EVERY_10MINUTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_1MINUTE")
    def LINEAR_10_PERCENT_EVERY_1_MINUTE(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "LINEAR_10PERCENT_EVERY_1MINUTE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_2MINUTES")
    def LINEAR_10_PERCENT_EVERY_2_MINUTES(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "LINEAR_10PERCENT_EVERY_2MINUTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_3MINUTES")
    def LINEAR_10_PERCENT_EVERY_3_MINUTES(cls) -> ILambdaDeploymentConfig:
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "LINEAR_10PERCENT_EVERY_3MINUTES"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentConfigImportProps",
    jsii_struct_bases=[],
    name_mapping={"deployment_config_name": "deploymentConfigName"},
)
class LambdaDeploymentConfigImportProps:
    def __init__(self, *, deployment_config_name: builtins.str) -> None:
        '''Properties of a reference to a CodeDeploy Lambda Deployment Configuration.

        :param deployment_config_name: The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        :see: LambdaDeploymentConfig#import
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codedeploy as codedeploy
            
            lambda_deployment_config_import_props = codedeploy.LambdaDeploymentConfigImportProps(
                deployment_config_name="deploymentConfigName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a5dc9a960a38b7f02258b4324d11ea96b72ed4e87d1b2d9dcd052feb913e33)
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployment_config_name": deployment_config_name,
        }

    @builtins.property
    def deployment_config_name(self) -> builtins.str:
        '''The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.'''
        result = self._values.get("deployment_config_name")
        assert result is not None, "Required property 'deployment_config_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDeploymentConfigImportProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILambdaDeploymentGroup)
class LambdaDeploymentGroup(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroup",
):
    '''
    :resource: AWS::CodeDeploy::DeploymentGroup
    :exampleMetadata: infused

    Example::

        # application: codedeploy.LambdaApplication
        # alias: lambda.Alias
        config = codedeploy.CustomLambdaDeploymentConfig(self, "CustomConfig",
            type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
            interval=Duration.minutes(1),
            percentage=5
        )
        deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
            application=application,
            alias=alias,
            deployment_config=config
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: _aws_cdk_aws_lambda_5443dbc3.Alias,
        alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]] = None,
        application: typing.Optional[ILambdaApplication] = None,
        auto_rollback: typing.Optional[typing.Union[AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
        post_hook: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction] = None,
        pre_hook: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alias: Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment. [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to. Default: - One will be created for you.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param post_hook: The Lambda function to run after traffic routing starts. Default: - None.
        :param pre_hook: The Lambda function to run before traffic routing starts. Default: - None.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceeebdb84ca7d1945e4f590ec096aa02b0899b6ce32fafc38740b2f8c2aaf666)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaDeploymentGroupProps(
            alias=alias,
            alarms=alarms,
            application=application,
            auto_rollback=auto_rollback,
            deployment_config=deployment_config,
            deployment_group_name=deployment_group_name,
            ignore_poll_alarms_failure=ignore_poll_alarms_failure,
            post_hook=post_hook,
            pre_hook=pre_hook,
            role=role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromLambdaDeploymentGroupAttributes")
    @builtins.classmethod
    def from_lambda_deployment_group_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application: ILambdaApplication,
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
    ) -> ILambdaDeploymentGroup:
        '''Import an Lambda Deployment Group defined either outside the CDK app, or in a different AWS region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        :return: a Construct representing a reference to an existing Deployment Group
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d86ebe9212f20df82e2ab01786ba1c32e99b26547b2147884d867f5d2fc0241e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = LambdaDeploymentGroupAttributes(
            application=application,
            deployment_group_name=deployment_group_name,
            deployment_config=deployment_config,
        )

        return typing.cast(ILambdaDeploymentGroup, jsii.sinvoke(cls, "fromLambdaDeploymentGroupAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm) -> None:
        '''Associates an additional alarm with this Deployment Group.

        :param alarm: the alarm to associate with this Deployment Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d32d76ed2ce69d612c5813b803464e20e30f3d1fe2a074ad93886550f107804)
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
        return typing.cast(None, jsii.invoke(self, "addAlarm", [alarm]))

    @jsii.member(jsii_name="addPostHook")
    def add_post_hook(self, post_hook: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Associate a function to run after deployment completes.

        :param post_hook: function to run after deployment completes.

        :throws: an error if a post-hook function is already configured
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2b9723e942f77b3d6ff2b61fdc38bfaf9de807c86a9aaece040a7117838282)
            check_type(argname="argument post_hook", value=post_hook, expected_type=type_hints["post_hook"])
        return typing.cast(None, jsii.invoke(self, "addPostHook", [post_hook]))

    @jsii.member(jsii_name="addPreHook")
    def add_pre_hook(self, pre_hook: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Associate a function to run before deployment begins.

        :param pre_hook: function to run before deployment beings.

        :throws: an error if a pre-hook function is already configured
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8548fbac5cf57f2ed80cab677ddf9d93546b3e29c3361ea9be73a3016b9bbbea)
            check_type(argname="argument pre_hook", value=pre_hook, expected_type=type_hints["pre_hook"])
        return typing.cast(None, jsii.invoke(self, "addPreHook", [pre_hook]))

    @jsii.member(jsii_name="grantPutLifecycleEventHookExecutionStatus")
    def grant_put_lifecycle_event_hook_execution_status(
        self,
        grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
    ) -> _aws_cdk_aws_iam_940a1ce0.Grant:
        '''Grant a principal permission to codedeploy:PutLifecycleEventHookExecutionStatus on this deployment group resource.

        :param grantee: to grant permission to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce87694829e78520edf43e5b065805ef1fbe56c0b683f27b51e2b9a1c288c5aa)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.Grant, jsii.invoke(self, "grantPutLifecycleEventHookExecutionStatus", [grantee]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> ILambdaApplication:
        '''The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.'''
        return typing.cast(ILambdaApplication, jsii.get(self, "application"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> ILambdaDeploymentConfig:
        '''The Deployment Configuration this Group uses.'''
        return typing.cast(ILambdaDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''The ARN of this Deployment Group.'''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''The physical name of the CodeDeploy Deployment Group.'''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_940a1ce0.IRole:
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.IRole, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "deployment_group_name": "deploymentGroupName",
        "deployment_config": "deploymentConfig",
    },
)
class LambdaDeploymentGroupAttributes:
    def __init__(
        self,
        *,
        application: ILambdaApplication,
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
    ) -> None:
        '''Properties of a reference to a CodeDeploy Lambda Deployment Group.

        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        :see: LambdaDeploymentGroup#fromLambdaDeploymentGroupAttributes
        :exampleMetadata: infused

        Example::

            # application: codedeploy.LambdaApplication
            
            deployment_group = codedeploy.LambdaDeploymentGroup.from_lambda_deployment_group_attributes(self, "ExistingCodeDeployDeploymentGroup",
                application=application,
                deployment_group_name="MyExistingDeploymentGroup"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ac4f2a97a31475c8e50165fb9936569d742b53bc6fbf903f9c39aa630d7eb6)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument deployment_config", value=deployment_config, expected_type=type_hints["deployment_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application": application,
            "deployment_group_name": deployment_group_name,
        }
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> ILambdaApplication:
        '''The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.'''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(ILambdaApplication, result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        '''The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.'''
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_config(self) -> typing.Optional[ILambdaDeploymentConfig]:
        '''The Deployment Configuration this Deployment Group uses.

        :default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[ILambdaDeploymentConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDeploymentGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "alarms": "alarms",
        "application": "application",
        "auto_rollback": "autoRollback",
        "deployment_config": "deploymentConfig",
        "deployment_group_name": "deploymentGroupName",
        "ignore_poll_alarms_failure": "ignorePollAlarmsFailure",
        "post_hook": "postHook",
        "pre_hook": "preHook",
        "role": "role",
    },
)
class LambdaDeploymentGroupProps:
    def __init__(
        self,
        *,
        alias: _aws_cdk_aws_lambda_5443dbc3.Alias,
        alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]] = None,
        application: typing.Optional[ILambdaApplication] = None,
        auto_rollback: typing.Optional[typing.Union[AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
        post_hook: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction] = None,
        pre_hook: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''Construction properties for {@link LambdaDeploymentGroup}.

        :param alias: Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment. [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to. Default: - One will be created for you.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param post_hook: The Lambda function to run after traffic routing starts. Default: - None.
        :param pre_hook: The Lambda function to run before traffic routing starts. Default: - None.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.

        :exampleMetadata: infused

        Example::

            # application: codedeploy.LambdaApplication
            # alias: lambda.Alias
            config = codedeploy.CustomLambdaDeploymentConfig(self, "CustomConfig",
                type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
                interval=Duration.minutes(1),
                percentage=5
            )
            deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
                application=application,
                alias=alias,
                deployment_config=config
            )
        '''
        if isinstance(auto_rollback, dict):
            auto_rollback = AutoRollbackConfig(**auto_rollback)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7cc606a317a6d6b894aaccf39de3c6d980f6d24dd86cd6eaca0719083be810d)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument auto_rollback", value=auto_rollback, expected_type=type_hints["auto_rollback"])
            check_type(argname="argument deployment_config", value=deployment_config, expected_type=type_hints["deployment_config"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument ignore_poll_alarms_failure", value=ignore_poll_alarms_failure, expected_type=type_hints["ignore_poll_alarms_failure"])
            check_type(argname="argument post_hook", value=post_hook, expected_type=type_hints["post_hook"])
            check_type(argname="argument pre_hook", value=pre_hook, expected_type=type_hints["pre_hook"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias": alias,
        }
        if alarms is not None:
            self._values["alarms"] = alarms
        if application is not None:
            self._values["application"] = application
        if auto_rollback is not None:
            self._values["auto_rollback"] = auto_rollback
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name
        if ignore_poll_alarms_failure is not None:
            self._values["ignore_poll_alarms_failure"] = ignore_poll_alarms_failure
        if post_hook is not None:
            self._values["post_hook"] = post_hook
        if pre_hook is not None:
            self._values["pre_hook"] = pre_hook
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def alias(self) -> _aws_cdk_aws_lambda_5443dbc3.Alias:
        '''Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment.

        [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        '''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(_aws_cdk_aws_lambda_5443dbc3.Alias, result)

    @builtins.property
    def alarms(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]]:
        '''The CloudWatch alarms associated with this Deployment Group.

        CodeDeploy will stop (and optionally roll back)
        a deployment if during it any of the alarms trigger.

        Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method.

        :default: []

        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]], result)

    @builtins.property
    def application(self) -> typing.Optional[ILambdaApplication]:
        '''The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        :default: - One will be created for you.
        '''
        result = self._values.get("application")
        return typing.cast(typing.Optional[ILambdaApplication], result)

    @builtins.property
    def auto_rollback(self) -> typing.Optional[AutoRollbackConfig]:
        '''The auto-rollback configuration for this Deployment Group.

        :default: - default AutoRollbackConfig.
        '''
        result = self._values.get("auto_rollback")
        return typing.cast(typing.Optional[AutoRollbackConfig], result)

    @builtins.property
    def deployment_config(self) -> typing.Optional[ILambdaDeploymentConfig]:
        '''The Deployment Configuration this Deployment Group uses.

        :default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[ILambdaDeploymentConfig], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''The physical, human-readable name of the CodeDeploy Deployment Group.

        :default: - An auto-generated name will be used.
        '''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_poll_alarms_failure(self) -> typing.Optional[builtins.bool]:
        '''Whether to continue a deployment even if fetching the alarm status from CloudWatch failed.

        :default: false
        '''
        result = self._values.get("ignore_poll_alarms_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def post_hook(self) -> typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction]:
        '''The Lambda function to run after traffic routing starts.

        :default: - None.
        '''
        result = self._values.get("post_hook")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction], result)

    @builtins.property
    def pre_hook(self) -> typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction]:
        '''The Lambda function to run before traffic routing starts.

        :default: - None.
        '''
        result = self._values.get("pre_hook")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The service Role of this Deployment Group.

        :default: - A new Role will be created.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDeploymentGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancer(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-codedeploy.LoadBalancer",
):
    '''An interface of an abstract load balancer, as needed by CodeDeploy.

    Create instances using the static factory methods:
    {@link #classic}, {@link #application} and {@link #network}.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_elasticloadbalancing as elb
        
        # lb: elb.LoadBalancer
        
        lb.add_listener(
            external_port=80
        )
        
        deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
            load_balancer=codedeploy.LoadBalancer.classic(lb)
        )
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="application")
    @builtins.classmethod
    def application(
        cls,
        alb_target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationTargetGroup,
    ) -> "LoadBalancer":
        '''Creates a new CodeDeploy load balancer from an Application Load Balancer Target Group.

        :param alb_target_group: an ALB Target Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1528685c0259cb07878830feea2956a700666dbdf37e0f9d8e519b1480a23701)
            check_type(argname="argument alb_target_group", value=alb_target_group, expected_type=type_hints["alb_target_group"])
        return typing.cast("LoadBalancer", jsii.sinvoke(cls, "application", [alb_target_group]))

    @jsii.member(jsii_name="classic")
    @builtins.classmethod
    def classic(
        cls,
        load_balancer: _aws_cdk_aws_elasticloadbalancing_976be337.LoadBalancer,
    ) -> "LoadBalancer":
        '''Creates a new CodeDeploy load balancer from a Classic ELB Load Balancer.

        :param load_balancer: a classic ELB Load Balancer.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768fa549b61f39169073c727ab35e998374c320b8f95889af73975968341654b)
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
        return typing.cast("LoadBalancer", jsii.sinvoke(cls, "classic", [load_balancer]))

    @jsii.member(jsii_name="network")
    @builtins.classmethod
    def network(
        cls,
        nlb_target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
    ) -> "LoadBalancer":
        '''Creates a new CodeDeploy load balancer from a Network Load Balancer Target Group.

        :param nlb_target_group: an NLB Target Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ecaf7a3cedc0145d0b3c3b9a15b91a8575e241b955c9d87f1f666539e6cc23)
            check_type(argname="argument nlb_target_group", value=nlb_target_group, expected_type=type_hints["nlb_target_group"])
        return typing.cast("LoadBalancer", jsii.sinvoke(cls, "network", [nlb_target_group]))

    @builtins.property
    @jsii.member(jsii_name="generation")
    @abc.abstractmethod
    def generation(self) -> "LoadBalancerGeneration":
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        ...


class _LoadBalancerProxy(LoadBalancer):
    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> "LoadBalancerGeneration":
        return typing.cast("LoadBalancerGeneration", jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, LoadBalancer).__jsii_proxy_class__ = lambda : _LoadBalancerProxy


@jsii.enum(jsii_type="@aws-cdk/aws-codedeploy.LoadBalancerGeneration")
class LoadBalancerGeneration(enum.Enum):
    '''The generations of AWS load balancing solutions.'''

    FIRST = "FIRST"
    '''The first generation (ELB Classic).'''
    SECOND = "SECOND"
    '''The second generation (ALB and NLB).'''


class MinimumHealthyHosts(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.MinimumHealthyHosts",
):
    '''Minimum number of healthy hosts for a server deployment.

    :exampleMetadata: infused

    Example::

        deployment_config = codedeploy.ServerDeploymentConfig(self, "DeploymentConfiguration",
            deployment_config_name="MyDeploymentConfiguration",  # optional property
            # one of these is required, but both cannot be specified at the same time
            minimum_healthy_hosts=codedeploy.MinimumHealthyHosts.count(2)
        )
    '''

    @jsii.member(jsii_name="count")
    @builtins.classmethod
    def count(cls, value: jsii.Number) -> "MinimumHealthyHosts":
        '''The minimum healhty hosts threshold expressed as an absolute number.

        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1cdd5cdf6a1fd32ffbcdf9983c0bf5874cdbd41f99cc67fa2302224e025dfbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("MinimumHealthyHosts", jsii.sinvoke(cls, "count", [value]))

    @jsii.member(jsii_name="percentage")
    @builtins.classmethod
    def percentage(cls, value: jsii.Number) -> "MinimumHealthyHosts":
        '''The minmum healhty hosts threshold expressed as a percentage of the fleet.

        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1df3a535b0223a7993a6d4c5bae09297a1e65f2003b2da445bf8daba3bb7255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("MinimumHealthyHosts", jsii.sinvoke(cls, "percentage", [value]))


@jsii.implements(IServerApplication)
class ServerApplication(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.ServerApplication",
):
    '''A CodeDeploy Application that deploys to EC2/on-premise instances.

    :resource: AWS::CodeDeploy::Application
    :exampleMetadata: infused

    Example::

        application = codedeploy.ServerApplication(self, "CodeDeployApplication",
            application_name="MyApplication"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224e785aa50b70b11b91e5cbe68721409d347f67ad619be0c27807c4d2a53ab3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServerApplicationProps(application_name=application_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerApplicationName")
    @builtins.classmethod
    def from_server_application_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        server_application_name: builtins.str,
    ) -> IServerApplication:
        '''Import an Application defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param server_application_name: the name of the application to import.

        :return: a Construct representing a reference to an existing Application
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b944fd717186f695ea9fcdd2ee287159a97d98f349bcbf21b499a80a11ae42d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_application_name", value=server_application_name, expected_type=type_hints["server_application_name"])
        return typing.cast(IServerApplication, jsii.sinvoke(cls, "fromServerApplicationName", [scope, id, server_application_name]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.ServerApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName"},
)
class ServerApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construction properties for {@link ServerApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :exampleMetadata: infused

        Example::

            application = codedeploy.ServerApplication(self, "CodeDeployApplication",
                application_name="MyApplication"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7cb49e7b4ff527eb7c590525e3b5f8927e30c37df95258e37a198873cdb37a)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The physical, human-readable name of the CodeDeploy Application.

        :default: an auto-generated name will be used
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IServerDeploymentConfig)
class ServerDeploymentConfig(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentConfig",
):
    '''A custom Deployment Configuration for an EC2/on-premise Deployment Group.

    :resource: AWS::CodeDeploy::DeploymentConfig
    :exampleMetadata: infused

    Example::

        deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
            deployment_config=codedeploy.ServerDeploymentConfig.ALL_AT_ONCE
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        minimum_healthy_hosts: MinimumHealthyHosts,
        deployment_config_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param minimum_healthy_hosts: Minimum number of healthy hosts.
        :param deployment_config_name: The physical, human-readable name of the Deployment Configuration. Default: a name will be auto-generated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b491822923ec11db67494a3d27a19b5a1ef1ce65458b28be03d1e386f5a019)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServerDeploymentConfigProps(
            minimum_healthy_hosts=minimum_healthy_hosts,
            deployment_config_name=deployment_config_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerDeploymentConfigName")
    @builtins.classmethod
    def from_server_deployment_config_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        server_deployment_config_name: builtins.str,
    ) -> IServerDeploymentConfig:
        '''Import a custom Deployment Configuration for an EC2/on-premise Deployment Group defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param server_deployment_config_name: the properties of the referenced custom Deployment Configuration.

        :return: a Construct representing a reference to an existing custom Deployment Configuration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7caaf673514e7a0c9e290a335496c56387976d51aeaa883536f86155532bb061)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument server_deployment_config_name", value=server_deployment_config_name, expected_type=type_hints["server_deployment_config_name"])
        return typing.cast(IServerDeploymentConfig, jsii.sinvoke(cls, "fromServerDeploymentConfigName", [scope, id, server_deployment_config_name]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> IServerDeploymentConfig:
        return typing.cast(IServerDeploymentConfig, jsii.sget(cls, "ALL_AT_ONCE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HALF_AT_A_TIME")
    def HALF_AT_A_TIME(cls) -> IServerDeploymentConfig:
        return typing.cast(IServerDeploymentConfig, jsii.sget(cls, "HALF_AT_A_TIME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ONE_AT_A_TIME")
    def ONE_AT_A_TIME(cls) -> IServerDeploymentConfig:
        return typing.cast(IServerDeploymentConfig, jsii.sget(cls, "ONE_AT_A_TIME"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "minimum_healthy_hosts": "minimumHealthyHosts",
        "deployment_config_name": "deploymentConfigName",
    },
)
class ServerDeploymentConfigProps:
    def __init__(
        self,
        *,
        minimum_healthy_hosts: MinimumHealthyHosts,
        deployment_config_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construction properties of {@link ServerDeploymentConfig}.

        :param minimum_healthy_hosts: Minimum number of healthy hosts.
        :param deployment_config_name: The physical, human-readable name of the Deployment Configuration. Default: a name will be auto-generated

        :exampleMetadata: infused

        Example::

            deployment_config = codedeploy.ServerDeploymentConfig(self, "DeploymentConfiguration",
                deployment_config_name="MyDeploymentConfiguration",  # optional property
                # one of these is required, but both cannot be specified at the same time
                minimum_healthy_hosts=codedeploy.MinimumHealthyHosts.count(2)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca225f403944407e6a5165349a498802f1bab25f8eeec4dace2a3fb6a9af1e5b)
            check_type(argname="argument minimum_healthy_hosts", value=minimum_healthy_hosts, expected_type=type_hints["minimum_healthy_hosts"])
            check_type(argname="argument deployment_config_name", value=deployment_config_name, expected_type=type_hints["deployment_config_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "minimum_healthy_hosts": minimum_healthy_hosts,
        }
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name

    @builtins.property
    def minimum_healthy_hosts(self) -> MinimumHealthyHosts:
        '''Minimum number of healthy hosts.'''
        result = self._values.get("minimum_healthy_hosts")
        assert result is not None, "Required property 'minimum_healthy_hosts' is missing"
        return typing.cast(MinimumHealthyHosts, result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''The physical, human-readable name of the Deployment Configuration.

        :default: a name will be auto-generated
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerDeploymentConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IServerDeploymentGroup)
class ServerDeploymentGroup(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroup",
):
    '''A CodeDeploy Deployment Group that deploys to EC2/on-premise instances.

    :resource: AWS::CodeDeploy::DeploymentGroup
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_elasticloadbalancing as elb
        
        # lb: elb.LoadBalancer
        
        lb.add_listener(
            external_port=80
        )
        
        deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
            load_balancer=codedeploy.LoadBalancer.classic(lb)
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]] = None,
        application: typing.Optional[IServerApplication] = None,
        auto_rollback: typing.Optional[typing.Union[AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scaling_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]] = None,
        deployment_config: typing.Optional[IServerDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        ec2_instance_tags: typing.Optional[InstanceTagSet] = None,
        ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
        install_agent: typing.Optional[builtins.bool] = None,
        load_balancer: typing.Optional[LoadBalancer] = None,
        on_premise_instance_tags: typing.Optional[InstanceTagSet] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The CodeDeploy EC2/on-premise Application this Deployment Group belongs to. Default: - A new Application will be created.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param auto_scaling_groups: The auto-scaling groups belonging to this Deployment Group. Auto-scaling groups can also be added after the Deployment Group is created using the {@link #addAutoScalingGroup} method. [disable-awslint:ref-via-interface] is needed because we update userdata for ASGs to install the codedeploy agent. Default: []
        :param deployment_config: The EC2/on-premise Deployment Configuration to use for this Deployment Group. Default: ServerDeploymentConfig#OneAtATime
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ec2_instance_tags: All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional EC2 instances will be added to the Deployment Group.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param install_agent: If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances. Default: true
        :param load_balancer: The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group. Default: - Deployment Group will not have a load balancer defined.
        :param on_premise_instance_tags: All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional on-premise instances will be added to the Deployment Group.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311282204eb7f067f04bc785deb39431553d3b313a3548fc87d6f28eb7099bf9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServerDeploymentGroupProps(
            alarms=alarms,
            application=application,
            auto_rollback=auto_rollback,
            auto_scaling_groups=auto_scaling_groups,
            deployment_config=deployment_config,
            deployment_group_name=deployment_group_name,
            ec2_instance_tags=ec2_instance_tags,
            ignore_poll_alarms_failure=ignore_poll_alarms_failure,
            install_agent=install_agent,
            load_balancer=load_balancer,
            on_premise_instance_tags=on_premise_instance_tags,
            role=role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerDeploymentGroupAttributes")
    @builtins.classmethod
    def from_server_deployment_group_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application: IServerApplication,
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional[IServerDeploymentConfig] = None,
    ) -> IServerDeploymentGroup:
        '''Import an EC2/on-premise Deployment Group defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: ServerDeploymentConfig#OneAtATime

        :return: a Construct representing a reference to an existing Deployment Group
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aafb651529a90f3ae3232b48d921af0e1a8ad1dd79fa3ca4c632bf70f072e5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ServerDeploymentGroupAttributes(
            application=application,
            deployment_group_name=deployment_group_name,
            deployment_config=deployment_config,
        )

        return typing.cast(IServerDeploymentGroup, jsii.sinvoke(cls, "fromServerDeploymentGroupAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm) -> None:
        '''Associates an additional alarm with this Deployment Group.

        :param alarm: the alarm to associate with this Deployment Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9f59310a8a2bccf5e0adf1915b1bf3b222b9771e709d24b6323197e973923f)
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
        return typing.cast(None, jsii.invoke(self, "addAlarm", [alarm]))

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(
        self,
        asg: _aws_cdk_aws_autoscaling_92cc07a7.AutoScalingGroup,
    ) -> None:
        '''Adds an additional auto-scaling group to this Deployment Group.

        :param asg: the auto-scaling group to add to this Deployment Group. [disable-awslint:ref-via-interface] is needed in order to install the code deploy agent by updating the ASGs user data.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df7d18b2185ef19c303f9ef73e9186337a581b00c37a238f1aace976b66183c)
            check_type(argname="argument asg", value=asg, expected_type=type_hints["asg"])
        return typing.cast(None, jsii.invoke(self, "addAutoScalingGroup", [asg]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> IServerApplication:
        return typing.cast(IServerApplication, jsii.get(self, "application"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IServerDeploymentConfig:
        return typing.cast(IServerDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]], jsii.get(self, "autoScalingGroups"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "deployment_group_name": "deploymentGroupName",
        "deployment_config": "deploymentConfig",
    },
)
class ServerDeploymentGroupAttributes:
    def __init__(
        self,
        *,
        application: IServerApplication,
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional[IServerDeploymentConfig] = None,
    ) -> None:
        '''Properties of a reference to a CodeDeploy EC2/on-premise Deployment Group.

        :param application: The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: ServerDeploymentConfig#OneAtATime

        :see: ServerDeploymentGroup#import
        :exampleMetadata: infused

        Example::

            # application: codedeploy.ServerApplication
            
            deployment_group = codedeploy.ServerDeploymentGroup.from_server_deployment_group_attributes(self, "ExistingCodeDeployDeploymentGroup",
                application=application,
                deployment_group_name="MyExistingDeploymentGroup"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af97d4ed675dd4a09b147155f911da9ac9132a0d9bc8b6143f2ef406f25bc64f)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument deployment_config", value=deployment_config, expected_type=type_hints["deployment_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application": application,
            "deployment_group_name": deployment_group_name,
        }
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> IServerApplication:
        '''The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.'''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(IServerApplication, result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        '''The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.'''
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_config(self) -> typing.Optional[IServerDeploymentConfig]:
        '''The Deployment Configuration this Deployment Group uses.

        :default: ServerDeploymentConfig#OneAtATime
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[IServerDeploymentConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerDeploymentGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarms": "alarms",
        "application": "application",
        "auto_rollback": "autoRollback",
        "auto_scaling_groups": "autoScalingGroups",
        "deployment_config": "deploymentConfig",
        "deployment_group_name": "deploymentGroupName",
        "ec2_instance_tags": "ec2InstanceTags",
        "ignore_poll_alarms_failure": "ignorePollAlarmsFailure",
        "install_agent": "installAgent",
        "load_balancer": "loadBalancer",
        "on_premise_instance_tags": "onPremiseInstanceTags",
        "role": "role",
    },
)
class ServerDeploymentGroupProps:
    def __init__(
        self,
        *,
        alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]] = None,
        application: typing.Optional[IServerApplication] = None,
        auto_rollback: typing.Optional[typing.Union[AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scaling_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]] = None,
        deployment_config: typing.Optional[IServerDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        ec2_instance_tags: typing.Optional[InstanceTagSet] = None,
        ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
        install_agent: typing.Optional[builtins.bool] = None,
        load_balancer: typing.Optional[LoadBalancer] = None,
        on_premise_instance_tags: typing.Optional[InstanceTagSet] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''Construction properties for {@link ServerDeploymentGroup}.

        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The CodeDeploy EC2/on-premise Application this Deployment Group belongs to. Default: - A new Application will be created.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param auto_scaling_groups: The auto-scaling groups belonging to this Deployment Group. Auto-scaling groups can also be added after the Deployment Group is created using the {@link #addAutoScalingGroup} method. [disable-awslint:ref-via-interface] is needed because we update userdata for ASGs to install the codedeploy agent. Default: []
        :param deployment_config: The EC2/on-premise Deployment Configuration to use for this Deployment Group. Default: ServerDeploymentConfig#OneAtATime
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ec2_instance_tags: All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional EC2 instances will be added to the Deployment Group.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param install_agent: If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances. Default: true
        :param load_balancer: The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group. Default: - Deployment Group will not have a load balancer defined.
        :param on_premise_instance_tags: All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional on-premise instances will be added to the Deployment Group.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_elasticloadbalancingv2 as elbv2
            
            # alb: elbv2.ApplicationLoadBalancer
            
            listener = alb.add_listener("Listener", port=80)
            target_group = listener.add_targets("Fleet", port=80)
            
            deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
                load_balancer=codedeploy.LoadBalancer.application(target_group)
            )
        '''
        if isinstance(auto_rollback, dict):
            auto_rollback = AutoRollbackConfig(**auto_rollback)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e85786bcce11146ebc2645efc1961da7acb8349b794d4ebf561217c764cf0d)
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument auto_rollback", value=auto_rollback, expected_type=type_hints["auto_rollback"])
            check_type(argname="argument auto_scaling_groups", value=auto_scaling_groups, expected_type=type_hints["auto_scaling_groups"])
            check_type(argname="argument deployment_config", value=deployment_config, expected_type=type_hints["deployment_config"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
            check_type(argname="argument ec2_instance_tags", value=ec2_instance_tags, expected_type=type_hints["ec2_instance_tags"])
            check_type(argname="argument ignore_poll_alarms_failure", value=ignore_poll_alarms_failure, expected_type=type_hints["ignore_poll_alarms_failure"])
            check_type(argname="argument install_agent", value=install_agent, expected_type=type_hints["install_agent"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument on_premise_instance_tags", value=on_premise_instance_tags, expected_type=type_hints["on_premise_instance_tags"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarms is not None:
            self._values["alarms"] = alarms
        if application is not None:
            self._values["application"] = application
        if auto_rollback is not None:
            self._values["auto_rollback"] = auto_rollback
        if auto_scaling_groups is not None:
            self._values["auto_scaling_groups"] = auto_scaling_groups
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name
        if ec2_instance_tags is not None:
            self._values["ec2_instance_tags"] = ec2_instance_tags
        if ignore_poll_alarms_failure is not None:
            self._values["ignore_poll_alarms_failure"] = ignore_poll_alarms_failure
        if install_agent is not None:
            self._values["install_agent"] = install_agent
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if on_premise_instance_tags is not None:
            self._values["on_premise_instance_tags"] = on_premise_instance_tags
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def alarms(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]]:
        '''The CloudWatch alarms associated with this Deployment Group.

        CodeDeploy will stop (and optionally roll back)
        a deployment if during it any of the alarms trigger.

        Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method.

        :default: []

        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]], result)

    @builtins.property
    def application(self) -> typing.Optional[IServerApplication]:
        '''The CodeDeploy EC2/on-premise Application this Deployment Group belongs to.

        :default: - A new Application will be created.
        '''
        result = self._values.get("application")
        return typing.cast(typing.Optional[IServerApplication], result)

    @builtins.property
    def auto_rollback(self) -> typing.Optional[AutoRollbackConfig]:
        '''The auto-rollback configuration for this Deployment Group.

        :default: - default AutoRollbackConfig.
        '''
        result = self._values.get("auto_rollback")
        return typing.cast(typing.Optional[AutoRollbackConfig], result)

    @builtins.property
    def auto_scaling_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]]:
        '''The auto-scaling groups belonging to this Deployment Group.

        Auto-scaling groups can also be added after the Deployment Group is created
        using the {@link #addAutoScalingGroup} method.

        [disable-awslint:ref-via-interface] is needed because we update userdata
        for ASGs to install the codedeploy agent.

        :default: []
        '''
        result = self._values.get("auto_scaling_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]], result)

    @builtins.property
    def deployment_config(self) -> typing.Optional[IServerDeploymentConfig]:
        '''The EC2/on-premise Deployment Configuration to use for this Deployment Group.

        :default: ServerDeploymentConfig#OneAtATime
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[IServerDeploymentConfig], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''The physical, human-readable name of the CodeDeploy Deployment Group.

        :default: - An auto-generated name will be used.
        '''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_instance_tags(self) -> typing.Optional[InstanceTagSet]:
        '''All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group.

        :default: - No additional EC2 instances will be added to the Deployment Group.
        '''
        result = self._values.get("ec2_instance_tags")
        return typing.cast(typing.Optional[InstanceTagSet], result)

    @builtins.property
    def ignore_poll_alarms_failure(self) -> typing.Optional[builtins.bool]:
        '''Whether to continue a deployment even if fetching the alarm status from CloudWatch failed.

        :default: false
        '''
        result = self._values.get("ignore_poll_alarms_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def install_agent(self) -> typing.Optional[builtins.bool]:
        '''If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances.

        :default: true

        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-install.html
        '''
        result = self._values.get("install_agent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def load_balancer(self) -> typing.Optional[LoadBalancer]:
        '''The load balancer to place in front of this Deployment Group.

        Can be created from either a classic Elastic Load Balancer,
        or an Application Load Balancer / Network Load Balancer Target Group.

        :default: - Deployment Group will not have a load balancer defined.
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[LoadBalancer], result)

    @builtins.property
    def on_premise_instance_tags(self) -> typing.Optional[InstanceTagSet]:
        '''All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group.

        :default: - No additional on-premise instances will be added to the Deployment Group.
        '''
        result = self._values.get("on_premise_instance_tags")
        return typing.cast(typing.Optional[InstanceTagSet], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The service Role of this Deployment Group.

        :default: - A new Role will be created.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerDeploymentGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILambdaDeploymentConfig)
class CustomLambdaDeploymentConfig(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.CustomLambdaDeploymentConfig",
):
    '''A custom Deployment Configuration for a Lambda Deployment Group.

    :resource: AWS::CodeDeploy::DeploymentGroup
    :exampleMetadata: infused

    Example::

        # application: codedeploy.LambdaApplication
        # alias: lambda.Alias
        config = codedeploy.CustomLambdaDeploymentConfig(self, "CustomConfig",
            type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
            interval=Duration.minutes(1),
            percentage=5
        )
        deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
            application=application,
            alias=alias,
            deployment_config=config
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        interval: _aws_cdk_core_f4b25747.Duration,
        percentage: jsii.Number,
        type: CustomLambdaDeploymentConfigType,
        deployment_config_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param interval: The interval, in number of minutes: - For LINEAR, how frequently additional traffic is shifted - For CANARY, how long to shift traffic before the full deployment.
        :param percentage: The integer percentage of traffic to shift: - For LINEAR, the percentage to shift every interval - For CANARY, the percentage to shift until the interval passes, before the full deployment.
        :param type: The type of deployment config, either CANARY or LINEAR.
        :param deployment_config_name: The verbatim name of the deployment config. Must be unique per account/region. Other parameters cannot be updated if this name is provided. Default: - automatically generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4020d66a752c0866da27ea75c1918881149bb3c1a1b09ae78e9f73383c6c7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CustomLambdaDeploymentConfigProps(
            interval=interval,
            percentage=percentage,
            type=type,
            deployment_config_name=deployment_config_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''The arn of the deployment config.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''The name of the deployment config.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))


@jsii.implements(IEcsApplication)
class EcsApplication(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codedeploy.EcsApplication",
):
    '''A CodeDeploy Application that deploys to an Amazon ECS service.

    :resource: AWS::CodeDeploy::Application
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_codedeploy as codedeploy
        
        ecs_application = codedeploy.EcsApplication(self, "MyEcsApplication",
            application_name="applicationName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b292d0c57cb211c1c562e5ef35fa87c359a1dfe09bcb7823c81c0d1d100376b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsApplicationProps(application_name=application_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromEcsApplicationName")
    @builtins.classmethod
    def from_ecs_application_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        ecs_application_name: builtins.str,
    ) -> IEcsApplication:
        '''Import an Application defined either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param ecs_application_name: the name of the application to import.

        :return: a Construct representing a reference to an existing Application
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc95fb335409b85efff2b6652278c19ed3a8e9e644b58a1a1c927dae2f033110)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ecs_application_name", value=ecs_application_name, expected_type=type_hints["ecs_application_name"])
        return typing.cast(IEcsApplication, jsii.sinvoke(cls, "fromEcsApplicationName", [scope, id, ecs_application_name]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


__all__ = [
    "AutoRollbackConfig",
    "CfnApplication",
    "CfnApplicationProps",
    "CfnDeploymentConfig",
    "CfnDeploymentConfigProps",
    "CfnDeploymentGroup",
    "CfnDeploymentGroupProps",
    "CustomLambdaDeploymentConfig",
    "CustomLambdaDeploymentConfigProps",
    "CustomLambdaDeploymentConfigType",
    "EcsApplication",
    "EcsApplicationProps",
    "EcsDeploymentConfig",
    "EcsDeploymentGroup",
    "EcsDeploymentGroupAttributes",
    "IEcsApplication",
    "IEcsDeploymentConfig",
    "IEcsDeploymentGroup",
    "ILambdaApplication",
    "ILambdaDeploymentConfig",
    "ILambdaDeploymentGroup",
    "IServerApplication",
    "IServerDeploymentConfig",
    "IServerDeploymentGroup",
    "InstanceTagSet",
    "LambdaApplication",
    "LambdaApplicationProps",
    "LambdaDeploymentConfig",
    "LambdaDeploymentConfigImportProps",
    "LambdaDeploymentGroup",
    "LambdaDeploymentGroupAttributes",
    "LambdaDeploymentGroupProps",
    "LoadBalancer",
    "LoadBalancerGeneration",
    "MinimumHealthyHosts",
    "ServerApplication",
    "ServerApplicationProps",
    "ServerDeploymentConfig",
    "ServerDeploymentConfigProps",
    "ServerDeploymentGroup",
    "ServerDeploymentGroupAttributes",
    "ServerDeploymentGroupProps",
]

publication.publish()

def _typecheckingstub__605851913ed777aee04db2e3c374d7fe83f634585d1e95effc589bd736845166(
    *,
    deployment_in_alarm: typing.Optional[builtins.bool] = None,
    failed_deployment: typing.Optional[builtins.bool] = None,
    stopped_deployment: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57070171a52dbcb8c8007b068e92610e76ea3736bf16da94bae78c926cd0adcb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_name: typing.Optional[builtins.str] = None,
    compute_platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f6849f15c9bdb611442d516d0f6b52593a57f70c5d2e288d16c43e495ac496(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66640ebe0980baefbd22e3b5f35b2468aca6d1f282fd238cb8a2fb216645f9c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036ddbacf10084fe8aeedbf98ed8f631ed6ff7b122d703b8e75f94b319f243a5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cecb3429c262600af779d07124a8c383cfb8bae0037c1dfbce324ebc9e8e169(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d7b812cf377e04d7149ca17f0b92069a11575036f5a81b910127af7b77615a(
    *,
    application_name: typing.Optional[builtins.str] = None,
    compute_platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f1fc004e296fae6e27af576eecb11fed838de28169a83d7a45d7888b755cac(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    compute_platform: typing.Optional[builtins.str] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    minimum_healthy_hosts: typing.Optional[typing.Union[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    traffic_routing_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentConfig.TrafficRoutingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef54e07197b0477f8a7ee45cb97dc1280eb2cfa4e087ce945a1c9f31dda83ac(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada52b09cbd16bb11ba784bd5a704a890cccc4083c70314faf7913828a45ad91(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5348b2627f88113b047f5ded63617f4e7e3f8e203e9d7e263bd10cdce7b2cd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4dd14739bd1c9b089872d80465742d359387d9923b3174455eb151e1662217a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58087e08b52b1bf97151460b4a1dee1e057b8bbb688b9010467ffa2c6702790(
    value: typing.Optional[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9f1a5b5e2860f72b63c42ebf27eec7560dadeee919e3e5feedcd93f9ee26bc(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentConfig.TrafficRoutingConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067c76eb1570e8ace61108a4926d15106ce2dfe743bbd2a27f81a90e2bd91edc(
    *,
    type: builtins.str,
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050b52f4f9272ece28171329a0fadfa68ba88ea5ec4a9269c7c4468dd9596cc0(
    *,
    canary_interval: jsii.Number,
    canary_percentage: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ec2fa88d9e338a88798602fff3be534859979c88ed5ae34ed05e0c34085c1d(
    *,
    linear_interval: jsii.Number,
    linear_percentage: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c13213d6b7d84a46c3b432bf8a7f5b623ee5d4c5cd8725d239d40307224d8f(
    *,
    type: builtins.str,
    time_based_canary: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentConfig.TimeBasedCanaryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_based_linear: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentConfig.TimeBasedLinearProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e19ebdd6f3f4b5754c88f2a801ba3acad8eba9dd91abfd1df9601d18cb45b2b(
    *,
    compute_platform: typing.Optional[builtins.str] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    minimum_healthy_hosts: typing.Optional[typing.Union[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    traffic_routing_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentConfig.TrafficRoutingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95d485a4928133eade6a5746d8b869f3e1eec126410c040e8a17b7927c8a977(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_name: builtins.str,
    service_role_arn: builtins.str,
    alarm_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.AlarmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_rollback_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.AutoRollbackConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_scaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    blue_green_deployment_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.DeploymentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
    deployment_style: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.DeploymentStyleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ec2_tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.EC2TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_tag_set: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.EC2TagSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecs_services: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.ECSServiceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    load_balancer_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.LoadBalancerInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_premises_instance_tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    on_premises_tag_set: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.OnPremisesTagSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outdated_instances_strategy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trigger_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e038f11d648429cc1962c39ff4f56fc3e85ba36217ca66ea4b78edd69cc479b7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6867e67aeee5a75fa5d501ab2ffee05422bdc46d5095c98924f07a9b189753a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39c582d1c2caee3f96b221093309f964e8d3e095332f5ffbf9b796cc6349325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca3e28b31d1043e3516e03d7f3bfab87f3c200093722b8a744de19b139b0ce1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d00940baadfac660c47c9b837c4390f3ed8e30de5b9748cf11cdb2d9c9251a4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.AlarmConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cca6d2eb3cfdf1d3492f0d0ad571471480bca384234889419a7c57a5384d5c0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.AutoRollbackConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e609c28a5df074ac5b8f0e87ceb0e1620a04a75c58df16e8c8bcb482a70c8d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc853ba4aefef735099fdc93b20025d3885a18938727c7bcbf58dfe98346f3b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c37dd51dfc99e4b3c20e0f4864aa6501e1c741122524b87cd25dc261da86010(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.DeploymentProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8eb3ae1c9b54eea4f388aad8be7102e30b3cf69c4f3a3a029b7dd5c6600458e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d70dc9848ed6202f0ce82ec76e2c252552dbfe8abb3293de90447b44fadcce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7a3736c71edfbfa61d8e29da612add92a505b233cb16df24d3d6ef9bcc1619(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.DeploymentStyleProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316af0ae6ee1665191c52a9898322d517e413c26f933cc0a1648ee7a3ab3f06e(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.EC2TagFilterProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b830a6718978d7143c40a2e722c089de1553c73a1edcad7370e665e9f8a4ea16(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.EC2TagSetProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68842caab6c87e2eddf975b8ea0dc2e17e79972f26fc536fcdc0fc1a16ef3129(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.ECSServiceProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a847944247bd7d95118b7ce5e95c3be1902d4041d0cd2b3e7a83f275ff36d181(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.LoadBalancerInfoProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08756510974482c0f196ae15eda8a4d5f03856707e74f2d253c435eda61bd4f(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.TagFilterProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077a2fd4e7ccd378baf86d8f8b24361b2c638ce1df4ceffd833f2a6cd277aba6(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.OnPremisesTagSetProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28169e8766e476263e1d44dbd0fe172c026dbcef4f49f465261fd17aa1b5cb4b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b0a771fd74097c279e0b5b97cc323e6dceaf400e4a14d6d9fefba01366f08b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeploymentGroup.TriggerConfigProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c8c62dcf61aa9385b775f860ad9636fcfc138e3250a98cddd0e62f322727ce(
    *,
    alarms: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.AlarmProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45193bd8a7ece69b47f0ba563bdfdc61466d988183dae6f3faef1e710a15ad78(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0a738bad235b2c4aa8ec9bdd9b7c9ba60435bbdf583d0474ca8d0c9c9bf115(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750b2a264d6615f1fe1caf8f5b2183c0a93dede85e2ff87a46665bb958a82c83(
    *,
    deployment_ready_option: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.DeploymentReadyOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    green_fleet_provisioning_option: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.GreenFleetProvisioningOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    terminate_blue_instances_on_deployment_success: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.BlueInstanceTerminationOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbc5dcf0d68a7b9226f773453a766a7ab513891a0b212d40fb4902039c3e212(
    *,
    action: typing.Optional[builtins.str] = None,
    termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9e7f9793c200e263c0ca670579df13092f8ced397fad8a6d272a8cefd7401d(
    *,
    revision: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.RevisionLocationProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    ignore_application_stop_failures: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cb709bfd169e790006ffdc2a15548b968a024ff825f6f5925e15c70ecd68f2(
    *,
    action_on_timeout: typing.Optional[builtins.str] = None,
    wait_time_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec5c208fef39c240620a9a796e7caece22751adedcf1dd71ebd1bd586b23b4d(
    *,
    deployment_option: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacd8ee63f774a8946719ed0af134a9e27d2a1baf50ea2836b900186354a92b4(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb5f57b9ed9a32de3e7db7fcbae560f1052ec90428062a4b4071a018b4dacd5(
    *,
    ec2_tag_group: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.EC2TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15744d000d2706fd6c381dd06af7a21dcfe1d0481373c4f80c053557e023954(
    *,
    ec2_tag_set_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.EC2TagSetListObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090e50bc68a192fd778a12a9810451fe8b55e0ea35a27c0f5553cb2ace63a947(
    *,
    cluster_name: builtins.str,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca14c2421963a6eeba5a31651f8260ff7125a735713d359ecceefca86fba9ff(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf3e9c63163ff3e85724337ef3a68ee0fc629928a93912237e878709c594ef3(
    *,
    commit_id: builtins.str,
    repository: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__955b6a8750e6f0227bae7bd92ec12951a0a2ca191046321ee2d0c93b4d5ab745(
    *,
    action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0ff8b5cb32d65c037fe993b5cfd941ee1d576aa807118432fb679a7c723ed2(
    *,
    elb_info_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.ELBInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_group_info_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TargetGroupInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_group_pair_info_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TargetGroupPairInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87eccb71adb9f86e141e17a68451b981b71f585ac8f0e4bf33453702b4328786(
    *,
    on_premises_tag_group: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59946fdee8e1bfe3e95438b58d3c58685e30b6aac538907f66601323554a75b(
    *,
    on_premises_tag_set_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.OnPremisesTagSetListObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4c29be242d375a46503ce1033f0b668156aca0230778a95967aac6066d41d6(
    *,
    git_hub_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.GitHubLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    revision_type: typing.Optional[builtins.str] = None,
    s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c7a1f811d3545fc6314b3ff07cf93d3d140d41bcdfb23a4bd6eaa4a6a35848(
    *,
    bucket: builtins.str,
    key: builtins.str,
    bundle_type: typing.Optional[builtins.str] = None,
    e_tag: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662b8e7a786d5d29bc7de1c947f63d36919ddb171dcf7f55125894ab8a165679(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92609e668302326a6dd512565c0f4d74ba84021072744b7da06ccc30e00278c6(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331d1e2a2c4f04e057bfc15dda83dc34f57b3f49ba1634d92b92556f47d886a6(
    *,
    prod_traffic_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TrafficRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TargetGroupInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    test_traffic_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TrafficRouteProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b90ebd86517bc152cc6fed54d7422ddac9fb112def88475e5806d06ea0790ec(
    *,
    listener_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c4d0f7b5ab989df16831c67f97942381ac0581a6f05241435aca79c40b5023(
    *,
    trigger_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    trigger_name: typing.Optional[builtins.str] = None,
    trigger_target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a8d133dcae4b53273f86cc50d10afc50283d03497fd856ce0fae712135e42b(
    *,
    application_name: builtins.str,
    service_role_arn: builtins.str,
    alarm_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.AlarmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_rollback_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.AutoRollbackConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_scaling_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    blue_green_deployment_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.BlueGreenDeploymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.DeploymentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_config_name: typing.Optional[builtins.str] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
    deployment_style: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.DeploymentStyleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ec2_tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.EC2TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_tag_set: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.EC2TagSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecs_services: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.ECSServiceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    load_balancer_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.LoadBalancerInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_premises_instance_tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    on_premises_tag_set: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.OnPremisesTagSetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outdated_instances_strategy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trigger_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeploymentGroup.TriggerConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9feaae1d9b0c4dfb6d46153dd3b10f0cca0c561f5809080a8ca3627095f87281(
    *,
    interval: _aws_cdk_core_f4b25747.Duration,
    percentage: jsii.Number,
    type: CustomLambdaDeploymentConfigType,
    deployment_config_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbca5e37a04e380c6af6e64bd1931c5a09e46aecdafc0ea5357d6b2570e55f26(
    *,
    application_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be66b99c6bfa2b3df2a8fea748affba4c03af95be95a054c442e16af44d5a6c(
    _scope: _constructs_77d1e7e8.Construct,
    _id: builtins.str,
    ecs_deployment_config_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478c802d3b879cff23e2fda7e29df1aa4a639fdf328f5e7e96b8420dd02382bb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application: IEcsApplication,
    deployment_group_name: builtins.str,
    deployment_config: typing.Optional[IEcsDeploymentConfig] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db916a90a6b615d5cc50b383fcb199b74a4638f7986f4255e7ead48eaf8a0c02(
    *,
    application: IEcsApplication,
    deployment_group_name: builtins.str,
    deployment_config: typing.Optional[IEcsDeploymentConfig] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51eea36e8ea4ea5b540cf931f80bdd815f59138a75b2b96f4fc4a5fe5ce9a7dd(
    *instance_tag_groups: typing.Mapping[builtins.str, typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3d4007fc8470b3911221c247263ec7f1bcd4d5908a970dc8b5e3016dd09cb9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07be6c7dba10ea1f17730a9313391ec490570edf70793a78a6ab6c29e8c85281(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    lambda_application_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d218c184beddb4529b19437d4e36b191ae599a6bad4f297368fc9fb0d0f9c9d(
    *,
    application_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ace3a1194fb6f1be0dce1ab20a666d2592b01d05cb716c02107f953d0af6855(
    _scope: _constructs_77d1e7e8.Construct,
    _id: builtins.str,
    *,
    deployment_config_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a5dc9a960a38b7f02258b4324d11ea96b72ed4e87d1b2d9dcd052feb913e33(
    *,
    deployment_config_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceeebdb84ca7d1945e4f590ec096aa02b0899b6ce32fafc38740b2f8c2aaf666(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: _aws_cdk_aws_lambda_5443dbc3.Alias,
    alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]] = None,
    application: typing.Optional[ILambdaApplication] = None,
    auto_rollback: typing.Optional[typing.Union[AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
    ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
    post_hook: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction] = None,
    pre_hook: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d86ebe9212f20df82e2ab01786ba1c32e99b26547b2147884d867f5d2fc0241e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application: ILambdaApplication,
    deployment_group_name: builtins.str,
    deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d32d76ed2ce69d612c5813b803464e20e30f3d1fe2a074ad93886550f107804(
    alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2b9723e942f77b3d6ff2b61fdc38bfaf9de807c86a9aaece040a7117838282(
    post_hook: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8548fbac5cf57f2ed80cab677ddf9d93546b3e29c3361ea9be73a3016b9bbbea(
    pre_hook: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce87694829e78520edf43e5b065805ef1fbe56c0b683f27b51e2b9a1c288c5aa(
    grantee: _aws_cdk_aws_iam_940a1ce0.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ac4f2a97a31475c8e50165fb9936569d742b53bc6fbf903f9c39aa630d7eb6(
    *,
    application: ILambdaApplication,
    deployment_group_name: builtins.str,
    deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7cc606a317a6d6b894aaccf39de3c6d980f6d24dd86cd6eaca0719083be810d(
    *,
    alias: _aws_cdk_aws_lambda_5443dbc3.Alias,
    alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]] = None,
    application: typing.Optional[ILambdaApplication] = None,
    auto_rollback: typing.Optional[typing.Union[AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
    ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
    post_hook: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction] = None,
    pre_hook: typing.Optional[_aws_cdk_aws_lambda_5443dbc3.IFunction] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1528685c0259cb07878830feea2956a700666dbdf37e0f9d8e519b1480a23701(
    alb_target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationTargetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768fa549b61f39169073c727ab35e998374c320b8f95889af73975968341654b(
    load_balancer: _aws_cdk_aws_elasticloadbalancing_976be337.LoadBalancer,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ecaf7a3cedc0145d0b3c3b9a15b91a8575e241b955c9d87f1f666539e6cc23(
    nlb_target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1cdd5cdf6a1fd32ffbcdf9983c0bf5874cdbd41f99cc67fa2302224e025dfbe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1df3a535b0223a7993a6d4c5bae09297a1e65f2003b2da445bf8daba3bb7255(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224e785aa50b70b11b91e5cbe68721409d347f67ad619be0c27807c4d2a53ab3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b944fd717186f695ea9fcdd2ee287159a97d98f349bcbf21b499a80a11ae42d2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    server_application_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7cb49e7b4ff527eb7c590525e3b5f8927e30c37df95258e37a198873cdb37a(
    *,
    application_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b491822923ec11db67494a3d27a19b5a1ef1ce65458b28be03d1e386f5a019(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    minimum_healthy_hosts: MinimumHealthyHosts,
    deployment_config_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7caaf673514e7a0c9e290a335496c56387976d51aeaa883536f86155532bb061(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    server_deployment_config_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca225f403944407e6a5165349a498802f1bab25f8eeec4dace2a3fb6a9af1e5b(
    *,
    minimum_healthy_hosts: MinimumHealthyHosts,
    deployment_config_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311282204eb7f067f04bc785deb39431553d3b313a3548fc87d6f28eb7099bf9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]] = None,
    application: typing.Optional[IServerApplication] = None,
    auto_rollback: typing.Optional[typing.Union[AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scaling_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]] = None,
    deployment_config: typing.Optional[IServerDeploymentConfig] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
    ec2_instance_tags: typing.Optional[InstanceTagSet] = None,
    ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
    install_agent: typing.Optional[builtins.bool] = None,
    load_balancer: typing.Optional[LoadBalancer] = None,
    on_premise_instance_tags: typing.Optional[InstanceTagSet] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aafb651529a90f3ae3232b48d921af0e1a8ad1dd79fa3ca4c632bf70f072e5e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application: IServerApplication,
    deployment_group_name: builtins.str,
    deployment_config: typing.Optional[IServerDeploymentConfig] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9f59310a8a2bccf5e0adf1915b1bf3b222b9771e709d24b6323197e973923f(
    alarm: _aws_cdk_aws_cloudwatch_9b88bb94.IAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df7d18b2185ef19c303f9ef73e9186337a581b00c37a238f1aace976b66183c(
    asg: _aws_cdk_aws_autoscaling_92cc07a7.AutoScalingGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af97d4ed675dd4a09b147155f911da9ac9132a0d9bc8b6143f2ef406f25bc64f(
    *,
    application: IServerApplication,
    deployment_group_name: builtins.str,
    deployment_config: typing.Optional[IServerDeploymentConfig] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e85786bcce11146ebc2645efc1961da7acb8349b794d4ebf561217c764cf0d(
    *,
    alarms: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudwatch_9b88bb94.IAlarm]] = None,
    application: typing.Optional[IServerApplication] = None,
    auto_rollback: typing.Optional[typing.Union[AutoRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scaling_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_autoscaling_92cc07a7.IAutoScalingGroup]] = None,
    deployment_config: typing.Optional[IServerDeploymentConfig] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
    ec2_instance_tags: typing.Optional[InstanceTagSet] = None,
    ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
    install_agent: typing.Optional[builtins.bool] = None,
    load_balancer: typing.Optional[LoadBalancer] = None,
    on_premise_instance_tags: typing.Optional[InstanceTagSet] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4020d66a752c0866da27ea75c1918881149bb3c1a1b09ae78e9f73383c6c7b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    interval: _aws_cdk_core_f4b25747.Duration,
    percentage: jsii.Number,
    type: CustomLambdaDeploymentConfigType,
    deployment_config_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b292d0c57cb211c1c562e5ef35fa87c359a1dfe09bcb7823c81c0d1d100376b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc95fb335409b85efff2b6652278c19ed3a8e9e644b58a1a1c927dae2f033110(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    ecs_application_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
