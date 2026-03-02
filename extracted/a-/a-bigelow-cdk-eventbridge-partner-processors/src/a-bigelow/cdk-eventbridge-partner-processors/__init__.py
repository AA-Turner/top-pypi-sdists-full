'''
# Eventbridge SaaS Partner fURLs

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-eventbridge-partner-processors)](https://constructs.dev/packages/cdk-eventbridge-partner-processors)

[![npm version](https://badge.fury.io/js/cdk-eventbridge-partner-processors.svg)](https://badge.fury.io/js/cdk-eventbridge-partner-processors)
[![PyPI version](https://badge.fury.io/py/a-bigelow.cdk-eventbridge-partner-processors.svg)](https://badge.fury.io/py/a-bigelow.cdk-eventbridge-partner-processors)
[![Go project version](https://badge.fury.io/go/github.com%2Fa-bigelow%2Fcdk-eventbridge-partner-processors-go.svg)](https://badge.fury.io/go/github.com%2Fa-bigelow%2Fcdk-eventbridge-partner-processors-go)

This CDK Construct library provides CDK constructs for the 1st-party (i.e. developed by AWS) lambda fURL webhook receivers for:

* GitHub
* Stripe
* Twilio

## Usage Examples (Simplified)

These examples are consistent for all 3 primary exported constructs of this library:

* `GitHubEventProcessor`
* `TwilioEventProcessor`
* `StripeEventProcessor`

> Note: Click on the above `View on Construct Hub` button to view auto-generated examples in Python/Go

### Typescript

```python
import { GitHubEventProcessor } from 'cdk-eventbridge-partner-processors';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { EventBus } from 'aws-cdk-lib/aws-events';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';

export class MyStackWithABetterName extends Stack {
    constructor(scope: Construct, id: string, props: StackProps) {
        super(scope, id, props);

        // This library has no opinion on how you reference your EventBus,
        // It just needs to fulfill the IEventBus protocol
        const myEventBus = new EventBus(this, 'TheBestBusEver', {
            eventBusName: 'TheGreatestBus'
        });

        // This library has no opinion on how you reference your secret,
        // It just needs to fulfill the ISecret protocol
        const mySecret = Secret.fromSecretNameV2(this, 'MyNuclearCodeSecret', '/home/recipes/icbm')

        // Function will automatically receive permission to:
        // 1. Post events to the given bus
        // 2. Read the given secret
        const githubEventProcessor = new GitHubEventProcessor(this, 'GitHubProcessor', {
            eventBus: myEventBus,
            webhookSecret: mySecret,
            lambdaInvocationAlarmThreshold: 2000,
        })

    }
}
```

### Golang

```go
package main

import (
	partner "github.com/a-bigelow/cdk-eventbridge-partner-processors-go"
	"github.com/aws/aws-cdk-go/awscdk/v2"
	"github.com/aws/aws-cdk-go/awscdk/v2/awsevents"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type ClusterStackProps struct {
	awscdk.StackProps
}

func NewClusterStack(scope constructs.Construct, id string, props *ClusterStackProps) awscdk.Stack {
	var sprops awscdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := awscdk.NewStack(scope, &id, &sprops)

	// The code that defines your stack goes here
	eventProps := awsevents.EventBusProps{EventBusName: jsii.String("name")}

	eventBus := awsevents.NewEventBus(stack, jsii.String("id"), &eventProps)

	secret := secretsmanager.secret.fromSecretNameV2(scope, jsii.String("secret"), jsii.String("secretName"))
	partnerProcessor := partner.GithubEventProcessor{
		EventBus:                       eventBus,
		WebhookSecret:                  secret,
		LambdaInvocationAlarmThreshold: 2000,
	}

	_ = partner.NewGitHubEventProcessor(stack, jsii.String("id"), partnerProcessor)

	return stack
}
```

### Disclaimer

> :warning: The Lambda Functions that handle the actual event processing in this Library are owned and maintained by Amazon Web Services. This CDK Construct library provides a thin deployment wrapper for these functions. Changes made to the S3 location of the functions will break this library. Until I have a way to deterministically track where these things are, please raise an **issue** if you have reason to believe that the functions have moved.

### AWS Documentation

See [here](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html) for additional information.
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

import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.GitHubProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus": "eventBus",
        "lambda_invocation_alarm_threshold": "lambdaInvocationAlarmThreshold",
        "webhook_secret": "webhookSecret",
    },
)
class GitHubProps:
    def __init__(
        self,
        *,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1bd2d473034327ab0b7448d3a790cedfd1e129eb0b33a7897eabdec4ca3225)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument lambda_invocation_alarm_threshold", value=lambda_invocation_alarm_threshold, expected_type=type_hints["lambda_invocation_alarm_threshold"])
            check_type(argname="argument webhook_secret", value=webhook_secret, expected_type=type_hints["webhook_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_bus": event_bus,
            "lambda_invocation_alarm_threshold": lambda_invocation_alarm_threshold,
            "webhook_secret": webhook_secret,
        }

    @builtins.property
    def event_bus(self) -> _aws_cdk_aws_events_ceddda9d.IEventBus:
        '''Eventbus to send GitHub events to.'''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.IEventBus, result)

    @builtins.property
    def lambda_invocation_alarm_threshold(self) -> jsii.Number:
        '''Maximum number of concurrent invocations on the fURL function before triggering the alarm.'''
        result = self._values.get("lambda_invocation_alarm_threshold")
        assert result is not None, "Required property 'lambda_invocation_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def webhook_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''SM Secret containing the secret string used to validate webhook events.'''
        result = self._values.get("webhook_secret")
        assert result is not None, "Required property 'webhook_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InvocationAlarm(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eventbridge-partner-processors.InvocationAlarm",
):
    '''Cloudwatch Alarm used across this construct library.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        threshold: jsii.Number,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_function: The function to monitor.
        :param threshold: Lambda Invocation threshold.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e616b18c8574b9329245a870553db00a72c805b54dda04ce8903824546cdf8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InvocationAlarmProps(
            event_function=event_function, threshold=threshold
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.InvocationAlarmProps",
    jsii_struct_bases=[],
    name_mapping={"event_function": "eventFunction", "threshold": "threshold"},
)
class InvocationAlarmProps:
    def __init__(
        self,
        *,
        event_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        threshold: jsii.Number,
    ) -> None:
        '''
        :param event_function: The function to monitor.
        :param threshold: Lambda Invocation threshold.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f119052cafc83b6d17e0e01fd3b9f6cb6bc45df64d3aba10dbffe5a50e7ef209)
            check_type(argname="argument event_function", value=event_function, expected_type=type_hints["event_function"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_function": event_function,
            "threshold": threshold,
        }

    @builtins.property
    def event_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The function to monitor.'''
        result = self._values.get("event_function")
        assert result is not None, "Required property 'event_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Lambda Invocation threshold.'''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InvocationAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-eventbridge-partner-processors.Partner")
class Partner(enum.Enum):
    '''Supported partners with fURL integrations.'''

    GITHUB = "GITHUB"
    STRIPE = "STRIPE"
    TWILIO = "TWILIO"


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.PartnerFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "eventbridge_partner": "eventbridgePartner",
        "event_bus": "eventBus",
        "lambda_invocation_alarm_threshold": "lambdaInvocationAlarmThreshold",
        "webhook_secret": "webhookSecret",
    },
)
class PartnerFunctionProps:
    def __init__(
        self,
        *,
        eventbridge_partner: Partner,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param eventbridge_partner: The partner to create an events processor for.
        :param event_bus: Eventbus to send Partner events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__028e83c402bbb273f6b9bf4210b6fd995eaed5152ba0cdd582586c2200c34532)
            check_type(argname="argument eventbridge_partner", value=eventbridge_partner, expected_type=type_hints["eventbridge_partner"])
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument lambda_invocation_alarm_threshold", value=lambda_invocation_alarm_threshold, expected_type=type_hints["lambda_invocation_alarm_threshold"])
            check_type(argname="argument webhook_secret", value=webhook_secret, expected_type=type_hints["webhook_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "eventbridge_partner": eventbridge_partner,
            "event_bus": event_bus,
            "lambda_invocation_alarm_threshold": lambda_invocation_alarm_threshold,
            "webhook_secret": webhook_secret,
        }

    @builtins.property
    def eventbridge_partner(self) -> Partner:
        '''The partner to create an events processor for.'''
        result = self._values.get("eventbridge_partner")
        assert result is not None, "Required property 'eventbridge_partner' is missing"
        return typing.cast(Partner, result)

    @builtins.property
    def event_bus(self) -> _aws_cdk_aws_events_ceddda9d.IEventBus:
        '''Eventbus to send Partner events to.'''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.IEventBus, result)

    @builtins.property
    def lambda_invocation_alarm_threshold(self) -> jsii.Number:
        '''Maximum number of concurrent invocations on the fURL function before triggering the alarm.'''
        result = self._values.get("lambda_invocation_alarm_threshold")
        assert result is not None, "Required property 'lambda_invocation_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def webhook_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''SM Secret containing the secret string used to validate webhook events.'''
        result = self._values.get("webhook_secret")
        assert result is not None, "Required property 'webhook_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PartnerFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PartnerProcessor(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-eventbridge-partner-processors.PartnerProcessor",
):
    '''Abstract class for Lambda-driven Eventbridge integrations.

    This only works because the pattern for the S3 Keys lines up to: lambda-templates/-lambdasrc.zip

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        eventbridge_partner: Partner,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param eventbridge_partner: The partner to create an events processor for.
        :param event_bus: Eventbus to send Partner events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1aaedba265abc004370697d4332b171363032e5ada55af8d579b24403a88a10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PartnerFunctionProps(
            eventbridge_partner=eventbridge_partner,
            event_bus=event_bus,
            lambda_invocation_alarm_threshold=lambda_invocation_alarm_threshold,
            webhook_secret=webhook_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="invocationAlarm")
    def invocation_alarm(self) -> InvocationAlarm:
        return typing.cast(InvocationAlarm, jsii.get(self, "invocationAlarm"))

    @invocation_alarm.setter
    def invocation_alarm(self, value: InvocationAlarm) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f9b86e2a5d331d9abd8be3415540b618a4b8f36fd7661f8463dfcc2d873e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationAlarm", value)

    @builtins.property
    @jsii.member(jsii_name="partnerEventsFunction")
    def partner_events_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "partnerEventsFunction"))

    @partner_events_function.setter
    def partner_events_function(
        self,
        value: _aws_cdk_aws_lambda_ceddda9d.Function,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d350e05b65a56c1b9abbe6ed813c66027a84a2543c40b4ebbe4a27c628de58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerEventsFunction", value)


class _PartnerProcessorProxy(PartnerProcessor):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PartnerProcessor).__jsii_proxy_class__ = lambda : _PartnerProcessorProxy


class StripeEventProcessor(
    PartnerProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eventbridge-partner-processors.StripeEventProcessor",
):
    '''CDK wrapper for the Stripe Eventbridge processor.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html#furls-connection-github
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b81872d01bacdee390f3593b17973b7a2769595dff51de8c1c87cbbc17f7ca2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StripeProps(
            event_bus=event_bus,
            lambda_invocation_alarm_threshold=lambda_invocation_alarm_threshold,
            webhook_secret=webhook_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.StripeProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus": "eventBus",
        "lambda_invocation_alarm_threshold": "lambdaInvocationAlarmThreshold",
        "webhook_secret": "webhookSecret",
    },
)
class StripeProps:
    def __init__(
        self,
        *,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a564ddfb54d12999fe1941bf5325952fd08c061e36e1fe0223e2af8cb09817)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument lambda_invocation_alarm_threshold", value=lambda_invocation_alarm_threshold, expected_type=type_hints["lambda_invocation_alarm_threshold"])
            check_type(argname="argument webhook_secret", value=webhook_secret, expected_type=type_hints["webhook_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_bus": event_bus,
            "lambda_invocation_alarm_threshold": lambda_invocation_alarm_threshold,
            "webhook_secret": webhook_secret,
        }

    @builtins.property
    def event_bus(self) -> _aws_cdk_aws_events_ceddda9d.IEventBus:
        '''Eventbus to send GitHub events to.'''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.IEventBus, result)

    @builtins.property
    def lambda_invocation_alarm_threshold(self) -> jsii.Number:
        '''Maximum number of concurrent invocations on the fURL function before triggering the alarm.'''
        result = self._values.get("lambda_invocation_alarm_threshold")
        assert result is not None, "Required property 'lambda_invocation_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def webhook_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''SM Secret containing the secret string used to validate webhook events.'''
        result = self._values.get("webhook_secret")
        assert result is not None, "Required property 'webhook_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StripeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TwilioEventProcessor(
    PartnerProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eventbridge-partner-processors.TwilioEventProcessor",
):
    '''CDK wrapper for the Twilio Eventbridge processor.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html#furls-connection-github
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d81a8259896513fe5e83d0a5ae35708c6a956ffc1d3df41cba4fb888c0484a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TwilioProps(
            event_bus=event_bus,
            lambda_invocation_alarm_threshold=lambda_invocation_alarm_threshold,
            webhook_secret=webhook_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.TwilioProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus": "eventBus",
        "lambda_invocation_alarm_threshold": "lambdaInvocationAlarmThreshold",
        "webhook_secret": "webhookSecret",
    },
)
class TwilioProps:
    def __init__(
        self,
        *,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61022a329bdeaaa8396b6a94dbdce4613b0785ca8680c0dce6d7f6b0054eab39)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument lambda_invocation_alarm_threshold", value=lambda_invocation_alarm_threshold, expected_type=type_hints["lambda_invocation_alarm_threshold"])
            check_type(argname="argument webhook_secret", value=webhook_secret, expected_type=type_hints["webhook_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_bus": event_bus,
            "lambda_invocation_alarm_threshold": lambda_invocation_alarm_threshold,
            "webhook_secret": webhook_secret,
        }

    @builtins.property
    def event_bus(self) -> _aws_cdk_aws_events_ceddda9d.IEventBus:
        '''Eventbus to send GitHub events to.'''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.IEventBus, result)

    @builtins.property
    def lambda_invocation_alarm_threshold(self) -> jsii.Number:
        '''Maximum number of concurrent invocations on the fURL function before triggering the alarm.'''
        result = self._values.get("lambda_invocation_alarm_threshold")
        assert result is not None, "Required property 'lambda_invocation_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def webhook_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''SM Secret containing the secret string used to validate webhook events.'''
        result = self._values.get("webhook_secret")
        assert result is not None, "Required property 'webhook_secret' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TwilioProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubEventProcessor(
    PartnerProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eventbridge-partner-processors.GitHubEventProcessor",
):
    '''CDK wrapper for the GitHub Eventbridge processor.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html#furls-connection-github
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b67205eb2c9ef2798d48efeefdbe28f6e4434ca50b7160d50f44514dd390be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubProps(
            event_bus=event_bus,
            lambda_invocation_alarm_threshold=lambda_invocation_alarm_threshold,
            webhook_secret=webhook_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "GitHubEventProcessor",
    "GitHubProps",
    "InvocationAlarm",
    "InvocationAlarmProps",
    "Partner",
    "PartnerFunctionProps",
    "PartnerProcessor",
    "StripeEventProcessor",
    "StripeProps",
    "TwilioEventProcessor",
    "TwilioProps",
]

publication.publish()

def _typecheckingstub__da1bd2d473034327ab0b7448d3a790cedfd1e129eb0b33a7897eabdec4ca3225(
    *,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    lambda_invocation_alarm_threshold: jsii.Number,
    webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e616b18c8574b9329245a870553db00a72c805b54dda04ce8903824546cdf8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    threshold: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f119052cafc83b6d17e0e01fd3b9f6cb6bc45df64d3aba10dbffe5a50e7ef209(
    *,
    event_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    threshold: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028e83c402bbb273f6b9bf4210b6fd995eaed5152ba0cdd582586c2200c34532(
    *,
    eventbridge_partner: Partner,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    lambda_invocation_alarm_threshold: jsii.Number,
    webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1aaedba265abc004370697d4332b171363032e5ada55af8d579b24403a88a10(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    eventbridge_partner: Partner,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    lambda_invocation_alarm_threshold: jsii.Number,
    webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f9b86e2a5d331d9abd8be3415540b618a4b8f36fd7661f8463dfcc2d873e23(
    value: InvocationAlarm,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d350e05b65a56c1b9abbe6ed813c66027a84a2543c40b4ebbe4a27c628de58(
    value: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b81872d01bacdee390f3593b17973b7a2769595dff51de8c1c87cbbc17f7ca2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    lambda_invocation_alarm_threshold: jsii.Number,
    webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a564ddfb54d12999fe1941bf5325952fd08c061e36e1fe0223e2af8cb09817(
    *,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    lambda_invocation_alarm_threshold: jsii.Number,
    webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d81a8259896513fe5e83d0a5ae35708c6a956ffc1d3df41cba4fb888c0484a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    lambda_invocation_alarm_threshold: jsii.Number,
    webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61022a329bdeaaa8396b6a94dbdce4613b0785ca8680c0dce6d7f6b0054eab39(
    *,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    lambda_invocation_alarm_threshold: jsii.Number,
    webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b67205eb2c9ef2798d48efeefdbe28f6e4434ca50b7160d50f44514dd390be(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    lambda_invocation_alarm_threshold: jsii.Number,
    webhook_secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass
